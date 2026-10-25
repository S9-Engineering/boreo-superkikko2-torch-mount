# BOREO Superkikko2 Torch Mount — R13 printing and assembly

**Unreleased development package. Ready for printing as a prototype in My setup; not physically fit/load/heat validated.** Designed around the measured Petzl BOREO M/L and original Superkikko2 butterfly/U-bracket. Do not modify the helmet or use force to fit this trial.

## Selected print files

| File | Quantity | Orientation and material |
| --- | --- | --- |
| [R13_PONTE_CENTRATO_PETG.stl](print/stl/R13_PONTE_CENTRATO_PETG.stl) | 1 | As exported, base of curved skin on the plate, arms raised; PETG |
| [R13_BASE_APPOGGI_PETG.stl](print/stl/R13_BASE_APPOGGI_PETG.stl) | 1 | As exported, plate standing on its lower edge; PETG |
| [BOREO_R13_COMPLETO_PETG_PRO_ECC2_04.3mf](print/3mf/BOREO_R13_COMPLETO_PETG_PRO_ECC2_04.3mf) | 1 job | Two separate objects on one plate, exact configuration in My setup |

The native 3MF includes profiles, supports and an embedded sliced path; it is not geometry-only or a universal PETG profile. The new package contains no standalone G-code. For any other machine or material variant, import STL in **millimetres** and reslice appropriately. Do not mix revision files.

Bridge size 104.98 × 50.05 × 28.80 mm; base size 102.80 × 25.61 × 46.00 mm. Curved skin 2 mm, arms 9.2 × 3.2 mm, nominal ribbed local envelope up to **4.4 mm**. Remove supports but preserve the tapered ribs.

### Assembly BOM and Amazon.it examples

Listings checked **25 October 2026**. Non-affiliate sourcing examples, not mandatory brands; written specifications govern equivalents. No purchase was made. Prices and delivery promises are omitted. Listing verification does not inspect delivered hardware.

