# Diamond Rush Native Android Port — Roadmap through Build 258

- Builds 198–239: resource decoding, sprite/composite raster foundations, animation and viewport reconstruction.
- Builds 240–244: room structure and resource candidate census.
- Builds 245–252: renderer callsite inventory, callee semantics, caller producer provenance, descriptor contracts, conservative slice replay.
- Builds 253–256: exact renderer method recovery, corrected CFG extraction and structural integrity.
- Build 257: initial conservative worklist over 322 blocks: 247 reachable, 20 stack-shape conflicts, 13/25 callsite snapshots with sufficient raw stack depth; no argument tuples promoted.
- Build 258: parsed the original classfile Code attribute for `i.D()V`; exception table is empty. No exception CFG edges exist. The 75 unreachable blocks form a component rooted at offset 6171, immediately after `return` at 6170. Reachability remains 247/322 blocks and 13/25 renderer callsites.

## Next milestone — Build 259
Audit the disconnected bytecode region beginning at 6171: classify its control-flow structure, identify all renderer callsites within it, compare its instructions with the preceding method tail, and determine whether it is dead code under ordinary JVM entry semantics. Preserve the distinction between syntactically present callsites and entry-reachable callsites. Then resume operand-stack provenance only on reachable code, unless independent evidence establishes a valid alternate entry.
