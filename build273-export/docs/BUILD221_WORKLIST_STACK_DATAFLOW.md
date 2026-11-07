# Build 221 — Worklist-Based Stack Dataflow and Array Alias Tracking

## Objective

Build 220 provided a basic-block index and a linear stack trace. Build 221 advances to an instruction-level worklist analysis: each reachable instruction receives an abstract operand-stack and local-variable state; branch successors receive merged states; array references can be carried through locals; and repeated loop visits are bounded by a finite abstract-value merge.

## Results

Five priority methods analyzed: `aj()`, `as()`, `W()`, `aa()`, and instance `j()`.

- Instruction-entry states recorded: **6107**
- Distinct array-store sites with a worklist state: **148**
- Sites retaining a known map-plane row reference: **39**
- Sites with unresolved array target: **109**
- Unmodeled-opcode observations: **1984**

Outputs:
- `research/build221_worklist_stack_store_attribution.csv`
- `research/build221_instruction_entry_stack_states.csv`
- `research/build221_method_dataflow_summary.csv`
- `research/build221_unmodeled_opcode_sites.csv`
- `research/build221_dispatch_value_link_audit.csv`

## Method

The analyzer:
1. Parses bytecode offsets and explicit branch/switch destinations.
2. Builds instruction-level successor lists with fallthrough edges where applicable.
3. Seeds the first instruction with an empty operand stack and empty local map.
4. Propagates abstract values using a worklist.
5. Merges stack and local values at join points using bounded symbolic unions.
6. Tracks `getstatic` map-plane references through `aaload`, local stores/loads, and common stack operations.
7. Records array-store receiver, index, and value expressions at each store site.

## Limitations and safety rails

This remains a partial abstract interpreter, not a JVM verifier:
- Exception-handler edges are not modeled.
- `dup2_x1` / `dup2_x2` and other uncommon stack forms are conservatively invalidated.
- Some opcodes or constant-pool descriptors may be unmodeled; they are listed explicitly.
- Merging different stack heights yields `TOP` placeholders and does not claim verifier correctness.
- The parser follows explicit switch targets but relies on decoded instruction offsets; malformed or omitted javap metadata would limit coverage.
- A target plane is labeled only when the merged array reference still directly identifies a known `ROW(FIELD(...))`.
- It does not yet prove whether the stored value is a tile ID, object ID, flag, animation state, or other semantic value.

The dispatch link audit intentionally leaves the relation to Build 216 domains `bJ` and `bI` as `NOT_PROVEN_IN_THIS_MILESTONE`. Separate render switches are not conflated.

## Interpretation

This milestone establishes a reusable worklist framework and carries aliases through local variables and branch joins where modeled. It is a meaningful step beyond Build 220's linear stack walk, but unresolved sites remain unresolved. Any `TOP` or `UNKNOWN` must be revisited with additional opcode semantics or targeted bytecode inspection.

## Next milestone — Build 222

1. Add exception table parsing and handler-entry stack states.
2. Complete stack semantics for every opcode actually encountered.
3. Improve field/method descriptor parsing and category-2 values.
4. Trace map-plane reads to render dispatch consumers across the complete relevant methods, not just the five mutation hotspots.
5. Separate room-load initialization, per-frame mutation, and object update pathways using reachable CFG evidence.
6. Produce an evidence-backed mutation taxonomy only after read/write chains are complete.

## Validation boundaries

- Static worklist dataflow: performed with documented opcode and CFG limitations.
- Regression tests: see `BUILD221_TEST_RESULTS.txt`.
- Kotlin compilation, Android Gradle, device runtime, visual parity, and APK: not performed.
