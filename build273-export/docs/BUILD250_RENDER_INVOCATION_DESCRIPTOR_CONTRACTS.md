# Build 250 — Render Invocation Descriptor Contracts

## Objective

Add descriptor-aware invocation contracts for the 25 original sprite-render callsites catalogued in Build245/248. This is a safe prerequisite for a focused JVM operand-stack interpreter: the invocation descriptor defines the exact parameter types and verifier stack-slot count expected at each call.

## Results

- 25 callsites catalogued.
- Two overloads distinguished:
  - `f.a(Graphics;IIIIII)V`: 7 parameters, 7 parameter slots, 8 slots including receiver.
  - `f.a(Graphics;IIIIIII)V`: 8 parameters, 8 parameter slots, 9 slots including receiver.
- All 25 entries retain the original receiver classification from Build248.
- Composite group remains UNKNOWN for every entry.

## Important boundary

This milestone validates descriptor contracts only. It does not claim that the producer slice has been interpreted into a complete runtime operand stack. In particular, no callsite argument value or composite group is promoted from constants/field references alone. The Build221 worklist snapshots remain partial abstract states, not a JVM verifier.

## Reproduction

```bash
python research/build250_render_invocation_descriptor_contracts.py
python -m pytest -q tests/test_build250_render_invocation_descriptor_contracts.py
```

## Next: Build251

Implement a focused instruction interpreter over the exact basic-block paths feeding the 25 invoke instructions. Track typed stack values, category-1/category-2 widths, local loads/stores, dup-family operations, arithmetic, array access, field access, and CFG merges. At each invoke, pop arguments in descriptor order and then receiver; reject underflow, type mismatch, or incompatible predecessor states. Only unique, fully supported values may become verified render arguments.

No full-room rasterization, Android Gradle build, device runtime, screenshot parity, or APK packaging is claimed.
