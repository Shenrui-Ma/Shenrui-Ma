# Profile illustration

- Original file: `closure.png`, supplied directly by the owner for this profile.
- Original dimensions: 1216 × 1088 RGBA. Original bytes and transparency are retained unchanged.
- Original SHA-256: `ec06fb3d0aaf2c9634bfa0024392d466262fdf3d4f81ff0282bfbd352d8841e8`.
- Display file: `closure-feathered.svg`, embedding those exact PNG bytes and applying a vector opacity mask. No generation, redrawing, recoloring or face smoothing.
- Display SHA-256: `00919fbc92b8cd3d3c1fbe3a9e4c46020021099d1116609b132caf5b868b4517`.
- Mask: ellipse radii 62% × 60%, center 50% × 38%; opacity stops 0%/1, 68%/1, 76%/0.94, 86%/0.62, 95%/0.18, 100%/0. This is equivalent to the owner's CSS radial-gradient mask; white controls mask luminance without tinting the artwork.
- Responsive display: the compact variant is 128px at 481–600px and 104px at 480px or below. The wide variant renders the same approximately 280px artwork inside a 460px transparent canvas, moving the visible portrait about 180px inward rather than against the far-right edge. A 16px horizontal inset is retained.
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
