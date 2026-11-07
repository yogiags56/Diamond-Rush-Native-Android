# Diamond Rush Native Android Port — Roadmap Through Build 227

## Invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31.
- Tile unit 24×24.
- Preserve original assets, map planes, packed bits, signed-byte behavior, animation timing, and composite draw order.
- Keep uncertain field meanings opaque and numeric.

## Stages
- Stage 1 — Resource/asset reconstruction: baseline completed.
- Stage 2 — Graphics reconstruction: static sprite/composite baseline completed.
- Stage 3 — Gameplay reconstruction: room loading, mutation, CFG/dataflow, exception flow, and render-dispatch static audit completed as a baseline.
- Stage 4 — Native gameplay runtime: in progress.
  - Build 223: room/map data model and payload decoder.
  - Build 224: logical canvas, viewport, camera and logical surface.
  - Build 225: camera-aligned bounds, redraw strips and vertical-step correction.
  - Build 226: two main switch domains, shared tails and secondary overlay attribution.
  - Build 227: typed main-pass and overlay resolver; animation-table and composite graph integration.
- Stage 5 — Android integration/release: not started.

## Build 227 deliverables
- `LegacyRenderDispatchResolver.kt`
- `Build227RenderDispatchResolverChecks.kt`
- `tests/test_build227_render_dispatch_resolver.py`
- `docs/BUILD227_TYPED_RENDER_DISPATCH_RESOLVER.md`

## Next
- Build 228: deterministic per-cell render trace and golden synthetic fixtures.
- Build 229+: room scene rendering, actors/effects, HUD/menu, Android lifecycle/input/audio, device parity and release packaging.
