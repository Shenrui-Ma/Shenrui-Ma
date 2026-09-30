# Official logo sources

Verified on 2026-09-30. The updater never downloads or changes these assets. Civitai, Bilibili and Xiaohongshu website-sourced icons were added later in this local review; their records are below. The OpenClaw PNG and both Hermes SVGs are byte-for-byte copies of the pinned upstream files. The ASu PNG is a generated transparent-background derivative explicitly approved by the owner; see its processing record below. Display size is 20 × 20 CSS pixels.

The commit below identifies the repository revision containing the asset. The separately labeled Git blob SHA identifies file bytes and is not a commit. SHA-256 values apply to the local copies.

## OpenClaw

- Repository: [openclaw/openclaw](https://github.com/openclaw/openclaw)
- Source commit: [`509cb47840c0cdd57567f401426f11cde6828c1a`](https://github.com/openclaw/openclaw/commit/509cb47840c0cdd57567f401426f11cde6828c1a)
- Local asset: `openclaw.png`; original dimensions/viewBox: `[180, 180]`.
  - [Pinned source file](https://github.com/openclaw/openclaw/blob/509cb47840c0cdd57567f401426f11cde6828c1a/ui/public/apple-touch-icon.png); [raw bytes](https://raw.githubusercontent.com/openclaw/openclaw/509cb47840c0cdd57567f401426f11cde6828c1a/ui/public/apple-touch-icon.png).
  - SHA-256: `e8c7ce0a3a6c52bd904cc55e31a5b3a8b6392dcd70ba9e220ecf0ef1d6bd8c16`.
  - Git blob SHA: `71781843f857e274449a0e7a2b151c06d92b5e4f`.
  - Conversion: none.

Identity: the official [Control UI HTML](https://github.com/openclaw/openclaw/blob/509cb47840c0cdd57567f401426f11cde6828c1a/ui/index.html) links `/apple-touch-icon.png` as its 180 × 180 Apple touch icon. Visual inspection confirms the red mascot. The animated favicon is not used.

License source: [upstream LICENSE](https://github.com/openclaw/openclaw/blob/509cb47840c0cdd57567f401426f11cde6828c1a/LICENSE). The corresponding original notice is reproduced below.

## Hermes Agent

- Repository: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- Source commit: [`f42f579cf8bac4918ac9599bece71618afadd846`](https://github.com/NousResearch/hermes-agent/commit/f42f579cf8bac4918ac9599bece71618afadd846)
- Local asset: `hermes-agent.svg`; original dimensions/viewBox: `0 0 1024 1024`.
  - [Pinned source file](https://github.com/NousResearch/hermes-agent/blob/f42f579cf8bac4918ac9599bece71618afadd846/assets/icon-master.svg); [raw bytes](https://raw.githubusercontent.com/NousResearch/hermes-agent/f42f579cf8bac4918ac9599bece71618afadd846/assets/icon-master.svg).
  - SHA-256: `c5bf1ba37b6e402140ea74898cfe36dcd085708661924bb9a526d3a5df100412`.
  - Git blob SHA: `04aa7f1e0f8d22100b75416d25598644af189ab9`.
  - Conversion: none.
- Local asset: `hermes-agent-dark.svg`; original dimensions/viewBox: `0 0 1024 1024`.
  - [Pinned source file](https://github.com/NousResearch/hermes-agent/blob/f42f579cf8bac4918ac9599bece71618afadd846/assets/icon-master-dark.svg); [raw bytes](https://raw.githubusercontent.com/NousResearch/hermes-agent/f42f579cf8bac4918ac9599bece71618afadd846/assets/icon-master-dark.svg).
  - SHA-256: `905739f89c89a4313c5ab7110cfe324038336e923453d72bbebb3a602958bc4d`.
  - Git blob SHA: `27fa292482123b19269ad7b40a71e59c46cfbb0e`.
  - Conversion: none.

Identity and appearance: [`scripts/generate_icons.py`](https://github.com/NousResearch/hermes-agent/blob/f42f579cf8bac4918ac9599bece71618afadd846/scripts/generate_icons.py) identifies the two master SVGs as generated application icons, composed from the Nous brand-kit girl artwork and official platform backgrounds. It assigns `icon-master.svg` to light appearance and `icon-master-dark.svg` to dark appearance. Both original variants are retained and selected using `<picture>`; neither is redrawn. XML inspection found no scripts, animation, external image references, or foreignObject elements.

License source: [upstream LICENSE](https://github.com/NousResearch/hermes-agent/blob/f42f579cf8bac4918ac9599bece71618afadd846/LICENSE). The corresponding original notice is reproduced below.

## ASu-skills

- Repository: [Hisn00w/ASu-skills](https://github.com/Hisn00w/ASu-skills)
- Source commit: [`cb9f3080897c24305b2a888d6c363367aed53563`](https://github.com/Hisn00w/ASu-skills/commit/cb9f3080897c24305b2a888d6c363367aed53563)
- Local asset: `asu-skills.png`; original dimensions/viewBox: `[1254, 1254]`.
  - [Pinned source file](https://github.com/Hisn00w/ASu-skills/blob/cb9f3080897c24305b2a888d6c363367aed53563/assets/asu-avatar-circle.png); [raw bytes](https://raw.githubusercontent.com/Hisn00w/ASu-skills/cb9f3080897c24305b2a888d6c363367aed53563/assets/asu-avatar-circle.png).
  - Local derivative SHA-256: `0120276000d57e687b65aeb822bb7cfd153b6583acd37744d8be6f84a08b38f1`.
  - Original upstream SHA-256: `dcac9dc2562485a17026829be84c19675ffbbe39f70cc42125f99549ed99a195`.
  - Original upstream Git blob SHA: `838e2ec279d0f1a344acecba78754888d044b079` (does not identify the local derivative).
  - Processing: built-in `image_gen` background extraction, transparent RGBA PNG, 1254 × 1254. The prompt requested removal of only the white exterior and preservation of the circular blue artwork. Pixel checks found interior differences; the owner explicitly accepted the generated transparent version after that finding. This derivative is not an unchanged or pixel-identical upstream asset.

Identity: the official [README](https://github.com/Hisn00w/ASu-skills/blob/cb9f3080897c24305b2a888d6c363367aed53563/README.md) directly renders `assets/asu-avatar-circle.png` with alt text `ASu-skills 图标`. The local PNG retains the circular avatar composition, with the exterior white background replaced by transparency. The generated derivative was reviewed at the intended 20px size in light and dark appearances.

License source: [upstream LICENSE](https://github.com/Hisn00w/ASu-skills/blob/cb9f3080897c24305b2a888d6c363367aed53563/LICENSE). The corresponding original notice is reproduced below.

## Rights and attribution scope

The three pinned root LICENSE files contain MIT notices. OpenClaw’s repository metadata reports `NOASSERTION`, while its pinned LICENSE and README explicitly state MIT; the actual pinned file is the source recorded here. The root directory listings, the relevant README/HTML/icon generator, the master SVGs, and the root LICENSE files were inspected. No separate logo-specific grant or brand policy was found in those reviewed sources. This is a scoped observation, not a claim that no policy exists anywhere.

A code license is not treated here as a blanket trademark or endorsement grant. These official-source assets (including the owner-approved ASu transparency derivative) identify their respective upstream projects in a factual contributions list. Project names and marks remain associated with their respective owners; the profile does not claim ownership, sponsorship, or endorsement. No broader brand permission is asserted. If an owner identifies an additional applicable restriction, re-review the local copy and consider an owner-approved hosted asset.

## Original license notices

### OpenClaw

```text
MIT License

Copyright (c) 2026 OpenClaw Foundation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Third-party notices for incorporated or adapted code are recorded in
THIRD_PARTY_NOTICES.md.
```

### Hermes Agent

```text
MIT License

Copyright (c) 2025 Nous Research

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### ASu-skills

```text
MIT License

Copyright (c) 2026 Hisn00w

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Civitai platform icon

- Official source: [https://civitai.red/user/Shenrui_Ma](https://civitai.red/user/Shenrui_Ma).
- Local file: `civitai.svg`; SVG viewBox -1 0 22.7 22.7; displayed at 20 × 20 CSS pixels.
- Local SHA-256: `6f5ae8477fa127597592ed78c09d04a2ec79aba50c5d1c7424cbf42ac2d26d83`.
- Processing: Extracted the compact SVG inside the official navigation link with aria-label Civitai home. Removed the page-specific responsive CSS class and normalized XML serialization; paths, gradients, colors and viewBox are unchanged. No image generation or redraw.
- Retrieved: 2026-09-30. Website asset rather than a pinned Git repository file; no source commit or Git blob SHA is claimed.
- Used to identify the linked platform account; no ownership or endorsement is claimed. No independent asset-specific redistribution license was supplied by the observed page. This record does not extend the upstream projects’ MIT notices to these platform marks.

## Bilibili platform icon

- Official source: [https://www.bilibili.com/favicon.ico](https://www.bilibili.com/favicon.ico).
- Local file: `bilibili.png`; PNG 32 × 32; displayed at 20 × 20 CSS pixels.
- Local SHA-256: `094011359a6e0308828b7e5644200c724ac9bea433da022c869ce02d89add0d4`.
- Processing: Downloaded the favicon declared by the official account page and converted its original 32 × 32 ICO frame to RGBA PNG without resizing or changing colors. Transparent background preserved.
- Retrieved: 2026-09-30. Website asset rather than a pinned Git repository file; no source commit or Git blob SHA is claimed.
- Used to identify the linked platform account; no ownership or endorsement is claimed. No independent asset-specific redistribution license was supplied by the observed page. This record does not extend the upstream projects’ MIT notices to these platform marks.
- Original ICO SHA-256: `2681561eb24e7435fea1acf26f3af95e4efc9f7d451587b58bef62f030f337e9`. Source declaration: the profile at https://space.bilibili.com/12595237 uses this URL as `rel="icon"`.

## Xiaohongshu platform icon

- Official source: [page-declared Apple touch icon](https://picasso-static.xiaohongshu.com/fe-platform/f43dc4a8baf03678996c62d8db6ebc01a82256ff.png), linked by the HTML of the owner-supplied profile page https://www.xiaohongshu.com/user/profile/68483ecb000000001b019555.
- Local file: `xiaohongshu.png`; original 180 × 180 PNG; displayed at 20 × 20 CSS pixels for both accounts.
- SHA-256: `2912c4df1ab479d734ef132e9c45b4f17afa80b2aa3eaf4438acd54afc70b20a`.
- Processing: none; exact downloaded bytes. No generation, redraw, or recoloring.
- Retrieved: 2026-09-30. CDN asset rather than a pinned Git repository file; no commit or Git blob SHA is claimed.
- This platform mark identifies the linked accounts. No ownership, endorsement, or broader trademark permission is claimed. The observed page supplies no independent asset-specific redistribution license; the upstream projects’ MIT notices do not extend to this icon.

### Rounded Xiaohongshu display variant

- Display file: `xiaohongshu.svg`; original `xiaohongshu.png` is retained.
- Processing: an SVG rounded-rectangle clip (36px radius on a 180px canvas) wraps the embedded original PNG. Only corner visibility changes; the embedded image bytes, artwork and colors are unchanged. No generative image editing.
- SVG SHA-256: `c89ff47548eb8ab1483dad1e976a8ce499859d9e3911c0182b7c1797da804a22`.
