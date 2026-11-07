# Diamond Rush Native Android Port — Roadmap Through Build 225

## Invariants
- Native Android implementation, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at canvas y=31.
- Tile size 24×24.
- Preserve original room data planes and signed values.
- Keep `bJ` and `bI` as separate raw dispatch domains.
- Do not invent cell semantics, draw ordering, or asset mappings.

## Milestones
- Stage 1 — Resource and asset reconstruction: baseline completed.
- Stage 2 — Graphics engine reconstruction: static audit baseline completed.
- Stage 3 — Gameplay engine reconstruction: static baseline completed through room data, mutation analysis, CFG/dataflow, and render dispatch.
- Stage 4 — Native gameplay runtime: in progress.
  - Build 223: room/map storage model and payload decoder.
  - Build 224: logical canvas, viewport, camera decomposition, visible-cell scaffold and logical surface.
  - Build 225: camera aligned bounds, initial and incremental redraw-strip planning, vertical camera step, corrected map-coordinate orientation.
- Stage 5 — Android integration and release: not started.

## Build 225 verified static facts
- `D()` computes camera tile and sub-tile components using 24-pixel units.
- `cE/cF/cG/cH` cache the prior aligned redraw bounds.
- Initial render uses one full aligned map-region helper call.
- X and Y boundary crossings are handled independently as exposed strips.
- The room's first map dimension is X/column; the second is Y/row.
- Camera viewport uses logical 320×178 extents.

## Next
- Build 226: two-pass visible-cell branch/resource/animation attribution.
- Then: evidence-backed scene fixtures, actor/effect updates, HUD/menu reconstruction, Android input/lifecycle/audio, device parity and release.
