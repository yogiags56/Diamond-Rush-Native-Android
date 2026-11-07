# Diamond Rush Native Android Port — Roadmap through Build 246

## Fixed invariants
- Native Android port, not J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; tile target 24×24.
- Preserve original assets and bytecode-derived behavior.
- Unproven arguments/fields remain opaque.

## Completed milestones
- Builds198–212: resource parsing, sprite decoding, composites and raster foundations.
- Build213: MIDP transform and palette audit.
- Builds214–231: animation, viewport, room/camera, dispatch and archive reconstruction.
- Builds232–235: resource origins, static/dynamic bindings and composite attribution.
- Build236: concrete leaf draw operations.
- Build237: palette-bound pixels and Kotlin parser correction.
- Build238: sprite raster execution.
- Build239: resolved frame/composite raster pipeline.
- Build240: original room cell manifest.
- Build241: CFG-derived dynamic resource candidates.
- Build242: dynamic resource origin trace.
- Build243: dynamic sprite/composite attribution.
- Build244: room cell to dynamic composite candidate join.
- Build245: exact sprite draw callsite catalog.
- Build246: bytecode producer slices and conservative receiver-slot provenance.

## Build246 validation
- Python: 232 passed, 4 existing Pillow deprecation warnings.
- All 54 Kotlin production/test sources compile.
- Existing Kotlin regression runner through Build245 passes.
- 25 sprite callsites retained; composite group arguments remain unresolved.

## Next: Build247
Trace receiver and integer arguments through local variables and CFG merges. Inspect callee `f.a(...)` overload implementations to establish what the six- and seven-integer arguments mean. Only promote resource/group/transform semantics when supported by caller and callee evidence.

## Outstanding
Full-room rasterization, Android Gradle/device runtime, visual parity, and APK packaging remain outstanding.
