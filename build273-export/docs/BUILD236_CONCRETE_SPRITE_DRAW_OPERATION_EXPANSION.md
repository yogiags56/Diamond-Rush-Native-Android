# Build 236 — Concrete Sprite Draw-Operation Expansion

## Objective
Convert Build 235's resource-bound composite leaf references and the existing animation/composite resolver output into deterministic, resource-bound sprite draw-operation records. The output is renderer-neutral: it describes what a later renderer must draw, without claiming that pixels have been rasterized or that a complete room is visible.

## Implementation
Added `LegacyConcreteSpriteDrawOperation.kt` with:
- `LegacyConcreteSpriteDrawOperation`, a typed immutable operation record.
- `LegacyConcreteSpriteDrawOperationResolver.expand`, which joins an already-resolved animation/composite result to the exact Build235 `LegacyBoundSpriteResource`.
- Exact global `f[]` slot validation; a result for one slot cannot be attached to another slot.
- Local sprite-index validation against the resource's decoded sprite records.
- Width and height copied from the bound sprite record.
- Preservation of X/Y, incoming and adjusted draw flags, opaque arguments, source group path, and source component path.
- Stable ordinal assignment and canonical CSV serialization.

Direct-draw requests remain outside this composite expansion path. `0xFF` no-group frames do not produce composite leaf operations. Supplemental resource requests remain separate. Those distinctions are intentional.

## Kotlin checks
Added `Build236ConcreteSpriteDrawOperationChecks.kt` covering:
1. Multiple leaf commands bind to the correct local sprite dimensions and retain order.
2. Global resource-slot mismatch is rejected.
3. A leaf sprite missing from the bound resource is rejected.
4. Canonical CSV output is deterministic and preserves provenance.

## Validation
- Python regression suite: **195 passed, 4 warnings**. The warnings are existing Pillow `Image.getdata()` deprecations in Build213 tests.
- Kotlin: all files in `android/src/main/kotlin/com/diamondrush/legacy/*.kt` plus the Build236 check source compiled with `kotlinc`; `Build236ConcreteSpriteDrawOperationChecks.runAll()` executed successfully (`BUILD236_KOTLIN_CHECKS_PASSED`).
- ZIP integrity: verified separately for the release archive.
- Android Gradle build: not performed.
- Android device runtime: not performed.
- Full original-room rasterization or visual parity: not performed.
- APK: not produced.

## Evidence boundary and remaining work
Build236 provides the typed bridge from a resolved composite leaf command to the exact decoded sprite dimensions. It does not yet generate a complete command list from every original room cell. The caller must still supply a bytecode-grounded resolved overlay and its resource binding. Palette selection, pixel decode integration, actual Canvas/bitmap execution, first/second main-pass shared-tail behavior, direct draw, supplemental paths, camera clipping, and full room ordering remain follow-up work.

## Next milestone — Build237
Build237 adds explicit palette-aware pixel binding and corrects the Kotlin DF03 parser to consume interleaved sprite length/payload records. The full Kotlin original-JAR audit validates all 94 DF03 resources and 2,604 sprite/palette combinations. See `docs/BUILD237_PALETTE_AWARE_PIXEL_BINDING.md` and `docs/ROADMAP_THROUGH_BUILD237.md`.
