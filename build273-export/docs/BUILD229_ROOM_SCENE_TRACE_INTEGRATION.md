# Build 229 — Room-to-Scene Trace Integration

## Objective

Join the recovered room map-plane model (Build 223), camera/viewport candidate traversal (Builds 224–225), and typed per-cell render resolver (Builds 227–228) into one deterministic, row-major scene trace.

## Implementation

- `LegacyRoomSceneTraceBuilder` calls the existing `LegacyVisibleCellTraversal.candidates()`; it does not invent new loop bounds or camera math.
- All 160 candidates from the observed row `-1..8` and column `-1..14` scan are retained in order.
- Out-of-room candidates are explicit `OUT_OF_BOUNDS` records and never read a plane array.
- In-bounds candidates are joined to the room planes and passed through `LegacyPerCellRenderTrace.traceCell()`.
- Logical canvas Y is recorded as gameplay-relative screen Y plus the proven viewport translation of 31 pixels.
- Canonical CSV adds `logicalCanvasY` and `boundsStatus`, with a stable header, row order, and final newline.

## Plane provenance and limits

The current join uses the room model's primary byte plane as the signed `bI` selector and the secondary integer plane as the packed `bJ` value. The serialized integer plane is deliberately not silently substituted. This mapping follows the reconstructed renderer read provenance; it remains a raw numeric mapping, not a gameplay object classification.

The scene trace records dispatch decisions, not rendered pixels. It does not yet expand every main-switch branch into concrete sprite commands, nor does it rasterize a real decoded room. Animation resources required by a selected secondary overlay must be supplied by the caller; missing required tables fail explicitly rather than fabricating frame data.

## Validation

- Python regression suite: **161 passed, 4 warnings**.
- Kotlin production sources compiled with `kotlinc`.
- Framework-free Build 228 and Build 229 Kotlin checks executed: `BUILD229_KOTLIN_CHECKS_PASSED`.
- Kotlin checks cover 160 candidate retention, 16 in-bounds + 144 out-of-bounds for a synthetic 4×4 room at camera (0,0), no array reads for out-of-bounds candidates, `-1` second-pass skip, canvas Y translation, and stable CSV markers.
- The four Python warnings are existing Pillow `Image.getdata()` deprecations.

## Not claimed

No Android Gradle build, APK, Android-device execution, original-room scene rasterization, or visual parity is claimed. The synthetic room fixture validates joining and ordering only; it is not represented as original game content.

## Next

Build 230 should connect resolved main-pass branch targets and the already recovered composite/cache structures to ordered draw-command records, while retaining unknown branches as opaque commands. Then use a genuinely decoded room payload and real sprite resources to produce the first reproducible scene trace and, only after command semantics are supported, a raster output.
