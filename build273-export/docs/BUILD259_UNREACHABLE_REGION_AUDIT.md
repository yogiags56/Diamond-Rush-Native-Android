# Build259 — Unreachable Renderer Region Audit

## Scope
This build investigates the 75 blocks not reachable from entry in `i.D()V` after the Build256 corrected normal-flow CFG and Build258 direct classfile exception-table audit. It does not modify or force the CFG to make detached code reachable.

## Findings
- The unreachable blocks form exactly **one** undirected connected component under the existing CFG edges.
- The component starts at bytecode offset **6171** and extends through the final block beginning at **8021**.
- The preceding instruction at **6170** is an unconditional JVM `return`; offset 6171 begins with `aload_0`, followed at 6172 by `invokespecial P()V`.
- There are **926 instructions** in the detached component, **75 basic blocks**, and **12 of the 25 renderer callsites**.
- There are **zero CFG edges from an entry-reachable block into the detached component**.
- The remaining 13 renderer callsites are in entry-reachable blocks.

## Interpretation
Under ordinary JVM method invocation semantics, execution begins at bytecode offset zero. With no exception-table entries (Build258), no reachable normal-flow edge into the detached component, and an unconditional `return` immediately before it, the region is **unreachable from the method entry in the extracted CFG**. Its contents resemble a substantial alternate rendering/update tail, but this audit cannot establish why the compiler or obfuscator retained it. Possible explanations such as compiler artifact, obfuscator transformation residue, or intentionally retained but disconnected code remain hypotheses.

The 12 renderer callsites inside this region must not be used as evidence of executed room-rendering behavior unless another legitimate entry mechanism is found (for example, another method invokes a separate equivalent routine; that would not make these offsets reachable within `D()V`).

## Validation
- 25 renderer callsites partitioned: 13 entry-reachable, 12 detached.
- No reachable-to-detached CFG edge.
- Python test suite: **264 passed, 4 warnings** (existing Pillow deprecations).
- No Kotlin compile, Android Gradle build, device runtime, room rasterization, visual parity, or APK packaging is claimed.

## Reproduction
`python research/build259_unreachable_region_audit.py`
`pytest -q`

## Generated evidence
- `research/build259_unreachable_components.csv`
- `research/build259_cross_region_edges.csv`
- `research/build259_callsite_region_audit.csv`
- `research/build259_region_boundary_instructions.csv`
- `research/build259_summary.csv`
- `research/build259_unreachable_region_audit.py`
- `tests/test_build259_unreachable_region_audit.py`
