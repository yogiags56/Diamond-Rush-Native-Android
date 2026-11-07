# Build 234 — DF03 Sprite Payload Decoder Reconstruction

## Result

**The DF03 parser alignment bug is fixed.** The previous parser treated one table length as `count * 2`, but the original bytecode allocates that table with `iconst_2; ishl`, meaning `count << 2` (**count × 4**). That cursor error shifted every subsequent field and made many valid resource entries look truncated or malformed.

After correcting the bytecode interpretation:

- **94 / 94** DF03 resource entries parse successfully, found among **121 directory entries across 24 `.f` bundles**.
- **1,372** sprite records are indexed.
- **139,268 bytes** of encoded sprite pixel data are accounted for.
- **0** parser failures.
- **0** trailing bytes across the 94 successfully parsed payloads.

The four-byte table and the later paired table both use `count << 2`; the earlier inventory's “2-byte table” label was incorrect.

## Exact parser structure

`f.a(byte[], int)` starts its payload cursor at byte offset 6. It processes the following structures in order:

1. Signed-short sprite count; if positive, `count * 2` bytes of width/height pairs.
2. Signed-short table count; if positive, `count << 2` bytes.
3. Signed-short metadata count; if positive, per row: one stored byte, one skipped byte, one signed short.
4. A second table allocated as `metadataCount << 2` bytes.
5. Signed-short count followed by `count * 5` bytes.
6. Signed-short count followed by per row: one stored byte, one skipped byte, one signed short.
7. If sprite count is positive: palette format, palette count, colors per palette, palette payloads according to the original format switch, and pixel format.
8. A first pass over signed-short sprite lengths, followed by the corresponding encoded sprite payload bytes.

The resource bundle helper separately confirms an unsigned one-byte directory count, 8-byte directory records, and little-endian 32-bit payload offset and length fields. The original JAR contains 24 `.f` bundles with 121 total directory entries; 94 entries carry the DF03 signature and are included in this decoder audit.

## Mapped global sprite slots: now parsed

The ten static Build233 mappings now resolve to these decoded payload summaries:

| Global slot | Bundle entry | Sprite records | Palette colors | Pixel format |
|---:|---|---:|---:|---:|
| 10 | `mmv.f` #0 | 23 | 2 × 32 | 5632 |
| 46 | `mmv.f` #5 | 12 | 1 × 30 | 5632 |
| 55 | `mmv.f` #4 | 3 | 1 × 14 | 5632 |
| 18 | `ui.f` #3 | 5 | 1 × 28 | 5632 |
| 54 | `mmv.f` #1 | 1 | 1 × 22 | 5632 |
| 53 | `mmv.f` #2 | 1 | 1 × 30 | 5632 |
| 52 | `mmv.f` #3 | 1 | 1 × 22 | 5632 |
| 59 | `cm.f` #2 | 4 | 2 × 24 | 5632 |
| 17 | `ms.f` #0 | 20 | 1 × 30 | 5632 |
| 9 | `cm.f` #7 | 17 | 1 × 28 | 5632 |

Together, these ten mappings account for **87 sprite records**. `research/build234_mapped_sprite_directory.csv` records each sprite's width, height, encoded payload length, pixel format, and palette format.

## New implementation

- `LegacySpriteResourceBundleParser.kt`
  - Reads original `.f` bundle directories.
  - Extracts individual resource entries using 8-byte directory records.
  - Parses DF03 tables, palette payloads, dimensions, and encoded sprite data.
  - Keeps opaque tables numeric and uninterpreted.
- `Build234SpriteResourceParserChecks.kt`
  - Synthetic parser and bundle-directory checks.

The Python audit tool `research/df03_full_parser_audit.py` is corrected to match the original bytecode. The former pre-fix inventory is retained as `*_build233_baseline.csv`; the canonical `df03_full_resource_inventory.csv` now contains the corrected 94-entry result. The Build209 parser boundary fixture was updated to use the correct four-byte table width.

## Validation

- Python regression tests: **185 passed, 4 warnings**.
- Full original resource audit: **94 parsed, 0 failed**.
- Mapped resources: **10 / 10 parsed; 87 sprite records indexed**.
- Kotlin compilation: not run (`kotlinc` unavailable).
- Android Gradle build, device runtime, visual parity, and APK: not performed.

The four warnings remain existing Pillow deprecation warnings from older raster tests.

## Next milestone: Build 235

Bind decoded sprite records to room-cell and composite-resource references. The next step should use the numeric resource consumer and room map evidence already gathered, without assigning semantic names to opaque table fields until their consumers are proven.

## Build237 follow-up correction
Build237's Kotlin end-to-end pixel audit exposed a cursor-order defect in the initial `LegacySpriteResourceBundleParser` implementation: it read all sprite length words before reading the sprite payloads. The original bytecode and the Build234 Python reference parser both use an interleaved `[length][payload]` record stream. The Kotlin parser was corrected in Build237, and a two-sprite interleaving regression fixture was added. The full Kotlin audit then parsed all 94 DF03 resources and decoded all 1,372 sprite records across their 112 palette rows (2,604 sprite/palette combinations). The original Build234 Python audit result remains valid; the correction concerns the Kotlin parser implementation.
