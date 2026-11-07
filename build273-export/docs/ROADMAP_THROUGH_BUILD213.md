# Diamond Rush Native Android Port — Roadmap through Build 213

## Core target
- Native Android implementation, not a J2ME emulator wrapper.
- Logical canvas: 320×240.
- Gameplay region target: 320×178 at y=31.
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
| 213 | Draw-flag semantics and palette selection | **Complete at reference level** |
| 214 | Original renderer and screen assembly | Next |

## Build 213 verified totals
- 1,129 original composite groups.
- 10,258 leaf draw commands.
- Transform distribution: 7,820 none; 1,642 mirror+180; 439 mirror; 357 rotate180.
- 528 groups contain at least one transformed leaf.
- 1,125 non-empty groups rasterized.
- 10 multi-palette resources; 110 palette rows across 94 resources.
- 58/58 Python regression tests pass; Kotlin source compiles and runtime audit matches Python RGBA output for all 1,125 non-empty groups.

## Validation boundary
Build 213's original bytecode audit, Python reference rasterization, Kotlin compilation, and Kotlin runtime parity audit are complete. No Android rendering, original-game visual parity, or playable APK is claimed.

## Next gate
Build 214 maps palette state and the five-byte renderer records to actual game-level call sites, then begins 320×240 scene assembly.
