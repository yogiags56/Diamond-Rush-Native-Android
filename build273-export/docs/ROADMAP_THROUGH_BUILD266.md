# Diamond Rush Native Android Port — Roadmap through Build266

## Latest milestone

Build266 adds local-variable snapshots to the eight renderer callsite records and a standalone, tested JVM stack-shape helper for category-1/category-2 values and stack-manipulation instructions. The two unresolved operands at `c.a(Graphics, byte[], int)` offset 873 are localized to local slots 0 and 4 and remain UNKNOWN.

## Completed foundations

- Original JAR resource parsing and DF03 sprite/palette decoding.
- Sprite raster execution and composite/frame integration prototypes.
- Room archive and scene/camera evidence.
- Renderer overload semantics and callsite descriptor contracts.
- Corrected `i.D()V` CFG and unreachable-region audit.
- Cross-class renderer invocation inventory.
- Method-local CFG reachability for `b`, `c`, and `g`.
- CFG-aware symbolic operand worklist for eight cross-class renderer callsites.
- Build266 local-state snapshots and tested category-aware JVM stack-shape helpers.

## Build267

1. Parse classfile Code attributes directly for exception tables in the four selected methods.
2. Add exceptional CFG edges only where the original classfile defines protected ranges and handlers.
3. Track local-variable definitions and incoming predecessor expressions at the two unresolved slots (local 0 and local 4) in `c` offset 873.
4. Implement a bounded provenance-set merge so different incoming expressions remain auditable instead of collapsing immediately to a bare UNKNOWN.
5. Integrate category-2 widths and all supported stack-manipulation forms into the abstract interpreter, or explicitly mark any unsupported form.

## Later milestones

- Connect proven call arguments to composite resource records and decoded sprite instances.
- Reconstruct the actual renderer command sequence for a room.
- Implement renderer behavior in native Kotlin/Android while retaining the 320x240 logical canvas, 320x178 gameplay viewport at y=31, and 24x24 tile target.
- Validate visual parity before claiming complete room rendering.
- Only claim Android APK/playability after an actual Gradle build and device/runtime verification.
