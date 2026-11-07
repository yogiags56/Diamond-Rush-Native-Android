# Diamond Rush Native Android Port — Roadmap through Build265

## Current milestone

Build265 implements a conservative CFG-aware abstract operand-stack interpreter for eight proven cross-class renderer callsites. All eight are reachable and have sufficient stack depth for their method descriptors. Seven callsites have fully symbolically expressed operands; one callsite retains two `UNKNOWN` operands.

## Completed foundations

- Original JAR resource parsing and DF03 sprite/palette decoding.
- Sprite raster execution and composite/frame integration prototypes.
- Room archive and scene/camera evidence.
- Renderer overload semantics and callsite descriptor contracts.
- Corrected `i.D()V` CFG and unreachable-region audit.
- Cross-class renderer invocation inventory.
- Method-local CFG reachability for `b`, `c`, and `g`.
- Build265 symbolic operand-stack worklist.

## Build266 — next

1. Add exception-table parsing and exceptional CFG edges for the selected caller methods, particularly `c.a(Graphics, byte[], int)`.
2. Model category-2 values and JVM stack manipulation forms precisely, or explicitly reject unsupported forms.
3. Improve local-variable provenance at switch joins and explain the two unknown operands at `c` offset 873.
4. Add stack-shape invariants against descriptors and compare pre-invoke argument order with independent producer-slice evidence.
5. Keep opaque method calls and unresolved field/array values symbolic.

## Later milestones

- Connect proven call arguments to composite resource records and decoded sprite instances.
- Reconstruct the actual renderer command sequence for a room.
- Implement the renderer behavior in native Kotlin/Android while retaining the 320x240 logical canvas, 320x178 gameplay viewport at y=31, and 24x24 tile target.
- Validate visual parity before claiming complete room rendering.
- Only claim Android APK/playability after an actual Gradle build and device/runtime verification.
