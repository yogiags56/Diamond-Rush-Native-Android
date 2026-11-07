# Diamond Rush Native Android Port — Roadmap through Build 211

## Core target
- Native Android implementation, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay region target 320×178 at y=31; tile target 24×24.
- Preserve original assets, logic, room content, animation, and audiovisual behavior.
- GitHub-ready source and reproducible tests.

## Milestones
| Build | Focus | Status |
|---|---|---|
| 198–203 | Decoder core, resource loader, bundle research | Historical source retained |
| 204–205 | Composite record model and nested graph | Retained |
| 206 | Composite inventory | Revalidated by Build 210 |
| 207 | Composite object resolver | Revalidated by Build 210 |
| 208 | Pixel formats and full-resource investigation | Historical; parser superseded |
| 209 | Parser boundary trace | Superseded by Build 210 |
| 210 | Original class field-consumer audit | Complete; 94/94 resources |
| 211 | Native sprite pixel decode validation | **Complete** |
| 212 | Composite sprite rasterization | Next |

## Build 211 verified totals
- 94/94 DF03 resources; 1,372/1,372 sprites decoded.
- Formats: 0x1600 (1300), 0x27F1 (71), 0x0400 (1).
- No truncation, trailing payload, dimension, or palette-index errors.
- Python and Kotlin decoded index planes match by SHA-256 for every sprite.
- Four reference atlases generated.

## Validation boundary
Build 211 compiles and executes Kotlin source against the original JAR and passes the full regression suite. It does not yet implement Android rendering, composite rasterization, visual parity, or a playable APK.
