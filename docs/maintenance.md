# Maintaining the profile

The profile shows accepted contributions from the configured upstream repositories.
Merged contributions count original PRs, including documentation contributions.
At the owner's request, Hermes adoption counts unique verified landing commits:
the initial snapshot has **3 adopted commits from 2 source PRs**. Other repositories
default to counting original adopted PRs. It does not claim that
every merged PR targets the default branch or that accepted code remains unchanged.

## Local refresh

Python 3.13 and its standard library are sufficient; there are no package dependencies.

```sh
python -m unittest discover -s tests -v
python scripts/update_contributions.py --dry-run
python scripts/update_contributions.py --write
```

The dry run queries GitHub and prints a diff without modifying files. The write mode
updates only the marked block in `README.md` and `CONTRIBUTIONS.md`, after all upstream
checks succeed. Neither mode runs Git commands. Identical generated content leaves
files unchanged. API/search failures preserve the last successful files and exit
with an error. No cached or example counts replace a failed live query.

Before the profile repository exists, explicitly pass `--profile-branch main` for a
local preview. This is a proposed publication branch, not a verified remote default.
After publication, omit this flag so GitHub supplies the actual default branch.
Do not use the override to hide a repository access error.

Public API requests work without authentication within GitHub's rate limits. The
hosted workflow uses only its supplied `GITHUB_TOKEN`; no personal token is required.
The script never discovers credentials from Git, the CLI, or a keychain.

## Add an upstream repository

Add a repository object to `contributions.json`: upstream `repository`, official
`display_name`, stable lowercase `anchor`, and local `logo` path. Optional `logo_dark`
provides an official dark appearance asset. Optional `adopted_unit: "commits"` counts
unique verified landing commits instead of original adopted PRs.
Homepage labels stay short (`merged` / `adopted`); the details file explains the units. Only Hermes currently uses this explicit owner choice.
Verify and record the logo's provenance
in `assets/logos/SOURCES.md` before adding it. Counts are discovered from GitHub;
do not add a count field. Actual star integers determine order, but are not displayed.
Only configured upstream repositories are queried. A user's fork is not an upstream.

## Record an adopted PR

First manually inspect the original PR, upstream integration PR, and landing commits.
Require explicit source and author credit, and confirm adoption into the upstream
default branch. A mention or closed source PR alone is insufficient. Add the reviewed
mapping to `confirmed_adoptions`, including its reviewed evidence records. Each record
identifies a pull body, issue comment, or commit message and stores its SHA-256 plus
the exact source/attribution excerpts checked by the updater. Hash the API text exactly
with `hashlib.sha256(body.encode("utf-8")).hexdigest()`; do not normalize whitespace,
line endings, or Markdown. The evidence set must establish both the source
relationship and credit to the configured author; the script does not infer adoption.

The updater rechecks the source author, merged integration target, evidence text, and
landing-commit ancestry against a fixed default-branch head. With the default PR unit,
two landing commits from one source PR count once. With Hermes' commit unit, both count,
and a commit appearing in more than one mapping still counts once. A source PR later
merged directly is counted only as merged; its mapping is excluded from adopted counts.
If previously reviewed evidence changes, inspect the new text and update the reviewed
mapping only after confirming that it still proves the relationship. Do not bypass a
failed check by deleting a valid historic adoption or entering a manual count.

## Enable or restore updates — only after owner approval

The workflow has UTC schedule `17 */6 * * *` and a **Run workflow** entry. Its update
job remains disabled until the repository variable `ENABLE_PROFILE_UPDATES` equals
`true`. Publication and automatic writes require separate owner approval. Leave the
variable unset during review. Setting it is a repository setting change.

After approval, publish to the actual default branch, set the variable, and use
Actions → Update contributions → Run workflow. Check the run and the real GitHub
profile in light/dark appearances; the local HTML preview is only layout evidence.
To suspend writes, remove the variable or set it to `false`.

