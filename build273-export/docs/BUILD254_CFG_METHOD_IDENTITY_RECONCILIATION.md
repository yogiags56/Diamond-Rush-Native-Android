# Build 254 — CFG Method Identity Reconciliation

## Finding
The 25 renderer callsites in Build248 are labeled `i.D()V`. The CFG/basic-block artifacts in Build220 contain four method labels: `W, aa, aj, as, j`. There is no exact method-name identity match.

This explains why Build253's direct predecessor lookup produced no matches: it attempted to join unrelated method namespaces. Offset equality cannot repair a method identity mismatch.

## Audit
- Renderer callsites inspected: 25
- CFG methods available: 5
- Exact method identity matches: 0
- Callsite-to-basic-block assignments: 0 (deliberately withheld)
- Argument and composite-group values: UNKNOWN

## Required correction
Before Build255's worklist propagation, recover the actual disassembly/method identity mapping for `i.D()V`, then regenerate CFG and block boundaries from that exact method body. Do not reuse `as` CFG merely because prior artifacts treated it as a possible alias. Method aliasing must be supported by class-file method name + descriptor or a reproducible obfuscation mapping.

## Scope
No symbolic state propagation, Kotlin compilation, Android Gradle build, device runtime, room rasterization, visual parity, or APK packaging is claimed.
