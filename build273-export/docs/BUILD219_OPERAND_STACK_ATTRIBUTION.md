# Build 219 — Operand-Stack Attribution and Cell/Object Binding

## Objective

Build 218 identified candidate map-plane stores by nearby field references. Build 219 tightens that evidence for the five priority methods (`aj()`, `as()`, `W()`, `aa()`, and `j()`) by requiring a visible static map-plane reference and a two-dimensional array-row load (`aaload`) in the seven-instruction window immediately before the store.

This is a conservative **direct-pattern attribution**, not a complete JVM abstract-interpretation engine. It does not claim full stack-state propagation across arbitrary branches, stack duplication, local aliases, or merged control-flow paths.

## 1. Scope and results

- Methods inspected: j, W, aa, aj, as
- Array stores inspected: **315**
- Stores matching the direct `getstatic map-plane → aaload row → ... → array store` pattern: **221**
- Stores whose stack provenance remains unresolved by this conservative window: **94**
- Direct-pattern attributions by plane:
  - `a:[[B`: 73
  - `b:[[B`: 32
  - `c:[[B`: 42
  - `a:[[I`: 17
  - `b:[[I`: 57

The per-store evidence is in `research/build219_store_operand_provenance.csv`; method totals are in `research/build219_method_operand_attribution_summary.csv`.

## 2. Attribution rule and limitations

A store is marked `DIRECT_GETSTATIC_AALOAD_WINDOW` only when its preceding seven decoded instruction lines contain both:
1. a `getstatic` reference to one of the five known map planes; and
2. an `aaload` row extraction.

This narrows the candidate set and gives an auditable bytecode context. It is not a full operand-stack proof in cases where multiple field references occur in the same window or where stack values were produced earlier and carried through locals. Accordingly:
- `candidate_field` is an evidence label, not a semantic assertion about the cell's role;
- `UNRESOLVED_STACK_PROVENANCE` is retained for all sites that do not satisfy the rule;
- no site is promoted to a gameplay action such as digging, falling, collecting, or collision handling solely from its opcode.

## 3. Priority method observations

`aj()` remains the largest hotspot. Its store density and references to all five map planes make it a high-value target for a later full stack-dataflow pass, but method name and store count do not reveal gameplay semantics.

`j()` is especially mixed: its outer state switch has cases 0–10, while nested switches and jumps occur inside several branches. The switch excerpt is stored in `research/build219_j_state_dispatch_excerpt.txt`. Build 219 deliberately does **not** assign stores to simple byte-offset intervals: nested control flow can cross those intervals, and linear proximity is not proof of reachability.

`W()`, `aa()`, and `as()` likewise contain both direct-pattern writes and unresolved stores. The unresolved sites remain in the CSV rather than being discarded.

## 4. Cell/object binding candidates

`research/build219_cell_object_binding_candidates.csv` lists each direct-pattern map-plane store as a candidate binding record. The stored value is preserved as `OPAQUE_RUNTIME_VALUE`, and the relation to Build 216's two dispatch domains (`bJ` and `bI`) is `NOT_PROVEN`.

This is intentional. Build 216 established two distinct render dispatch domains, but the current evidence does not yet prove that every runtime value written to a map plane is a direct tile-dispatch key, nor whether packed metadata, object state, and render identifiers share a numeric namespace.

## 5. Build 219 conclusions

- The candidate map-write inventory is narrower and more auditable for the five priority methods.
- The exact bytecode context for every examined store is retained.
- Unknown stack provenance and value semantics remain explicit.
- `j()` state-switch entry points are indexed without inventing exclusive state ranges.
- No unsupported semantic labels are assigned to map cells or object IDs.

## 6. Next milestone — Build 220

1. Implement basic-block and operand-stack dataflow over decoded bytecode, including branch merge handling.
2. Track array references through locals and `dup`/`dup2` operations.
3. Recover row/column operand expressions for the highest-confidence stores.
4. Split `j()` into reachable CFG blocks from each outer state-switch target, rather than linear offset ranges.
5. Trace values read from `a:[[I` into the two distinct Build 216 render dispatch domains.
6. Add representative mutation traces while preserving unknown values.

## Validation boundaries

- Static javap instruction-window extraction: performed for five methods.
- Direct-pattern attribution: 221/315 stores matched.
- Regression tests: run in the packaged workspace; results recorded in `BUILD219_TEST_RESULTS.txt`.
- Full JVM operand-stack dataflow: **not yet performed**.
- Kotlin compilation, Android Gradle, device runtime, visual parity, and APK: **not performed**.
