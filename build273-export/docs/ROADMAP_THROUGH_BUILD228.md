# Diamond Rush Native Android Port — Roadmap through Build 228

## Foundation and reverse engineering

- Builds 198–212: resource inventory, sprite parsing/decoding, composite graph reconstruction, and rasterization groundwork.
- Build 213: draw-flag/palette selection; 1,125 composite raster parity checks passed in the historical Kotlin audit.
- Build 214: five-byte animation records, 188 sequences / 1,238 records, frame placement, and 320×240 canvas / 320×178 gameplay viewport at y=31.
- Build 215: gameplay scene/camera traversal audit.
- Build 216: independent `bJ` and `bI` dispatch domains and secondary overlay attribution.
- Build 217: room binary loader and plane model.
- Build 218–221: mutation control flow, operand stack attribution, CFG, and worklist stack analysis.
- Build 222: exception flow and render read provenance.
- Build 223: native Kotlin room/map plane model and decoder.
- Build 224–225: logical canvas, viewport, camera, and redraw-strip scaffold.
- Build 226: bytecode-derived render dispatch catalog and overlay route attribution.
- Build 227: typed dispatch resolver, signed-byte behavior, animation selection, and composite overlay connection.
- Build 228: deterministic per-cell render trace with stable CSV serialization.

## Next implementation milestones

- **Build 229:** connect decoded room planes, camera/viewport iteration, and per-cell trace into ordered scene-level draw commands. Preserve uncertainty around axis mapping and ordering until proven.
- **Build 230:** resolve scene command expansion against actual decoded resources and room fixtures.
- **Build 231+:** integrate remaining gameplay layers, effects, HUD, menu/background/hint, input, audio, and Android lifecycle.
- **Final validation:** Kotlin/Gradle build, emulator/device execution, original-game screenshot comparisons, behavioral checks, packaging, and APK delivery.

## Validation policy

A Python reference test is not a Kotlin compile; Kotlin compilation is not an Android Gradle build; an APK build is not device validation; and successful execution is not visual parity. Each claim must be reported separately with its actual evidence.
