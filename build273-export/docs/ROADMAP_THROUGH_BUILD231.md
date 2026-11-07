# Diamond Rush Native Android Port — Roadmap through Build 231

| Build | Milestone | Status |
|---|---|---|
| 223 | Native room/map model and payload decoder | Complete; Python-tested |
| 224 | Logical canvas and gameplay viewport scaffold (320×240; viewport 320×178 at y=31) | Complete; source checks |
| 225 | Camera offsets and redraw-strip planner | Complete; source-level reconstruction |
| 226 | Independent main render dispatch and secondary overlay attribution | Complete; bytecode-derived numeric routes |
| 227 | Typed dispatch resolver and animation-frame selection | Complete; resolver semantics retained |
| 228 | Deterministic per-cell render trace | Complete; canonical CSV |
| 229 | Room-map + viewport + per-cell scene trace integration | Complete; ordered candidates and explicit bounds state |
| 230 | Main-pass branch-to-draw-command planner | Complete; ordered commands, opaque targets preserved |
| 231 | Original `w0.bin` / `w1.bin` / `w2.bin` room archive integration | Complete; 41 actual room records indexed; selected-record decoder connected |
| 232 | Sprite-resource consumer attribution and room-to-resource binding | Next |
| 233+ | Proven scene draw expansion, rasterization, effects, HUD, menus, lifecycle, input, audio, parity | Planned |

## Invariants

- Native Android implementation; not an emulator wrapper.
- Logical canvas remains 320×240; gameplay viewport remains 320×178 at y=31.
- Tile target remains 24×24.
- Preserve original assets, room content, logic, animation, and audiovisual behavior where evidence permits.
- Numeric IDs and unresolved field meanings remain opaque; no invented gameplay labels.
- Python tests, Kotlin compilation, Android Gradle build, device runtime, visual parity, and APK are separate validation levels.

## Build 231 evidence boundary

The original JAR contains three room archives. The first prefix byte is opaque; the second byte supplies the room-record count. All 41 records are validated against the established 4-byte-dimension-header plus three-plane payload contract. The new Kotlin archive decoder delegates to the existing record decoder. DF03 sprite resources are catalogued separately, but Build 231 does not claim room-to-resource associations or rasterized gameplay output.
