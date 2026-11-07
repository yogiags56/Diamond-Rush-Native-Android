# Build 241 — Main Dispatch Art Evidence Audit

## Goal
Bridge the bytecode main-pass dispatch selectors to the art/resource accesses reachable from each branch while preserving uncertainty.

## Implementation
`LegacyMainDispatchArtEvidence.kt` adds a typed evidence row and catalog. It accepts the Build226 CFG audit fields and preserves selector domain, branch target, reachable instruction count, direct `f[]` access offsets, candidate resource indices, and reachable render-call count.

The catalog deliberately labels any resource set as `CFG_REACHABLE_CANDIDATES_ONLY` and marks it `NOT_AN_EXCLUSIVE_BINDING`. CFG reachability unions conditional alternatives; they are not proof that every candidate is used for a given selector or that one candidate is the selector's art. Empty rows are marked `NO_REACHABLE_ART_EVIDENCE`.

## Original room coverage
The research generator counts selector values from the three original serialized room archives `w0.bin`, `w1.bin`, and `w2.bin`. It emits 88 rows: 35 bJ switch cases, 50 bI switch cases, and three explicit control-flow boundary/sentinel rows. The original archives contribute 100,906 selector observations across both map planes.

## Key result and limitation
The CFG audit yields candidate resource indices 27, 30, and 56 for some bJ cases. These do not match the ten static bundle-to-slot assignments from Build233. Build233 also identified dynamic `f[]` writes, but their runtime object origins are not yet resolved for these candidates. Therefore Build241 does not bind any of these candidate IDs to decoded assets or render them. The f[42] direct six-int draw path remains opaque.

## Validation
- Python regression suite: 217 passed, 4 existing Pillow deprecation warnings.
- All production and test Kotlin source files compiled together.
- New Build241 Kotlin evidence checks passed in the regression runner.

## Next
Build242 should trace the dynamic `f[]` object origins and runtime index derivation for candidate indices 27, 30, and 56 from the original loader/control-flow. Only a proven object origin and matching bundle/entry should allow an executable sprite binding. Continue keeping the main-pass bJ and bI domains separate.
