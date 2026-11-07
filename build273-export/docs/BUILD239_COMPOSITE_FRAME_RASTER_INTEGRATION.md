# Build 239 — Composite/Frame Raster Integration

## Objective

Connect the already validated Build 214–238 stages into one deterministic path for a resolved animation frame: animation selection/placement → composite leaf expansion → exact resource binding → explicit palette-bound pixels → logical-canvas raster execution.

## New implementation

`LegacyCompositeFrameRasterPipeline.kt` introduces `LegacyCompositeFrameRasterPipeline.rasterize` and `LegacyCompositeFrameRasterResult`.

The entry point accepts an evidence-backed `LegacyBoundSpriteResource`, an already resolved `LegacyResolvedCompositeOverlay`, decoded sprites, an explicit palette index, and canvas/clip dimensions. It does not calculate animation time, select a palette, infer a resource slot, or interpret the direct-draw argument path.

Validation boundaries:
- selection must be `ANIMATION_SEQUENCE_FRAME`;
- selected `f[]` slot must equal the bound resource slot;
- every decoded sprite must belong to that same slot;
- leaf commands are expanded through Build236;
- pixels are attached through Build237 with explicit palette index and dimension checks;
- the final operations are executed by Build238.

The original `0xFF` no-group sentinel is handled as an empty operation list and therefore a transparent/blank output surface. This is not treated as a missing-data error. The direct six-int draw argument route remains deliberately excluded because its semantics are not yet established.

## Tests

Kotlin checks cover:
1. A synthetic resolved frame passing through concrete operation expansion, pixel binding, and raster execution with exact expected pixels.
2. A no-group sentinel producing an empty operation list and blank surface.
3. Rejection of a mismatched resource slot and a direct-draw selection.

Python regression suite: 213 passed, 4 existing Pillow deprecation warnings.
All production and test Kotlin source files compile together; the Build223–239 Kotlin regression runner passes.

## Limitations

This milestone integrates a resolved frame/composite into the rasterizer; it does not yet construct all resolved frames for an original room or execute the complete room render pass. The room map's tile dispatch, multiple overlay paths, scene/camera placement, and frame scheduling still need to be orchestrated before claiming full-room output. Android Gradle/device runtime, screenshot parity, and APK packaging have not been performed.
