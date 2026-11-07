# Diamond Rush Native Android — Roadmap through Build268

## Completed foundations (Build198–243)

- Original JAR resource extraction and inventory.
- DF03 bundle parsing, sprite/palette decoding, MIDP transforms.
- Composite graphs, frame animation, sprite and composite raster prototypes.
- Room archive and three-plane data decoding.
- Camera, viewport, dispatch, and resource attribution research.

## Renderer reverse engineering (Build244–263)

- Room-cell candidate joins and dynamic resource attribution.
- Renderer overload contracts and composite callee semantics.
- Corrected renderer CFG for `i.D()V`.
- Unreachable bytecode-region audit.
- Cross-class renderer invocation inventory.
- Symbolic operand producer provenance.

## Control-flow and operand analysis (Build264–268)

- Method-local CFG for cross-class renderer callers.
- Initial abstract operand stack interpreter.
- Category-1/category-2 stack-shape contract helpers.
- Original classfile exception-table parser.
- Build268 corrected switch-table parsing and conservative exception-handler transfer.
- All eight cross-class renderer callsites now reachable with descriptor-sized stacks.
- Two offset-873 operands upgraded from `UNKNOWN` to explicit PHI provenance; concrete runtime values remain unresolved.

## Next: Build269–272 — stabilize symbolic renderer contracts

1. Add path predicates for the `lookupswitch` case and conditional interpolation branches.
2. Reduce PHI alternatives for local 0 and local 4 at offset 873 without inventing runtime values.
3. Integrate the Build266 category-2 stack-shape rules into the main interpreter.
4. Validate all callsite operand ordering against method descriptors and producer slices.
5. Join renderer receiver/resource expressions to the decoded DF03 composite inventory.

## Next: Build273–280 — room draw-sequence reconstruction

1. Select a room with known dimensions and decoded planes.
2. Reconstruct dispatch selection for each cell.
3. Resolve resource, sequence, frame, coordinates, transform, and draw order.
4. Produce a deterministic draw-command list.
5. Compare Python reference rasterization against known source assets and room screenshots where available.

## Android integration phase — after renderer contracts are stable

1. Create Gradle Android application skeleton and manifest.
2. Add Activity/entry point and lifecycle-aware game surface.
3. Port/integrate asset loading and Kotlin sprite/composite renderer.
4. Connect room model, camera, viewport, input, and frame loop.
5. Add gameplay state, collision/interactions, HUD, menus, audio, and transitions.
6. Build APK, install on device, test, and compare visual parity.

## Current honest status

The project has substantial reverse-engineering data and Kotlin engine components, but the latest audited snapshot does not establish a complete Android Gradle application, a successful APK build, device runtime, full room rendering, visual parity, or a playable game. The immediate work remains renderer behavior reconstruction before full application integration.
