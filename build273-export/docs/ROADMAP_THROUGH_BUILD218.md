# Diamond Rush Native Android — Roadmap through Build 218

## Project invariants
- Native Android port, not an emulator wrapper.
- Logical canvas 320×240.
- Gameplay viewport 320×178 at y=31.
- Tile unit 24×24.
- Preserve original resources, logic, animation, and room data.
- Keep unknown field/value semantics opaque until proven by bytecode/runtime evidence.
- Keep source GitHub-ready and validation claims separated.

## Current position
**Stage 3 — Gameplay Engine Reconstruction.** The graphics foundation and room-data structure have been audited. We are now mapping state-dependent changes to the room map and connecting them to rendering/object dispatch.

## Milestone history

| Build | Result | Status |
|---|---|---|
| 198–209 | Resource discovery, DF03 parser, payload decoding, composite tracing | Completed |
| 210 | Field consumer audit across 94 resources | Completed |
| 211 | Sprite pixel decode 1,372/1,372 | Completed |
| 212 | Composite rasterization baseline, 300 no-transform groups | Completed |
| 213 | MIDP transforms, draw flags, palette selection; 1,125 group parity checks | Completed |
| 214 | Animation records, palette state, 320×178 viewport at y=31 | Completed |
| 215 | Gameplay render helpers, camera/map traversal, two cell passes | Completed |
| 216 | Two tile dispatch tables: 35 cases and 50 cases | Completed |
| 217 | Room header, three serialized planes, two runtime byte overlays, central setter | Completed |
| 218 | 66 map-related methods, 552 array stores, 458 candidate map-plane stores, 7,143 CFG edges | Completed |

## Stage 1 — Resource & Asset Reconstruction
Completed foundation: resource inventory, decoding, composite graph and rasterization.

## Stage 2 — Graphics Engine Reconstruction
Completed main audits: MIDP transforms, palette selection, animation frame record layout, viewport geometry, render pass and tile dispatch attribution.

## Stage 3 — Gameplay Engine Reconstruction (current)

### Build 219 — Operand-Stack Attribution and Cell/Object Binding
- Confirm exact target array for candidate stores.
- Separate room initialization from runtime mutation.
- Trace coordinate/index calculations.
- Relate mutation values to Build 216 cell dispatch.
- Build a conservative cell/object binding table.

### Build 220 — Camera, Occlusion, and Layer Ordering
- Finish camera offset and exposed-strip behavior.
- Resolve render pass order, overlays, effects, actors, and occlusion.
- Validate bounds against the 320×178 viewport.

### Build 221 — Deterministic Original Scene
- Reconstruct one complete room from original data.
- Build a deterministic 320×240 scene fixture.
- Compare object bounds and draw order against bytecode-derived expectations.

### Build 222 — Animation and Timing Integration
- Connect five-byte animation records to actual consumers.
- Resolve frame progression, looping, pauses, and duration units.
- Integrate offsets, flags, and palette state.

## Stage 4 — Native Gameplay Runtime

### Build 223 — Native Map and Entity Model
Implement separate static map, dynamic map state, entity, and overlay structures in Kotlin.

### Build 224 — Native Renderer Integration
Integrate original sprite/composite rendering with map traversal, camera, clipping, layers, and animation.

### Build 225 — Input and Gameplay State
Reconstruct keypad/action mapping, movement, collision, interaction, and state transitions.

### Build 226 — Room and Level Progression
Implement room loading, transitions, reset behavior, and progression.

## Stage 5 — Android Integration and Release

### Build 227 — Android Application Shell
Lifecycle, display scaling, orientation, input surface, asset packaging, memory handling.

### Build 228 — Runtime Performance and Compatibility
Frame pacing, audio, input latency, device compatibility, low-memory behavior.

### Build 229 — Full Gameplay Parity Audit
Compare original and native scenes and state transitions; resolve remaining differences.

### Build 230 — Release Candidate
Gradle build, APK creation, installation/device tests, reproducible build instructions.

## Remaining work at a glance
- Exact operand-stack attribution for map writes.
- Full tile/cell semantic catalogue.
- Complete entity and collision model.
- Final layer/occlusion/camera behavior.
- Complete original-room scene reconstruction.
- Native gameplay runtime and Android integration.
- Kotlin/Gradle/device validation and APK release.

## Validation policy
Python reference tests do not imply Kotlin compilation, Android Gradle success, device execution, visual parity, or APK generation. Each result is reported only when actually performed.
