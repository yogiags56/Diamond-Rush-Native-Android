# Build 210 — Original Sprite Class Field-Consumer Audit

## Executive result

Build 210 resolves the uncertainty introduced in Build 209 by returning to the original `f.class` bytecode and auditing both the parser and the methods that consume its fields.

**The corrected field-aligned parser successfully parses all 94 original DF03 resources.** It reconstructs 1,372 sprites, 1,129 composite groups, 10,149 four-byte component records, and 139,268 bytes of concatenated sprite pixel payloads.

The Build 209 result of 19/94 was caused by incorrect field widths in the reconstructed parser, not by 75 malformed resources. Build 209's conclusion that the original resources were generally failing the parser was incorrect and is superseded here.

## Corrected parser field sequence

Starting at byte offset 6, the original `f.a(byte[], int)` method reads:

1. `f:[B`: signed-short count, then 2 bytes per sprite.
2. `h:[B`: signed-short count, then 4 bytes per component record.
3. `g:[B` and `b:[S`: signed-short group count; for each group, one component-count byte, one skipped byte, and one signed-short component-record start.
4. `a:[B`: 4 bytes per group.
5. `c:[B`: signed-short count, then 5 bytes per record.
6. `b:[B` and `a:[S`: signed-short count; for each record, one byte, one skipped byte, and one signed short.
7. Palette format, palette count, colors per palette, then palette data for recognized formats.
8. Pixel format.
9. Sprite payload records, each stored as `[signed-short length][payload bytes]`.

The last point confirms the interleaved length-plus-payload behavior that Build 209 had identified correctly. The correction is in the earlier table widths and field assignments.

The parser's `int` argument is not used for the initial header count: the original bytecode reads offsets 6 and 7 directly. Resource callers pass a sliced payload beginning at byte zero.

## Field consumers confirmed

| JVM field | Confirmed use |
|---|---|
| `f:[B` | Two-byte sprite dimensions; image creation reads width and height |
| `h:[B` | Four-byte composite component records |
| `g:[B` | Component count for each composite group |
| `b:[S` (private) | Starting component-record index for each group |
| `a:[B` | Four-byte-per-group public auxiliary table; no read found in audited `f` methods |
| `c:[B` | Five-byte records consumed by the lower-level component renderer |
| `b:[B` | Byte table returned by the public `a(int)` accessor |
| `a:[S` (public) | Start offsets for five-byte records |
| `b:I` | Palette count |
| `a:[[I` | Decoded ARGB palette rows |
| `a:S` | Pixel format |
| `c:[S` | Cumulative sprite payload offsets |
| `d:[B` | Concatenated sprite pixel payload bytes |
| `a:[[Image;` | Lazy image cache |
| `a:I` (public) | Currently selected palette |
| `a:Z` | Transparency state |

### Four-byte composite record

The group renderer's consumer confirms this layout for each `h:[B` record:

- byte 0: sprite index, or nested group index when control bit `0x10` is set;
- byte 1: signed X offset;
- byte 2: signed Y offset;
- byte 3: control flags.

The renderer uses bit `0x10` to select nested-group recursion. The low nibble is XORed with incoming flags. Incoming flag bits 0 and 1 determine whether X/Y offsets and the sprite's width/height anchor are subtracted rather than added/left unchanged. The opaque four-byte `a:[B` per-group table is retained without assigning unsupported meaning.

## Corrected original-JAR audit

- DF03 resources parsed: **94/94**.
- Sprite records: **1,372**.
- Composite groups: **1,129**.
- Four-byte component records: **10,149**.
- Concatenated pixel payload bytes: **139,268**.
- Pixel format distribution:
  - `0x1600`: 1,300 sprites.
  - `0x27F1`: 71 sprites.
  - `0x0400`: 1 sprite.
- Direct literal-index sprite-bundle call sites: **16/16 parsed**.
- Composite nested edges: **11**.
- Invalid nested targets: **0**.
- Invalid group component ranges: **0**.
- Composite cycles: **0**.

The corrected parser confirms the earlier Build 206/207 composite counts. Their composite group and component-record mapping was valid because the first three composite structures were aligned correctly. The old Build 206 parser did, however, read only two bytes per group for the auxiliary `a:[B` table; the actual table is four bytes per group. That old parser is now marked deprecated for full-resource parsing.

## Build 207 resolver revalidation

Using the corrected resource extraction and the existing Build 207 resolver reference logic:

- All 1,129 root groups expanded.
- 10,258 leaf draw commands were emitted.
- Maximum leaf commands from one root group: 111.
- 120 leaf commands were reached through nested group paths.
- All group component ranges were valid.
- All 11 nested references had valid targets.
- No cycles were detected.

This supports retaining the Build 207 resolver as the current composite expansion model. It is still a reference-level reconstruction, not proof of pixel-perfect rendering.

## Source additions

- `android/src/main/kotlin/com/diamondrush/legacy/LegacySpriteFieldLayout.kt` — field-aligned Kotlin parser, opaque table retention, palettes, pixel format, offsets, and interleaved payloads.
- `research/audit_build210_fields.py` — reproducible parser and original-JAR inventory.
- `research/audit_build210_callsites.py` — corrected call-site verification.
- `research/audit_build210_composite_graph.py` — nested graph and bounds/cycle validation.
- `research/build210_field_consumers.csv` — field-to-consumer evidence map.
- `tools/Build210OriginalJarAudit.kt` — Kotlin runtime audit against the original JAR.

The Build 209 positional trace parser and the older Build 206 composite-section parser are marked deprecated to prevent accidental use as complete resource parsers.

## Validation

- Python test suite: **44/44 passed**.
- All legacy Kotlin sources compile.
- Kotlin runtime audit against the original JAR: **94 resources, 1,372 sprites, 1,129 groups, 10,149 components, 139,268 pixel bytes**.
- Corrected direct call-site audit: 16/16 parsed.
- No Android Gradle build, device runtime, actual Android rendering, visual parity, or playable APK is claimed.

## Next build — Build 211: Native Sprite Pixel Decode Validation

1. Audit the remaining pixel decoder switch branches and exact bit/byte consumption.
2. Cross-check all 1,372 extracted payloads against sprite dimensions and palette sizes.
3. Determine whether any resource uses a pixel format outside the three formats found in the original JAR inventory.
4. Implement a reproducible Python reference rasterizer and Kotlin decoder parity tests.
5. Decode representative sprites from `ms.f`, `ui.f`, and gameplay bundles.
6. Only after parity checks, generate composite raster previews.

Do not claim Android rendering or visual parity until the native renderer is integrated and compared on-device.
