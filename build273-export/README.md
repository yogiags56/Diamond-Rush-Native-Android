# Diamond Rush — Native Android Port (Build 273)

A research-driven native Android porting project for the classic J2ME edition of **Diamond Rush**. The repository preserves the reverse-engineering tools, Kotlin rendering prototypes, Python analysis scripts, test suite, CSV evidence, and milestone documentation through Build 273.

> **Current state:** reverse engineering and renderer research. This repository is **not yet a complete Android Studio/Gradle application**, does not currently produce a playable APK, and has not passed on-device validation.

## Current checkpoint: Build 273

Build 273 traces the room selector dataflow for all 90 cells in W0 room0:

- Six raw `bJ` selector values: `3, 4, 5, 6, 7, 8` (15 cells each).
- Selector 4 conditionally resolves through `aJ=20` to `f[43]`.
- Selector 7 resolves through `aJ=4` to `f[56]`, with a separate guarded direct `f[56]` draw.
- Selector 8 resolves through `aJ=23` to `f[45]`.
- Selectors 3 and 6 resolve through the helper to `-1`; selector 5 does not assign a new `aJ`.
- Resource bundle identities and runtime predicate values remain unresolved.

See [`docs/BUILD273_EXACT_SELECTOR_DATAFLOW_TRACE.md`](docs/BUILD273_EXACT_SELECTOR_DATAFLOW_TRACE.md) and [`docs/ROADMAP_THROUGH_BUILD273.md`](docs/ROADMAP_THROUGH_BUILD273.md).

## Repository layout

- `android/src/main/kotlin/` — Kotlin decoding, scene, camera, sprite, and renderer prototypes.
- `research/` — Python reverse-engineering scripts and structured CSV/text evidence.
- `tests/` — automated regression and evidence tests.
- `docs/` — build reports, technical audits, and roadmap history.
- `tools/` — supporting utilities.

## Run the available tests

Python 3.10+ is recommended.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The public source repository intentionally does not redistribute the original commercial game JAR, extracted game assets, compiled class files, or rendered sprite previews. Tests that require those local research inputs are automatically skipped when the inputs are absent. The remaining source/evidence tests run normally. To reproduce the full local research suite, provide a legally obtained original JAR and locally generated research fixtures/previews; do not commit or redistribute those files unless you have the necessary rights.

## Porting principles

1. Native Android implementation; not a J2ME emulator wrapper.
2. Preserve original game behavior, assets, timing, and rendering semantics where evidence establishes them.
3. Treat unknown fields and resource mappings as opaque until proven.
4. Keep the logical canvas at 320×240, gameplay viewport at 320×178 with top offset 31, and 24×24 tile target unless later evidence requires a correction.
5. Do not claim runtime selection, visual parity, or playability without reproducible validation.

## Copyright and license

This repository contains project-authored source code, analysis, and documentation. The original game and its proprietary assets remain the property of their respective rights holders and are not included. No license is granted to redistribute the original game. A project license for the authored code has not yet been selected; until one is added, do not assume the source is licensed for reuse.
