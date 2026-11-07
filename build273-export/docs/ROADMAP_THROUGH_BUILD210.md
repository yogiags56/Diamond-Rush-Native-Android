# Diamond Rush Native Android Port — Roadmap through Build 210

## Core target
- Native Android implementation, not a J2ME emulator wrapper.
- Original logical canvas: 320×240.
- Gameplay region target: 320×178 at y=31.
- Tile target: 24×24.
- Preserve original assets, logic, room content, animation, and audiovisual behavior.
- GitHub-ready source code and reproducible tests.

## Milestones
| Build | Focus | Status |
|---|---|---|
| 198 | Native legacy sprite decoder core | Historical source retained |
| 199–203 | Resource loader, bundle layout, sprite/group research | Historical source retained |
| 204 | Four-byte composite component model | Abstract model retained |
| 205 | Nested composite graph index | Retained |
| 206 | DF03 composite inventory | Composite prefix counts validated by Build 210; old full parser deprecated |
| 207 | Composite object resolver | Revalidated against corrected original resources |
| 208 | Additional pixel formats and full-tail investigation | Historical investigation; full parser superseded |
| 209 | Parser bytecode boundary reconciliation | Superseded: field widths in its trace were incorrect |
| 210 | Original class field-consumer audit | **Complete** |
| 211 | Native sprite pixel decode validation | Next |

## Build 210 verified totals
- 94/94 DF03 resources parsed.
- 1,372 sprite records.
- 1,129 composite groups.
- 10,149 four-byte component records.
- 139,268 pixel payload bytes.
- Pixel formats: 0x1600 (1,300), 0x27F1 (71), 0x0400 (1).
- 11 nested edges, no invalid targets, no bad component ranges, no cycles.
- Build 207 reference resolver: 10,258 leaf commands across all root groups; 120 leaf commands came through nested paths.

## Build 209 correction
Build 209's 19/94 trace-complete result was a parser reconstruction error. The original class allocates `h:[B` at four bytes per record, then reads the group descriptor table and a four-byte-per-group `a:[B` table. The old trace interpreted those widths incorrectly. Build 210 corrects the layout and parses all 94 resources.

The interleaved `[length][payload]` sprite stream was correctly recognized in Build 209 and remains confirmed.

## Validation boundary
Build 210: 44/44 Python tests pass; Kotlin sources compile; Kotlin parser runtime audit passes against the original JAR. No Android Gradle build, device rendering, visual parity, or playable APK yet.

## Next gate
Build 211 validates every extracted sprite's decoded pixel indices and palette mapping, then compares Kotlin and reference decoder outputs before composite raster previews are generated.
