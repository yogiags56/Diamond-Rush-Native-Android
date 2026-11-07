# Diamond Rush Native Android Port — Roadmap through Build 242

## Fixed invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31.
- Target tile 24×24.
- Preserve original assets, room data, bytecode-derived logic, animation and audiovisual behavior.
- Keep unproven arguments/fields opaque.

## Completed foundation
- Builds198–212: resource parsing, sprite decoding, composite graph/raster foundations.
- Build213: MIDP transform and palette-selection audit; 1,125 composite parity checks.
- Builds214–222: animation records, viewport, scene traversal, dispatch attribution, room/map-plane and bytecode control-flow reconstruction.
- Builds223–231: room map model, camera/render dispatch, per-cell tracing, room archive decoding.
- Builds232–235: resource consumers, static `f[]` bundle attribution, DF03 parsing, resource/composite/animation bindings.
- Build236: concrete resource-bound leaf draw operations.
- Build237: palette-aware pixel binding; Kotlin interleaved sprite payload parser correction.
- Build238: bounded ARGB raster execution, clipping, alpha and MIDP transforms.
- Build239: resolved animation-frame/composite → pixel binding → raster integration.
- Build240: original room render assembly manifest for `w0.bin` room 0; not a full raster.
- Build241: CFG candidate art evidence for main dispatch; candidates explicitly non-exclusive.
- Build242: exact dynamic `f[]` resource origins traced through `i.j()V`; 63 records across `/{aA}.f`, `genN.f`, and `cm.f`; candidate slots 27, 30, and 56 mapped to original DF03 payloads and parsed.

## Build242 validation
- Python: 219 passed, 4 existing Pillow deprecation warnings.
- Kotlin: all production and test sources compile; Build223–242 regression runner passes.
- Three exact original dynamic payloads parsed by Kotlin: 11, 11, and 6 sprites respectively.
- No Android Gradle build, device runtime, full-room raster, screenshot parity, or APK.

## Next: Build243 — Dynamic Sprite Index and Composite Attribution
1. Decode all sprite records in `f[27]`, `f[30]`, and `f[56]` using the proven palette rows.
2. Join sprite records to composite/animation metadata only where exact resource slot and index evidence exists.
3. Trace the `bJ=6` dispatch branch through the original method to the actual draw calls and arguments.
4. Preserve conditional branches and per-cell selector values; do not promote the CFG candidate union to an exclusive binding.
5. Build a provenance-rich operation list for the first supported `bJ=6` room cells.
6. Keep `f[42]` direct six-int draw route opaque until its argument semantics are proven.

The near-term objective is a first original-room layer containing genuine, dynamically loaded art with traceable source records. Full-room rasterization and Android runtime remain later milestones.
