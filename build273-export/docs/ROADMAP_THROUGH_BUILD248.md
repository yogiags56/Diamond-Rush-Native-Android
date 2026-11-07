# Diamond Rush Native Android — Roadmap through Build248

## Invariants
- Native Android port; no J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; target tile 24×24.
- Preserve original assets and bytecode-derived behavior; unknown values stay opaque.

## Milestones
- Builds198–212: resource/sprite/composite decoding foundations.
- Build213: MIDP transform, draw flag, and palette audit.
- Builds214–231: animation, viewport, scene/camera, dispatch, room decoding and tracing.
- Builds232–235: static/dynamic resource origin and binding.
- Builds236–239: concrete draw operations, palette pixels, raster execution, composite-frame integration.
- Builds240–244: original room cell manifest, dispatch/resource evidence, candidate joins.
- Build245: 25 sprite draw callsites catalogued.
- Build246: 13 explicit `f[]` receivers identified; 12 unresolved.
- Build247: callee semantics established for 7-, 6-, and 4-int overloads.
- Build248: producer evidence catalogued for all 25 callers, without overstating partial stack slices.

## Build248 validation
- Three focused Python tests pass; complete regression count recorded in `BUILD248_PYTEST_OUTPUT.txt`.
- The source remains a research/build milestone, not a playable APK.

## Next: Build249 — CFG Worklist Stack Provenance
1. Construct exact instruction CFG for `i.D()V`.
2. Propagate typed operand stack and local-variable provenance per instruction.
3. Merge predecessor states conservatively; preserve ambiguous values.
4. Resolve receiver and integer argument values at each `invokevirtual f.a`.
5. Add branch-specific fixtures, including signed byte semantics.
6. Promote only unique proven receiver/group/coordinate values into render commands.

## Outstanding
Full-room rasterization, Android Gradle/device runtime, visual parity, and APK packaging remain outstanding.
