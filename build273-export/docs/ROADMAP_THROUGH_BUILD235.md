# Diamond Rush Native Android Port — Roadmap Through Build 235

## Project invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas: 320×240.
- Gameplay viewport: 320×178 at y=31.
- Tile target: 24×24.
- Preserve original assets, logic, room content, animation, and audiovisual behavior.
- Keep unknown field/value semantics opaque until proven by bytecode/runtime evidence.
- Keep source GitHub-ready and distinguish static evidence from runtime validation.

## Milestone status
| Build | Milestone | Status |
|---|---|---|
| 223 | Native room/map model | Complete |
| 224–225 | Canvas, viewport, camera and render scaffolding | Complete |
| 226–227 | Main render dispatch and typed resolver | Complete |
| 228–229 | Per-cell trace and deterministic room scene trace | Complete |
| 230 | Main-pass draw-command planner | Complete |
| 231 | Original room archive integration (41 records) | Complete |
| 232 | Numeric sprite-resource consumer attribution | Complete |
| 233 | Static bundle-entry to global `f[]` slot attribution | Complete |
| 234 | DF03 resource parser reconstruction | Complete |
| 235 | Sprite-to-room/composite binding catalog | Complete |
| 236 | Concrete sprite draw-operation expansion | Next |
| 237+ | Scene rasterization, HUD/menu/effects integration | Planned |
| Final | Android lifecycle/input/audio, device parity, APK | Not started |

## Build235 result
Ten static `f[]` slots bind to 87 decoded sprite records. Their resource-local composite data contains 843 component references, and all groups expand to in-range leaf sprite records. Animation tables expose 85 referenced frame records: 82 valid composite-group references and three explicit `0xFF` no-group sentinels. Expanding valid animation frame groups yields 719 leaf references.

Only `f[9]` and `f[10]` from this ten-slot static loader set are direct `i.D()V` render-method consumers. The other eight have indexed consumers in other methods. This distinction is preserved in the binding report; static loading alone is not treated as proof of room-cell drawing.

## Next: Build236
Join cell dispatch and overlay selections to proven resource bindings, then emit concrete draw operations with sprite index, dimensions, position, flags, composite path, animation sequence/frame, and source bytecode evidence. Keep direct-draw and supplemental-resource paths distinct. Do not claim full scene parity until compared against original runtime output.

## Validation boundary
Python tests and targeted Kotlin compilation/runtime checks pass. Android Gradle build, device execution, visual parity, and APK packaging remain outstanding. Static resource bindings do not by themselves establish runtime draw visibility or full scene parity.
