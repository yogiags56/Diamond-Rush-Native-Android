# Build 223 — Native Kotlin Room and Map Data Model

## Objective

Begin Stage 4 by implementing the room/map storage contract already supported by the original bytecode trace. This milestone deliberately implements the data boundary only: it does not assign tile IDs, collision behavior, object classes, or gameplay meanings to opaque values.

## Implemented Kotlin sources

- `android/src/main/kotlin/com/diamondrush/legacy/LegacyRoomMapPlanes.kt`
- `android/src/main/kotlin/com/diamondrush/legacy/LegacyRoomPayloadDecoder.kt`

### Preserved room record contract

1. Four-byte header.
2. First and second dimensions are unsigned little-endian 16-bit integers.
3. Three serialized planes follow, each containing `firstDimension * secondDimension` bytes.
4. Plane 1 is retained as `ByteArray`.
5. Planes 2 and 3 are converted to `IntArray` by signed byte extension, matching `baload` then `iastore`.
6. Two independent runtime byte overlays are allocated and zero-initialized.
7. Non-selected records are skipped by exactly three payload planes after their four-byte header.

### Map indexing

The model preserves the source JVM two-dimensional array orientation: the first coordinate selects the outer row, and the second selects the cell within that row. Flattening uses `first * secondDimension + second`, without swapping dimensions.

### Proven setter

`setPrimaryAndSerializedInt(first, second, byteValue, intValue)` updates only the primary byte plane and the first serialized integer plane. It intentionally leaves the other integer plane and both runtime overlays untouched.

### Defensive checks

- Positive dimensions required.
- Product computed in `Long` and checked against `Int.MAX_VALUE`.
- Truncated headers and payloads rejected.
- Missing selected record rejected.
- Coordinate bounds checked.
- Constructor validates all five plane lengths.
- Public plane-copy methods return defensive copies.

## Validation

A standalone Kotlin test runner is included at:
`android/src/test/kotlin/com/diamondrush/legacy/Build223RoomDecoderChecks.kt`

Checks cover little-endian dimensions, signed byte extension, multi-record skipping, zeroed independent overlays, setter isolation, malformed input, missing room, and bounds.

Python regression tests cover the source contract. Kotlin compilation/test execution is reported separately below depending on tool availability.

## Not implemented

- Android Gradle module integration or app entry point.
- Native rendering, camera, input, audio, object simulation, collision, or room transitions.
- Semantic naming of any map values.
- APK or device validation.

## Next — Build 224

Integrate this room model with the deterministic logical canvas and gameplay viewport:
- 320×240 logical surface;
- gameplay clip 320×178 at y=31;
- preserve separate `bJ` and `bI` dispatch domains;
- add camera and visible-cell traversal scaffolding;
- render only evidence-backed content and keep unknown cases explicit.
