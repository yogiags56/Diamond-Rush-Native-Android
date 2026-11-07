# Build 258 — Exception Table and CFG Reachability Audit

## Result
The original `i.class` method `i.D()V` has a Code attribute with `code_length=8029`, `max_stack=9`, `max_locals=14`, and **zero exception-table entries**. Therefore there are no JVM exception-handler CFG edges to add for this method.

The corrected Build256 normal-flow CFG remains unchanged: 322 blocks, 247 reachable from method entry, and 75 unreachable. The 25 renderer callsites remain 13 reachable and 12 unreachable. This is not evidence of missing exception edges.

## Structural explanation discovered
The unreachable region has a single component root at bytecode offset **6171**. The preceding instruction at **6170** is `return`; the next instruction at 6171 begins a new disconnected sequence (`aload_0`, followed by `invokespecial P()V`). The 75 unreachable blocks are connected downstream from this root. The CFG has no normal-flow predecessor to 6171. This is consistent with dead/unreachable bytecode following an unconditional return, rather than an exception-handler island.

Do not force the 12 unreachable renderer callsites into the entry-reachable worklist. The next analysis should establish whether the bytecode region is intentionally dead code, a decompiler/compiler artifact, or has any non-standard entry semantics outside ordinary JVM method invocation. Standard JVM execution of `D()V` begins at offset 0; no exception table supplies another entry.

## Limits
- This build parses the classfile Code attribute and exception table directly; it does not implement a JVM verifier.
- No new exception edges were added because none exist.
- Build257's conservative stack transfer and merge limitations remain: no verifier-grade type lattice, no exception-flow states, incomplete category-2 support, and unknown argument values.
- The 13 reachable callsite stack-depth snapshots do not prove argument values/order or composite group identity.
- No Kotlin compile, Android Gradle build, device runtime, room rasterization, visual parity, or APK is claimed.

## Reproduction
Run `python research/build258_exception_cfg_audit.py`, then `pytest -q`.

## Artifacts
- `research/build258_exception_table.csv`
- `research/build258_exception_cfg_edges.csv`
- `research/build258_block_reachability_audit.csv`
- `research/build258_callsite_reachability_delta.csv`
- `research/build258_summary.csv`
- `research/build258_exception_cfg_audit.py`
- `tests/test_build258_exception_cfg_audit.py`
