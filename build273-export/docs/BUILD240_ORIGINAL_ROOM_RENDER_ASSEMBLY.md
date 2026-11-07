# Build 240 — Original Room Render Assembly

## Objective

Move from an isolated resolved composite/frame (Build239) to an ordered, room-derived viewport pass using actual room data from the original game archives.

## New implementation

`LegacyRoomRenderAssembly.kt` adds `LegacyRoomRenderAssembly.assemble` and the immutable `LegacyAssembledRoomPass` / `LegacyAssembledRoomCell` records.

For each of the 160 bytecode-derived visible-cell candidates (-1..8 rows and -1..14 columns), the assembler:
- preserves row/column, map coordinates, screen coordinates, and logical canvas Y;
- marks out-of-bounds cells without reading room planes;
- reads the original packed integer plane and signed primary byte plane for in-bounds cells;
- resolves the two proven main dispatch decisions independently;
- records a secondary overlay resource route when the raw selector matches a proven route;
- records supplemental resource requests independently;
- retains unknown/main-switch behavior as raw dispatch kinds and bytecode branch offsets.

The assembler does not attach sprite art to opaque main switch targets, does not select animation frames, and does not reinterpret the direct six-int draw route. This is a render-pass manifest, not yet a room rasterizer.

## Actual original archive audit

The original JAR contains `w0.bin`, `w1.bin`, and `w2.bin`: 41 room records in total. All records were indexed and the full archive payloads consumed without trailing bytes (Build231 baseline).

Build240 re-audited the third serialized plane's low-byte selectors across all 41 rooms. Observed animation overlay selectors:
- `20..25` → resource `f[3]`: present.
- `31` → `f[15]`: absent in these original room records.
- `32` → `f[16]`: absent.
- `36` → `f[20]`: absent.
- `80..207` signed-byte direct route → `f[42]`: present.

Absence is reported as absence, not treated as evidence that the bytecode route is invalid. Synthetic resolver fixtures continue to test the selector branches.

## Actual assembled room sample

Audit command:

`java -cp BUILD240_ROOM_AUDIT.jar:BUILD240_KOTLIN_CHECKS.jar Build240RoomAssemblyAuditKt original.jar w0.bin 0`

Result:
- `w0.bin`, room 0, dimensions 26×21.
- Camera `(0,0)`.
- 160 visible candidates; 135 in bounds; 25 out of bounds.
- 10 secondary overlay routes: five to `f[3]`, five to `f[42]` direct route.
- CSV: `research/build240_w0_room0_camera0_manifest.csv`.
- Full 41-room selector census: `research/build240_original_room_overlay_selector_census.csv`.

## Validation

- Python regression suite: 215 passed, 4 existing Pillow deprecation warnings.
- All Kotlin production and test sources compile together.
- Build223–240 Kotlin regression runner passes.
- Actual original JAR room sample decoded and assembled into an ordered manifest.

## Explicit limitations

Build240 does not yet produce a visually complete room. The main-pass branch offsets are not all mapped to concrete sprite assets, and the direct-draw path remains opaque. Animation tables/frame resolution have not yet been applied to all actual room requests. No full-room pixel output, Android Gradle build, device runtime, screenshot parity, or APK is claimed.

## Next: Build241 — Evidence-Backed Main-Dispatch Art Binding

1. Select the first main-pass branch targets occurring in the actual `w0.bin` room 0 manifest.
2. Trace each target's bytecode call arguments and static/dynamic `f[]` consumers.
3. Bind only targets with exact resource/sequence/frame/composite evidence.
4. Keep unresolved targets explicitly opaque.
5. Produce per-cell source provenance and a bounded first visible render layer where pixel binding is complete.
6. Re-run the full 41-room census to ensure no room-specific values are silently dropped.
