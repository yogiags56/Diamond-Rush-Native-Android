# Diamond Rush Native Android Port — Roadmap Through Build 219

## Project invariants
- Native Android implementation; not a J2ME emulator wrapper.
- Logical canvas 320×240.
- Gameplay viewport 320×178 at y=31.
- Tile target 24×24.
- Preserve original assets, logic, room content, animation and audiovisual behavior.
- Keep unknown field/value semantics opaque until bytecode or runtime evidence resolves them.

## Milestone status

| Stage | Builds | Status |
|---|---:|---|
| 1. Resource & Asset Reconstruction | 198–212 | Completed |
| 2. Graphics Engine Reconstruction | 213–214 | Main static audit completed |
| 3. Gameplay Engine Reconstruction | 215–222 | In progress — Build 219 completed |
| 4. Native Gameplay Runtime | 223–226 | Not started |
| 5. Android Integration & Release | 227–230 | Not started |

## Build history
- **198–212:** resource discovery, DF03 parsing, payload decoding, composite graph, sprite decode, rasterization.
- **213:** draw-flag transform semantics and palette selection; Kotlin/Python parity audit completed for the tested composite groups.
- **214:** animation-record layout and viewport geometry.
- **215:** gameplay scene layers, camera/map traversal, render passes, HUD boundary.
- **216:** two distinct tile/cell render dispatch domains (`bJ`, `bI`); do not collapse them.
- **217:** room data-plane loading; three selected-room payload planes and a proven setter for `a:[[B` and `b:[[I`.
- **218:** map mutation candidate sites and 7,143 validated instruction-level branch edges; no full operand-stack analysis.
- **219:** conservative direct-pattern attribution for five priority methods; unresolved sites and opaque cell/object bindings retained.

## Current focus: Build 220
- Build basic-block CFG and operand-stack dataflow with merge states.
- Track map-array references through locals and stack duplication.
- Resolve row/column expressions and values at store sites.
- Trace outer `j()` switch targets through reachability, not linear bytecode ranges.
- Relate values read from `a:[[I` to `bJ`/`bI` only when supported by direct dataflow.
- Keep semantic labels unknown until evidence supports them.

## Validation status
- Static resource/bytecode analysis and Python reference tests: multiple milestones completed.
- Build 213 Kotlin reference compilation: completed in that milestone only.
- Current Build 219 Kotlin compile: not run.
- Android Gradle build, device runtime, full gameplay parity, and APK: not yet achieved.
