Build 249 — CFG Worklist State Join

Source: Build221 instruction-entry worklist states, joined to all 25 Build248 draw callsites.
Method alias: `as` (offset alignment verified against i.D()V bytecode callsite offsets).

Results:
- Draw callsites: 25
- Callsite offsets with matching worklist entry state: 4
- Callsite offsets without matching state: 21
- Composite groups resolved: 0

Important semantic boundary:
These are instruction-entry stack snapshots, not a complete reconstruction of the invocation operand stack. The prior abstract interpreter tracks TOP/constant/unknown values and has known unmodeled opcode limitations. A matching entry state alone does not prove receiver, argument ordering, or composite group.

This milestone joins existing CFG/worklist evidence without promoting uncertain values. Build250 must extend the interpreter for the exact opcode paths between each callsite's argument producers and invoke instruction, model dup/swap/category-2 values and merge semantics, and validate stack depth against JVM descriptors before resolving any argument.

## Reproduction

```bash
python research/build249_worklist_state_join.py
```

## Limitations

No new full JVM verifier is claimed. No render operation is promoted. Android Gradle/device runtime, full-room rasterization, visual parity, and APK packaging remain outstanding.
