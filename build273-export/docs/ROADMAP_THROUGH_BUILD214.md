# Diamond Rush Native Android Port — Roadmap through Build 214

## Core target
- Native Android implementation, not a J2ME emulator wrapper.
- Logical canvas: 320×240.
- Gameplay viewport: 320×178 at y=31 (now directly confirmed by original renderer bytecode).
- Tile target: 24×24.
- Preserve original assets, logic, room content, animations, and audiovisual behavior.
- GitHub-ready source and reproducible tests.

## Milestones
| Build | Focus | Status |
|---|---|---|
| 198–203 | Decoder core, resource loader, bundle research | Historical source retained |
| 204–205 | Composite record model and nested graph | Retained |
| 206 | Composite inventory | Revalidated by Build 210 |
| 207 | Composite resolver | Nested flag propagation corrected in Build 213 |
| 208 | Pixel formats and full-resource investigation | Historical parser superseded |
| 209 | Parser boundary trace | Superseded by Build 210 |
| 210 | Original class field-consumer audit | Complete; 94/94 resources |
| 211 | Sprite pixel decode validation | Complete; 1,372/1,372 |
| 212 | Composite rasterization | 300 no-transform groups rasterized |
| 213 | Draw-flag semantics and palette selection | Complete at reference level; Kotlin/Python parity 1,125/1,125 |
| 214 | Five-byte animation records, palette state, viewport geometry | **Complete at bytecode/reference level** |
| 215 | Gameplay scene layer reconstruction | Next |

## Build 214 verified totals
- 94 DF03 resources parsed.
- 37 resources contain animation frame tables.
- 188 animation sequences.
- 1,238 five-byte frame records.
- 1,235 valid composite group references.
- 3 explicit 0xFF no-group sentinel frames.
- No invalid sequence ranges or invalid non-sentinel group references.
- 69/69 Python regression tests pass.
- Original renderer confirms 320×240 canvas and 320×178 gameplay viewport at y=31.

## Validation boundary
Build 214 adds a bytecode-backed Kotlin animation table model and a Kotlin runtime audit harness, but Kotlin compilation was not run in this environment. No Android Gradle build, device rendering, original-game visual parity, or playable APK is claimed.

## Next gate
Build 215 reconstructs the gameplay-specific render passes and layer order, then assembles a deterministic 320×240 scene from original resource data.
