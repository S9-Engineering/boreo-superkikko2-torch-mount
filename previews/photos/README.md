# Real-print photographs

Six user-supplied HEIC captures document a black printed mount installed on a red BOREO with the original Superkikko2 metal bracket and lamp. The user confirms the latest model was printed in PETG. Actual print settings were not supplied. The prepared PETG job is checked digitally; the actual settings used for the photographed print were not supplied. The upper butterfly slot is visibly unfastened, long trial bolts protrude and support-contact residue remains visible. These are observations of a trial assembly, not proof of dimensional fit, final hardware, strength, heat dissipation or protective compatibility.

## Public images

- `edited/*-real.jpg`: full-resolution, upright public references with the approved SVG S9 Engineering watermark, without generative alterations. HEIC was decoded by Apple ImageIO and converted to JPEG at quality 94; this format conversion is lossy. Removal of private JPEG metadata was separately verified to leave decoded JPEG pixels identical before the watermark was applied. The pre-branding hash is retained in the provenance.
- `gallery/*.jpg`: web-size copies, at most 2000 pixels on the longest edge, with the full scene and aspect ratio retained and the S9 Engineering watermark.
- [hero-enhanced.png](edited/hero-enhanced.png): a lightly AI-enhanced version of the side photograph with the full S9 Engineering signature at bottom-right and **AI-enhanced photo** at bottom-left. The six references remain the documentary source. [Exact edit prompt](hero-edit-prompt.txt).
- [edits.json](edits.json): source/public hashes, dimensions, conversion and review provenance. Contains no GPS coordinates.

## Untouched originals and privacy

The untouched `originals/*.HEIC` files contain GPS metadata. They are retained locally and narrowly ignored by Git. Public full-resolution references and all derivative images were checked for private location/EXIF metadata. Source hashes verify preservation without publishing the private captures. The originals are not included in ZIPs, portal bundles or GitHub.

## Reproduce the public conversion

On macOS, use Python with **PyObjC Quartz/Foundation**, **Pillow** and **ImageMagick 7** and **librsvg (`rsvg-convert`)** installed. Verified photo tooling: macOS 26.6.2, Pillow 11.3.0, PyObjC Quartz/core 12.1 and ImageMagick 7.1.2-33. The CAD environment is separate and need not contain these photo tools. From the project root:

    python3 source/prepare_photos.py --input /path/to/private-captures

The input folder must contain the six `IMG_1670.HEIC` through `IMG_1675.HEIC` captures. The script also calls [brand_publication.py](../../source/brand_publication.py) to apply the exact project-local SVG artwork and refresh any existing local portal exports. The non-generative branding pass can be rerun separately with `python3 source/brand_publication.py`; hashes prevent stacked watermarks. Temporary unbranded working copies stay in ignored `.cache/branding/`.

The script installs the private-original ignore rule before copying them, verifies full-resolution orientation, strips private metadata and checks decoded pixel preservation across metadata removal. It does not reproduce the generative cover; that cover and its prompt are retained separately. Review any newly generated photographs before publication.
