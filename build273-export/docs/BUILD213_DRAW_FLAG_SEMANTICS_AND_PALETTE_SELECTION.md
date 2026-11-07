# Build 213 — Draw-Flag Semantics and Palette Selection

## Executive result

Build 213 audits the original `f.class` draw methods and palette-preload method. It adds the four transform values that the original game actually passes to MIDP `Graphics.drawRegion`, adds explicit palette-row selection for sprite decoding, and corrects nested composite flag propagation in the resolver.

The earlier Build 213 progress note contained an incorrect transform label: value `1` is **`TRANS_MIRROR_ROT180`**, not `TRANS_MIRROR_ROT90`. The implementation and this report use the correct MIDP 2.0 constants. The Oracle MIDP reference lists `TRANS_MIRROR_ROT180 = 1`, `TRANS_MIRROR = 2`, and `TRANS_ROT180 = 3`.

## 1. Original draw method evidence

The original `f.class` was extracted from `DMR320x240-Celsius.jar` and disassembled with `javap -c -p -s`.

### Composite method

The original four-byte component record is read as:
- byte 0: leaf sprite index or nested composite group index;
- byte 1: signed X offset;
- byte 2: signed Y offset;
- byte 3: control flags.

The composite renderer computes:

`drawFlags = incomingFlags XOR (control & 0x0F)`

For nested components (control bit `0x10`), the recursive call receives `drawFlags`. The Build 207/212 resolver had passed the unmodified incoming flags through nested edges. Build 213 corrects that call.

The position offsets and leaf width/height anchor adjustments are evaluated using the incoming flags before the XOR, matching the bytecode instruction order.

All 11 nested edges in the current original JAR have a zero low control nibble. Therefore this resolver correction does not change the current 1,129-root inventory output, but it makes the implementation match the original method for future or synthetic data.

### Leaf draw method

The original leaf method checks bits 0 and 1 of the draw flags and passes their two-bit value directly to `Graphics.drawRegion`.

| Value | MIDP 2.0 constant | Pixel effect |
|---:|---|---|
| 0 | `TRANS_NONE` | unchanged |
| 1 | `TRANS_MIRROR_ROT180` | vertical flip |
| 2 | `TRANS_MIRROR` | horizontal flip |
| 3 | `TRANS_ROT180` | horizontal and vertical flip |

All four values preserve width and height. The original method ignores bits 2 and 3 at the leaf draw call; only the low two bits become the MIDP transform argument.

Official reference: Oracle Java ME MIDP 2.0 `Sprite` API — https://docs.oracle.com/javame/config/cldc/ref-impl/midp2.0/jsr118/javax/microedition/lcdui/game/Sprite.html

## 2. Transform audit across the original JAR

Across the 1,129 composite roots, the corrected resolver emits 10,258 leaf draw commands.

| Transform | Leaf command count |
|---|---:|
| 0 — no transform | 7,820 |
| 1 — mirror + rotate 180 | 1,642 |
| 2 — mirror | 439 |
| 3 — rotate 180 | 357 |
| **Total** | **10,258** |

- 528 composite roots contain at least one transformed leaf.
- 597 roots contain no transformed leaves.
- 4 groups are empty and emit no leaf commands.
- 1,125 non-empty roots were rasterized using the corrected transform mapping.
- No leaf commands use bits 2 or 3 in the low control nibble in this resource set.

## 3. Palette selection

The original `f.a(int, int, int, int)` method was audited:
- Its first argument is stored in field `a:I` and is the active palette-row index.
- Its third argument controls the highest sprite index preloaded.
- The second and fourth arguments are not read in the audited method body.
- It temporarily selects the requested palette row while constructing cached images, then restores the previous selection.

The game callers use literal palette indices 0, 1, and 2, and one caller supplies a dynamic state field `aA:I`. The exact mapping of that state field to every resource's palette rows remains a separate caller-state investigation.

Original resource inventory:
- 94 DF03 resources.
- 84 resources have one palette row.
- 10 resources have multiple palette rows.
- Multi-palette counts: six resources have 2 rows, three have 3 rows, and one has 5 rows.
- 110 palette rows total across the 94 resources.
- The largest palette count is five (`o.f`, entry 0).

