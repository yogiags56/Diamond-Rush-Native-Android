# Build 257 — Conservative CFG Worklist Abstract Interpretation

## Worklist execution
The abstract interpreter now propagates stack/local states over the corrected `i.D()V` CFG. It uses a bounded value domain: integer constants where directly proven, symbolic unknowns for fields/arrays/invocation results, and explicit stack-shape conflict markers.

- CFG blocks: 322
- Blocks reached from method entry: 247
- Worklist block visits: 881
- Blocks with predecessor stack-depth conflicts: 20
- Unsupported opcode transfer handlers encountered: 0 for the current opcode set
- Renderer callsites: 25
- Callsite pre-invoke snapshots obtained on reachable paths: 13
- Snapshots with at least descriptor-consumed stack depth: 13
- Callsite argument tuples promoted: 0
- Composite groups promoted: 0

## Why only 13 callsite snapshots?
Only 247 blocks are reachable from the method entry in the extracted normal-flow CFG. Twelve renderer callsites are in blocks not reached by the current graph. This may reflect missing exceptional/control-flow edges or extraction limitations; they are not treated as dead code. The 13 reachable callsite snapshots also have only a depth sufficiency check, not a proven typed operand-to-argument mapping.

## Safety limits
This is an initial conservative worklist prototype, not a JVM verifier. It does not yet model exception-handler edges, full JVM category-2 values, precise field/array provenance, invocation receiver typing, or all merge semantics. Stack-shape conflicts are marked explicitly. All argument values and composite groups remain UNKNOWN.

## Tests
- Full Python suite: 257 passed, 4 warnings.
- New Build257 tests: CFG worklist reachability, stack-shape conflict reporting, and fail-closed callsite audit.
- No Kotlin compilation, Android Gradle build, device runtime, room rasterization, visual parity, or APK packaging is claimed.

## Next
Build258 should add exception-table edges from the classfile Code attribute, validate all 25 callsites' reachability, and strengthen verifier-style stack/local merges before argument-level provenance is attempted.
