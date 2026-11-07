# Diamond Rush Native Android Port — Roadmap through Build 209

## Core target

- Native Android implementation, not a J2ME emulator wrapper.
- Original logical canvas: 320×240.
- Gameplay region target: 320×178 at y=31.
- Tile target: 24×24.
- Preserve original assets, logic, room content, animation, and audiovisual behavior.
- Keep source code suitable for GitHub.

## Milestones

| Build | Focus | Current status |
|---|---|---|
| 198 | Native legacy sprite decoder core | Historical source retained |
| 199–203 | Resource loader, bundle layout, sprite/group research | Historical source retained |
| 204 | Four-byte composite component model | Abstract model retained |
| 205 | Nested composite graph index | Abstract model retained |
| 206 | DF03 composite inventory | **Provisional; original table alignment under re-audit** |
| 207 | Composite object resolver | **Abstract resolver retained; original-JAR mapping not verified** |
| 208 | Additional pixel formats and full-tail investigation | Two decoder formats added; full parser interpretation superseded |
| 209 | Original parser bytecode boundary reconciliation | **Complete; 41/41 tests and Kotlin compile pass** |
| 210 | Field-consumer and renderer audit | Next |

## Build 209 findings

The original `f.a(byte[], int)` parser reads more positional tables than the earlier Build 206 parser accounted for. It also stores sprite payloads as interleaved length-plus-payload records. The old 1,129-group / 10,149-component totals and Build 207 full expansion counts are retained only as historical artifacts pending revalidation.

Build 209 does not produce PNGs or an APK. It deliberately avoids rasterizing data whose field mapping is not yet proven.

## Validation boundary

Build 209:
- 41/41 Python tests passed.
- Kotlin source compilation passed.
- 19/94 DF03 payloads passed the current structural trace.
- 3/16 direct literal-index sprite-bundle call sites passed the trace; their pixel format remains unsupported.
- Android Gradle, device runtime, rendering, visual parity, and playable APK remain unverified.

## Next technical gate

Build 210 must identify actual field consumers and renderer behavior before the composite graph is reconstructed. Do not use the historical Build 206/207 inventory as authoritative until this gate is passed.
