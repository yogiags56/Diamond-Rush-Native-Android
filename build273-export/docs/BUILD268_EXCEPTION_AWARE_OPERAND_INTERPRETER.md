# Build268 — Exception-Aware Operand Interpreter

## Main result

Build268 corrects the switch-table termination bug in the Build265 interpreter and integrates conservative exception-handler transfers parsed from the original classfile in Build267.

- Renderer callsites: 8/8 reachable.
- Descriptor stack depth: 8/8 sufficient, with exact observed depth at each callsite.
- Unsupported opcode handlers encountered: 0 for the selected four methods and traversed paths.
- Stack-depth merge conflicts: 0.
- Exception handlers modeled: 4 in `c.a(Graphics, byte[], int)`.
- Conservative instruction-to-handler candidates in the full protected ranges: 116 (Build267 inventory).
- Reachable exceptional transfers propagated by the Build268 worklist: 69.
- Handler-entry stack: exactly one `EXCEPTION(java/lang/Exception)` abstract reference at offsets 939, 964, 1132, and 1157.

## Important correction: switch parsing

The earlier Build265 parser did not stop consuming switch labels at the closing brace of the `javap` switch table. That could corrupt the normal-flow CFG. Build268 now terminates switch-table collection at `}`. In `c.a(Graphics, byte[], int)`, the lookupswitch case `4` correctly reaches offset 729, and that path reaches renderer invocation offset 873.

## Previously unresolved operands at offset 873

The two arguments previously printed as `UNKNOWN` now carry explicit merge provenance:

- Renderer argument 4: `PHI#028`
- Renderer argument 5: `PHI#047`

Their alternatives are recorded in `research/build268_phi_provenance.csv`. They are symbolic conditional-merge values built from the arithmetic and field/byte-array producers in the case-4 path. This resolves the missing provenance, **not the concrete runtime integers**. The interpreter can now represent the merge without collapsing it to `UNKNOWN`; it does not prove a single numeric value. The PHI alternatives remain dependent on values read from the input byte array and instance field `THIS.b`.

The relevant bytecode computes the two values through the interpolation formula around offsets 799–836, stores them into local 0 and local 4, then pushes those locals at offsets 867 and 868 before invoking `f.a` at 873.

## Exception semantics and limitations

For each instruction offset within a protected interval, Build268 adds a conservative exceptional transfer to the declared handler. Handler-entry state preserves the source instruction's locals and replaces the operand stack with one exception reference. This is a conservative analysis approximation; it does not claim every protected instruction actually throws.

This remains an abstract interpreter, not a JVM verifier. It does not yet implement complete JVM verification types, exact exception behavior per opcode, all category-2 stack forms in the main transfer engine, or path predicates that would collapse PHI alternatives. The separate Build266 category-1/category-2 stack-contract helpers are not yet fully integrated into the interpreter.

## Android status

No Android Gradle build, Kotlin compilation, device execution, full room rendering, visual parity, or playable APK is claimed.
