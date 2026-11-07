# Diamond Rush Native Android — Complete Roadmap through Build 217

## Project identity and invariants

- Project: **Diamond Rush Native Android port**.
- Target: native Android implementation, not a J2ME emulator wrapper.
- Logical canvas: 320×240.
- Gameplay viewport: 320×178, origin y=31.
- Tile unit: 24×24.
- Preserve original game resources, room content, sprite records, transforms, packed metadata, timing, and behavior.
- Keep unknown field meanings opaque until original bytecode or runtime evidence proves them.
- All code and documentation should remain GitHub-ready.

## Where we are now

<badge>Stage 3 — Gameplay Engine Reconstruction</badge>

The project has moved beyond basic asset extraction and image decoding. The graphics/resource foundations are substantially audited, and the current work is reconstructing how the original game loads room data, dispatches map cells, updates objects, and draws the gameplay scene.

The next major transition is from **static reverse-engineering** to a **deterministic native gameplay scene and runtime**. We are not there yet.

## Milestone history

| Milestone | Completed work | Current status |
|---|---|---|
| Builds 198–209 | Resource discovery, DF03 parsing, payload decoding, composite graph tracing, parser and bytecode boundary audits | Foundation completed; some later audits supersede early assumptions |
| Build 210 | Original class field consumer audit across 94 resources | Completed |
| Build 211 | Sprite pixel decoding validation, 1,372/1,372 | Completed |
| Build 212 | Composite sprite rasterization baseline; 300 no-transform groups | Completed |
| Build 213 | MIDP transform semantics, recursive draw flags, palette selection, Kotlin/Python parity for 1,125 groups | Completed |
| Build 214 | Five-byte animation frame records, palette-state audit, viewport geometry | Completed |
| Build 215 | Gameplay render helper audit, camera/map traversal, two visible-cell passes, HUD boundary | Completed |
| Build 216 | First and second cell dispatch tables; 35 cases (`bJ`) and 50 cases (`bI`), packed metadata and resource references | Completed |
| Build 217 | Room binary plane loading, dimensions, three serialized cell planes, two runtime byte overlays, central setter | Completed |

### Key technical facts already established

**Graphics and assets**
- Original DF03 resources are inventoried and decoded.
- Composite sprite graph and leaf commands are reconstructed.
- MIDP transform values are corrected and tested.
- Palette selection and animation-record layouts are audited.
- Animation frame records are five bytes each; duration units are not yet converted to milliseconds.
- Kotlin source exists for portions of the resource/renderer foundation, but the latest build has not been validated with a Kotlin compiler or Android Gradle.

**Canvas and rendering**
- Logical canvas is 320×240.
- Original gameplay clip is 320×178 at y=31.
- Top and bottom strips occupy y=0..30 and y=209..239.
- Renderer uses 24×24 tile units.
- Two separate cell dispatch domains exist; they must not be collapsed into one generic tile switch.
- The known high bits in the integer map plane are consumed as packed rendering metadata.

**Room data**
- Selected room resource is loaded from an `InputStream`.
- Four-byte header contains two unsigned little-endian 16-bit dimensions.
- Selected room reads three width×height byte payloads:
  1. `a:[[B`;
  2. `b:[[I`, populated from signed byte values;
  3. `a:[[I`, populated from signed byte values.
- `b:[[B` and `c:[[B` are separately allocated runtime byte overlays.
- Non-selected room records are skipped using width×height×3 bytes after the dimension header.
- Central setter `a(short, short, byte, int)` updates `a:[[B` and `b:[[I` together.
- Many gameplay methods also write map arrays directly; their event semantics are not yet fully attributed.

## Remaining roadmap

### Stage 3 — Gameplay Engine Reconstruction (current)

**Build 218 — Map Mutation Control-Flow Graph**
- Trace every direct write to the five map planes.
- Identify common write helpers and bypass paths.
- Trace representative state transitions and cell mutations.
- Decode the selected-room post-load scan.
- Preserve unknown bits and values.

**Build 219 — Cell Semantics and Object Binding**
- Connect proven cell values to original composite resources and animation sequences.
- Identify which cell entries represent static map content versus dynamic entities.
- Trace actor/entity creation and map occupancy changes.
- Assign semantic names only when supported.

**Build 220 — Camera, Occlusion, and Layer Ordering**
- Complete camera offset and exposed-strip behavior.
- Resolve first-pass and second-pass draw order.
- Attribute effects, actors, map overlays, and occlusion.
- Validate bounds against the 320×178 viewport.

**Build 221 — Deterministic Original Scene Fixture**
- Select one known room and reconstruct its initial planes.
- Build a reproducible scene snapshot at 320×240.
- Compare expected object bounds and render ordering.
- Produce reference previews from original resources.

**Build 222 — Gameplay Animation and Timing Integration**
- Connect five-byte animation records to actual object consumers.
- Resolve frame progression, pause/loop behavior, and timing units.
- Integrate draw flags, offsets, and palette state.

### Stage 4 — Native Gameplay Runtime

**Build 223 — Native Map and Entity Model**
- Kotlin data structures for the proven map planes.
- Separate static map, dynamic state, entities, and overlay planes.
- Preserve signed values and packed metadata.

**Build 224 — Native Renderer Integration**
- Integrate original sprite/composite renderer with map traversal.
- Reproduce viewport clipping, camera, layers, and animation.
- Build deterministic screenshot fixtures.

**Build 225 — Input and Gameplay State**
- Reconstruct keypad/action mapping and state transitions.
- Integrate movement, collisions, interactions, and object updates.
- Compare behavior with original game evidence.

**Build 226 — Room/Level Progression**
- Load multiple room records.
- Validate transitions, reset state, and persistent progression.
- Test representative levels and edge cases.

### Stage 5 — Android Integration and Verification

**Build 227 — Android Application Shell**
- Android lifecycle, display scaling, orientation, and input surface.
- Asset packaging and memory management.

**Build 228 — Runtime Performance and Compatibility**
- Frame pacing, audio, input latency, and device compatibility.
- Resource lifecycle and low-memory behavior.

**Build 229 — Full Gameplay Parity Audit**
- Compare original and native gameplay scenes and state transitions.
- Resolve remaining visual/behavioral differences.

**Build 230 — Release Candidate**
- Gradle build, signed/debug APK as appropriate, install and device tests.
- Final source/archive and reproducible build instructions.

## What is not finished yet

- Complete semantic catalogue of all tile/cell IDs.
- Full control-flow graph of direct map mutations.
- Exact meaning of every integer-plane bit and runtime overlay.
- Full entity creation/update and collision behavior.
- Complete layer ordering, occlusion, and camera parity.
- Deterministic complete gameplay scene from an original room.
- Full animation timing integration.
- Native gameplay runtime.
- Android lifecycle/input/audio integration.
- Kotlin/Gradle validation for the latest code.
- Device testing, visual parity sign-off, and APK release.

## Honest validation policy

A passing Python regression test suite proves only the tested static/reference behavior. It does not mean Kotlin compilation, Android Gradle build, emulator/device execution, gameplay parity, or APK creation. Each must be reported separately when actually performed.
