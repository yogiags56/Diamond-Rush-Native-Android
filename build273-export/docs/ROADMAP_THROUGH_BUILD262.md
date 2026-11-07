# Diamond Rush Native Android Port — Roadmap through Build262

## Fixed technical constraints

- Native Android implementation, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; target tile 24×24.
- Preserve original assets, room content, logic, animation, and audiovisual behavior.
- Keep unresolved renderer values opaque until bytecode/runtime evidence proves them.

## Renderer reverse-engineering progress

- Builds255–256: corrected `i.D()V` CFG; 3,811 instructions, 322 blocks, 564 edges.
- Build257: conservative worklist; 247 blocks reachable; 13/25 renderer callsites reached; values remain unknown.
- Build258: exception table for `i.D()V` has zero entries.
- Build259: 75 blocks / 926 instructions occur after the return at offset 6170; 12 renderer callsites lie in this disconnected region.
- Build260: cross-class constant-pool reference audit.
- Build261: actual `f.a` invocation instructions; eight renderer calls outside class `i`.
- Build262: descriptor contracts and bounded bytecode context for all eight cross-class renderer calls; no operand values decoded.

## Next milestone — Build263

Implement a verified method-local CFG and abstract operand-stack engine for the eight cross-class caller methods. Start with `b.a(Graphics)`, `c.a(Graphics)`, `c.a(Graphics,byte[],int)`, and `g.a(Graphics)`. Add opcode transfer tests, switch/branch edge tests, stack-depth merge audits, and per-callsite pre-invoke snapshots. Preserve UNKNOWN whenever provenance or control flow is ambiguous.

## Validation boundary

Python tests and bytecode audits do not establish Kotlin compilation, Android Gradle success, device runtime, full room rendering, visual parity, or a playable APK. Those remain separate milestones.
