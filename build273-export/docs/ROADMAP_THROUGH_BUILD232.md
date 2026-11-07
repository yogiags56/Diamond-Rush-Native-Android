# Roadmap Through Build 232

| Build | Milestone | Status |
|---|---|---|
| 223 | Native room map model | Complete |
| 224–225 | Logical canvas, camera, viewport traversal | Complete |
| 226–227 | Main render dispatch and typed resolver | Complete |
| 228–229 | Deterministic per-cell and room scene trace | Complete |
| 230 | Main-pass draw-command planner | Complete |
| 231 | Original room archive integration (41 records) | Complete |
| 232 | Numeric sprite-resource consumer attribution | Complete |
| 233 | Bundle-to-resource slot attribution | Next |
| 234 | Room-to-sprite binding and draw expansion | Planned |
| 235+ | Scene rasterization, HUD/menu/effects integration | Planned |
| Final | Android lifecycle/input/audio, device parity, APK | Not started |

## Build 232 boundary

The original `f[]` resource array has 61 slots. The render method `i.D()V` has statically indexed references to 23 distinct slots. Secondary overlay consumers already attributed in earlier builds are indices 3, 7, 13, 15, 16, 20, and 42. Bundle names are not yet mapped to these slots.