`LegacySpritePaletteSelector.decodeSprites(layout, paletteIndex)` now decodes all sprites against an explicitly selected palette row. The rasterizer itself accepts the selected decoded sprite set, keeping palette state separate from geometry.

## 4. Opaque auxiliary table

The four-byte-per-group `a:[B` field is allocated and copied by the original parser, then nulled during cleanup. No read of that field occurs in the audited methods of `f.class`, including composite traversal and leaf drawing. It remains opaque and is not repurposed as transform or palette metadata.

## 5. Rasterization results

- Total groups: 1,129.
- Non-empty groups rasterized: 1,125.
- Leaf commands: 10,258.
- Transformed roots: 528.
- Alternate palette rows validated for every resource.
- Reference composite PNGs generated from original JAR pixel data using palette row 0.
- Additional alternate-palette examples generated for `o.f` entry 0 (five palette rows) and `cm.f` multi-palette entries.

Representative previews:
- `previews/build213_transformed_composite_contact_sheet.png`
- `previews/build213_o_f_five_palette_comparison.png`
- `previews/build213_palette_comparison.png`

These are reference rasters, not screenshots from the original game or Android.

## 6. Source additions and corrections

- `android/src/main/kotlin/com/diamondrush/legacy/CompositeSpriteRasterizer.kt`
  - Implements the exact 0–3 transform values.
  - Ignores high draw flag bits as the original leaf method does.
- `android/src/main/kotlin/com/diamondrush/legacy/LegacySpritePaletteSelector.kt`
  - Decodes a sprite set using a caller-selected palette row.
- `android/src/main/kotlin/com/diamondrush/legacy/CompositeSpriteObjectResolver.kt`
  - Passes XOR-adjusted flags through nested recursion.
- `research/build213_composite_raster.py`
  - Reproducible reference rasterizer.
- `research/build213_composite_inventory.csv`
  - 1,125 non-empty composite roots.
- `research/build213_transform_histogram.csv`
  - Transform distribution.
- `research/build213_multi_palette_resources.csv`
  - Multi-palette resource inventory.
- `research/build213_palette_callsite_audit.csv`
  - Palette setter call-site summary.
- `research/build213_f_field_access_audit.csv`
  - Evidence for the still-opaque auxiliary field.
- `research/build213_kotlin_python_parity.csv`
  - Exact per-composite RGBA parity records.
- `research/build213_palette_parity.csv`
  - Five-row palette selector parity records.
- `tools/Build213KotlinCompositeAudit.kt`
  - Kotlin runtime audit harness.
- `build213-kotlin-audit.jar`
  - Compiled JVM audit artifact.
- `research/build213_bytecode/f_class_full.javap.txt`
  - Full disassembly of original class `f`.

## 7. Validation boundary

- Python regression suite: **58/58 passed**.
- Original `f.class` disassembly: completed.
- Full original-resource transform audit: completed.
- Python reference rasterization: 1,125 non-empty groups.
- Kotlin source compilation: **passed with Kotlin 1.9.0**.
- Kotlin runtime audit: 78 resources containing groups, 1,129 groups, 1,125 non-empty rasters, and 10,258 leaf commands.
- Kotlin/Python exact RGBA parity: **1,125/1,125 composites**.
- Palette selector parity: **5/5 palette rows** for `o.f` entry 0, group 0.
- No Android Gradle build, device rendering, original-game visual parity, or playable APK is claimed.

## Next build — Build 214: Original Renderer and Screen Assembly

1. Audit the game-level call sites that select palette rows and draw composite groups.
2. Map the dynamic palette state `aA:I` to the resource/palette rows it controls.
3. Audit the five-byte `c:[B` record renderer and its flag bit `0x20`.
4. Reconstruct layer ordering and the use of the five-byte records.
5. Identify the resource groups that form menu, HUD, and gameplay scenes.
6. Begin assembling a 320×240 logical scene and validate the 320×178 gameplay viewport at y=31.

The group auxiliary table remains opaque until an actual consumer is found.
