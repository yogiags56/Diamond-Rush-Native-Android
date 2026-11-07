# Diamond Rush Native Android Port — Roadmap through Build264

## Project invariants

- Native Android implementation; not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; target tile 24×24.
- Preserve original assets, room content, animation, game logic, and audiovisual behavior.
- Unknown bytecode semantics and runtime values remain explicitly unknown until supported by evidence.

## Renderer reconstruction progress

- Builds237–239: corrected DF03 resource parser, sprite decoding, transforms, and composite raster foundations.
- Builds242–247: dynamic resource attribution, composite inventory, and renderer overload semantics.
- Builds248–251: producer slices, renderer descriptors, and callsite contracts; runtime stack values not yet proven.
- Builds255–257: corrected `i.D()V` instruction extraction, CFG, conservative worklist, and abstract stack snapshots.
- Builds258–259: verified zero exception-table entries for `i.D()V`; isolated 75 normal-flow-unreachable blocks after offset 6170.
- Build260: cross-class method-reference audit.
- Build261: eight actual cross-class Graphics renderer invocations identified in `b`, `c`, and `g`.
- Build262: callsite instruction windows collected.
- Build263: 64 symbolic operand records across eight callsites; 59 source expressions marked PROVEN and five expressions DERIVED. These are symbolic source expressions, not decoded runtime numeric values.
- Build264: method-local CFGs built for the eight cross-class callsites; all eight are structurally reachable from their respective method entries.

## Build264 quantitative results

- 8/8 callsites structurally reachable.
- 4 selected caller methods.
- 847 basic-block intervals.
- 862 instruction-level CFG edges.
- No operand-value interpreter or runtime-value decoding added.

## Next: Build265

1. Add conservative abstract operand-stack propagation over the method-local CFGs.
2. Model only verified opcode stack effects and preserve `UNKNOWN` for unsupported operations.
3. Implement explicit merge records for stack-height and symbolic-value disagreements.
4. At each renderer invocation, compare inferred stack shape with the descriptor contract.
5. Never promote a symbolic expression to a concrete runtime value without proven input state.

## Validation boundaries

Python tests validate the analysis scripts and datasets. They do not substitute for Kotlin compilation, Android Gradle builds, device runtime, room rendering, visual parity, or a playable APK. Those milestones remain open.
