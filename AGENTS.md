# Profile maintenance conventions

## Avoid upstream timeline noise

When maintaining this profile or recording accepted contributions:

- Keep commit titles and bodies focused on the profile change.
- Do not put upstream PR/issue URLs, qualified repository-and-number references,
  or user/team mentions in commit messages, including trailers.
- Omit upstream `Related`, `Fixes`, `Closes`, and similar reference trailers.
- Keep verifiable contribution links in `CONTRIBUTIONS.md` and the reviewed
  configuration instead of commit messages. Preserve the evidence itself.
- Do not post comments or other announcements to upstream conversations as part
  of profile maintenance unless the owner explicitly asks.
- Preserve the existing generic commit message used by the update workflow.
- Do not rewrite published history to address an old reference without an
  explicit request; a rewrite does not establish that GitHub removed its event.

The aim is to avoid automatic upstream timeline entries caused by profile updates.

## Star display preference

- Show stars beside the upstream projects (`show_stars: true`).
- Hide only the owner's personal repository star total (`own_stars.show: false`).
- Keep automatic updates disabled unless explicitly requested.

## Contribution evidence presentation

- Do not display merge or adoption dates in `CONTRIBUTIONS.md`.
- Keep contribution counts, upstream target branches, and verifiable evidence links.
