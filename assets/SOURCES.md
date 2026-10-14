# Profile illustration

- Original file: `closure.png`, supplied directly by the owner for this profile.
- Original dimensions: 1216 × 1088 RGBA. Original bytes and transparency are retained unchanged.
- Original SHA-256: `ec06fb3d0aaf2c9634bfa0024392d466262fdf3d4f81ff0282bfbd352d8841e8`.
- Display file: `closure-feathered.svg`, embedding those exact PNG bytes and applying a vector opacity mask. No generation, redrawing, recoloring or face smoothing.
- Display SHA-256: `00919fbc92b8cd3d3c1fbe3a9e4c46020021099d1116609b132caf5b868b4517`.
- Mask: ellipse radii 62% × 60%, center 50% × 38%; opacity stops 0%/1, 68%/1, 76%/0.94, 86%/0.62, 95%/0.18, 100%/0. This is equivalent to the owner's CSS radial-gradient mask; white controls mask luminance without tinting the artwork.
- Responsive display: the compact variant is 128px at 481–600px and 104px at 480px or below. The wide variant renders the same approximately 280px artwork inside a 460px transparent canvas, moving the visible portrait about 180px inward rather than against the far-right edge. GitHub supplies 20px of left padding; no additional horizontal inset is used.
- The source image is not overwritten. Edit the SVG gradient stops to adjust feathering; original pixels remain intact.
- This provenance record does not assert ownership or a new license for the artwork.

## Wide layout variant

- File: `closure-profile-wide.svg`. It uses the same embedded PNG and feather mask as `closure-feathered.svg`.
- The root canvas is widened to 2000 × 1088; only transparent space to the right is added. The visible artwork is not stretched, recolored or redrawn.
- Rendered at 460px wide, the 1216px artwork occupies approximately 280px and sits closer to the text column.
- SHA-256: `5f25c4d4d7d3f0240baec6bba285d3351bdfd99045c61e2dfea23e26a9e25a68`.

## Academic marks within the existing transparent area

`closure-affiliations-spaced.svg` and `closure-affiliations-wide-spaced.svg` preserve the respective original canvas, character image bytes, and feather mask. They place the original CASIA and UCAS logo bytes within the same x=8..188 strip: CASIA has a white circular backdrop centered at (98,170) with radius 89 and
its complete original mark inset to 124 × 122.96; UCAS occupies y=340..520
in the character’s 1216 × 1088 coordinate space. These rectangles were verified to
contain no opaque character pixels. The wide layout displays each mark at about
41px. The overall canvas, text boundary and logo centers remain fixed. Only the portrait is shifted slightly right to add separation from the marks.
Both displays have white circular backdrops for dark-mode contrast; the original logo pixels
and brand colors are unchanged. Individual sources and usage statements are in
`logos/SOURCES.md`.

- `closure-affiliations-spaced.svg` SHA-256: `3b85636b3b7388e9a3f6fec2396e14f56352f5c32db741e1201d8aa4da555a29`.

- `closure-affiliations-wide-spaced.svg` SHA-256: `61fb4a11c97771d8ba180b6e0f235725c098f0aa0ab77705df529c40cc554bdb`.

### Portrait-only spacing adjustment

The wide portrait is translated 48 source units right (about 11px at display
size). In the compact variant it is translated right and uniformly scaled by
0.960526316 about its vertical center to keep the full artwork within the same
canvas. No part is cropped; the academic marks and text geometry are unchanged.

## Enlarged academic marks

Current display files are `closure-affiliations-marks-close.svg` and
`closure-affiliations-wide-marks-close.svg`. Both academic marks and their white
circular backdrops use an exact 1.5× scale (wide circle diameter about 61px).
Centers are (188,399) and (188,689), preserving their vertical stack. Original
embedded image bytes and the feather mask remain unchanged. The wide portrait
is translated to x=304 with its original scale. The compact portrait is fitted
within the unchanged 1216×1088 canvas using translate(208,93.052632) and
scale(0.828947368), avoiding clipping beside the marks.

- `closure-affiliations-marks-close.svg` SHA-256: `60774b2413470c990e196e3241505511f91e149ce1f06ad0aead55ab90c60bd5`.

- `closure-affiliations-wide-marks-close.svg` SHA-256: `21e55231d0d71fed595251c3b44a4a495337779687c67bc5c9098ea9090537a6`.

The UCAS mark is centered at y=689, leaving a 23-source-unit gap
(about 5px on the wide layout) between the two circular marks.
The portrait, logo scales and overall canvas are unchanged.

The wide portrait receives a further 96 source units of rightward translation
(about 22px on desktop). The academic marks, portrait scale, feather mask and
compact layout remain unchanged.

Both academic marks now use 1.5× their original scale (75% of the preceding
2× version), with centers at (188,399) and (188,689). Portrait
transforms and the containing canvases are unchanged.

## Vertically centered academic marks

The `academic-logos` group is translated down by 199 source units in both current display variants. Its two centers are (188,399) and (188,689), so the stack midpoint is (188,544), matching the portrait canvas midpoint. The wide display moves the pair down about 46 CSS pixels; the existing 5px gap, white circular backdrops, embedded image bytes, portrait geometry and feather mask are preserved.

## Personal photo below the portrait

- Local file: `profile-photo.png`, supplied by the profile owner; original PNG bytes preserved.
- Dimensions: 1341 × 1173.
- SHA-256: `bef6935112510b092886f27cd8db487a7e62e8b0a2f142c1b0b8d9e5785dde8a`.
- The photo is embedded below the existing portrait in both current composite SVGs, keeping the original aspect ratio and horizontal alignment. At desktop size it is about 280px wide, with a 15px gap below the original illustration canvas and a 15px corner radius. The compact version uses the same width as its fitted portrait.
- Rounded corners use an SVG clip, with no pixel edits or resampling of the embedded original. Only the outer canvas extends downward; the portrait, feather mask and logo positions remain unchanged.
