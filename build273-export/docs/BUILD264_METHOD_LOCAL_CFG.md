# Build264 — Method-local CFG and renderer callsite reachability

## Scope

Build264 constructs normal-flow, instruction-level control-flow graphs for the eight cross-class renderer callsites identified in Build261/263. Input is the original `original.jar`; instruction offsets and opcode spellings are obtained with `javap -p -c`. The graph builder records conditional branch targets, unconditional branches, switch targets, and ordinary fallthrough. Return/throw instructions terminate fallthrough.

This is a structural CFG audit only. It is not a JVM verifier, does not model exception edges, does not interpret operand values, and does not prove that every runtime path is feasible under application state. Switch and branch edges are conservative structural possibilities.

## Results

- 8 of 8 cross-class renderer callsites are reachable from their respective method entry under the extracted normal-flow CFG.
- `b.a(Graphics)`: callsites 87, 113, 141 are reachable.
- `c.a(Graphics)`: callsites 280, 304, 382 are reachable.
- `c.a(Graphics, byte[], int)`: callsite 873 is reachable through the switch-controlled method body.
- `g.a(Graphics)`: callsite 80 is reachable through the loop and conditional join.
- 847 basic-block intervals and 862 instruction-level CFG edges were emitted across the four selected methods.

The `g` method is a useful validation case: the conditional at offset 24 has a branch edge to 42 and a fallthrough edge to 27; the conditional at 50 branches to 83 and falls through to 53. Both routes can reach the renderer invocation at 80 through the join at 63. The `c` byte-array method's switch edges are retained, and the renderer call at 873 is reachable through its switch-selected body.

## Important interpretation

Reachability means there is a structural normal-flow path in the decoded method CFG. It does not mean the path is taken during a particular game state. Build263 symbolic operands remain symbolic expressions; Build264 does not upgrade them to runtime numeric values. No room rasterization, Kotlin compilation, Android Gradle build, device runtime, visual parity, or APK packaging is claimed.

## Reproduction

```bash
python research/build264_method_local_cfg.py
pytest -q
```

Outputs:

- `research/build264_callsite_reachability.csv`
- `research/build264_method_basic_blocks.csv`
- `research/build264_method_cfg_edges.csv`
- `tests/test_build264_method_local_cfg.py`
