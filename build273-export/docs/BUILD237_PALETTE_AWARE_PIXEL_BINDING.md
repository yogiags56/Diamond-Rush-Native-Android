# Build 237 — Palette-Aware Pixel Binding

## Objective
Connect Build236 concrete sprite draw operations to decoded ARGB pixels while preserving the original global `f[]` slot, local sprite index, dimensions, explicit palette row, draw position, flags, and composite provenance. This milestone binds pixels to operations; it does not yet execute MIDP transforms or draw into a room canvas.

## Implementation
Added `LegacyPaletteBoundSpriteDraw.kt`:
- `LegacyPaletteAwareSpriteDecoder.decodeResource` accepts a caller-supplied global resource slot and explicit palette index.
- Raw palette entries are converted through the existing `LegacySpriteDecoder.decodePalette` implementation.
- Encoded sprite indices are decoded through `LegacySpriteDecoder.decodeIndices`.
- Every decoded index is checked against the selected palette row.
- `LegacyDecodedSpriteRecord` retains global slot, local sprite index, dimensions, pixel format, palette format, palette index, ARGB pixels, and transparency state.
- `bindOperations` joins by the exact `(globalArraySlot, spriteIndex)` identity and rejects missing pixels, palette mismatch, or dimension mismatch.
- Draw operation position and flag fields remain unchanged. No palette is inferred from sprite identity or resource slot.

## Build234 parser correction discovered during Build237
The Kotlin `LegacySpriteResourceBundleParser` previously read all sprite lengths first and then consumed all payloads. The original bytecode and the Python reference parser establish an interleaved stream:

`[signed-short length][payload][signed-short length][payload]...`

This caused misalignment in Kotlin for multi-sprite resources even though the Python full-resource audit had parsed the original JAR correctly. The Kotlin parser now reads each length immediately followed by that sprite's payload. `Build234SpriteResourceParserChecks.verifySpriteLengthAndPayloadRecordsAreInterleaved` protects this behavior with a two-sprite fixture.

## Original JAR validation
Two reproducible Kotlin audits were run against `original.jar`:

### Full DF03 audit
- 24 `.f` bundles.
- 94 DF03 payloads parsed.
- 1,372 sprite records.
- 112 palette rows across those resources.
- 2,604 sprite/palette combinations decoded.
- 415,896 ARGB pixels decoded and palette-index validated.
- No decode or palette-index failures.

Output: `research/build237_full_df03_pixel_decode_audit.csv`.

### Build235 statically mapped slots
- 10 static global `f[]` slots.
- 12 palette variants across those resources.
- 114 sprite/palette instances.
- 28,932 ARGB pixels decoded.
- Both palette rows were decoded for `f[10]` and `f[59]`; all other mapped slots expose one palette row.
- Palette rows remain explicit. This audit does not prove which palette row is selected at every runtime callsite.

Output: `research/build237_original_mapped_sprite_decode_audit.csv`.

Reproducible audit sources:
- `research/build237_full_df03_pixel_decode_audit.kt`
- `research/build237_original_mapped_sprite_decode_audit.kt`

## Regression validation
- Python regression suite: **203 passed, 4 warnings**. All four are existing Pillow `Image.getdata()` deprecation warnings from Build213 tests.
- Kotlin: all pure legacy package sources plus Build234, Build236, and Build237 check sources compiled with `kotlinc`; all three check suites executed successfully (`BUILD237_KOTLIN_CHECKS_PASSED`).
- Full original-JAR Kotlin parser/pixel audit completed successfully: 94/94 DF03 resources, 1,372 sprite records, 2,604 sprite/palette decodes.
- ZIP integrity verified separately.

## Explicit non-claims
- Runtime palette selection at every callsite is not yet fully established; caller must supply palette index.
- MIDP transform execution, clipping, blend/compositing behavior, and target-surface writes are not implemented by this milestone.
- No complete room image, Android Gradle build, device runtime, visual parity result, or APK is claimed.

## Next milestone — Build238
Implement deterministic sprite raster execution: apply the proven MIDP transform mapping, preserve alpha behavior, clip against the logical viewport, and write pixels into a test surface. Use golden pixel fixtures before integrating full composite/frame and room rendering.
