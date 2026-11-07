# Build 220 — Basic-Block CFG and Operand-Stack Trace

## Objective

Build 219 narrowed map-plane store candidates using a local instruction-window rule. Build 220 adds an instruction-offset basic-block index, branch/switch edge extraction, conservative entry reachability, and a lightweight linear abstract-stack trace for five priority methods.

## Results

- Priority methods: `aj, as, W, aa, j`
- Basic blocks indexed: **1202**
- Branch/switch edges extracted: **906**
- Edge targets matching decoded instruction offsets: **906**
- Edge targets not matched: **0**
- Array stores traced in the local stack walk: **236**
- Stores whose linear stack trace retained a direct known map-plane row reference: **202**
- Stores with unresolved target provenance: **34**

Detailed outputs:
- `research/build220_basic_blocks.csv`
- `research/build220_cfg_edges.csv`
- `research/build220_block_reachability.csv`
- `research/build220_linear_stack_store_trace.csv`
- `research/build220_method_cfg_stack_summary.csv`

## Important analysis boundary

This is not yet a sound JVM verifier or full CFG dataflow solver. The current stack walk is intentionally linear and clears the abstract stack at control-transfer instructions. It does not merge incoming stack states at branch targets, and it only models a subset of JVM opcodes. Unsupported instructions can therefore interrupt provenance. A direct target label is evidence only when the local abstract stack still contains a `ROW(FIELD(...))` reference at the store.

The block reachability output is also approximate: it combines extracted explicit branch/switch edges with conservative lexical fallthrough. It is useful as an index for deeper work, not as proof that every marked block is executable.

## Interpretation

- The new stack trace improves traceability from an array-store instruction to its immediately available array-row provenance.
- Any `UNKNOWN` remains unknown; it is not classified as a local array or a gameplay map write without further proof.
- The two Build 216 render dispatch domains (`bJ`, `bI`) remain separate. Build 220 does not equate a stored map-plane value with either domain absent a proven read-to-dispatch dataflow chain.
- Coordinate arithmetic and object semantics are not yet reconstructed globally; local expressions are retained as abstract tokens where recognized.

## Next milestone — Build 221

1. Replace linear stack walking with worklist-based CFG dataflow and explicit stack-state merges.
2. Add opcode semantics for all instructions encountered in the five methods, including method calls and stack manipulation.
3. Resolve array references loaded into local variables.
4. Trace values read from `a:[[I` to dispatch consumers in `bJ` and `bI`.
5. Recover row/column expressions for representative mutations and distinguish initialization from runtime updates.
6. Add evidence-backed mutation categories only where source dataflow supports them.

## Validation boundaries

- Static instruction parsing and CFG indexing: performed.
- Lightweight linear abstract-stack trace: performed, deliberately incomplete.
- Python regression suite: see `BUILD220_TEST_RESULTS.txt`.
- Full operand-stack CFG dataflow: not completed.
- Kotlin compile, Android Gradle, device runtime, visual parity, APK: not performed.
