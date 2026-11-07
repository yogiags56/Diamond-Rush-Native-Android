# Diamond Rush Native Android Port — Roadmap Through Build 220

## Project invariants
- Native Android implementation, not a J2ME emulator wrapper.
- Logical canvas: 320×240.
- Gameplay viewport: 320×178 at y=31.
- Tile target: 24×24.
- Preserve original assets, logic, room content, animations, and audiovisual behavior.
- Keep unknown field/value semantics opaque until supported by bytecode or runtime evidence.

## Milestone status

| Stage | Builds | Status |
|---|---:|---|
| 1. Resource & Asset Reconstruction | 198–212 | Completed |
| 2. Graphics Engine Reconstruction | 213–214 | Main static audit completed |
| 3. Gameplay Engine Reconstruction | 215–222 | In progress — Build 220 completed |
| 4. Native Gameplay Runtime | 223–226 | Not started |
| 5. Android Integration & Release | 227–230 | Not started |

## Build history
- **198–212:** resource discovery, DF03 parsing, payload decoding, composite graph, sprite decode, rasterization.
- **213:** draw-flag transform semantics and palette selection.
- **214:** animation records and viewport geometry.
- **215:** gameplay scene layers, camera/map traversal, render passes, HUD boundary.
- **216:** two separate tile/cell render dispatch domains (`bJ`, `bI`).
- **217:** room data-plane loading and proven setter for `a:[[B` / `b:[[I`.
- **218:** map mutation candidate sites and instruction-level branch-edge inventory.
- **219:** conservative direct-pattern map-plane attribution in five priority methods.
- **220:** basic-block index, branch/switch edges, approximate reachability, and lightweight linear stack trace.

## Next: Build 221
- Implement worklist-based stack-state propagation across CFG edges.
- Merge abstract stack values at branch joins.
- Model method invocations, array aliases, locals, and all encountered stack opcodes.
- Trace `a:[[I` reads into `bJ` and `bI` dispatch consumers.
- Recover representative row/column expressions and separate room initialization from runtime mutation.

## Validation
Static Python analysis and regression tests are not Android runtime validation. Kotlin compilation, Android Gradle build, device execution, visual parity, and APK packaging remain outstanding for this gameplay milestone.
