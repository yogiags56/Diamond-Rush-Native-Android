# Build269 — Case-4 interpolation operand audit

## Purpose

Build269 narrows the two merged symbolic operands at renderer callsite `c.a(Graphics, byte[], int)` offset 873 to the exact producer slice in the original classfile. It does not replace the Build268 abstract interpreter or claim concrete runtime values.

## Bytecode evidence

The `lookupswitch` case `4` enters at offset 729. The producer slice reads signed-short values through `i.a(byte[], int)` followed by `i2s`, computes a clamped interpolation factor, stores two interpolated values, and loads them immediately before `f.a(Graphics;IIIIII)V`.

Definitions:

- `v2 = S16(i.a(data, index + 2))`
- `v4 = S16(i.a(data, index + 4))`
- `v6 = S16(i.a(data, index + 6))`
- `v6b = S16(i.a(data, index + 6))` (a separate bytecode read into a separate local)
- `v14 = S16(i.a(data, index + 14))`
- `m = min(this.b, v14)`, as implemented by `if_icmple` at 792 and the conditional assignment at 795–797.

Renderer integer argument sourced from local 0 (stored at 817):

`S16((v6 * m + v2 * (v14 - m)) / v14)`

Renderer integer argument sourced from local 4 (stored at 836):

`S16((v6b * m + v4 * (v14 - m)) / v14)`

The JVM performs the multiply/add/subtract/divide operations as integer operations; `i2s` then narrows the result to signed 16-bit. Division-by-zero behavior is not abstracted away: if `v14` is zero, the original bytecode can throw `ArithmeticException` and the method's exception behavior must be considered.

## Important distinctions

- The two formulas are bytecode-proven expressions, not concrete numeric values.
- `data`, `index`, and `this.b` are runtime inputs/state; their actual values are not known from this static slice.
- The two reads at `index + 6` are separate bytecode producers, even though they have the same source expression.
- The renderer call at offset 873 consumes `local 0` and `local 4` at offsets 867 and 868 respectively.
- Build268 PHI alternatives are preserved as historical path-insensitive merge evidence. Build269's case-4 slice provides a branch-specific, direct bytecode explanation for the operands without claiming all PHI alternatives have been eliminated globally.

## Validation

`research/build269_case4_instruction_trace.csv` records 94 verified instruction offsets/opcodes from `javap` on the original JAR. `research/build269_case4_operand_formulas.csv` records the two formulas and their confidence classification.

This remains reverse-engineering research. No Android Gradle build, APK, device runtime, full-room rendering, or visual parity is claimed.