| Item | Required quantity | Specification / fit constraint | Amazon example and pack |
| --- | --- | --- | --- |
| Bridge/base screws | 2 | M3 × 16 mm, full thread, cylindrical socket head, ISO 4762 / DIN 912, stainless A2; CAD head Ø5.5 × 3 mm | [ProRaje M3 × 16, 10 screws](https://www.amazon.it/dp/B0DHPJTV8P); one 10-piece pack |
| Self-locking nuts | 2 | M3 nylon insert, DIN 985; target AF 5.5 / height 4 mm, for AF 5.85 / depth 4.3 mm pockets | [qjuwhua M3 nuts and washers](https://www.amazon.it/dp/B0GFC9H67Y); one pack contains 100 nuts and 100 washers, shared with the next row |
| Flat washers | 2 | M3 DIN 125; nominal ID 3.2 / OD 7 / thickness 0.5 mm | Same [nuts-and-washers pack](https://www.amazon.it/dp/B0GFC9H67Y); no second pack needed |
| PETG filament | About 45 g plus trial/loading allowance | Suitable PETG and its own profile; 1.75 mm for the prepared machine | [ELEGOO PETG black, 1 kg](https://www.amazon.it/dp/B0F443Q9KS), one spool if needed. **This is PETG, not a verified PETG Pro SKU: reslice the STL using its own profile** |
| Lamp interface | 1 | Original Superkikko2 butterfly plate and U-bracket with measured 2 mm slots | Reuse the matching original assembly; no replacement selected |
| Butterfly-to-base fasteners | Up to 3 sets, pending | M1.6 screw/washer/nut is only a candidate. Length and head/washer clearance require metal thickness and rivet measurements | **Not selected for purchase.** M3 does not fit the original 2 mm slots |
| Helmet | 1 | The measured BOREO M/L used for this project | Existing device; no wider fit claim |

The nut/washer listing identifies the required standards but does not independently confirm every dimension. Check actual nut height/AF and washer dimensions before assembly. Relevant tools are a 2.5 mm hex key and 5.5 mm spanner for the defined joint, plus a caliper and small support-removal tool. Confirm the actual screw drive. No general tool kit is specified.


## My setup

This setup was **prepared and digitally checked**, not physically printed as R13.

| Setting | Prepared configuration |
| --- | --- |
| Printer | ELEGOO Centauri Carbon 2 Combo; internal profile: Elegoo Centauri Carbon 2 0.4 nozzle |
| Nozzle / plate | 0.4 mm / textured PEI |
| Filament | ELEGOO PETG Pro, 1.75 mm; physical colour not documented |
| Slicer | ElegooSlicer 1.5.3.5; CLI engine 2.4.2 |
| Temperatures | 240 °C nozzle / 65 °C plate; within the [manufacturer's PETG Pro range](https://www.elegoo.com/products/petg-pro-filament-1-75mm-colored-1kg) |
| Layers / walls / infill | 0.20 mm / 5 / 30% gyroid; 5 top/bottom layers |
| Flow limit / speeds | 5 mm³/s; outer/inner/infill/first-layer: 40/60/70/25 mm/s; bridges 25 mm/s |
| Supports | Normal snug, plate only; top/bottom Z gaps 0.40 mm, XY gap 0.55 mm, two interface layers at 0.5 mm spacing |
| Adhesion / material changes | No brim, skirt, raft or purge tower; one filament, printing by layer |
| Slicer estimate | **2 h 55 min 19 s / 44.23 g**, supports included; 230 layers |

Flow 0.98, pressure advance 0.1 and cooling are initial profile values, not new spool calibrations. Larger support gaps aim to reduce welded residue; a clean underside is not guaranteed. Use dry material and follow its manufacturer's drying guidance. Profiles are embedded in the included native3MF and retained separately in the source repository.


## How to

![Exploded CAD illustration of bridge, base and M3 hardware](assembly/r13-exploded.png)

1. **Choose the matching package.** Until publication, use the linked prototype pack. After publication, open the [Releases page](https://github.com/S9-Engineering/boreo-superkikko2-torch-mount/releases), select the matching revision/setup, expand **Assets**, download its named **print-pack.zip**, extract it and read the included README. GitHub's automatic source ZIP is different. Keep files from one revision together.
2. **Choose a printing route.** Use the native 3MF only with the matching setup, or import both STL files and slice for your own configuration. Confirm units, quantity, orientation, supports and first layer before printing.
3. **Clean separate pieces.** Cool before removing support towers. Clear residue from pockets and passage surfaces. Preserve the tapered ribs beneath the arms: they are part of the model.
4. **Try the helmet fit first.** With the helmet stationary and not worn, insert without bending arms or compressing foam. Stop if the ribbed transition binds. Check padding/adjustment hardware in both bridge orientations; do not modify the helmet to accommodate it.
5. **Try the M3 joint.** Slide the base onto the arms, insert nuts from below, then washers and screws. Seat lightly for the dimensional trial. No validated working torque is specified; do not clamp the helmet foam.
6. **Check the butterfly with the lamp off and bench-supported.** Confirm slot alignment, rivet relief and tool/head clearance before choosing the three fastening sets. Do not widen the metal slots or use M3 in them. Printed passages are not self-tapping threads.
7. **Record results.** Insertion, lamp fastening, load/time retention and contact temperature still require physical checks. Full backing does not establish heat dissipation. Cold wet and submerged use remain unverified.


## Fit and evidence limits

The bridge/base M3 joint uses Ø3.4 holes, 0.4 mm diametral screw clearance, 0.35 mm per-side arm-seat clearance, AF 5.85 / depth 4.3 mm nut pockets and nominal AF 5.5 / height 4 mm nuts.

The butterfly's 2 mm metal slots are user-confirmed. Its 57.5 mm lateral interaxis is photo-derived, and upper centre Z41.5 remains provisional. The thickness of the metal plate and rivet protrusion still determine the final small fastener selection. Printed 3 × 1.9 mm passages are not threads or proof of a working M1.6 joint. Do not load or heat-test an unsupported lamp on an unvalidated interface.

Original R13 checks: 140 geometry checks, 98 package checks, 230 layers reviewed, no slicer warnings or candidate islands. These are digital checks. The current file hashes have been checked again without changing the model or reslicing it. Earlier orange-coupon fit reports do not validate R13. No carrying capacity, safe service temperature, protective compatibility, wet/immersed performance or support-removal finish is established.

## Integrity and licences

The clean package is selected by an explicit manifest. Check its SHA256SUMS.txt after extraction. The CAD sources, research and historical reports remain separately in the project repository and are intentionally outside this print pack.

Original design/documentation: [CC BY-NC-SA 4.0](LICENSE.txt). Original S9 code: [PolyForm Noncommercial 1.0.0](LICENSE-SOFTWARE.txt), source-available. Read [LICENSING.md](LICENSING.md) for scope, Required Notice, third-party content and branding.
