# Diamond Rush Native Android Port — Roadmap through Build 229

| Build | Milestone | Status |
|---|---|---|
| 223 | Native room/map model and payload decoder | Complete; Python-tested |
| 224 | Logical canvas and gameplay viewport scaffold (320×240; viewport 320×178 at y=31) | Complete; Python/Kotlin source checks |
| 225 | Camera offsets and redraw-strip planner | Complete; source-level reconstruction |
| 226 | Independent main render dispatch and secondary overlay attribution | Complete; bytecode-derived numeric routes |
| 227 | Typed dispatch resolver and animation-frame selection | Complete; resolver semantics retained |
| 228 | Deterministic per-cell render trace | Complete; canonical CSV |
| 229 | Room-map + viewport + per-cell scene trace integration | Complete; 160 ordered candidates, explicit bounds state |
| 230 | Main-pass branch-to-draw-command integration | Next |
| 231 | Real decoded room and sprite-resource scene trace | Planned |
| 232+ | Scene rasterization, effects, HUD, menus, lifecycle, input, audio, parity | Planned |

## Invariants

- Native Android implementation; not an emulator wrapper.
- Logical canvas remains 320×240; gameplay viewport remains 320×178 at y=31.
- Tile target remains 24×24.
- Original assets, room content, logic, animation and audiovisual behavior are preserved where evidence permits.
- Numeric IDs and unresolved field meanings remain opaque; no invented gameplay labels.
- Python tests, Kotlin compilation, Android Gradle build, device runtime, visual parity and APK are reported as separate validation levels.

## Build 229 evidence boundary

Build 229 joins the recovered room planes to the observed row-major viewport candidates. Out-of-bounds candidates are retained without array access. This is a scene-level **dispatch trace**, not yet a pixel renderer or a full expansion of all main-switch branches. Synthetic fixtures validate the integration contract, not original room contents.
