"""All fixtures are synthetic and offline; no live state or network is needed."""

from contextlib import redirect_stderr, redirect_stdout
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

SPEC = importlib.util.spec_from_file_location("updater", Path(__file__).resolve().parents[1] / "scripts/update_contributions.py")
u = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(u)
REPO = "Upstream/project"
SHA1, SHA2, HEAD = "a" * 40, "b" * 40, "c" * 40
BODY = "Salvages #7 (@Person), both commits cherry-picked.\n"


def metadata(repo=REPO, stars=10, branch="main"):
    return {"full_name": repo, "html_url": "https://github.com/" + repo, "stargazers_count": stars, "default_branch": branch}


def pr(number=1, merged=True, author="Person", repo=REPO, branch="main"):
    return {"number": number, "user": {"login": author}, "title": f"Example PR {number}", "html_url": f"https://github.com/{repo}/pull/{number}", "base": {"repo": {"full_name": repo}, "ref": branch}, "merged": merged, "merged_at": "2026-09-01T01:02:03Z" if merged else None, "merge_commit_sha": SHA1 if merged else None, "body": BODY, "state": "closed"}


def mapping():
    return {"repository": REPO, "source_pr": 7, "landing_pr": 8, "evidence_url": f"https://github.com/{REPO}/pull/8", "landing_commits": [SHA1, SHA2], "reviewed_evidence": [{"kind": "pull_body", "number": 8, "sha256": hashlib.sha256(BODY.encode()).hexdigest(), "source_excerpt": "Salvages #7", "attribution_excerpt": "@Person"}]}


def configuration(adoptions=None):
    return {"version": 1, "username": "Person", "profile_repository": "Person/Person", "sort_by": "stars_desc", "show_stars": False, "logo_size": 18, "repositories": [{"repository": REPO, "display_name": "Project", "anchor": "project", "logo": "assets/logos/project.png"}], "confirmed_adoptions": adoptions or []}


def owned_repo(number, stars=1, fork=False):
    return {"id": number, "full_name": f"Person/project{number}", "owner": {"login": "Person"},
            "private": False, "fork": fork, "stargazers_count": stars}


