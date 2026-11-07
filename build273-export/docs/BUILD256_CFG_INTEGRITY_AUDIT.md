# Build 256 — CFG Integrity Audit and Worklist Readiness

## Correction to Build255 extraction
The initial bytecode parser accidentally interpreted numeric `tableswitch`/`lookupswitch` case labels as instruction offsets. Build256 corrected this by excluding numeric-only switch-body rows from the instruction stream and rebuilding the CFG. This correction supersedes the Build255 counts previously reported.

## Corrected CFG
- Actual JVM instructions: 3811
- Basic blocks: 322
- CFG edges: 564
- Switch instructions parsed: 10
- Renderer callsites mapped and verified: 25/25
- Instruction offsets unique: True
- Instructions covered exactly once by block intervals: True
- Reachable blocks from method entry under extracted normal-flow edges: 247
- Blocks not reached under this graph: 75

## Interpretation
The 75 blocks not reached may include dead/unreachable code, extraction gaps, or edges not modeled by this normal-flow CFG. Exception-handler edges and verifier-grade stack typing are not yet included. Reachability is not proof of semantic dead code.

The worklist abstract interpreter is not yet implemented. This build establishes corrected structural inputs and validation checks only.

## Tests
The complete Python regression suite is expected to be run after the new CFG integrity tests are added. No Kotlin/Android build, device runtime, room rasterization, visual parity, or APK packaging is claimed.
