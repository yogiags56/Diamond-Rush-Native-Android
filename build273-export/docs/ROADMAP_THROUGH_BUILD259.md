# Diamond Rush Native Android Port — Roadmap through Build259

## Architecture and invariants
- Native Android port; not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; target tile 24×24.
- Preserve original assets, room content, animation, audiovisual behavior, and source semantics.
- Keep unproven runtime fields and argument tuples opaque.

## Completed technical foundations
- Builds198–212: original resource parsing, sprite decoding, composite graphs and rasterization.
- Build213: MIDP transform/draw flags and palette audit; Python/Kotlin parity checks.
- Builds214–231: animation, viewport, scene/camera, room data, dispatch, mutation and stack-flow research.
- Builds233–244: global sprite slot attribution, dynamic resource tracing, composite/palette binding and room-cell candidate joins.
- Builds245–251: renderer callsite provenance, argument producer slices, callee semantics and descriptor stack contracts.
- Builds252–255: method identity reconciliation and initial renderer CFG reconstruction.
- Build256: corrected switch-aware instruction extraction and CFG; 3,811 instructions, 322 blocks, 564 edges, 247 entry-reachable blocks.
- Build257: conservative initial worklist; 13 reachable callsite snapshots with adequate descriptor stack depth, but no argument tuples or composite groups promoted.
- Build258: direct classfile exception-table audit; `i.D()V` has zero exception-table entries, so no exception CFG edges.
- Build259: detached-region audit; 75 blocks / 926 instructions form one component beginning at 6171 after `return` at 6170; no edge from reachable code enters it; 12 renderer callsites are inside it.

## Current evidence boundary
The 13 renderer callsites in entry-reachable code remain the only callsites eligible for normal execution reconstruction in `i.D()V`. Even for those, stack-depth snapshots do not establish concrete argument values, ordering, receiver identity beyond separately proven cases, or composite group identity. The 12 callsites in the detached region are structurally present but unreachable from method entry under the current CFG.

## Next milestone: Build260
1. Audit the classfile and whole-JAR for other methods that invoke or duplicate the detached tail's behavior.
2. Compare detached-region field/method references and renderer call patterns with reachable code and other methods.
3. Check whether a separate method contains an equivalent sequence or whether offsets 6171–8028 are an orphaned compiler/obfuscator residue.
4. Continue operand-stack analysis only on entry-reachable callsites; implement explicit verifier-like type/width tracking and merge diagnostics before attempting argument recovery.
5. Preserve unresolved values as UNKNOWN; do not promote inferred arguments based only on matching stack depth.

## Validation status
Build259 Python suite: 264 passed, 4 Pillow deprecation warnings. No claim of Kotlin/Android build, device runtime, full room rendering, visual parity, or APK.
