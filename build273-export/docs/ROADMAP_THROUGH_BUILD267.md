# Diamond Rush Native Android Port — Roadmap through Build267

## Completed foundations

- Original JAR extraction and DF03 resource/palette/sprite decoding.
- Sprite raster execution, composite graph and frame integration prototypes.
- Room archive/plane decoding and camera/viewport evidence.
- Renderer overload semantics, callsite contracts and producer-slice catalogues.
- Corrected `i.D()V` CFG and its unreachable bytecode region audit.
- Cross-class renderer call inventory and method-local reachability.
- CFG-aware symbolic operand prototype for eight cross-class callsites.
- Build266 local snapshots and standalone category-aware JVM stack-shape contracts.
- Build267 direct classfile parsing of exception tables for four selected renderer-caller methods; four handlers and 116 conservative potential exception edges identified.

## Current phase: renderer behavior reconstruction

1. Integrate category-1/category-2 values and stack manipulation into the abstract interpreter.
2. Integrate exception edges and handler-entry stack semantics for `c.a(Graphics, byte[], int)`.
3. Resolve local 0/local 4 and the two unknown operands at offset 873.
4. Join proven renderer arguments to resource/composite records.
5. Reconstruct ordered draw commands for a real room and compare against original assets/reference output.

## Android implementation phase

Existing Kotlin source prototypes under `android/src/main/kotlin/com/diamondrush/legacy` include sprite decoding, composite rasterization, room decoding, camera/viewport, render dispatch and command-planning components. These are engine/library foundations, not yet a complete Android application.

Before calling the project an Android app, add and validate a Gradle Android application structure, manifest, Activity/entry point, asset packaging and lifecycle integration. Then connect the proven room/render pipeline to a native Canvas/Surface renderer, game loop, touch/key input, camera, animation, HUD/menu/audio and gameplay state.

## Release validation phase

- Gradle assemble and APK artifact verification.
- Install and run on a physical Android device/emulator.
- Compare room screenshots and sprite placement against the original.
- Validate input, transitions, save/state behavior, audio and gameplay progression.
- Optimize and package a playable release.

## Fixed invariants

- Native Android implementation, not a J2ME emulator wrapper.
- Logical canvas 320x240.
- Gameplay viewport 320x178 at y=31.
- Target tile size 24x24.
- Preserve original assets, room data, animation, and audiovisual behavior.
- Unknown bytecode values remain UNKNOWN until supported by evidence.

## Honest progress assessment

The project has substantial reverse-engineering and Kotlin engine prototypes, but has not yet reached a verified Android application build. No Gradle wrapper/build files or AndroidManifest were present in the Build266 project snapshot. No device runtime, complete room rendering, visual parity, or playable APK is claimed.
