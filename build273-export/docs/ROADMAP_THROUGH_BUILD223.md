# Diamond Rush Native Android Port — Roadmap Through Build 223

## Project invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas: 320×240.
- Gameplay viewport: 320×178 at y=31.
- Tile target: 24×24.
- Preserve original resources, room content, animation data and audiovisual behavior.
- Preserve signed byte-extension behavior and packed values.
- Unknown map IDs and field semantics remain opaque until proven.

## Milestone status

| Stage | Builds | Status |
|---|---:|---|
| 1. Resource & Asset Reconstruction | 198–212 | Completed |
| 2. Graphics Engine Reconstruction | 213–214 | Main static audit completed |
| 3. Gameplay Engine Reconstruction | 215–222 | Static baseline consolidated; unresolved semantics carried forward |
| 4. Native Gameplay Runtime | 223–226 | In progress — Build 223 |
| 5. Android Integration & Release | 227–230 | Not started |

## Stage 4
- **223 — Native room/map model:** Kotlin five-plane data model, room payload decoder, validation.
- **224 — Logical canvas and render scaffolding:** 320×240 surface, viewport, camera and two separate render passes.
- **225 — Cell mutation and object-state interfaces:** only evidence-backed mutation contracts.
- **226 — Integrated gameplay loop:** deterministic fixtures and initial room lifecycle.

## Stage 5
- **227:** Android app shell, lifecycle, input surface and asset packaging.
- **228:** performance, audio, compatibility and memory lifecycle.
- **229:** visual/behavioral parity audit.
- **230:** Gradle build, release checks, install tests and APK.

## Validation boundaries
Python tests validate source contracts, not Kotlin runtime. Kotlin compile/test, Android Gradle, device runtime, visual parity and APK must be reported independently.
