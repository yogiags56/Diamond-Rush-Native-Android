# Diamond Rush Native Android — Roadmap through Build 216

## Project invariants
- Native Android implementation; no J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31.
- Tile unit 24×24.
- Preserve original assets, room content, animation records, flags, and unknown packed fields.
- No semantic labels without bytecode/runtime evidence.

## Completed milestones
- Build 213: MIDP transform semantics and palette selection.
- Build 214: five-byte animation records, palette-state audit, and viewport geometry.
- Build 215: gameplay dispatch, camera setup, incremental map redraw, two visible-cell passes, and HUD boundary.
- Build 216: explicit tile/cell dispatch domains and branch/resource attribution inventory.

## Build 216 evidence
- First visible-cell dispatch: field `bJ`, switch offset 783, values 3–37 (35 cases).
- Second visible-cell dispatch: field `bI`, switch offset 2239, values 0–49 (50 cases).
- Integer map plane carries packed metadata in addition to the low-byte dispatch value.
- CSV attribution is a conservative navigation aid, not a complete CFG.

## Next: Build 217
Trace map construction and mutation sites. Establish where each map plane is populated and which runtime systems write representative IDs. Build a CFG-aware attribution graph and retain unknown fields as opaque.

## Validation policy
A passing Python audit is not a Kotlin build, Android Gradle build, device test, visual parity result, or APK. Report each independently.
