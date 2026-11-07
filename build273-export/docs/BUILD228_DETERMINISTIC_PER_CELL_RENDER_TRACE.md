# Build 228 — Deterministic Per-Cell Render Trace

## Objective

Build 228 adds a deterministic trace record for an explicitly supplied room cell. It combines the already audited Build 227 typed dispatch resolver with caller-supplied map/screen coordinates, while keeping the two main dispatch passes and the secondary overlay pass independent.

## Implementation

- `LegacyCellTraceInput` carries row/column, map coordinates, screen coordinates, and the typed raw-plane sample.
- `LegacyCellRenderTrace` retains all raw plane values and resolved decisions without assigning gameplay names to numeric IDs.
- `LegacyPerCellRenderTrace.traceCell()` resolves the first `bJ` pass, second `bI` pass, secondary overlay selection, and supplemental resource conditions through Build 227's resolver.
- `canonicalLine()` and `canonicalCsv()` provide locale-independent deterministic serialization for golden fixtures and later scene-diff tooling.
- Framework-free Kotlin checks cover a known explicit `bJ` case alongside `bI == -1` skip and stable CSV header serialization.
- Python source-contract tests protect the trace schema, pass separation, and coordinate provenance.

## Important boundaries

This is a per-cell trace API, not yet a full room renderer. It intentionally does not invent row/column traversal, camera coordinate conversion, viewport clipping, or the relationship between map axes and screen axes. The caller supplies those coordinates. It does not rasterize real room assets or prove pixel parity. Animation-backed overlay IDs require the corresponding decoded animation table; direct-draw overlay routes remain represented as direct arguments by the existing resolver.

## Validation

- Python regression suite: **157 passed, 4 warnings**. The four warnings are existing Pillow `Image.getdata()` deprecations.
- Kotlin: all 18 production source files plus `Build228PerCellTraceChecks.kt` compiled successfully with `kotlinc`; framework-free checks executed successfully.
- The compile uncovered and Build 228 repaired one unmatched closing brace at the end of the inherited Build 227 resolver source. This was a syntax repair only; resolver semantics were unchanged.
- No Android Gradle build, device runtime, visual parity, or APK is claimed.

## Next

Build 229 should bind the proven room-plane model and the audited viewport/camera iteration to this trace API, producing ordered scene-level draw commands from real decoded room records. Any uncertain axis mapping or render ordering must remain explicit until supported by bytecode evidence.
