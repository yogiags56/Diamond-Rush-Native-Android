# Build 212 — Composite Sprite Rasterization

## Executive result

Build 212 combines the corrected Build 210 field-aligned resource parser, the Build 207 composite resolver, and the Build 211 sprite decoder to reconstruct composite images from the original JAR.

**300 composite roots were rasterized from original sprite pixels. The Kotlin rasterizer and Python reference rasterizer produced byte-identical RGBA output for all 300 composites.**

This is a strong cross-implementation consistency check. It is not yet proof of pixel-perfect parity with the original J2ME renderer or an Android device.

## Scope and selection

The original DF03 resources contain 1,129 composite groups. The Build 212 selection policy was deliberately conservative:

- 430 groups emitted fewer than three leaf draw commands and were not included in the visual audit set.
- 399 groups contained non-zero draw flags and were deferred because their transform semantics are not yet implemented in the rasterizer.
- 300 groups had at least three leaf commands and all resulting `drawFlags == 0`; these were rasterized.

This means Build 212 does not silently guess the meaning of non-zero draw flags. The rasterizer rejects flagged commands instead of applying speculative flips, rotations, palette changes, or other transformations.

## Reconstruction pipeline

1. Parse each original DF03 resource with `LegacySpriteFieldLayoutParser`.
2. Build the composite view with `LegacySpriteCompositeSection.fromFieldLayout`.
3. Expand the selected root group with `CompositeSpriteObjectResolver`.
4. Decode each leaf sprite using `LegacySpriteDecoder`.
5. Compute the union bounds from each sprite's resolved position and dimensions.
6. Draw leaf sprites in resolver order, preserving component order.
7. Composite ARGB pixels with source-over alpha blending.
8. Compare the Kotlin output against the Python reference output.

The rasterizer uses the first palette row for each resource. Additional palette rows and non-zero draw flags are intentionally deferred.

## Results

- Total original composite groups: **1,129**.
- Groups eligible for this conservative raster pass: **300**.
- Groups with fewer than three leaf commands: **430**.
- Groups requiring non-zero draw flags: **399**.
- Kotlin composites produced: **300**.
- Python/Kotlin exact RGBA matches: **300/300**.
- Raster dimension/origin/command-count mismatches: **0**.
- Regression suite: **52/52 passed**.
- Kotlin source compilation: **passed**.
- Kotlin runtime composite audit against original JAR: **300 composites**.

## Representative outputs

- `previews/build212_composite_contact_sheet.png`
- `previews/composite_ms_f_e1_g0.png` — 88 leaf commands, 198×139.
- `previews/composite_ui_f_e1_g0.png` — 89 leaf commands, 20×27.
- `previews/composite_ui_f_e2_g21.png` — 6 leaf commands, 65×31.
- `previews/composite_0_f_e1_g1.png` — 8 leaf commands, 25×25.
- `previews/composite_o_f_e0_g37.png` — 9 leaf commands, 23×44.

The preview images are reference rasters generated from original JAR sprite payloads. They are not screenshots from the original game or from Android.

## Source additions and changes

- `android/src/main/kotlin/com/diamondrush/legacy/CompositeSpriteRasterizer.kt`
  - Pure Kotlin ARGB rasterizer.
  - Derives output bounds from resolved sprite positions.
  - Preserves leaf command order and source-over alpha behavior.
  - Explicitly rejects non-zero draw flags pending further reverse engineering.
- `android/src/main/kotlin/com/diamondrush/legacy/LegacySpriteCompositeSection.kt`
  - Adds `fromFieldLayout` so real resources use Build 210's corrected field parser.
  - Renames the opaque per-group data to `groupAuxiliaryBytes`; retains a deprecated compatibility alias.
- `research/build212_composite_raster.py`
  - Python reference composite rasterizer.
- `research/build212_composite_raster_inventory.csv`
  - Inventory of the 300 eligible composite roots.
- `research/build212_composite_raster_parity.csv`
  - SHA-256 and exact parity record for Kotlin RGBA outputs.
- `tools/Build212KotlinCompositeRasterAudit.kt`
  - Kotlin runtime audit against the original JAR.
- `tests/test_build212_composite_raster.py`
  - Build 212 regression tests.

## Validation boundary

Confirmed:
- Source compiles on the JVM.
- All 300 eligible composites rasterize in both implementations.
- All 300 RGBA byte arrays match exactly between Kotlin and Python.
- Regression tests pass.

Not yet confirmed:
- Exact equivalence to the original J2ME renderer's blend/compositing behavior.
- Semantics of non-zero draw flags.
- Alternate palette selection.
- Android Canvas/Bitmap rendering.
- 320×240 screen assembly.
- Android Gradle build, device runtime, or playable APK.

## Next build — Build 213: Draw-Flag Semantics and Palette Selection

1. Audit the original sprite draw method and all call sites that pass non-zero flags.
2. Determine each low-nibble control bit's exact effect (flip, anchor, palette, or other).
3. Audit how the opaque per-group auxiliary table is consumed.
4. Identify palette-selection inputs and verify alternate palette rows.
5. Extend the rasterizer only with bytecode-grounded transforms.
6. Validate transformed composite outputs against original game resources and known screen captures.

Only after these semantics are established should the project assemble complete 320×240 scenes.
