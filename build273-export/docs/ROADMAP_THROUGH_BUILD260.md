# Diamond Rush Native Android Port — Roadmap through Build260

## Fixed target
Native Android implementation (not a J2ME emulator wrapper), logical canvas 320×240, gameplay viewport 320×178 at y=31, 24×24 target tile. Preserve original assets, game logic, animation, room data, and audiovisual behavior. Unknown semantics remain explicitly unknown until bytecode/runtime evidence proves them.

## Progress
- Builds198–212: resource parsing, sprite decoding, composite graph and raster foundations.
- Build213: MIDP transform/draw-flag/palette audit and Python/Kotlin parity checks.
- Builds214–231: animation, viewport/camera, room data and bytecode dispatch reconstruction.
- Builds233–243: static/dynamic resource attribution, DF03 parsing, sprite and composite raster audits.
- Builds244–254: room candidate analysis, renderer callsites, descriptors, symbolic producer slices and CFG merge groundwork.
- Build255: initial renderer CFG extraction (later corrected).
- Build256: corrected switch-aware extraction; 3,811 instructions, 322 blocks, 564 edges, 10 switches.
- Build257: conservative abstract worklist; 247 reachable blocks, 13 reachable renderer callsites; no argument tuples promoted.
- Build258: exact exception table parse; zero exception handlers in `i.D()V`.
- Build259: 75 unreachable blocks / 926 instructions form one detached component beginning at 6171, immediately after `return` at 6170; 12 renderer callsites in that component.
- Build260: all 12 original JAR class files and 322 methods inventoried; cross-class constant-pool method references show renderer overloads are referenced in classes `b`, `c`, `f`, and `g` as well as `i`.

## Current evidence boundary
Build260's constant-pool reference inventory is not a whole-program call graph. It does not prove the detached region's purpose or identify executable invocation occurrences. No renderer argument tuple or composite group has been newly confirmed. No complete room renderer, Android runtime, visual parity, or APK has been validated.

## Next milestone: Build261
Decode actual invocation bytecodes in classes `b`, `c`, `f`, and `g`; map each invoke instruction to caller method, offset, target overload, and control-flow context. Prioritize the two renderer overloads with six/seven integer parameters. Compare their call semantics with `i.D()` callsites without assuming that all callers draw the same layer.
