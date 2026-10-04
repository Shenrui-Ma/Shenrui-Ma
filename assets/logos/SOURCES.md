# Official logo sources

Verified on 2026-09-30. The updater never downloads or changes these assets. Civitai, Bilibili and Xiaohongshu website-sourced icons were added later in this local review; their records are below. The OpenClaw PNG and both Hermes SVGs are byte-for-byte copies of the pinned upstream files. The ASu avatar is the owner-supplied WEBP displayed through a circular SVG clip; see its current source record below. Contribution-project and platform-account logos display at the original 20 × 20 CSS pixels.

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

- Current original: `asu-skills.webp`, supplied directly by the owner as `ddc7c6ae-5484-4319-9015-54e8038d47b9.webp`.
- Dimensions: 240 × 240; original WEBP bytes preserved exactly.
- Original SHA-256: `8f7ee2bbc727a4e1409c1d56d849e3351b4cfe6aee35547fbcbee815de118e12`.
- Display: `asu-skills.svg`, embedding the original WEBP and applying a circle centered at (120,120), radius 120. Only the corners are clipped; no generation, retouching, recoloring or replacement artwork is used.
- Display SHA-256: `650d5079356560bc4a3e09b2ec25223513f031f62a09e38ac30a7d55acd55ec8`.
- The previous generated transparency variant was replaced at the owner's request. Its earlier official-source record is retained in Git history; it is not the source of this new avatar.
- No license for this owner-supplied image is inferred from the upstream project's code license. The historical upstream notice below does not apply to this replacement.

## Rights and attribution scope

The three pinned root LICENSE files contain MIT notices. OpenClaw’s repository metadata reports `NOASSERTION`, while its pinned LICENSE and README explicitly state MIT; the actual pinned file is the source recorded here. The root directory listings, the relevant README/HTML/icon generator, the master SVGs, and the root LICENSE files were inspected. No separate logo-specific grant or brand policy was found in those reviewed sources. This is a scoped observation, not a claim that no policy exists anywhere.

A code license is not treated here as a blanket trademark or endorsement grant. These official-source assets (including the owner-supplied ASu avatar) identify their respective upstream projects in a factual contributions list. Project names and marks remain associated with their respective owners; the profile does not claim ownership, sponsorship, or endorsement. No broader brand permission is asserted. If an owner identifies an additional applicable restriction, re-review the local copy and consider an owner-approved hosted asset.

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

### ASu-skills (historical upstream asset)

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

## CASIA academic identity mark

- Institution: 中国科学院自动化研究所.
- Official identity page: [CASIA identity source](https://ia.cas.cn/gkjj/xxbs/).
- Original asset: [official download](https://ia.cas.cn/gkjj/xxbs/201010/W020101028581223717789.jpg).
- Local file: `casia.jpg`; dimensions: 238 × 236.
- SHA-256: `74240e44885cfaa7ad12059ac91b8e34ed5366dc8fd15ff43b4bd1dead1e5740`.
- Processing: None: byte-for-byte downloaded official identity-page image. Original white background retained.
- The identity page retains institute copyright. No independent asset license is asserted. The original image bytes are preserved and inset in a white circular display backdrop; no part of the triangular mark is cropped.

## UCAS academic identity mark

- Institution: 中国科学院大学.
- Official identity page: [UCAS identity source](https://onestop.ucas.edu.cn/home/info/6b9e95dc-5785-4eee-b25f-1f884698cfc3).
- Original asset: [official download](https://onestop.ucas.edu.cn/Content/Upload/2020/9/1.zip).
- Local file: `ucas.png`; dimensions: 298 × 298.
- SHA-256: `76133485b54c6190eaae6d061a7e0a1b2a67f3ba2a49c825824d1e033dc4db34`.
- Processing: None: exact member bytes extracted from official standard logo archive. Archive filenames decoded from GB18030 after ZIP CP437 presentation; pixels unchanged.
- Archive member: `中国科学院大学标准Logo下载/国科大标准Logo/中国科学院院徽.png`. The university officially provides this CAS seal in its standard logo archive.
- The official page retains copyright in the academy/university, requires approval or authorization outside reasonable-use exceptions, and explicitly mentions personal study and classroom teaching. No separate license or university approval is asserted here. See the linked source statement. The mark identifies the owner-supplied academic affiliation; it is not an endorsement claim.
- Display backdrop: a white circle behind the unchanged transparent image keeps the original blue seal readable on dark backgrounds.

## CodexBar

- Verified on 2026-10-03; used for the owner's accepted upstream contribution.
- Local file: `codexbar.png`, displayed at 20 × 20 CSS pixels, unchanged original bytes.
- Official source: [CodexBar app icon](https://github.com/steipete/CodexBar/blob/50ce15d2b1ad526356475f2ce1d7001e9812443e/docs/icon.png).
- Upstream commit: `50ce15d2b1ad526356475f2ce1d7001e9812443e`.
- Git blob SHA: `11da02f4f4ac8d4cd8dcc159e6a2f0074d826b7f`.
- SHA-256: `54cf6ac4663c7b341a085493e787815949c5680e5cb58bda865f8a2c5aab24b1`.
- Source repository [license](https://github.com/steipete/CodexBar/blob/50ce15d2b1ad526356475f2ce1d7001e9812443e/LICENSE): MIT. No separate trademark permission or endorsement is asserted.

```text
MIT License

Copyright (c) 2026 Peter Steinberger

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

## pnpm

Verified on 2026-10-04. The official no-text marks are copied unchanged and
displayed at 20 × 20 CSS pixels. The standard mark is used on light backgrounds;
the light mark is used on dark backgrounds.

- Local file: `pnpm.svg`.
  - [Official source](https://github.com/pnpm/pnpm/blob/bac8077715ac5af3857b1df970a014875d89b86c/pnpm/docs/static/img/logos/pnpm-standard-no-text.svg).
  - Upstream commit: `bac8077715ac5af3857b1df970a014875d89b86c`.
  - Git blob SHA: `d60132a0571c1585e728470e9a2bbd58cfbcd129`.
  - SHA-256: `94a665893839b1e13325df98ceb40fd5193b6c56ba695abd415677f493e9fb5c`.

- Local file: `pnpm-dark.svg`.
  - [Official source](https://github.com/pnpm/pnpm/blob/bac8077715ac5af3857b1df970a014875d89b86c/pnpm/docs/static/img/logos/pnpm-light-no-text.svg).
  - Upstream commit: `bac8077715ac5af3857b1df970a014875d89b86c`.
  - Git blob SHA: `0286ac9022238e7e84d6a96967e839f0ce4937c4`.
  - SHA-256: `803a44f9ad010770ee3de60a629852b5aecebb7a9657a95bf777351d0f38f8eb`.

Repository license: MIT. No separate trademark permission or endorsement is asserted.

```text
The MIT License (MIT)

Copyright (c) 2015-2016 Rico Sta. Cruz and other contributors
Copyright (c) 2016-2026 Zoltan Kochan and other contributors

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
