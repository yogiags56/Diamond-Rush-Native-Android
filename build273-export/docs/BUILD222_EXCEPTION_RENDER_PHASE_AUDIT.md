# Build 222 — Exception Flow, Render Read Provenance, and Gameplay Phase Audit

## Objective

Build 222 consolidates the static gameplay reconstruction with exception-table inventory, renderer dispatch provenance, map-plane read inventory, and a conservative distinction between room initialization, a proven mutation primitive, rendering, and unclassified mixed methods.

## 1. Exception-flow inventory

- Exception table entries: **84**
- Methods containing handlers: **18**
- Handler targets matching decoded instruction offsets: **84**
- Handler target mismatches: **0**

Exact protected ranges and catch types are in `research/build222_exception_handler_edges.csv`. This validates handler offsets but does not yet propagate handler-entry stack states through Build 221's worklist engine.

## 2. Renderer dispatch provenance

Owning method: `D()V`.

| Pass | Selector field | Switch offset | Explicit cases |
|---|---|---:|---:|
| Pass 1 | `bJ:I` | 783 | 35 |
| Pass 2 | `bI:I` | 2239 | 50 |

Both case target sets resolve to decoded instruction offsets. Before the second switch, the method separately reads `b:[[I` into local 8. This is not proof that the lookup result selects the switch. The two selector fields remain distinct and case numbers remain unnamed.

Evidence:
- `research/build222_render_dispatch_provenance.txt`
- `research/build222_render_dispatch_cases.csv`
- `research/build222_map_read_sites_D.csv`

## 3. Initialization versus runtime mutation

The current evidence supports only these limited labels:

- **Room initialization:** Build 217's room loader reads a room header and three width×height payload planes; non-selected room payloads are skipped.
- **Mutation primitive:** `a(short, short, byte, int)` writes `a:[[B` and `b:[[I`; universal caller coverage is not established.
- **Render dispatch:** `D()V` contains independent switches selected by `bJ:I` and `bI:I`.
- **Unclassified mixed behavior:** `aj()`, `as()`, `W()`, `aa()`, and `j()` contain stores, but unresolved array provenance and incomplete opcode semantics prevent blanket classification as initialization or runtime gameplay mutation.

See `research/build222_initialization_runtime_evidence.csv`.

## 4. Stage 3 status

The planned static reconstruction sequence (Builds 215–222) now has a consolidated baseline: scene/camera traversal, two render passes, room data-plane loading, mutation-site inventory, CFG indexing, partial stack/local propagation, exception-table inventory, and explicit unresolved semantics.

This is **not** a claim that all gameplay behavior has been reverse engineered. Exception-aware operand-stack propagation, complete opcode semantics, and several producer-to-consumer chains remain unresolved and must be handled carefully during runtime implementation.

## 5. Next stage — Build 223

Begin the native gameplay runtime foundation:
1. Define typed Kotlin room/map structures for the five map planes, preserving signed/unsigned behavior supported by evidence.
2. Implement room payload decoding and bounds validation.
3. Implement a deterministic 320×240 logical frame surface and 320×178 gameplay viewport at y=31.
4. Keep `bJ` and `bI` dispatch domains separate.
5. Add golden tests from extracted room/resource fixtures.
6. Keep unknown IDs and values opaque; do not invent collision or object semantics.

## Validation boundaries

- Exception table extraction and handler-target validation: performed.
- Render dispatch table and target validation: performed.
- Python regression tests: see `BUILD222_TEST_RESULTS.txt`.
- Exception-aware full operand-stack dataflow: not completed.
- Kotlin compile, Android Gradle, device runtime, visual parity, APK: not performed.
