# Build 252 — Symbolic Producer-Slice Replay

## Objective

Begin the Build251 roadmap's focused symbolic bytecode execution by replaying the extracted linear producer slices at all 25 renderer callsites.

## Implementation

`research/build252_symbolic_producer_slice.py` parses the Build248 callsite excerpts and symbolically handles a bounded subset of JVM instructions:
- integer constants (`iconst`, `bipush`, `sipush`, `ldc`);
- local loads/stores (`aload`, `iload`, `astore`, `istore`);
- `getstatic`, `getfield`;
- `aaload`, `baload`, `iaload`;
- integer arithmetic and bitwise operations;
- `i2b`, `i2s`, `i2c`;
- `dup`, `swap`, `pop`.

Branches, nested invokes, and unsupported opcodes are explicit barriers. Stack underflow creates `UNKNOWN_ENTRY_STACK`; it is never silently filled with guessed values.

## Results

- 25 callsite slices parsed.
- 447 bytecode instructions recognized.
- 427 supported operations symbolically processed.
- 32 stack underflows recorded as unknown.
- Python regression suite: 245 passed, 4 existing Pillow deprecation warnings.
- Three new Build252 tests pass.

## Important limitation

This is a conservative *linear producer-slice replay*, not a full JVM symbolic interpreter or verifier. The excerpts are not complete method CFG paths and may begin with values already on the operand stack. The analysis therefore does not promote any receiver, composite group, or invocation argument to verified status. Branches and unsupported instructions break the linear trace.

## Next: Build253 — CFG-Aware Symbolic State Merge

1. Decode full instruction sequences for `i.D()V` rather than local excerpts only.
2. Reuse the Build220 CFG and Build221 instruction-entry states.
3. Implement predecessor worklist propagation for the supported opcode subset.
4. Add stack/local merge with explicit TOP/UNKNOWN values.
5. Model branch conditions without assuming a path unless its predicate is proven.
6. Validate invocation stack shape against Build250/251 descriptors.
7. Resolve only values whose provenance is unique across all incoming paths.

## Not performed

No Kotlin changes, Android Gradle build, device runtime, full-room rasterization, screenshot parity, or APK packaging.
