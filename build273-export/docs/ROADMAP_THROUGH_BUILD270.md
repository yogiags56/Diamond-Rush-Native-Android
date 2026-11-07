# Roadmap through Build270

## Completed foundations

- Builds198–243: JAR/resource extraction, DF03 parsing, sprite/palette decoding, composite/frame rasterization, room data, camera/viewport and dispatch research.
- Builds244–263: room candidate joins, renderer callsite/descriptor audit, corrected renderer CFG, unreachable-region audit, cross-class invocations and symbolic operand provenance.
- Builds264–268: method-local CFG, abstract operand stack, JVM stack-shape helpers, classfile exception-table extraction, exception-aware symbolic propagation and corrected switch parsing.
- Build269: bytecode-proven case-4 interpolation expressions for the two operands consumed at `c.a(Graphics, byte[], int)` offset 873.
- Build270: executable JVM integer semantics for the audited expressions, including i32 overflow, idiv truncation, signed-short narrowing and divide-by-zero behavior.

## Evidence boundary

Build270 validates arithmetic semantics for the Build269 producer slice. It does not
know runtime byte-array contents, the runtime index, or `this.b`; therefore concrete
coordinates remain unknown until those inputs are sourced from an actual room/game
state. The arithmetic model is focused, not a full JVM verifier.

## Next milestones

### Build271 — Resource and draw-command binding
- Trace the resource-array index and frame/index operand at offset 873.
- Join proven expressions with dynamic resource inventory and DF03 composite records.
- Keep runtime-dependent selections symbolic.

### Build272 — Room draw-sequence reconstruction
- Connect room-plane values, dispatch cases, resource selection, coordinates and renderer calls.
- Produce a traceable candidate draw-command sequence for a bounded room region.
- Validate commands against existing sprite/composite raster fixtures.

### Android integration phase
After the renderer and room draw sequence have adequate evidence, create the Android
Gradle application skeleton, Activity, asset packaging, game surface/game loop, input
and lifecycle integration. Then run Gradle compilation, install/device tests, room
rendering and visual comparisons. A playable APK remains a later deliverable; it is
not present in Builds198–270.
