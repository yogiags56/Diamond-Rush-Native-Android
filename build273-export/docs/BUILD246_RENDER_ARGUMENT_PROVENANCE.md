# Build 246 — Render Argument Producer Provenance

## Objective

Continue Build245's exact callsite catalog by inspecting bytecode immediately preceding each sprite draw call in `i.D()V`.

## Findings

The audit re-examines all 25 sprite draw callsites: 16 calls with seven integer arguments and 9 with six integer arguments. It scans the local producer slice for an explicit `getstatic a:[Lf;`, constant array index, `aaload` sequence. When present, it records the receiver as an explicit `f[index]` reference. When absent, it leaves the receiver unresolved.

The CSV stores an 18-instruction producer slice before each callsite. This preserves raw bytecode for further analysis and avoids guessing from a nearby but unrelated array load.

Composite group arguments remain unresolved for all callsites. A receiver slot is not equivalent to a composite group index; the argument stack still needs complete producer/dataflow analysis, including locals, branches, and merge points.

## Reproduction

```bash
python research/build246_render_argument_provenance.py
python -m pytest -q
```

## Validation

- Python: 232 passed, 4 existing Pillow deprecation warnings.
- All 54 production and test Kotlin source files compile together.
- Existing Kotlin regression runner through Build245 passes.

## Next: Build247 — Local-Variable and CFG Merge Provenance

Trace unresolved receiver locals and the integer arguments through stores/loads and CFG merge points. Use conservative provenance sets and preserve ambiguity when multiple predecessor paths disagree. Prioritize offsets 1058, 3985, 4285, 4394, 5736, 5913, 5954, 6314, 6427, 6814, 6854, 7673, 7993, and 8018. Do not infer a composite group solely from argument position until the callee `f.a(...)` bytecode is inspected and its signature semantics established.

## Limitations

No full room rasterization, Android Gradle build, device runtime, screenshot parity, or APK packaging is claimed.
