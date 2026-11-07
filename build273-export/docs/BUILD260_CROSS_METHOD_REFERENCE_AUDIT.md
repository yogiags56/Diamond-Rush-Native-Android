# Build260 — JAR Cross-Method Reference Audit

## Purpose
Build259 isolated 75 basic blocks (926 instructions) after the `return` at offset 6170 in `i.D()V`. Build260 broadens the inspection from that single method to every class file in the original JAR, looking for method-reference relationships that may explain where sprite-rendering overloads are used elsewhere.

## Method
A reproducible class-file parser reads constant-pool method/interface-method references and method metadata (name, descriptor, Code length, exception-handler count). It inventories every class and records references by caller class and target class/method/descriptor. This is a constant-pool reference audit, **not** a bytecode invocation-occurrence or call-graph proof: a constant-pool entry can be unused, and repeated instructions can share one entry.

## Results
- 12 class files parsed.
- 322 methods parsed; all 322 have Code attributes.
- 568 method-reference constant-pool entries.
- 234 references target class `i`.
- 23 constant-pool references target `f.a` (multiple overload descriptors).
- `f.a(Graphics;IIIIIII)V` and `f.a(Graphics;IIIIII)V` references occur in class `i` and also in other classes (`b`, `c`, `f`, `g`) in the JAR.
- `i.D()V` remains 8,029 bytes with zero exception handlers.

## Interpretation
This establishes that sprite-drawing overloads are referenced outside `i.D()V`; therefore the 12 unreachable callsites in that method are not the only places in the JAR that can refer to the renderer overload family. It does **not** establish that those other references render the same room layer, nor does it prove that the detached region is compiler residue. The next step is to decode actual invocation instructions and caller methods in `b`, `c`, `f`, and `g`, then compare their call semantics with the 25 sites in `i.D()`.

## Limitations
- Constant-pool references are not necessarily executed invocation instructions.
- No full whole-program call graph is claimed.
- No renderer argument tuples are promoted from unknown.
- No Android/Kotlin build, device execution, room rendering, visual parity, or APK packaging is claimed.
