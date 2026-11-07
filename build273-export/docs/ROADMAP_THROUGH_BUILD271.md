# Diamond Rush Native Android — Roadmap through Build271

## Completed foundations

- Resource/JAR extraction, DF03 parsing, sprite/palette decoding and Kotlin
  sprite/composite raster prototypes.
- Room archive and plane decoding, viewport/camera foundations, dispatch
  inventories, renderer overload semantics and bytecode callsite audits.
- Corrected main-renderer CFG, cross-class invocation discovery, symbolic
  operand provenance, exception-table audit and JVM integer arithmetic model.

## Build271

Expanded the existing W0 room0 candidate joins into 4,110 component-level
candidate draw rows across 90 cells and 21 resource/group pairs. The join keeps
all alternatives and explicitly marks selection and final transform as
unresolved.

## Next milestones

### Build272 — Candidate narrowing and selector semantics

- Trace the exact runtime selector inputs and branch predicates for W0 room0.
- Join raw room-plane values to the dispatch selector without assuming that a
  candidate resource is selected.
- Resolve the relationship between global resource slots, group indices, and
  sprite indices using callee bytecode and source data.
- Preserve ambiguous alternatives until a unique selection is proven.

### Build273 — Draw geometry and transform semantics

- Trace composite component offsets through the six-int and four-int renderer
  overloads.
- Resolve transform/control flags, clipping and final coordinate adjustments.
- Validate leaf sprite dimensions and palette/frame selection.

### Build274+ — Room raster proof

- Assemble a room draw sequence from proven selections only.
- Render the first room into a deterministic 320x240 logical surface.
- Compare against an original reference capture if available.

### Android application integration

After renderer and first-room behavior are sufficiently proven:

1. Create Android Gradle project and manifest.
2. Add Activity/game surface and lifecycle-safe game loop.
3. Integrate asset loader, room decoder and Kotlin renderer.
4. Add camera, controls, animation, HUD, menus, audio and gameplay systems.
5. Build APK, install on device, validate performance and visual parity.

## Honest status

Build271 is still reverse-engineering and renderer-planning work. It does not
represent a playable Android application. Android Gradle integration, device
runtime, full-room visual validation and APK delivery remain outstanding.
