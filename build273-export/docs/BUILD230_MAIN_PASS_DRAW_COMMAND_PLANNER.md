# Build 230 — Main-Pass Branch-to-Draw-Command Planner

## Objective

Turn the per-cell resolver output into a deterministic ordered command stream while preserving the original bytecode branch targets and refusing to guess the meaning of unresolved cases.

## Implementation

- Added `LegacyCellDrawCommandPlanner.kt` and typed records for command kind and pass order.
- Each in-bounds cell emits the first main-pass decision, then the second main-pass decision, followed by any secondary-overlay request and supplemental resource requests.
- Main switch targets other than the two known shared-tail offsets remain `OPAQUE_BRANCH` records with their original numeric target.
- Targets 1995 and 5676 are labelled `SHARED_COMPOSITE_OR_CACHE_TAIL` only as a control-flow category; no assumption is made about which image/object is ultimately drawn.
- `SKIP_CELL` remains an explicit command record rather than being silently discarded.
- Animated overlay selections and direct draw requests are kept distinct. Supplemental resources remain independent commands.
- `LegacyRoomSceneTrace` now exposes `canonicalDrawCommandCsv()` separately from its existing per-cell CSV, preserving compatibility with prior trace output.

## Validation

- Python regression suite: **164 passed, 4 warnings**.
- All production Kotlin sources compiled with `kotlinc` alongside the Build 228–230 framework-free checks.
- Build 228, Build 229, and Build 230 Kotlin checks executed: `BUILD230_KOTLIN_CHECKS_PASSED`.
- Tests cover pass ordering, opaque branch target retention, shared-tail categorization, explicit skip records, and stable scene command CSV output.
- Four Python warnings remain existing Pillow `Image.getdata()` deprecations.

## Evidence boundary

This is a command-planning and trace layer, not yet a renderer. Main switch branch targets are not mapped to concrete sprite draw calls unless their semantics are independently proven. The planner does not rasterize room pixels and does not claim visual parity.

Not performed: Android Gradle build, APK packaging, Android-device runtime, real-room scene rasterization, or visual parity.

## Next

Build 231 should load a genuinely decoded room payload and its associated real sprite resources, then produce a reproducible scene trace. Main-pass branch bodies should be inspected to map only proven operations into typed draw commands. Unknown paths must remain opaque.
