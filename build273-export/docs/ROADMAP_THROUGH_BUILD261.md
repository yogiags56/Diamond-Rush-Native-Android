# Diamond Rush Native Android Port — Roadmap through Build261

## Current milestone

Build261 confirms actual cross-class renderer invocation instructions in `b`, `c`, and `g`, beyond the 25 callsites previously isolated in `i.D()V`. Eight additional Graphics renderer calls were extracted with method identity and bytecode offsets. This does not establish runtime reachability or complete argument provenance.

## Next: Build262

1. Recover the complete pre-invoke operand stack for the eight cross-class calls.
2. Reconstruct CFG and reachable blocks for their caller methods.
3. Trace receiver and integer argument producers, retaining `UNKNOWN` where dataflow cannot prove values.
4. Compare the `b`/`c`/`g` call patterns against `f`'s overload semantics established in Build247.
5. Join proven argument tuples to composite/resource records only when all required operands are supported by bytecode evidence.

## Stable foundations

- Native Android implementation; no J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; target tile 24×24.
- Original JAR resources and DF03 sprite/composite parsing remain authoritative.
- Build256 corrected CFG is authoritative: 3,811 instructions, 322 blocks, 564 normal-flow edges.
- Build258 found no exception handlers in `i.D()V`.
- Build259 isolated the 75-block unreachable region after `return` at offset 6170.
- Build260's constant-pool audit is reference evidence only; Build261 adds actual invoke-instruction evidence.

## Validation boundaries

Python research/tests are not equivalent to Kotlin compilation, Android Gradle build, device runtime, visual parity, or a playable APK. Report each separately.
