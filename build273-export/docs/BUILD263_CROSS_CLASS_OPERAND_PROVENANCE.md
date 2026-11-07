# Build263 — Cross-class renderer operand provenance

## Scope

Build262 supplied bounded instruction windows for eight real renderer invokes outside class `i`. Build263 maps the invocation operand stack in descriptor order by reading the actual producer instruction sequences in the corresponding `javap -c` method bodies.

## Results

- 8 callsites; 64 operand-stack entries (receiver + Graphics + integer arguments).
- 59 operands have directly identified symbolic sources (`PROVEN`).
- 5 operands are arithmetic expressions built from identified sources (`DERIVED`).
- 0 operands are marked `UNKNOWN` within these eight callsites.
- **No runtime values are decoded or evaluated.** Field values, array contents, method return values, and loop variables remain symbolic.

The five derived expressions are:

- `c.a(Graphics)` offset 280: `this.b % a[this.f].a(0)`.
- `c.a(Graphics)` offset 382: `this.c + 90` and `this.d - 6`.
- `g.a(Graphics)` offset 80: `local1 * 24` and `(local2 - 1) * 24 + static b`.

Other operands are direct arguments, local variables, fields, array entries, or literal zero. Evidence offsets are retained per operand in the CSV.

## Important interpretation limits

`PROVEN` means the symbolic producer expression and its position in the invoke sequence are supported by the bytecode instruction sequence. It does **not** mean the runtime numeric value is known. `DERIVED` means the expression is bytecode-derived, not numerically evaluated. This build does not execute the game, resolve field contents, prove that every enclosing method is reached in a live game session, or validate visual output.

Build262's warning remains relevant: the instruction windows themselves were excerpts, not stack simulations. Build263 therefore uses the exact producer sequences around each invoke and records the expression list in JVM invocation order. The next stage should independently validate these expressions with a CFG-aware abstract interpreter and stack-merge checks before using them in renderer reconstruction.

## Files

- `research/build263_cross_class_operand_provenance.py`
- `research/build263_cross_class_operand_provenance.csv`
- `research/build263_operand_provenance_summary.csv`
- `tests/test_build263_cross_class_operand_provenance.py`

## Validation

Run `python research/build263_cross_class_operand_provenance.py` and `pytest -q`.

No Kotlin compilation, Android Gradle build, device runtime, room rasterization, visual parity, or APK packaging is claimed.
