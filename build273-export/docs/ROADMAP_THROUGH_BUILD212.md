# Diamond Rush Native Android Port — Roadmap through Build 212

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
| 207 | Composite object resolver | Revalidated by Build 210 |
| 208 | Additional pixel formats and full-resource investigation | Historical; parser superseded |
| 209 | Parser boundary trace | Superseded by Build 210 field audit |
| 210 | Original class field-consumer audit | Complete; 94/94 resources |
| 211 | Native sprite pixel decode validation | Complete; 1,372/1,372 sprites; Kotlin/Python hashes match |
| 212 | Composite sprite rasterization | **Complete; 300/300 exact Kotlin/Python RGBA matches** |
| 213 | Draw-flag semantics and palette selection | Next |

## Build 212 verified scope
- Total original composite groups: 1,129.
- 430 groups have fewer than three leaf commands.
- 399 groups require non-zero draw flags and are deferred.
- 300 groups are eligible for the conservative no-transform raster pass.
- 300 composites rendered in Kotlin and Python.
- All 300 RGBA outputs match byte-for-byte.
- 52/52 regression tests pass.
- Kotlin source compiles and runtime audit against the original JAR completes.

## Validation boundary
Build 212 proves that the current corrected parser, resolver, sprite decoder, and no-transform rasterizer are internally consistent across Kotlin and Python. It does not yet prove parity with the original J2ME renderer or Android output.

## Next gate
Build 213 must identify non-zero draw-flag semantics and palette selection from original bytecode and call sites. Do not guess transformations or assemble full screens before that evidence is available.