class FakeAPI:
    def __init__(self, pulls=None, adoptions=False):
        self.calls = []
        self.data = {f"/repos/{REPO}": metadata(), "/repos/Person/Person": metadata("Person/Person", 0, "published"), f"/repos/{REPO}/commits/main": {"sha": HEAD}}
        self.pages = []
        pulls = pulls or []
        for value in pulls:
            self.data[f"/repos/{REPO}/pulls/{value['number']}"] = value
        for offset in range(0, len(pulls), 100):
            self.pages.append({"total_count": len(pulls), "incomplete_results": False, "items": [{"number": p["number"], "pull_request": {}} for p in pulls[offset:offset + 100]]})
        if not self.pages:
            self.pages = [{"total_count": 0, "incomplete_results": False, "items": []}]
        if adoptions:
            self.data[f"/repos/{REPO}/pulls/7"] = pr(7, False)
            self.data[f"/repos/{REPO}/pulls/8"] = pr(8, True, "Maintainer")
            for sha in (SHA1, SHA2):
                self.data[f"/repos/{REPO}/commits/{sha}"] = {"sha": sha, "author": {"login": "Person"}, "commit": {"message": BODY}}
                self.data[f"/repos/{REPO}/compare/{sha}...{HEAD}"] = {"status": "ahead", "ahead_by": 10702, "behind_by": 0, "total_commits": 10000, "base_commit": {"sha": sha}, "merge_base_commit": {"sha": sha}}

    def get(self, path, **params):
        self.calls.append((path, params))
        if path == "/users/Person/repos":
            return copy.deepcopy(self.owned_pages[params["page"] - 1])
        result = self.pages[params["page"] - 1] if path == "/search/issues" else self.data[path]
        if isinstance(result, Exception):
            raise result
        return copy.deepcopy(result)


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "assets/logos").mkdir(parents=True)
        (self.root / "assets/logos/project.png").write_bytes(b"synthetic logo")
        self.config = configuration()
        self.original = "# Person\r\n\r\nHandwritten café & intro.\r\n" + u.START + "\nold\n" + u.END + "\nKeep this suffix.\n"
        (self.root / "README.md").write_bytes(self.original.encode())
        (self.root / "CONTRIBUTIONS.md").write_text("previous details\n")
        self.save_config()

    def save_config(self):
        (self.root / "contributions.json").write_text(json.dumps(self.config))

    def run_generator(self, api, write=True):
        self.save_config()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return u.run(self.root, api, write=write, profile_branch="main")

    def assert_unchanged(self):
        self.assertEqual((self.root / "README.md").read_bytes(), self.original.encode())
        self.assertEqual((self.root / "CONTRIBUTIONS.md").read_text(), "previous details\n")

    def test_merged_one_and_all_target_branches(self):
        result = self.run_generator(FakeAPI([pr(branch="release/v1")]))
        self.assertIn("1 merged]", result[self.root / "CONTRIBUTIONS.md"])
        self.assertIn("release/v1", result[self.root / "CONTRIBUTIONS.md"])
        self.assertNotIn(" PR]", result[self.root / "README.md"])

    def test_detail_summary_preserves_counts_while_home_shows_only_projects(self):
        self.config = configuration([mapping()])
        self.config["show_stars"] = True
        result = self.run_generator(FakeAPI([pr()], adoptions=True))
        home = result[self.root / "README.md"]
        details = result[self.root / "CONTRIBUTIONS.md"]
        block = home.split(u.START)[1].split(u.END)[0].strip()
        self.assertNotIn("merged", block)
        self.assertNotIn("🍒picked", block)
        self.assertNotIn(" — ", block)
        project_line = next(line for line in block.splitlines() if line.startswith("- ["))
        counted_block = block.replace(project_line, project_line + " — [1 merged · 1 🍒picked](https://github.com/Person/Person/blob/main/CONTRIBUTIONS.md#project)")
        self.assertTrue(details.startswith("# 📜 Contributions\n\n" + counted_block + "\n\n"))
        self.assertLess(details.index(counted_block), details.index("Historical accepted contributions"))
        self.assertIn('CONTRIBUTIONS.md#project)', counted_block)
        self.assertIn('<a id="project"></a>', details)
        self.assertEqual(counted_block.count("(10&nbsp;⭐)"), 1)

    def test_new_merge_updates_details_without_churning_home(self):
        self.run_generator(FakeAPI([pr()]))
        path = self.root / "README.md"
        before = (path.read_bytes(), path.stat().st_mtime_ns)
        result = self.run_generator(FakeAPI([pr(), pr(2)]))
        self.assertEqual(before, (path.read_bytes(), path.stat().st_mtime_ns))
        self.assertIn("[2 merged]", result[self.root / "CONTRIBUTIONS.md"])

    def test_owned_stars_updates_only_its_marker_and_preserves_outline_symbol(self):
        self.config["own_stars"] = {"include_forks": False}
        old = u.OWN_START + "\nold total\n" + u.OWN_END + "\n" + self.original
        (self.root / "README.md").write_text(old)
        api = FakeAPI([pr()])
        api.owned_pages = [[owned_repo(1, 53), owned_repo(2, 99, True)]]
        result = self.run_generator(api)
        readme = result[self.root / "README.md"]
        self.assertIn('align="right"', readme)
        self.assertIn('☆ 53', readme)
        self.assertNotIn('☆ 152', readme)
        self.assertIn('alt="☆ 53"', readme)
        for asset in u.OWN_STAR_ASSETS:
            self.assertIn("☆ 53", result[self.root / asset])
        self.assertIn("#0969da", result[self.root / u.OWN_STAR_ASSETS[0]])
        self.assertIn("#4493f8", result[self.root / u.OWN_STAR_ASSETS[1]])
        self.assertEqual(readme.split(u.OWN_END)[1].split(u.START)[0],
                         old.split(u.OWN_END)[1].split(u.START)[0])
        self.config["own_stars"]["include_forks"] = True
        self.assertIn('☆ 152', self.run_generator(api)[self.root / "README.md"])

    def test_star_display_can_be_hidden_and_restored_without_losing_counts(self):
        self.config["own_stars"] = {"include_forks": True, "show": False}
        self.config["show_stars"] = False
        old = u.OWN_START + "\nold total\n" + u.OWN_END + "\n" + self.original
        (self.root / "README.md").write_text(old)
        api = FakeAPI([pr()]); api.owned_pages = [[owned_repo(1, 53), owned_repo(2, 6, True)]]
        result = self.run_generator(api)
        self.assertNotIn("☆", result[self.root / "README.md"])
        self.assertNotIn("⭐", result[self.root / "README.md"])
        self.assertNotIn("⭐", result[self.root / "CONTRIBUTIONS.md"])
        self.assertIn("[1 merged]", result[self.root / "CONTRIBUTIONS.md"])
        self.assertIn(u.OWN_START + "\n\n" + u.OWN_END, result[self.root / "README.md"])
        self.assertIn("☆ 59", result[self.root / u.OWN_STAR_ASSETS[0]])
        self.config["own_stars"]["show"] = True
        self.config["show_stars"] = True
        restored = self.run_generator(api)
        self.assertIn("☆ 59", restored[self.root / "README.md"])
        self.assertIn("⭐", restored[self.root / "README.md"])

    def test_own_star_display_flag_must_be_boolean(self):
        self.config["own_stars"] = {"include_forks": True, "show": "false"}
        with self.assertRaises(u.VerificationError):
            u.validate_config(self.config, self.root)

    def test_owned_stars_missing_marker_fails_before_network(self):
        self.config["own_stars"] = {"include_forks": False}
        api = FakeAPI([pr()])
        with self.assertRaises(u.VerificationError):
            self.run_generator(api)
        self.assertEqual(api.calls, [])
        self.assert_unchanged()

    def test_owned_stars_bad_data_preserves_both_files(self):
        self.config["own_stars"] = {"include_forks": False}
        old = u.OWN_START + "\n☆ 53\n" + u.OWN_END + "\n" + self.original
        (self.root / "README.md").write_text(old)
        api = FakeAPI([pr()]); api.owned_pages = [[owned_repo(1, -1)]]
        with self.assertRaises(u.VerificationError):
            self.run_generator(api)
        self.assertEqual((self.root / "README.md").read_bytes().decode(), old)
        self.assertEqual((self.root / "CONTRIBUTIONS.md").read_text(), "previous details\n")

    def test_closed_unmerged_search_hit_is_not_accepted(self):
        with self.assertRaises(u.VerificationError):
            self.run_generator(FakeAPI([pr(merged=False)]))
        self.assert_unchanged()

    def test_two_commits_one_adopted(self):
        self.config = configuration([mapping()])
        result = self.run_generator(FakeAPI(adoptions=True))
        self.assertIn("1 🍒picked]", result[self.root / "CONTRIBUTIONS.md"])
        self.assertNotIn(" merged", result[self.root / "README.md"])
        self.assertIn(SHA1[:12], result[self.root / "CONTRIBUTIONS.md"])
        self.assertIn(SHA2[:12], result[self.root / "CONTRIBUTIONS.md"])

    def test_configured_commit_unit_counts_union_of_landing_commits(self):
        other = mapping()
        other.update(source_pr=9, landing_commits=["d" * 40])
        self.config = configuration([mapping(), other])
        api = FakeAPI(adoptions=True)
        api.data[f"/repos/{REPO}/pulls/9"] = pr(9, False)
        api.data[f"/repos/{REPO}/commits/{'d' * 40}"] = {"sha": "d" * 40, "author": {"login": "Person"}}
        api.data[f"/repos/{REPO}/compare/{'d' * 40}...{HEAD}"] = dict(api.data[f"/repos/{REPO}/compare/{SHA1}...{HEAD}"], base_commit={"sha": "d" * 40}, merge_base_commit={"sha": "d" * 40})
        default = self.run_generator(api)
        self.assertIn("2 🍒picked]", default[self.root / "CONTRIBUTIONS.md"])
        self.config["repositories"][0]["adopted_unit"] = "commits"
        result = self.run_generator(api)
        self.assertIn("3 🍒picked]", result[self.root / "CONTRIBUTIONS.md"])
        self.assertIn("3 adopted commits from 2 source PRs", result[self.root / "CONTRIBUTIONS.md"])
        other["landing_commits"] = [SHA1]  # Shared commit is counted once across original PRs.
        result = self.run_generator(api)
        self.assertIn("2 🍒picked]", result[self.root / "CONTRIBUTIONS.md"])
        api.data[f"/repos/{REPO}/pulls/7"] = pr(7)
        result = self.run_generator(api)
        self.assertIn("1 merged · 1 🍒picked]", result[self.root / "CONTRIBUTIONS.md"])
        self.assertIn("1 adopted commit from 1 source PR", result[self.root / "CONTRIBUTIONS.md"])

    def test_later_merge_deduplicates_and_handles_search_index_lag(self):
        self.config = configuration([mapping()])
        for indexed in (False, True):
            with self.subTest(indexed=indexed):
                api = FakeAPI([pr(7)] if indexed else [], adoptions=True)
                api.data[f"/repos/{REPO}/pulls/7"] = pr(7)
                result = self.run_generator(api)
                self.assertIn("1 merged]", result[self.root / "CONTRIBUTIONS.md"])
                self.assertNotIn(" adopted", result[self.root / "README.md"])

    def test_bad_adoptions_preserve_last_snapshot(self):
        self.config = configuration([mapping()])
        mutations = [
            (f"/repos/{REPO}/pulls/7", lambda p: p.update(user=None)),
            (f"/repos/{REPO}/pulls/7", lambda p: p.update(user={"login": "Other"})),
            (f"/repos/{REPO}/pulls/8", lambda p: p.update(merged=False, merged_at=None)),
            (f"/repos/{REPO}/pulls/8", lambda p: p["base"].update(ref="develop")),
            (f"/repos/{REPO}/pulls/8", lambda p: p["base"]["repo"].update(full_name="ThirdParty/project")),
            (f"/repos/{REPO}/pulls/8", lambda p: p.update(body="Related #7 @Person")),
            (f"/repos/{REPO}/pulls/8", lambda p: p.update(body=None)),
            (f"/repos/{REPO}/commits/{SHA1}", lambda p: p.update(author=None)),
            (f"/repos/{REPO}/commits/{SHA1}", lambda p: p.update(author={"login": "Other"})),
            (f"/repos/{REPO}/compare/{SHA1}...{HEAD}", lambda p: p.update(status="behind")),
            (f"/repos/{REPO}/compare/{SHA1}...{HEAD}", lambda p: p.update(status="diverged")),
            (f"/repos/{REPO}/compare/{SHA1}...{HEAD}", lambda p: p.update(merge_base_commit={"sha": SHA2})),
            (f"/repos/{REPO}/compare/{SHA1}...{HEAD}", lambda p: p.pop("ahead_by")),
        ]
        for path, mutate in mutations:
            with self.subTest(path=path, mutation=mutate):
                api = FakeAPI(adoptions=True)
                mutate(api.data[path])
                with self.assertRaises(u.VerificationError):
                    self.run_generator(api)
                self.assert_unchanged()

    def test_no_semantic_inference_from_unregistered_mentions(self):
        result = self.run_generator(FakeAPI(adoptions=True))
        self.assertNotIn(" adopted", result[self.root / "README.md"])

    def test_fixed_default_head_for_every_compare(self):
        api = FakeAPI(adoptions=True)
        self.config = configuration([mapping()])
        self.run_generator(api)
        comparisons = [path for path, _ in api.calls if "/compare/" in path]
        self.assertEqual(len(comparisons), 2)
        self.assertTrue(all(path.endswith("..." + HEAD) for path in comparisons))
        self.assertEqual(sum(path.endswith("/commits/main") for path, _ in api.calls), 1)

    def test_identical_ancestry_is_accepted(self):
        api = FakeAPI(adoptions=True)
        api.data[f"/repos/{REPO}/compare/{SHA1}...{HEAD}"].update(status="identical", ahead_by=0)
        self.assertTrue(u.verify_adoption(api, mapping(), metadata(), HEAD, "Person")[1])

    def test_pagination_reads_all_101(self):
        api = FakeAPI([pr(i) for i in range(1, 102)])
        self.assertEqual(len(u.merged_pulls(api, REPO, "Person")), 101)
        self.assertEqual([params["page"] for path, params in api.calls if path == "/search/issues"], [1, 2])

    def test_incomplete_or_truncated_search_fails(self):
        mutations = [lambda p: p.update(incomplete_results=True), lambda p: p.update(total_count=1001), lambda p: p.update(total_count=2), lambda p: p.update(total_count=True), lambda p: p.update(items=[]), lambda p: p["items"][0].pop("pull_request")]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                api = FakeAPI([pr()])
                mutation(api.pages[0])
                with self.assertRaises(u.VerificationError):
                    self.run_generator(api)
                self.assert_unchanged()

    def test_duplicate_and_changed_search_pages_fail(self):
        for duplicate in (True, False):
            api = FakeAPI([pr(i) for i in range(1, 102)])
            if duplicate:
                api.pages[1]["items"][0]["number"] = 1
            else:
                api.pages[1]["total_count"] = 102
            with self.assertRaises(u.VerificationError):
                self.run_generator(api)
            self.assert_unchanged()

    def test_merged_crosschecks_author_repo_url_state(self):
        mutations = [lambda p: p.update(user=None), lambda p: p.update(user={"login": "Other"}), lambda p: p["base"]["repo"].update(full_name="Fork/project"), lambda p: p.update(html_url="https://evil.invalid/"), lambda p: p.update(merged_at=None), lambda p: p.update(merge_commit_sha=None)]
        for mutation in mutations:
            api = FakeAPI([pr()])
            mutation(api.data[f"/repos/{REPO}/pulls/1"])
            with self.assertRaises(u.VerificationError):
                self.run_generator(api)
            self.assert_unchanged()

    def test_stars_integer_and_stable_tie_sort(self):
        self.config["repositories"].extend([dict(self.config["repositories"][0], repository="aaa/other", display_name="A", anchor="a"), dict(self.config["repositories"][0], repository="zzz/other", display_name="Z", anchor="z")])
        api = FakeAPI()
        api.data["/repos/aaa/other"] = metadata("aaa/other", 9)
        api.data["/repos/zzz/other"] = metadata("zzz/other", 10)
        self.assertEqual([s["metadata"]["full_name"] for s in u.collect(api, self.config, "main")[1]], [REPO, "zzz/other", "aaa/other"])
        api.data["/repos/aaa/other"]["stargazers_count"] = 11
        self.assertEqual(u.collect(api, self.config, "main")[1][0]["metadata"]["full_name"], "aaa/other")

    def test_zero_categories_and_project_only_home(self):
        for count in (0, 1, 2):
            result = self.run_generator(FakeAPI([pr(i) for i in range(1, count + 1)]))
            readme = result[self.root / "README.md"]
            self.assertNotIn("0 ", readme)
            self.assertNotIn("adopted", readme)
            if count:
                self.assertIn("[Project]", readme)
                self.assertNotIn("merged", readme)
                self.assertNotIn(f"{count} merged]", readme)
                self.assertIn(f"{count} merged]", result[self.root / "CONTRIBUTIONS.md"])
                self.assertNotIn(" PR", readme)
            else:
                self.assertNotIn("[Project]", readme)
                self.assertNotIn("<h3>", readme)

    def test_readme_outside_markers_byte_preserved(self):
        self.run_generator(FakeAPI([pr()]))
        updated = (self.root / "README.md").read_bytes().decode()
        self.assertEqual(updated.split(u.START)[0], self.original.split(u.START)[0])
        self.assertEqual(updated.split(u.END)[1], self.original.split(u.END)[1])

    def test_bad_markers_fail_before_api(self):
        for value in ("none", u.START, u.END + u.START, u.START + u.START + u.END, u.START + u.END + u.END):
            (self.root / "README.md").write_text(value)
            api = FakeAPI()
            with self.assertRaises(u.VerificationError):
                self.run_generator(api)
            self.assertEqual(api.calls, [])
            self.assertEqual((self.root / "README.md").read_text(), value)

    def test_encoding_logo_order_and_theme(self):
        self.config["logo_size"] = 25
        self.config["repositories"][0].update(display_name='X [bad](url) <script> & "', logo_dark="assets/logos/project.png")
        api = FakeAPI([pr()])
        api.data[f"/repos/{REPO}/pulls/1"]["title"] = "<script>alert(1)</script> [click](https://evil.invalid)\n# heading"
        result = self.run_generator(api)
        readme = result[self.root / "README.md"]
        self.assertLess(readme.index("]("), readme.index("<picture>"))
        self.assertIn('width="25" height="25"', readme)
        self.assertIn('media="(prefers-color-scheme: dark)"', readme)
        self.assertNotIn("<script>", readme)
        self.assertIn("&quot;", readme)
        self.assertNotIn("<script>", result[self.root / "CONTRIBUTIONS.md"])
        self.assertIn("\\[click\\]", result[self.root / "CONTRIBUTIONS.md"])

    def test_badge_names_escape_shields_syntax_and_keep_details_plain(self):
        self.config["repositories"][0].update(display_name="ASu-skills_v2", badge_color="6265A8")
        result = self.run_generator(FakeAPI([pr()]))
        home = result[self.root / "README.md"]
        details = result[self.root / "CONTRIBUTIONS.md"]
        self.assertIn("https://img.shields.io/badge/ASu--skills__v2-6265A8?style=flat", home)
        self.assertIn("](https://github.com/Upstream/project)", home)
        self.assertLess(home.index("img.shields.io"), home.index('alt="ASu-skills_v2 logo"'))
        self.assertNotIn("img.shields.io", details)
        self.assertIn("[1 merged]", details)
        self.assertNotIn("[1 merged]", home)
        self.config["repositories"][0]["display_name"] = "Hermes Agent"
        self.assertIn("Hermes%20Agent-6265A8", self.run_generator(FakeAPI([pr()]))[self.root / "README.md"])

    def test_badge_color_rejects_non_hex_or_injected_values(self):
        for color in (None, True, "red", "#ff0000", "ff0000?logo=github", 'ffffff" onclick="bad'):
            with self.subTest(color=color):
                self.config["repositories"][0]["badge_color"] = color
                with self.assertRaises(u.VerificationError):
                    u.validate_config(self.config, self.root)

    def test_real_profile_branch_or_explicit_override_no_fallback(self):
        api = FakeAPI()
        self.assertEqual(u.collect(api, self.config)[0], "published")
        api.data["/repos/Person/Person"] = u.VerificationError("HTTP 404")
        with self.assertRaises(u.VerificationError):
            u.collect(api, self.config)
        self.assertEqual(u.collect(api, self.config, "planned/branch")[0], "planned/branch")
        branch, snapshots = u.collect(FakeAPI([pr()]), self.config, "planned/branch")
        self.assertIn("planned%2Fbranch", u.render(self.config, branch, snapshots)[0])

    def test_dry_run_diff_without_writes(self):
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(io.StringIO()):
            u.run(self.root, FakeAPI([pr()]), profile_branch="main")
        self.assertIn("--- a/README.md", output.getvalue())
        self.assertIn("+++ b/CONTRIBUTIONS.md", output.getvalue())
        self.assert_unchanged()

    def test_noop_keeps_bytes_mtime_and_ignores_star_only_changes(self):
        self.run_generator(FakeAPI([pr()]))
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in (self.root / "README.md", self.root / "CONTRIBUTIONS.md")}
        api = FakeAPI([pr()])
        api.data[f"/repos/{REPO}"]["stargazers_count"] = 999999
        self.run_generator(api)
        self.assertEqual(before, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in before})

    def test_shown_stars_use_live_integer_and_round_half_up(self):
        self.config["show_stars"] = True
        for stars, label in ((0, "(0 ⭐)"), (999, "(999 ⭐)"), (1000, "(~1k ⭐)"),
                             (383499, "(~383k ⭐)"), (383500, "(~384k ⭐)"),
                             (390815, "(~391k ⭐)"), (5274, "(~5k ⭐)")):
            with self.subTest(stars=stars):
                api = FakeAPI([pr()])
                api.data[f"/repos/{REPO}"]["stargazers_count"] = stars
                readme = self.run_generator(api)[self.root / "README.md"].replace("&nbsp;", " ")
                self.assertIn(label, readme)
                self.assertGreater(readme.index(label), readme.index('alt="Project logo">'))
                self.assertNotIn(" — ", readme)

    def test_shown_stars_only_write_when_display_changes(self):
        self.config["show_stars"] = True
        def api_with_stars(stars):
            api = FakeAPI([pr()])
            api.data[f"/repos/{REPO}"]["stargazers_count"] = stars
            return api
        self.run_generator(api_with_stars(383001))
        paths = (self.root / "README.md", self.root / "CONTRIBUTIONS.md")
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths}
        self.run_generator(api_with_stars(383499))
        self.assertEqual(before, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths})
        self.run_generator(api_with_stars(383500))
        self.assertIn("(~384k ⭐)", paths[0].read_text().replace("&nbsp;", " "))
        self.assertIn("(~384k ⭐)", paths[1].read_text().replace("&nbsp;", " "))
        self.assertNotEqual(before[paths[1]][0], paths[1].read_bytes())

    def test_api_error_preserves_files(self):
        api = FakeAPI()
        api.data[f"/repos/{REPO}"] = u.VerificationError("HTTP 404")
        with self.assertRaises(u.VerificationError):
            self.run_generator(api)
        self.assert_unchanged()

    def test_concurrent_edits_during_api_are_preserved(self):
        for name in ("README.md", "CONTRIBUTIONS.md"):
            with self.subTest(name=name):
                (self.root / "README.md").write_bytes(self.original.encode())
                (self.root / "CONTRIBUTIONS.md").write_text("previous details\n")
                api = FakeAPI([pr()])
                original_get = api.get
                changed = self.root / name
                def concurrent_get(path, **params):
                    changed.write_text("user changed this during verification\n")
                    return original_get(path, **params)
                api.get = concurrent_get
                with self.assertRaises(u.VerificationError):
                    self.run_generator(api)
                self.assertEqual(changed.read_text(), "user changed this during verification\n")
                if name == "CONTRIBUTIONS.md":
                    self.assertEqual((self.root / "README.md").read_bytes(), self.original.encode())
                else:
                    self.assertEqual((self.root / "CONTRIBUTIONS.md").read_text(), "previous details\n")

    def test_concurrent_edit_during_staging_rolls_back_other_file(self):
        real_replace = u.os.replace
        def edit_after_first(source, destination):
            real_replace(source, destination)
            (self.root / "CONTRIBUTIONS.md").write_text("user concurrent details\n")
        with patch.object(u.os, "replace", side_effect=edit_after_first), self.assertRaises(u.VerificationError):
            self.run_generator(FakeAPI([pr()]))
        self.assertEqual((self.root / "README.md").read_bytes(), self.original.encode())
        self.assertEqual((self.root / "CONTRIBUTIONS.md").read_text(), "user concurrent details\n")

    def test_second_replace_failure_rolls_back_first(self):
        real_replace = u.os.replace
        calls = []
        def fail_second(source, destination):
            calls.append(destination)
            if len(calls) == 2:
                raise OSError("simulated disk failure")
            return real_replace(source, destination)
        with patch.object(u.os, "replace", side_effect=fail_second), self.assertRaises(OSError):
            self.run_generator(FakeAPI([pr()]))
        self.assert_unchanged()
        self.assertEqual(list(self.root.glob(".contributions-*")), [])

    def test_missing_details_rolls_back_creation_on_later_error(self):
        new = self.root / "new.md"
        real_replace = u.os.replace
        def fail_second(source, destination):
            if destination.name == "README.md":
                raise OSError("simulated failure")
            return real_replace(source, destination)
        with patch.object(u.os, "replace", side_effect=fail_second), self.assertRaises(OSError):
            u.write_files({new: "new", self.root / "README.md": "changed"})
        self.assertFalse(new.exists())
        self.assert_unchanged()

    def test_configuration_rejects_bad_types_duplicates_and_paths(self):
        mutations = [lambda c: c.update(version=True), lambda c: c.update(show_stars="true"), lambda c: c.update(show_stars=1), lambda c: c.update(username="person query:inject"), lambda c: c.update(profile_repository="Another/Another"), lambda c: c.update(logo_size=100), lambda c: c["repositories"].append(dict(c["repositories"][0], repository=REPO.lower())), lambda c: c["repositories"][0].update(repository="Person/fork"), lambda c: c["repositories"][0].update(anchor='bad"'), lambda c: c["repositories"][0].update(logo="../outside.png"), lambda c: c["repositories"][0].update(logo="assets/logos/missing.png"), lambda c: c["repositories"][0].update(unexpected=True)]
        for mutation in mutations:
            config = copy.deepcopy(self.config)
            mutation(config)
            with self.assertRaises(u.VerificationError):
                u.validate_config(config, self.root)

    def test_mapping_requires_whitelist_review_and_unique_source(self):
        mutations = [lambda m: m.update(repository="ThirdParty/project"), lambda m: m.update(source_pr=True), lambda m: m.update(evidence_url="https://evil.invalid/"), lambda m: m.update(landing_commits=[SHA1, SHA1]), lambda m: m.update(reviewed_evidence=[]), lambda m: m["reviewed_evidence"][0].pop("attribution_excerpt"), lambda m: m["reviewed_evidence"][0].update(number=999), lambda m: m["reviewed_evidence"][0].update(sha256="not a hash")]
        for mutation in mutations:
            value = mapping()
            mutation(value)
            with self.assertRaises(u.VerificationError):
                u.validate_config(configuration([value]), self.root)
        with self.assertRaises(u.VerificationError):
            u.validate_config(configuration([mapping(), mapping()]), self.root)

    def test_reviewed_excerpt_must_be_present_even_with_matching_hash(self):
        value = mapping()
        value["reviewed_evidence"][0]["source_excerpt"] = "missing"
        with self.assertRaises(u.VerificationError):
            u.verify_adoption(FakeAPI(adoptions=True), value, metadata(), HEAD, "Person")

    def test_separate_source_and_commit_attribution_evidence(self):
        value = mapping()
        value["reviewed_evidence"][0].pop("attribution_excerpt")
        value["reviewed_evidence"].append({"kind": "commit_message", "commit": SHA1, "sha256": hashlib.sha256(BODY.encode()).hexdigest(), "attribution_excerpt": "@Person"})
        u.validate_config(configuration([value]), self.root)
        self.assertTrue(u.verify_adoption(FakeAPI(adoptions=True), value, metadata(), HEAD, "Person")[1])

    def test_comment_evidence_must_belong_to_integration(self):
        value = mapping()
        value["reviewed_evidence"][0].update(kind="issue_comment", number=44)
        api = FakeAPI(adoptions=True)
        api.data[f"/repos/{REPO}/issues/comments/44"] = {"body": BODY, "issue_url": f"https://api.github.com/repos/{REPO}/issues/8"}
        self.assertTrue(u.verify_adoption(api, value, metadata(), HEAD, "Person")[1])
        api.data[f"/repos/{REPO}/issues/comments/44"]["issue_url"] = f"https://api.github.com/repos/Fork/project/issues/8"
        with self.assertRaises(u.VerificationError):
            u.verify_adoption(api, value, metadata(), HEAD, "Person")

    def test_symlink_output_fails_safely(self):
        details = self.root / "CONTRIBUTIONS.md"
        details.unlink()
        outside = self.root / "outside.md"
        outside.write_text("untouched")
        details.symlink_to(outside)
        with self.assertRaises(u.VerificationError):
            self.run_generator(FakeAPI([pr()]))
        self.assertEqual(outside.read_text(), "untouched")


