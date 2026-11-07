# Build 231 — Original Room Archive Integration

## Objective

Connect the proven Build 223 room-record decoder to the actual room archive resources shipped in `original/DMR320x240-Celsius.jar`, without assigning semantic names to map values.

## Original archive format confirmed

The original class `i` static initializer declares three room archive resources: `/w0.bin`, `/w1.bin`, and `/w2.bin`. The original loader consumes two prefix bytes before iterating records. The second byte is used as the record count; the first byte is retained as opaque metadata because its meaning is not established here.

Each record is:

- 4-byte header containing two unsigned little-endian 16-bit dimensions;
- three serialized byte planes, each `firstDimension * secondDimension` bytes.

Build 231 adds `LegacyWorldRoomArchiveDecoder`:

- `index(bytes)` validates the prefix, declared count, each dimension pair, payload boundary, and trailing-byte count;
- `decode(bytes, archiveName, roomIndex)` strips only the two-byte archive prefix and delegates record decoding to the existing `LegacyRoomPayloadDecoder`;
- the original plane sign-extension, defensive copies, and zeroed runtime overlays remain unchanged;
- archive names are constrained to the three bytecode-proven resource names.

## Real archive inventory

| Archive | Declared rooms | Bytes | Room dimensions (first × second) |
|---|---:|---:|---|
| `w0.bin` | 14 | 47,686 | 26×21; 27×24; 27×26; 40×23; 51×24; 30×75; 26×45; 44×29; 35×14; 50×30; 50×31; 46×31; 46×31; 68×11 |
| `w1.bin` | 13 | 46,956 | 45×24; 40×24; 33×30; 43×30; 45×33; 43×33; 36×43; 53×27; 34×32; 35×25; 37×24; 60×20; 23×60 |
| `w2.bin` | 14 | 56,887 | 60×26; 39×35; 35×42; 38×38; 46×27; 49×28; 55×30; 51×20; 51×37; 104×17; 35×25; 45×28; 35×32; 35×26 |

All 41 declared room records were fully indexed; each archive ends exactly at the end of its final record (zero trailing bytes). See `research/build231_original_room_archive_index.csv`.

The existing DF03 sprite resource inventory is retained as a separate catalog (`research/build231_sprite_bundle_catalog.csv`). This is an availability inventory, not yet a proven room-to-sprite mapping. Resource indices used by rendering still require bytecode/call-site attribution before binding them to individual rooms or cells.

## Kotlin additions

- `android/src/main/kotlin/com/diamondrush/legacy/LegacyWorldRoomArchiveDecoder.kt`
- `android/src/test/kotlin/com/diamondrush/legacy/Build231WorldRoomArchiveChecks.kt`

Checks cover opaque prefix retention, multi-record indexing, selecting a later room, reuse of the established plane decoder, signed byte extension, and malformed/truncated archive rejection.

## Validation

- Python regression suite: **167 passed, 4 warnings**. The four warnings are pre-existing Pillow `Image.getdata()` deprecations.
- Kotlin main sources: compiled successfully with `kotlinc`.
- Build 231 Kotlin checks: executed successfully (`BUILD231_KOTLIN_CHECKS_PASSED`).
- Original JAR room archive validation: 41/41 records indexed; all three archive lengths exactly consumed.
- Android Gradle build, APK, device runtime, scene rasterization, and visual parity: **not performed**.

## Evidence boundary / not yet implemented

This build makes actual room payloads available to the native data model. It does not claim that the room's numeric plane values are semantically decoded, that the sprite bundle IDs are mapped to each room, or that a gameplay frame can yet be rasterized. Build 232 will trace resource-index consumers and establish evidence-backed bindings between render dispatch requests and concrete sprite resources.
