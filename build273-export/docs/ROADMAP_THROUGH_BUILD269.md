# Roadmap through Build269

## Completed foundations

- Builds198–243: JAR/resource extraction, DF03 parsing, sprite/palette decoding, composite/frame rasterization, room data, camera/viewport and dispatch research.
- Builds244–263: room candidate joins, renderer callsite/descriptor audit, corrected renderer CFG, unreachable-region audit, cross-class invocations and symbolic operand provenance.
- Builds264–268: method-local CFG, abstract operand stack, JVM stack-shape helpers, classfile exception-table extraction, exception-aware symbolic propagation and corrected switch parsing.
- Build269: branch-specific producer-slice audit for the two interpolation operands consumed at `c.a(Graphics, byte[], int)` offset 873.

## Current evidence boundary

The two values sourced from local 0 and local 4 are now described by exact bytecode-derived formulas. They are not concrete runtime integers because the byte-array contents, index, and instance field `this.b` vary at runtime. Build269 does not claim that all PHI alternatives in the whole method have been globally simplified.

## Next milestones

### Build270 — Arithmetic and exception semantics
- Model integer overflow and signed-short narrowing explicitly.
- Preserve division-by-zero exceptional behavior for the interpolation formula.
- Verify exception-handler transfer for the protected regions in the same method.

### Build271 — Resource and draw-command binding
- Trace the resource-array index and frame/index operand at offset 873.
- Join proven expressions with the dynamic resource inventory and DF03 composite records.
- Keep runtime-dependent selections symbolic.

### Build272 — Room draw-sequence reconstruction
- Connect room-plane values, dispatch cases, resource selection, coordinates and renderer calls.
- Produce a traceable candidate draw-command sequence for a bounded room region.
- Validate each command against existing sprite/composite raster fixtures.

### Android integration phase
After the renderer and room draw sequence have adequate evidence, create the Android Gradle application skeleton, Activity, asset packaging, game surface/game loop, input and lifecycle integration. Then run Gradle compilation, install/device tests, room rendering and visual comparisons. A playable APK remains a later deliverable; it is not present in Builds198–269.
