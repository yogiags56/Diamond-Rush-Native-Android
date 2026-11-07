# Diamond Rush Native Android — Roadmap through Build250

## Invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; target tile 24×24.
- Preserve original assets and bytecode-derived behavior.
- Keep unproven fields and arguments opaque.

## Completed foundation
Builds198–212 resource/sprite/composite foundations; Build213 transform/palette audit; Builds214–231 animation, viewport, room, CFG and render-dispatch reconstruction; Builds232–235 resource origin and binding; Build236 concrete leaf operations; Build237 palette-aware pixel binding; Build238 raster execution; Build239 resolved frame/composite integration; Build240 room manifest; Build241–244 dynamic resource and room-cell candidate attribution; Build245–248 render callsite/callee and caller evidence; Build249 worklist-state join; Build250 descriptor-aware invocation contracts.

## Build250 results
- 25 sprite-render callsites.
- Two overload contracts: 8 stack slots including receiver for Graphics + six ints; 9 slots including receiver for Graphics + seven ints.
- Descriptor contract only; runtime operand stack not yet proven.
- Composite group remains UNKNOWN.

## Next: Build251 — Focused JVM Operand-Stack Interpreter
1. Decode exact instructions/basic blocks feeding each invoke.
2. Track typed operand-stack values and JVM slot widths.
3. Model local loads/stores, dup/swap/pop, arithmetic, array/field operations and supported invokes.
4. Merge predecessor states conservatively.
5. Validate receiver/arguments against invocation descriptors.
6. Preserve UNKNOWN on unsupported instructions or ambiguous merges.

## Outstanding
Full-room rasterization, Android Gradle/device runtime, visual parity, and APK packaging remain outstanding.
