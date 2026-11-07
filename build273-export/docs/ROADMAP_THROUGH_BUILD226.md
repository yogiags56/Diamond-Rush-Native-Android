# Diamond Rush Native Android Port — Roadmap Through Build 226

## Invariants
- Native Android port, not a J2ME emulator wrapper.
- 320×240 logical canvas; gameplay viewport 320×178 at y=31.
- Tile unit 24×24.
- Preserve all original map planes, packed bits, signed byte values, assets, and animation timing.
- Keep raw selector domains and uncertain semantics opaque.

## Milestones
- Stage 1 — Resource/asset reconstruction: baseline completed.
- Stage 2 — Graphics reconstruction: static asset/sprite/composite baseline completed.
- Stage 3 — Gameplay reconstruction: room loader, map mutation audit, CFG/dataflow, exception audit and render-dispatch provenance completed as static baseline.
- Stage 4 — Native gameplay runtime: in progress.
  - Build 223: room/map data model and payload decoder.
  - Build 224: canvas, viewport, camera decomposition and logical surface.
  - Build 225: camera aligned bounds, redraw strips, vertical camera step, coordinate orientation correction.
  - Build 226: two main raw dispatch tables, shared render tails, and secondary overlay resource/frame attribution.
- Stage 5 — Android integration/release: not started.

## Build 226 facts
- Main per-cell loop scans 10×16 candidate positions and bounds-checks against room dimensions.
- `bJ` comes from the low 8 bits of `a:[[I`; switch domain 3..37.
- `bI` comes from signed `a:[[B`; switch domain 0..49 plus pre-switch signed-byte handling.
- Main pass queued composites are handled in separate shared tails.
- Secondary loop has numeric overlay routes for 20..25, 31, 32, 36 and signed-byte 80..207; supplemental resource conditions 13 and 7 are independent.
- Resource IDs and case values remain numeric, not semantic object names.

## Next
- Build 227: typed resolver for resource/frame selection, backed by `LegacySpriteResource` and animation table data.
- Build 228+: deterministic scene trace, actor/effect integration, HUD/menu, Android lifecycle/input/audio, device parity, release packaging.
