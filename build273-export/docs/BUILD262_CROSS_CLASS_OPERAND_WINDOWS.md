# Build262 — Cross-class renderer operand windows

## Scope

Build261 established eight actual renderer invoke instructions outside class `i`: three in `b`, four in `c`, and one in `g`. Build262 extracts a bounded bytecode context ending at each invocation and records the descriptor-level operand stack contract.

## Results

- 8 cross-class renderer invocation sites retained.
- 152 bytecode instructions included in the preceding context windows (up to 18 instructions before each invoke, plus the invoke itself).
- `f.a(Graphics;IIII)V`: receiver + Graphics + 4 integer arguments = 6 operand slots.
- `f.a(Graphics;IIIIII)V`: receiver + Graphics + 6 integer arguments = 8 operand slots.
- `f.a(Graphics;IIIIIII)V`: receiver + Graphics + 7 integer arguments = 9 operand slots.

The instruction windows are context excerpts, **not** reconstructed operand stacks. The values and provenance of the arguments remain undecoded. No CFG reachability result is asserted in this build; a preliminary generic CFG prototype exposed a control-flow parsing defect and was deliberately excluded rather than publishing unreliable reachability claims.

## Files

- `research/build262_cross_class_operand_windows.py`
- `research/build262_cross_class_callsite_summary.csv`
- `research/build262_cross_class_instruction_windows.csv`
- `tests/test_build262_cross_class_operand_windows.py`

## Reproduction

Run `python research/build262_cross_class_operand_windows.py`, then `pytest -q`.

No Kotlin compilation, Android Gradle build, device runtime, room rasterization, visual parity, or APK packaging is claimed.