class OwnedStarsTests(unittest.TestCase):
    def test_all_pages_and_fork_filter(self):
        api = FakeAPI()
        api.owned_pages = [[owned_repo(i) for i in range(1, 101)],
                           [owned_repo(101, 7), owned_repo(102, 100, True)]]
        self.assertEqual(u.owned_repository_stars(api, "Person"), 107)
        self.assertEqual(u.owned_repository_stars(api, "Person", True), 207)
        api.owned_pages = [[]]
        self.assertEqual(u.owned_repository_stars(api, "Person"), 0)

    def test_invalid_or_duplicate_repository_fails(self):
        bad = [{}, owned_repo(1, True), owned_repo(1, -1),
               dict(owned_repo(1), private=True), dict(owned_repo(1), fork="false"),
               dict(owned_repo(1), full_name="Someone/else"),
               dict(owned_repo(1), owner={"login": "Someone"})]
        for repo in bad:
            api = FakeAPI(); api.owned_pages = [[repo]]
            with self.subTest(repo=repo), self.assertRaises(u.VerificationError):
                u.owned_repository_stars(api, "Person")
        api = FakeAPI(); api.owned_pages = [[owned_repo(1), owned_repo(1)]]
        with self.assertRaises(u.VerificationError):
            u.owned_repository_stars(api, "Person")
        api.owned_pages = [{"message": "API error"}]
        with self.assertRaises(u.VerificationError):
            u.owned_repository_stars(api, "Person")


