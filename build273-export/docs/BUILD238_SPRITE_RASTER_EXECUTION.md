# Build 238 — Sprite Raster Execution

## Objective
Execute Build236 concrete sprite draw operations with Build237 palette-bound ARGB pixels onto a bounded logical pixel surface. Preserve original operation order, sprite geometry, MIDP transform flags, transparency, and clipping.

## Implementation
- `LegacyRasterClip`: half-open clip rectangle in logical-canvas coordinates.
- `LegacyRasterizedSurface`: deterministic ARGB output and execution counters.
- `LegacySpriteRasterExecution`: executes draw operations in input order, applies the Build213-proven MIDP transform mapping (`0` none, `1` vertical flip, `2` horizontal flip, `3` both), clips negative/out-of-bounds coordinates, skips fully transparent pixels, and performs straight-alpha source-over blending.
- Default target surface is 320×240. The gameplay viewport clip can be supplied as `(0,31)-(320,209)`.
- Camera translation remains upstream. Input coordinates are treated as logical-canvas coordinates and are not modified.
- A pixel-count safety limit and checked dimension/coordinate arithmetic prevent unsafe allocations and integer overflow.

## Regression coverage
`Build238SpriteRasterExecutionChecks` covers:
- Painter's order and untransformed blitting.
- All four MIDP transform values.
- Transparent-pixel preservation.
- Partial-alpha source-over blending.
- Negative coordinates and partial clipping.
- Gameplay viewport clipping and surface allocation limits.
- Invalid pixel payload rejection at the palette-bound draw boundary.

Python source-contract tests: `tests/test_build238_sprite_raster_execution.py`.

## Existing Kotlin test repairs discovered during full compilation
Full compilation of all production and test Kotlin sources exposed dormant defects in older test fixtures. They were repaired without changing production behavior:
- Build224: converted accidental literal `\\n` tokens into source newlines and corrected a test pixel expectation outside the 2×2 source bounds.
- Build225: corrected a camera-step fixture whose expected delta did not match the bytecode-derived modulo expression.
- Build226: converted accidental literal `\\n` tokens into source newlines.
- Build227: corrected an overflowing positive `Int` literal and expanded the synthetic animation fixture to include the sequence index exercised by the test.

These were test-source/fixture defects; they do not establish a defect in the corresponding production algorithms.

## Validation
- Python regression suite: **209 passed, 4 existing Pillow deprecation warnings**.
- Kotlin: all `android/src/main/kotlin` and `android/src/test/kotlin` sources compiled together with `kotlinc`.
- Kotlin regression runner: available Build223–Build238 checks passed, including parser/binding/operation/raster checks for Builds234–238.
- ZIP integrity: checked after packaging.

## Explicit non-claims
- No Android Gradle build was run.
- No Android device/emulator runtime was run.
- No complete original room has yet been rasterized end-to-end.
- No screenshot parity comparison has been performed.
- No APK has been packaged.
- Runtime camera state and palette selection at every original callsite remain separate upstream binding concerns.

## Next
Build239 — composite/frame render integration: join animation-frame placement, composite expansion, palette-bound leaf draws, and this raster execution stage while preserving provenance and painter's order. Then Build240 targets the first complete original room scene.
