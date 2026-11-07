# Build265 — CFG-aware abstract operand-stack interpreter

## Scope

Build265 adds a conservative symbolic operand-stack worklist to the four method bodies containing the eight cross-class Graphics renderer invocations:

- `b.a(Graphics)` — offsets 87, 113, 141
- `c.a(Graphics)` — offsets 280, 304, 382
- `c.a(Graphics, byte[], int)` — offset 873
- `g.a(Graphics)` — offset 80

The interpreter uses method-local normal-flow CFG edges and merges symbolic locals/stack values at joins. It checks the stack depth against each invoke descriptor before extracting receiver and arguments.

## Results

- 8/8 callsites are reachable.
- 8/8 have sufficient abstract stack depth for their invoke descriptors.
- 7/8 callsites have symbolic expressions for every operand.
- The `c` method callsite at offset 873 retains two `UNKNOWN` values; these are not guessed.
- 881 instruction-entry states are emitted.
- No unsupported opcodes or stack-depth merge conflicts were encountered in the selected method bodies.

Representative symbolic expressions include:

- `b` callsites: receiver `THIS.a`, Graphics `PARAM1`, and integer fields `THIS.d`, `THIS.e`, `THIS.a`, `THIS.b`, `THIS.c`.
- `c` offset 280: dynamic resource expression `STATIC.a[THIS.f]` and coordinate expression `(CALL[f.a](...), ... )`.
- `c` offset 382: coordinates derived from `THIS.c + 90` and `THIS.d - 6`.
- `g` offset 80: tile-scale terms containing multiplication by 24 and a static coordinate field.

These are symbolic source expressions, not concrete runtime values. The renderer receiver and its arguments are ordered according to the operand stack at the invoke instruction.

## Important limitations

This prototype is not a JVM verifier. It does not provide complete category-2 value semantics, exception-handler edges, full field/array provenance, or interprocedural callee effects. `CALL[...]` remains opaque. Stack/local merge uses a conservative `UNKNOWN` value when incoming expressions differ. The absence of unsupported opcodes applies only to the four selected methods and the current opcode transfer table.

No Android compilation, device runtime, complete room rendering, visual parity, or playable APK is claimed.