class TransportTests(unittest.TestCase):
    def test_url_encoded_query_timeout_token_and_cache(self):
        calls = []
        def opener(request, timeout):
            calls.append((request, timeout))
            return io.BytesIO(b'{"ok": true}')
        api = u.GitHub("synthetic-token", opener, lambda _: None)
        self.assertEqual(api.get("/search/issues", q="repo:A/B author:A is:merged"), {"ok": True})
        api.get("/search/issues", q="repo:A/B author:A is:merged")
        self.assertEqual(len(calls), 1)
        self.assertIn("repo%3AA%2FB+author%3AA+is%3Amerged", calls[0][0].full_url)
        self.assertEqual(calls[0][1], 30)
        self.assertEqual(calls[0][0].get_header("Authorization"), "Bearer synthetic-token")

    def test_bounded_retries_on_network_http_json_errors(self):
        errors = [urllib.error.URLError("offline"), TimeoutError(), OSError("network"), ValueError("invalid JSON")]
        errors.extend(urllib.error.HTTPError("https://api.github.com", code, "failure", {}, None) for code in (403, 429, 500, 503))
        for error in errors:
            attempts, delays = [], []
            def opener(request, timeout):
                attempts.append(request)
                raise error
            with self.assertRaises(u.VerificationError):
                u.GitHub(opener=opener, sleep=delays.append).get("/repos/A/B")
            self.assertEqual(len(attempts), 3)
            self.assertEqual(delays, [1, 2])

    def test_404_and_auth_fail_without_retry(self):
        for code in (401, 404, 422):
            attempts = []
            def opener(request, timeout):
                attempts.append(1)
                raise urllib.error.HTTPError(request.full_url, code, "failure", {}, None)
            with self.assertRaises(u.VerificationError):
                u.GitHub(opener=opener, sleep=lambda _: self.fail("unexpected retry")).get("/repos/A/B")
            self.assertEqual(len(attempts), 1)

    def test_repository_list_transport(self):
        api = u.GitHub(opener=lambda request, timeout: io.BytesIO(b"[]"))
        self.assertEqual(api.get("/users/Person/repos"), [])

    def test_invalid_json_recovers_on_retry(self):
        responses = iter([b"invalid", b'{"ok": true}'])
        api = u.GitHub(opener=lambda request, timeout: io.BytesIO(next(responses)), sleep=lambda _: None)
        self.assertTrue(api.get("/repos/A/B")["ok"])

    def test_redirect_never_forwards_token(self):
        with self.assertRaises(u.VerificationError):
            u.NoRedirect().redirect_request(None, None, 301, "moved", {}, "https://other.invalid/")

    def test_cli_errors_nonzero_without_traceback(self):
        with tempfile.TemporaryDirectory() as root, redirect_stderr(io.StringIO()) as stderr:
            self.assertEqual(u.main(["--root", root, "--dry-run"]), 1)
        self.assertIn("ERROR:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
