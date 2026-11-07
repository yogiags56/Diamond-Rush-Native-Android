# Diamond Rush Native Android Port — Roadmap Through Build 224

## Project invariants
- Native Android implementation; not a J2ME emulator wrapper.
- 320×240 logical canvas; gameplay viewport 320×178 at canvas y=31.
- 24×24 tile unit.
- Preserve original assets, room content, animation, audio, and gameplay behavior.
- Keep unknown bytecode fields/IDs opaque until evidence supports semantics.
- GitHub-ready source; report validation boundaries precisely.

## Completed stages / milestones
- Stage 1 — Resource and asset reconstruction: completed baseline.
- Stage 2 — Graphics engine reconstruction: static audit baseline completed; sprite decoding, palette selection, composite graph and rasterizer reconstructed in earlier builds.
- Stage 3 — Gameplay engine reconstruction: static bytecode baseline completed; room loader, render dispatch, CFG/dataflow and exception audit established across Builds 215–223.
- Stage 4 — Native gameplay runtime: in progress.
  - Build 223: Kotlin room/map storage model and room payload decoder.
  - Build 224: logical canvas, viewport, camera decomposition, dual-selector metadata, visible-cell candidate scaffold, clipped logical pixel surface.
- Stage 5 — Android integration and release: not started.

## Current technical boundaries
- `bJ` and `bI` are distinct switch domains (35 and 50 cases).
- Room map planes preserve original orientation and signed byte-to-int conversion.
- Candidate traversal is explicit but deliberately does not wrap coordinates.
- No full scene renderer, actor simulation, collision engine, input, audio integration, Gradle app build, APK, or device parity yet.

## Next
- Build 225: camera update and map-boundary/redraw-strip semantics.
- Build 226: decode evidence-backed branches in the two visible-cell passes and map them to original resource/animation tables.
- Subsequent work: deterministic scene fixture, actor/effect integration, HUD/menu, Android lifecycle/input/audio, performance and device parity, release packaging.
