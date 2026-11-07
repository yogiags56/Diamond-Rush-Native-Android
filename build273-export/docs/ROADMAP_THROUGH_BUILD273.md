# Diamond Rush Native Android — Roadmap through Build273

## Completed foundations

- JAR/resource extraction, DF03 parsing, sprite/palette decoding, and Kotlin
  sprite/composite raster prototypes.
- Room archive and plane decoding, viewport/camera foundations, dispatch
  inventories, renderer overload semantics, and bytecode callsite audits.
- Corrected main-renderer CFG, cross-class invocation discovery, symbolic
  operand provenance, exception-table audit, and JVM integer arithmetic model.
- Build271: 4,110 component-level candidate draw rows across 90 room cells and
  21 resource/group pairs. Resource/group selection and final transforms remain
  explicitly unresolved.
- Build272: selector/candidate ambiguity audit over 1,530 source candidate
  rows; six raw `bJ` selector values and 90 cells. The candidate union was
  explicitly not treated as runtime selection.
- Build273: exact bytecode dataflow for all 90 W0 room0 cells. Selector 4 maps
  through `aJ=20` to `f[43]` conditionally; selector 7 maps `aJ=4` to `f[56]`
  and has a separate guarded direct `f[56]` draw; selector 8 maps `aJ=23` to
  `f[45]`. Selectors 3 and 6 resolve through the helper to -1; selector 5's
  case does not assign a new `aJ`. The Build272 `f[27]`/`f[30]` candidate union
  is not supported as the selected slot for these six room0 selector cases.
  Resource bundle identity and runtime predicate values remain unresolved.

## Next milestones

### Build273 — Exact selector dataflow (completed)

- Traced the low-byte `bJ` value from the room integer plane through the main
  switch and the `a(int)` resource-index helper.
- Resolved `f[43]`, `f[45]`, and `f[56]` paths where the bytecode proves them.
- Preserved runtime predicates and resource bundle identities as unresolved.

### Build274 — Composite group and renderer argument binding

- Trace selected group/frame values into the composite expansion overload.
- Resolve nested-group versus leaf-sprite semantics and preserve draw ordering.
- Join palette/frame and resource selection only when proven.

### Build275 — Geometry and transform semantics

- Resolve transform/control flags, clipping, anchor conventions, and final
  coordinate adjustments through renderer bytecode.
- Validate sprite dimensions and camera-space to screen-space conversion.

### Build276+ — First-room raster proof

- Assemble draw commands from proven selections only.
- Render the first room into a deterministic 320x240 logical surface, with the
  gameplay viewport 320x178 at y=31 and 24x24 tile target.
- Compare against an original reference capture if available.

### Android application integration

After renderer and first-room behavior are sufficiently proven:

1. Create Android Gradle project, wrapper, manifest, and application entry point.
2. Add Activity/game surface and lifecycle-safe game loop.
3. Integrate asset loader, room decoder, and Kotlin renderer.
4. Add camera, controls, animation, HUD, menus, audio, and gameplay systems.
5. Build APK, install on device, validate performance and visual parity.

## Honest status

Build273 remains static reverse-engineering and evidence-audit work. It resolves
some selector-to-array-index paths but does not identify all resource bundle
contents, execute runtime predicates, render a complete room, compile Android,
validate device behavior or visual parity, or produce a playable APK.
