# Diamond Rush Native Android — Build269

Build269 adds a bytecode-anchored, case-4 interpolation audit for renderer callsite `c.a(Graphics, byte[], int)` at offset 873.

Key outputs:
- `research/build269_case4_interpolation_audit.py`
- `research/build269_case4_instruction_trace.csv`
- `research/build269_case4_operand_formulas.csv`
- `tests/test_build269_case4_interpolation_audit.py`
- `docs/BUILD269_CASE4_INTERPOLATION_AUDIT.md`
- `docs/ROADMAP_THROUGH_BUILD269.md`

The audit verifies 94 instruction offsets/opcodes from the original JAR. It reconstructs the two values loaded from local 0 and local 4 as signed-short interpolation expressions. Their concrete runtime integers remain unknown because they depend on the input byte array, index, and instance field `this.b`.

This is still reverse-engineering/engine research, not a completed Android application. No Gradle build, APK, device runtime, full-room rendering, or visual parity is claimed.
