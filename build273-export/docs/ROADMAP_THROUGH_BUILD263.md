# Diamond Rush Native Android Port — Roadmap through Build263

## Current research state

- Native Android port, logical canvas 320×240, gameplay viewport 320×178 at y=31, target tile 24×24.
- Original resource parsing, DF03 sprite decoding, palette handling, composite reconstruction, and sprite raster foundations remain in prior builds.
- Build256 corrected renderer CFG: 3,811 instructions, 322 basic blocks, 564 CFG edges.
- Build258 confirmed no exception-table entries in `i.D()V`.
- Build259 isolated the 75-block unreachable region after offset 6170 (`return`), beginning at 6171.
- Build260 audited cross-class method references.
- Build261 established eight actual renderer invoke instructions outside class `i`.
- Build262 extracted context windows and descriptor stack contracts for those eight invokes.
- Build263 mapped 64 symbolic operand-stack entries: 59 direct symbolic sources and 5 arithmetic expressions.

## Next milestone: Build264

Build a CFG-aware abstract operand-stack interpreter for the three caller classes/methods represented by the eight callsites. It must model branch/switch edges, locals, stack operations, invocation descriptors, and merges. Preserve `UNKNOWN` whenever a producer or merge cannot be established. Cross-check every Build263 expression against the interpreter and record mismatches rather than silently reconciling them.

## Explicitly not complete

No complete room renderer, full visual parity, Kotlin compilation, Android Gradle build, device runtime, or playable APK is established by Build263.
