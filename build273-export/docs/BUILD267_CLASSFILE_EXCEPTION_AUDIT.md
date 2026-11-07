# Build267 — Classfile Exception-Table Audit

## Result

The original `Code` attributes were parsed directly from `original.jar` for four methods used by the cross-class renderer audit.

| Class/method | Exception handlers |
|---|---:|
| `b.a(Graphics)` | 0 |
| `c.a(Graphics, byte[], int)` | 4 |
| `c.a(Graphics)` | 0 |
| `g.a(Graphics)` | 0 |

The four entries in `c.a(Graphics, byte[], int)` are:

| Protected interval (end exclusive) | Handler | Catch type |
|---|---:|---|
| `[912, 936)` | 939 | `java/lang/Exception` |
| `[945, 961)` | 964 | `java/lang/Exception` |
| `[1105, 1129)` | 1132 | `java/lang/Exception` |
| `[1138, 1154)` | 1157 | `java/lang/Exception` |

A conservative instruction-level expansion yields 116 potential exception edges. Every edge source is an instruction offset inside its protected interval. These are possible exceptional transfers, not a claim that every instruction throws. The edge list is kept separate from the normal-flow CFG until the interpreter can model handler-entry stack state (one exception reference) and merge locals correctly.

## Correction and scope

Build258's zero-entry result for `i.D()V` remains correct. It did not establish that every other renderer-related method has no handlers. Build267 demonstrates that `c.a(Graphics, byte[], int)` has four handlers.

Build267 does not yet integrate these edges into Build265's worklist. The standalone category-1/category-2 helpers from Build266 are also not yet integrated into that interpreter. The two unresolved local values at offset 873 remain unresolved.

No Kotlin compilation, Android Gradle build, device execution, complete room rendering, visual parity, or playable APK is claimed.
