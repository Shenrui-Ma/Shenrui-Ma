#!/usr/bin/env python3
"""Verify public contribution evidence and deterministically update two Markdown files."""

import argparse
import difflib
import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

START = "<!-- contributions:start -->"
END = "<!-- contributions:end -->"
OWN_START = "<!-- own-stars:start -->"
OWN_END = "<!-- own-stars:end -->"
SHA = re.compile(r"[0-9a-f]{40}\Z")
REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")


class VerificationError(Exception):
    """An incomplete or unverified snapshot must never replace existing files."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def positive_int(value):
    return type(value) is int and value > 0


def text(value, label):
    require(isinstance(value, str) and value.strip() and "\x00" not in value, f"Invalid {label}")
    return value


def exact_keys(value, required, optional=()):
    require(isinstance(value, dict), "Expected a JSON object")
    require(set(required) <= value.keys(), f"Missing keys: {set(required) - value.keys()}")
    require(value.keys() <= set(required) | set(optional), f"Unknown keys: {value.keys() - set(required) - set(optional)}")


def validate_config(config, root):
    exact_keys(config, ("version", "username", "profile_repository", "sort_by", "show_stars", "logo_size", "repositories", "confirmed_adoptions"), ("own_stars",))
    require(type(config["version"]) is int and config["version"] == 1, "Unsupported config version")
    require(isinstance(config["username"], str) and re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", config["username"]), "Invalid username")
    require(isinstance(config["profile_repository"], str) and REPO.fullmatch(config["profile_repository"]), "Invalid profile_repository")
    require(config["profile_repository"].lower() == "/".join([config["username"].lower()] * 2), "Profile must be the user's same-name repository")
    require(config["sort_by"] == "stars_desc" and type(config["show_stars"]) is bool, "Use stars_desc and a boolean show_stars")
    require(type(config["logo_size"]) is int and 18 <= config["logo_size"] <= 25, "logo_size must be 18–25")
    require(isinstance(config["repositories"], list) and config["repositories"], "No repositories configured")
    if "own_stars" in config:
        exact_keys(config["own_stars"], ("include_forks",))
        require(type(config["own_stars"]["include_forks"]) is bool, "include_forks must be boolean")
    repositories, anchors = set(), set()
    for repo in config["repositories"]:
        exact_keys(repo, ("repository", "display_name", "anchor", "logo"), ("logo_dark", "adopted_unit"))
        name = text(repo["repository"], "repository")
        require(REPO.fullmatch(name) and name.lower() not in repositories, "Invalid or duplicate repository")
        require(name.split("/")[0].lower() != config["username"].lower(), "User-owned repositories are not upstream contributions")
        repositories.add(name.lower())
        require(repo.get("adopted_unit", "prs") in ("prs", "commits"), "adopted_unit must be prs or commits")
        text(repo["display_name"], "display_name")
        require("\n" not in repo["display_name"] and "\r" not in repo["display_name"], "display_name must be one line")
        require(isinstance(repo["anchor"], str) and re.fullmatch(r"[a-z][a-z0-9-]*", repo["anchor"]) and repo["anchor"] not in anchors, "Invalid or duplicate anchor")
        anchors.add(repo["anchor"])
        for key in ("logo", "logo_dark"):
            if key not in repo:
                continue
            path = PurePosixPath(text(repo[key], key))
            require(not path.is_absolute() and ".." not in path.parts and str(path).startswith("assets/logos/") and path.suffix.lower() in (".png", ".svg"), "Logo must be a local assets/logos PNG or SVG")
            resolved = (root / str(path)).resolve()
            require(resolved.is_relative_to(root.resolve()) and resolved.is_file(), f"Missing or unsafe logo: {path}")
    require(isinstance(config["confirmed_adoptions"], list), "confirmed_adoptions must be a list")
    seen = set()
    for adoption in config["confirmed_adoptions"]:
        exact_keys(adoption, ("repository", "source_pr", "landing_pr", "evidence_url", "landing_commits", "reviewed_evidence"))
        repository = text(adoption["repository"], "adoption repository").lower()
        require(repository in repositories, "Adoption repository is outside the whitelist")
        require(positive_int(adoption["source_pr"]) and positive_int(adoption["landing_pr"]), "Invalid adoption PR number")
        key = (repository, adoption["source_pr"])
        require(key not in seen, "Duplicate adoption mapping")
        seen.add(key)
        require(adoption["source_pr"] != adoption["landing_pr"], "Source and integration PR must differ")
        require(text(adoption["evidence_url"], "evidence URL").lower() == f"https://github.com/{repository}/pull/{adoption['landing_pr']}".lower(), "evidence_url must identify the upstream integration PR")
        commits = adoption["landing_commits"]
        require(isinstance(commits, list) and commits and all(isinstance(c, str) and SHA.fullmatch(c) for c in commits), "Invalid landing commits")
        require(len(set(commits)) == len(commits), "Duplicate landing commit")
        evidence = adoption["reviewed_evidence"]
        require(isinstance(evidence, list) and evidence, "Adoption needs reviewed evidence")
        for record in evidence:
            exact_keys(record, ("kind", "sha256"), ("number", "commit", "source_excerpt", "attribution_excerpt"))
            require(isinstance(record["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", record["sha256"]), "Invalid evidence SHA-256")
            require(record["kind"] in ("pull_body", "issue_comment", "commit_message"), "Unsupported evidence kind")
            if record["kind"] == "commit_message":
                require(record.get("commit") in commits and "number" not in record, "Evidence commit must be a landing commit")
            else:
                require(positive_int(record.get("number")) and "commit" not in record, "Evidence needs a positive number")
                if record["kind"] == "pull_body":
                    require(record["number"] == adoption["landing_pr"], "Evidence pull must be the integration PR")
            require("source_excerpt" in record or "attribution_excerpt" in record, "Evidence needs a reviewed excerpt")
            for field in ("source_excerpt", "attribution_excerpt"):
                if field in record:
                    text(record[field], field)
        require(all(any(field in record for record in evidence) for field in ("source_excerpt", "attribution_excerpt")), "Adoption needs reviewed source and attribution evidence")
    return config


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise VerificationError("GitHub API redirected; review canonical repository configuration")


class GitHub:
    def __init__(self, token=None, opener=None, sleep=time.sleep):
        self.token = token
        self.opener = opener or urllib.request.build_opener(NoRedirect()).open
        self.sleep = sleep
        self.cache = {}

    def get(self, path, **params):
        require(path.startswith("/") and not path.startswith("//"), "Invalid API path")
        url = "https://api.github.com" + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        if url in self.cache:
            return self.cache[url]
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "profile-contributions-verifier"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        for attempt in range(3):
            try:
                with self.opener(urllib.request.Request(url, headers=headers), timeout=30) as response:
                    result = json.load(response)
                require(isinstance(result, (dict, list)), "GitHub API returned neither an object nor a list")
                self.cache[url] = result
                return result
            except urllib.error.HTTPError as error:
                retry = error.code in (403, 429) or error.code >= 500
                if not retry or attempt == 2:
                    raise VerificationError(f"GitHub API HTTP {error.code}: {path}") from error
            except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
                if attempt == 2:
                    raise VerificationError(f"GitHub API failed after 3 attempts: {path} ({type(error).__name__})") from error
            self.sleep(2 ** attempt)
        raise AssertionError("Unreachable")


def owned_repository_stars(api, username, include_forks=False):
    """Sum stars on public repositories owned by this user, across every page."""
    total, seen = 0, set()
    for page in range(1, 1001):
        repos = api.get(f"/users/{username}/repos", type="owner", sort="full_name",
                        direction="asc", per_page=100, page=page)
        require(isinstance(repos, list) and len(repos) <= 100, "Invalid owned repository page")
        for repo in repos:
            require(isinstance(repo, dict), "Invalid owned repository")
            name = repo.get("full_name")
            require(isinstance(name, str) and REPO.fullmatch(name) and
                    name.split("/")[0].lower() == username.lower() and
                    (repo.get("owner") or {}).get("login", "").lower() == username.lower(),
                    "Repository owner does not match")
            require(positive_int(repo.get("id")) and repo["id"] not in seen,
                    "Missing or duplicate owned repository")
            seen.add(repo["id"])
            require(repo.get("private") is False and type(repo.get("fork")) is bool,
                    "Expected a public repository with explicit fork status")
            stars = repo.get("stargazers_count")
            require(type(stars) is int and stars >= 0, "Invalid owned repository star count")
            if include_forks or not repo["fork"]:
                total += stars
        if len(repos) < 100:
            return total
    raise VerificationError("Owned repository pagination exceeds safety limit")


def repository_metadata(api, repository):
    value = api.get(f"/repos/{repository}")
    require(isinstance(value.get("full_name"), str) and value["full_name"].lower() == repository.lower(), f"Wrong repository metadata: {repository}")
    require(value.get("html_url", "").lower() == f"https://github.com/{repository}".lower(), "Unexpected repository URL")
    require(type(value.get("stargazers_count")) is int and value["stargazers_count"] >= 0, "Invalid star count")
    text(value.get("default_branch"), "default branch")
    return value


def pull(api, repository, number, username=None):
    value = api.get(f"/repos/{repository}/pulls/{number}")
    require(value.get("number") == number, "Wrong PR number")
    require(value.get("base", {}).get("repo", {}).get("full_name", "").lower() == repository.lower(), "PR belongs to a different upstream")
    require(value.get("html_url", "").lower() == f"https://github.com/{repository}/pull/{number}".lower(), "Unexpected PR URL")
    author = value.get("user") or {}
    require(isinstance(author.get("login"), str), "PR author cannot be verified")
    if username is not None:
        require(author["login"].lower() == username.lower(), "PR author does not match the configured user")
    require(type(value.get("merged")) is bool, "Missing structured PR merge state")
    require((value["merged"] and isinstance(value.get("merged_at"), str) and bool(value["merged_at"])) or (not value["merged"] and value.get("merged_at") is None), "Inconsistent PR merge state")
    text(value.get("title"), "PR title")
    text(value.get("base", {}).get("ref"), "PR target branch")
    return value


def merged_pulls(api, repository, username):
    result, expected = {}, None
    page = 1
    while True:
        response = api.get("/search/issues", q=f"repo:{repository} is:pr author:{username} is:merged", per_page=100, page=page)
        total = response.get("total_count")
        require(type(total) is int and 0 <= total <= 1000, "Search exceeds 1000 results or has invalid total; partition the query before publishing")
        require(response.get("incomplete_results") is False, "GitHub search returned incomplete results")
        require(expected is None or expected == total, "Search total changed during pagination; retry a consistent snapshot")
        expected = total
        items = response.get("items")
        require(isinstance(items, list) and len(items) <= 100, "Invalid search page")
        for item in items:
            require(isinstance(item, dict) and positive_int(item.get("number")) and isinstance(item.get("pull_request"), dict), "Search returned a non-PR item")
            number = item["number"]
            require(number not in result, "Search duplicated a PR across pages; snapshot incomplete")
            value = pull(api, repository, number, username)
            require(value["merged"], "Search claims merged but PR is not merged")
            result[number] = value
        require(len(result) <= total, "Search count mismatch")
        if len(result) == total:
            return result
        require(len(items) == 100 and page < 10, "Search pagination ended before all results were read")
        page += 1


def verify_adoption(api, mapping, metadata, head, username):
    repository = metadata["full_name"]
    source = pull(api, repository, mapping["source_pr"], username)
    if source["merged"]:
        return source, False
    landing = pull(api, repository, mapping["landing_pr"])
    require(landing["merged"] and landing["base"]["ref"] == metadata["default_branch"], "Integration PR has not merged into the upstream default branch")
    for commit in mapping["landing_commits"]:
        landed = api.get(f"/repos/{repository}/commits/{commit}")
        require(landed.get("sha") == commit and (landed.get("author") or {}).get("login", "").lower() == username.lower(), "Landing commit author cannot be mapped to the configured user; review attribution")
        comparison = api.get(f"/repos/{repository}/compare/{commit}...{head}")
        require(comparison.get("status") in ("ahead", "identical"), "Landing commit is not an ancestor of the fixed default-branch head")
        require(comparison.get("base_commit", {}).get("sha") == commit and comparison.get("merge_base_commit", {}).get("sha") == commit, "Comparison does not prove landing ancestry")
        require(type(comparison.get("behind_by")) is int and comparison["behind_by"] == 0 and type(comparison.get("ahead_by")) is int and comparison["ahead_by"] >= 0, "Incomplete commit comparison")
    for record in mapping["reviewed_evidence"]:
        if record["kind"] == "pull_body":
            body = landing.get("body")
        elif record["kind"] == "issue_comment":
            comment = api.get(f"/repos/{repository}/issues/comments/{record['number']}")
            require(comment.get("issue_url", "").lower() == f"https://api.github.com/repos/{repository}/issues/{mapping['landing_pr']}".lower(), "Evidence comment belongs to another PR")
            body = comment.get("body")
        else:
            commit = api.get(f"/repos/{repository}/commits/{record['commit']}")
            require(commit.get("sha") == record["commit"], "Wrong evidence commit")
            body = commit.get("commit", {}).get("message")
        require(isinstance(body, str), "Evidence text is unavailable; review mapping")
        require(hashlib.sha256(body.encode("utf-8")).hexdigest() == record["sha256"], "Reviewed evidence has changed; review and refresh its exact UTF-8 hash")
        for field in ("source_excerpt", "attribution_excerpt"):
            if field in record:
                require(record[field] in body, f"Reviewed {field} is missing")
    return source, True


def collect(api, config, profile_branch=None):
    if profile_branch is None:
        profile_branch = repository_metadata(api, config["profile_repository"])["default_branch"]
    text(profile_branch, "profile branch")
    snapshots = []
    for configured in config["repositories"]:
        metadata = repository_metadata(api, configured["repository"])
        repository = metadata["full_name"]
        merged = merged_pulls(api, repository, config["username"])
        adopted = {}
        mappings = [m for m in config["confirmed_adoptions"] if m["repository"].lower() == repository.lower()]
        head = None
        if mappings:
            branch = urllib.parse.quote(metadata["default_branch"], safe="")
            head = api.get(f"/repos/{repository}/commits/{branch}").get("sha")
            require(isinstance(head, str) and SHA.fullmatch(head), "Cannot freeze upstream default branch head")
        for mapping in mappings:
            source, is_adopted = verify_adoption(api, mapping, metadata, head, config["username"])
            if source["merged"]:
                merged[source["number"]] = source
            elif is_adopted:
                adopted[source["number"]] = (source, mapping)
        snapshots.append({"config": configured, "metadata": metadata, "merged": merged, "adopted": adopted, "head": head})
    snapshots.sort(key=lambda s: (-s["metadata"]["stargazers_count"], s["metadata"]["full_name"].lower()))
    return profile_branch, snapshots


def markdown(value):
    value = " ".join(value.splitlines())
    value = html.escape(value, quote=False)
    return re.sub(r"([\\`*_{}\[\]()#+.!|>~-])", r"\\\1", value)


def github_url(repository, suffix=""):
    return "https://github.com/" + urllib.parse.quote(repository, safe="/") + suffix


def adopted_count(snapshot):
    if snapshot["config"].get("adopted_unit", "prs") == "commits":
        return len({sha for _, mapping in snapshot["adopted"].values() for sha in mapping["landing_commits"]}), "commit"
    return len(snapshot["adopted"]), "PR"


def render_contribution_list(lines):
    return "<h3>\n\n" + "\n".join(f"- {line}" for line in lines) + "\n- …\n\n</h3>" if lines else ""


def render(config, branch, snapshots):
    profile = config["profile_repository"]
    branch_path = urllib.parse.quote(branch, safe="")
    lines, counted_lines = [], []
    units = "Adopted PRs count each original PR once."
    if any(repo.get("adopted_unit") == "commits" for repo in config["repositories"]):
        units += " Where explicitly configured, adopted commits count distinct verified landing commits instead; the original PR mappings remain listed below."
    details = ["Historical accepted contributions by [" + markdown(config["username"]) + "](" + github_url(config["username"]) + ").", "", "Merged PRs include all upstream target branches; each target branch is listed below. Adopted contributions are accepted via cherry-pick or upstream integration into the upstream default branch. " + units + " A later direct merge takes precedence and excludes that source PR's adoption mapping. Later refactoring or reverts do not erase historical acceptance.", ""]
    for snapshot in snapshots:
        repo, metadata = snapshot["config"], snapshot["metadata"]
        merged, adopted = snapshot["merged"], snapshot["adopted"]
        count, unit = adopted_count(snapshot)
        accepted = [(kind, number) for kind, number in (("merged", len(merged)), ("🍒picked", count)) if number]
        counts = [f"{number} {kind}" for kind, number in accepted]
        if counts:
            raw = f"https://raw.githubusercontent.com/{urllib.parse.quote(profile, safe='/')}/{branch_path}/"
            logo = f'<img src="{raw}{urllib.parse.quote(repo["logo"], safe="/")}" width="{config["logo_size"]}" height="{config["logo_size"]}" alt="{html.escape(repo["display_name"] + " logo", quote=True)}">'
            if "logo_dark" in repo:
                logo = f'<picture><source media="(prefers-color-scheme: dark)" srcset="{raw}{urllib.parse.quote(repo["logo_dark"], safe="/")}">{logo}</picture>'
            target = github_url(profile, f"/blob/{branch_path}/CONTRIBUTIONS.md#{repo['anchor']}")
            stars = metadata["stargazers_count"]
            star_text = f"~{(stars + 500) // 1000}k" if stars >= 1000 else str(stars)
            star_label = f" <sub>({star_text}&nbsp;⭐)</sub>" if config["show_stars"] else ""
            project = f'[{markdown(repo["display_name"])}]({metadata["html_url"]}) {logo}{star_label}'
            lines.append(project)
            counted_lines.append(f'{project} — [{" · ".join(counts)}]({target})')
        details.extend([f'<a id="{repo["anchor"]}"></a>', f'## [{markdown(repo["display_name"])}]({metadata["html_url"]})', ""])
        if adopted and unit == "commit":
            details.extend([f"{count} adopted commit{'s' if count != 1 else ''} from {len(adopted)} source PR{'s' if len(adopted) != 1 else ''} (distinct verified landing commits).", ""])
        if not counts:
            details.extend(["No verified accepted PRs.", ""])
        for number, pr in sorted(merged.items()):
            details.extend([f'- [#{number}: {markdown(pr["title"])}]({pr["html_url"]}) — Merged into **{markdown(pr["base"]["ref"])}** on {markdown(pr["merged_at"][:10])}.'])
            commit = pr.get("merge_commit_sha")
            require(isinstance(commit, str) and SHA.fullmatch(commit), "Merged PR is missing its merge commit SHA")
            details.append(f'  - [Recorded merge commit `{commit[:12]}`]({github_url(metadata["full_name"], "/commit/" + commit)}). GitHub confirms the merge; the API does not reliably distinguish merge, squash, and rebase methods.')
        for number, (pr, mapping) in sorted(adopted.items()):
            details.extend([f'- [#{number}: {markdown(pr["title"])}]({pr["html_url"]}) — Adopted via cherry-pick or upstream integration.', f'  - [Upstream integration #{mapping["landing_pr"]}]({mapping["evidence_url"]}); verified in the upstream default branch **{markdown(metadata["default_branch"])}**.'])
            commits = ", ".join(f'[`{sha[:12]}`]({github_url(metadata["full_name"], "/commit/" + sha)})' for sha in mapping["landing_commits"])
            details.append(f"  - Landing commits: {commits}.")
            for record in mapping["reviewed_evidence"]:
                if record["kind"] == "commit_message":
                    url = github_url(metadata["full_name"], "/commit/" + record["commit"])
                else:
                    url = mapping["evidence_url"] + (f'#issuecomment-{record["number"]}' if record["kind"] == "issue_comment" else "")
                for key, label in (("source_excerpt", "Source evidence"), ("attribution_excerpt", "Attribution evidence")):
                    if key in record:
                        details.append(f'  - [{label}]({url}): “{markdown(record[key])}”')
        details.append("")
    summary = render_contribution_list(counted_lines)
    details = ["# 📜 Contributions", "", summary, "", *details]
    return render_contribution_list(lines), "\n".join(details).rstrip() + "\n"


def replace_block(readme, block, start_marker=START, end_marker=END):
    require(readme.count(start_marker) == 1 and readme.count(end_marker) == 1 and readme.index(start_marker) < readme.index(end_marker), "README needs exactly one correctly ordered marker pair")
    start = readme.index(start_marker) + len(start_marker)
    return readme[:start] + "\n" + block + "\n" + readme[readme.index(end_marker):]


def read_exact(path):
    return path.read_bytes().decode("utf-8")


def write_files(changes, expected=None):
    """Stage all bytes first, preserve no-op mtimes, and roll back ordinary I/O errors."""
    staged, originals, replaced = {}, {}, []
    try:
        for path, content in changes.items():
            original = path.read_bytes() if path.exists() else None
            if expected is not None:
                require(original == expected[path], f"{path.name} changed during verification; retry without overwriting concurrent edits")
            data = content.encode("utf-8")
            if original == data:
                continue
            require(not path.is_symlink(), f"Refusing to replace a symlink: {path}")
            originals[path] = original
            with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".contributions-", delete=False) as temporary:
                staged[path] = Path(temporary.name)
                temporary.write(data)
                temporary.flush()
                os.fsync(temporary.fileno())
            os.chmod(staged[path], path.stat().st_mode & 0o777 if path.exists() else 0o644)
        for path, temporary in staged.items():
            require((path.read_bytes() if path.exists() else None) == originals[path], f"{path.name} changed during staging; refusing to overwrite concurrent edits")
            os.replace(temporary, path)
            replaced.append(path)
    except (OSError, VerificationError):
        for path in reversed(replaced):
            if path.is_symlink() or not path.exists() or path.read_bytes() != changes[path].encode("utf-8"):
                continue  # A concurrent edit takes precedence over rollback.
            if originals[path] is None:
                path.unlink()
            else:
                path.write_bytes(originals[path])
        raise
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)
    return len(staged)


def run(root, api, write=False, profile_branch=None):
    config = validate_config(json.loads(read_exact(root / "contributions.json")), root)
    readme_path, details_path = root / "README.md", root / "CONTRIBUTIONS.md"
    require(not readme_path.is_symlink() and not details_path.is_symlink(), "Generated Markdown paths must not be symlinks")
    originals = {path: path.read_bytes() if path.exists() else None for path in (readme_path, details_path)}
    require(originals[readme_path] is not None, "README.md is missing")
    readme = originals[readme_path].decode("utf-8")
    replace_block(readme, "")  # Validate the user's document before network access.
    if "own_stars" in config:
        replace_block(readme, "", OWN_START, OWN_END)
    branch, snapshots = collect(api, config, profile_branch)
    block, details = render(config, branch, snapshots)
    updated_readme = replace_block(readme, block)
    if "own_stars" in config:
        include_forks = config["own_stars"]["include_forks"]
        total = owned_repository_stars(api, config["username"], include_forks)
        scope = "Public repository stars" if include_forks else "Public non-fork repository stars"
        target = github_url(config["username"]) + "?tab=repositories"
        own_block = f'<div align="right"><a href="{target}" title="{scope}"><strong>☆ {total:,}</strong></a></div>'
        updated_readme = replace_block(updated_readme, own_block, OWN_START, OWN_END)
        print(f'Owned public repository stars: {total} (include_forks={include_forks})', file=sys.stderr)
    changes = {readme_path: updated_readme, details_path: details}
    for snapshot in snapshots:
        count, unit = adopted_count(snapshot)
        print(f'{snapshot["metadata"]["full_name"]}: stars={snapshot["metadata"]["stargazers_count"]} merged={len(snapshot["merged"])} PR(s) adopted={count} {unit}(s) adopted_source_prs={len(snapshot["adopted"])} default_head={snapshot["head"] or "not needed"}', file=sys.stderr)
    if write:
        print(f"Updated {write_files(changes, originals)} file(s).", file=sys.stderr)
    else:
        for path, new in changes.items():
            old = read_exact(path) if path.exists() else ""
            sys.stdout.writelines(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True), fromfile=f"a/{path.name}", tofile=f"b/{path.name}"))
    return changes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Show a diff; never write files (default)")
    mode.add_argument("--write", action="store_true", help="Write README.md and CONTRIBUTIONS.md after full verification")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--profile-branch", help="Explicit planned profile branch for local prepublication; otherwise query GitHub (never silently default)")
    args = parser.parse_args(argv)
    try:
        run(args.root.resolve(), GitHub(os.environ.get("GITHUB_TOKEN")), args.write, args.profile_branch)
    except (VerificationError, OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
