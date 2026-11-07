# Diamond Rush Native Android Port — Roadmap Through Build 222

## Invariants
- Native Android implementation; no J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31.
- Tile target 24×24.
- Preserve original resources, room content, animations, audiovisual behavior, and controls.
- Unknown field/value semantics remain opaque until proven.

## Milestone status
| Stage | Builds | Status |
|---|---:|---|
| 1. Resource & Asset Reconstruction | 198–212 | Completed |
| 2. Graphics Engine Reconstruction | 213–214 | Main static audit completed |
| 3. Gameplay Engine Reconstruction | 215–222 | Static baseline consolidated; unresolved semantics carried forward |
| 4. Native Gameplay Runtime | 223–226 | Next |
| 5. Android Integration & Release | 227–230 | Not started |

## Build history
- **198–212:** resource discovery, DF03 parsing, payload decoding, composite graph, sprite decode and rasterization.
- **213–214:** draw transforms, palette selection, animation records, viewport geometry.
- **215–216:** gameplay scene layers and separate `bJ` / `bI` render dispatch domains.
- **217:** room data-plane loading and setter write evidence.
- **218–221:** mutation inventory, CFG, basic blocks, partial stack/local dataflow.
- **222:** exception-table inventory, render dispatch provenance, initialization/runtime evidence classification.

## Stage 4 — Native Gameplay Runtime (Builds 223–226)
- Build 223: Kotlin room/map data model and room payload decoder.
- Build 224: deterministic logical canvas, viewport, camera and render-pass scaffolding.
- Build 225: evidence-backed cell mutation and object-state interfaces.
- Build 226: integrated native gameplay loop and golden regression fixtures.

## Stage 5 — Android Integration & Release (Builds 227–230)
- Android app shell, input mapping, lifecycle/audio integration.
- Device validation, performance, compatibility, visual parity.
- Packaging, release checks, APK.

## Validation
Static analysis and Python tests do not prove Android runtime correctness. Kotlin compilation, Android Gradle, device execution, visual parity and APK packaging remain outstanding.
