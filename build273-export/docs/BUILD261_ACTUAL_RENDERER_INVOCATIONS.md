# Build261 — Actual cross-class renderer invocation audit

## Scope

Build260 counted constant-pool references. Those references alone do not prove that an invocation instruction exists or is executed. Build261 disassembles the original `original.jar` classes `b`, `c`, `f`, `g`, and `i` with `javap -p -c`, then extracts actual invocation instructions targeting `f.a` with bytecode offsets, caller method, opcode, constant-pool index, and descriptor.

## Findings

- 175 actual `f.a` invocation instructions across the five inspected classes, including non-renderer overloads.
- 111 invocations use a `Graphics` descriptor and are classified as renderer-family calls.
- 103 of those are in class `i`; 8 are outside `i`.
- The 8 cross-class renderer invocations are in `b`, `c`, and `g`; none in `f`.
- Class `b`, method `a(Graphics)`: offsets 87 (7-int component), 113 (4-int leaf), 141 (6-int composite).
- Class `c`, method `a(Graphics, byte[], int)`: offset 873 (6-int composite).
- Class `c`, method `a(Graphics)`: offsets 280 (7-int component), 304 and 382 (6-int composite).
- Class `g`, static method `a(Graphics)`: offset 80 (6-int composite).

This is stronger evidence than Build260's constant-pool-only cross-reference count: these are actual invoke instructions in method Code attributes. It does not prove that all caller methods are reached at runtime, nor does it decode their complete operand values. The method and bytecode offset identify the next analysis targets.

## Renderer families

- `f.a(Graphics;IIII)V`: leaf 4-int overload.
- `f.a(Graphics;IIIIII)V`: composite 6-int overload.
- `f.a(Graphics;IIIIIII)V`: component 7-int overload.

## Reproduction and validation

Run `python research/build261_renderer_invocation_audit.py` from the project root. This uses the JDK `javap` disassembler and the original JAR. Then run `pytest -q`.

No Android Gradle build, device runtime, full room rendering, visual parity, or APK packaging is claimed by this milestone.