The job tests offline before fetching live data, has a ten-minute timeout, and
serializes manual/scheduled runs. It stages only `README.md` and `CONTRIBUTIONS.md`,
uses the GitHub Actions bot, and commits only changed content. It never force-pushes,
rebases, changes other repositories, or modifies your biography, configuration or logos.
Official action commits were resolved from the v6.1.0 checkout and v6.3.0 setup-python
tags and checked against their `action.yml` files during local preparation.

GitHub schedules can be delayed, and public-repository schedules can be disabled after
60 days without repository activity. Restore a disabled workflow in Actions after
checking its status and settings; do not create empty keep-alive commits. Updates run
on GitHub's runners and do not require your computer to stay on.

For a failed run, inspect its logs first. Rate limits, timeouts, incomplete searches,
missing repositories, changed evidence, or failed ancestry checks must not become zero
counts. Search results above GitHub's 1,000-result cap fail explicitly until a reviewed
query-partitioning implementation is added. Search indexing may delay a new merge.
For rejected writes, check token permissions and branch rules with the owner; do not
expand permissions or disable rules automatically. A non-fast-forward push fails safely;
the next run starts from the latest default-branch head.

## Edit text or logos

The `models` section links to the owner's Civitai profile and displays downloads
only; followers are intentionally omitted. The download figure is a manually
verified snapshot, outside the GitHub contribution markers. The initial displayed
41.3k downloads rounds to `41k downloads`. For future manual refreshes use
`floor(count / 1000 + 0.5)` and the lowercase `k` suffix. The current workflow does
not fetch or update Civitai statistics.

The `social` section links to Bilibili account `12595237` (四倍体果蝇-Ray). Its initial
verified follower total was 14,270, read from the profile's visible follower-count
tooltip, and is displayed as `14k followers` using the same rounding rule. This is
also a manual snapshot outside the contribution updater's managed region. Civitai
and Bilibili logos follow their linked platform names at 20px; their provenance is
recorded in `assets/logos/SOURCES.md`.

The two Rednote (Xiaohongshu) links are owner-supplied: `68483ecb000000001b019555` is the
fun account (二创号), and `6871d21d000000001b02205c` is the daily-life account
(日常号). They share a rounded-corner wrapper around the official platform icon and intentionally display no follower
counts. Keep these profile IDs distinct when editing the social section.

Edit the biography outside the two contribution markers. Keep exactly one start and
one end marker, in order. Logo refreshes are a separate, manually reviewed operation;
the count workflow does not redownload or recolor assets. Keep original brand notices
and recheck both themes at 20px. Repository code licenses do not automatically grant
trademark rights.

## Official platform references

- [Search limits and incomplete results](https://docs.github.com/en/rest/search/search#search-issues-and-pull-requests)
- [Comparing commits](https://docs.github.com/en/rest/commits/commits#compare-two-commits)
- [Scheduled and manual events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [GITHUB_TOKEN permissions](https://docs.github.com/en/actions/concepts/security/github_token)

The owner-supplied `assets/closure.png` is embedded unchanged in
`assets/closure-feathered.svg`, which applies the owner-requested elliptical opacity
mask. Wide screens use `closure-profile-wide.svg`: a 460px canvas containing the
same approximately 280px portrait with transparent space to its right, moving it
closer to the text. Compact screens use the original feathered SVG at 128px for
481–600px viewports and 104px below that. It sits beside the biography using
HTML image alignment without a clearing line break, so contributions follow the
biography without waiting for the image height. It is outside the updater region.
Keep the source aspect ratio and transparency; provenance is in `assets/SOURCES.md`.
The biography reads `Video Gen · Agent Harness`.

The biography and content rows use native `<h3>` groups for a larger, approximately
20px GitHub font. Section labels remain concise. Contribution generation must keep
its HTML link escaping and heading wrapper so refreshes preserve this typography.
