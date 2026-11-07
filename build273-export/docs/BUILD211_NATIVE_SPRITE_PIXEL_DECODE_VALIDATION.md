# Build 211 — Native Sprite Pixel Decode Validation

## Executive result

Build 211 validates every extracted sprite payload against its declared dimensions and palette bounds, then compares the Python reference decoder with the actual Kotlin `LegacySpriteDecoder` implementation.

**All 1,372 sprites decode successfully, and Python/Kotlin produce identical SHA-256 hashes for every decoded pixel-index plane.**

## Original JAR inventory

- DF03 resources: 94/94.
- Sprite records: 1,372/1,372.
- Pixel formats: `0x1600` indexed 4bpp: 1,300; `0x27F1` indexed RLE: 71; `0x0400` indexed 2bpp: 1.
- Payload truncation: 0.
- Trailing undecoded payload bytes: 0.
- Palette index overflow: 0.
- Pixel count/dimension mismatches: 0.
- Python/Kotlin SHA-256 mismatches: 0.

## Decoder parity

A Kotlin runtime audit was compiled from the project source and executed against the original JAR. It traverses each `.f` bundle, parses all DF03 resources with `LegacySpriteFieldLayoutParser`, decodes every sprite with `LegacySpriteDecoder.decodeIndices`, checks palette-index bounds, and records a SHA-256 digest for each decoded index plane. The Kotlin and Python inventories match for every `(bundle, entry, sprite)` identity, including dimensions, payload length, decoded count, maximum index, and digest.

## Visual reference atlases

Four atlases were generated directly from decoded original-JAR pixels: `ms.f`, `ui.f`, `0.f`, and `o.f`. These are Python/Pillow reference raster outputs using palette row 0. Resources with multiple palette rows may have alternate palette states not represented in the previews. The atlases are not Android Canvas output and do not establish full composite or scene parity.

## Source and artifacts

- `android/src/main/kotlin/com/diamondrush/legacy/LegacySpriteDecoder.kt` — decoder.
- `tools/Build211KotlinSpriteAudit.kt` — Kotlin runtime audit.
- `research/build211_sprite_decode_inventory.csv` — Python inventory.
- `research/build211_kotlin_decode_inventory.csv` — Kotlin inventory.
- `tests/test_build211_sprite_decode.py` — Build 211 tests.
- `previews/` — reference sprite atlases.

## Validation

- Python regression suite: 48 passed in 0.18s.
- Kotlin source compilation: passed.
- Kotlin runtime audit: passed (94 resources, 1,372 sprites).
- Python/Kotlin digest parity: 1,372/1,372 identical.
- Android Gradle build, Android device runtime, composite rasterization, visual parity, and playable APK remain unverified.

## Next build — Build 212: Composite Sprite Rasterization

1. Select representative root groups from `ms.f`, `ui.f`, and gameplay bundles.
2. Resolve component trees using the Build 207 resolver and validated sprite decoder.
3. Rasterize ordered leaf commands with signed offsets and flag-controlled anchor behavior.
4. Inspect nested groups, transparency, clipping, and overlapping layers.
5. Compare composite previews with original game references.
6. Then begin 320×240 scene assembly and the 320×178 gameplay viewport.
