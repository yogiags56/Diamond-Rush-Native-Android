# Build 255 — Renderer CFG Rebuilt from Original Classfile

## Confirmed method identity
Using `javap -p -c -s` on the bundled `original.jar`, class `i` contains the exact method `private void D();` with descriptor `()V`. The renderer callsites previously catalogued as `i.D()V` therefore belong to this exact method.

## Rebuilt CFG
- Instructions extracted: 3,925
- Basic blocks: 325
- CFG edges: 566
- Switch instructions parsed: 10 (all case and default targets included)
- Renderer callsites: 25
- Callsite offsets mapped to a containing basic block: 25
- Callsite instructions verified as `invokevirtual f.a`: 25

## Important boundary
The CFG is rebuilt from the actual classfile method, correcting Build254's identity mismatch. This is a structural CFG extraction, not yet a complete abstract interpreter. Branch edges are conservative; exception-handler edges and verifier-grade stack typing have not been added. Invocation arguments and composite groups remain unresolved pending worklist state propagation.

## Validation
- Python regression suite: 248 passed, 4 warnings.
- All 25 renderer callsite mappings and invocation opcodes verified by dedicated tests.
- No Kotlin compilation, Android Gradle build, device runtime, room rasterization, visual parity, or APK packaging is claimed.
