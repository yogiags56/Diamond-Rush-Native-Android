# Build 233 — Bundle-to-Global Sprite Slot Attribution

## Milestone

Build 233 establishes direct, bytecode-backed mappings from selected resource-bundle directory entries to slots in the original global `f[]` array.

The mappings are committed by `aastore` instructions in `i.b(I)V`. The loader call sites use the original static helper `a(String, int, int, int)`.

## Proven loader directory semantics

The original `public static byte[] a(String, int)` helper:

1. Opens the requested classpath resource using `getResourceAsStream`.
2. Reads one byte as the number of directory records.
3. Reads `recordCount * 8` bytes for the directory.
4. Computes the selected record's directory offset as `entryIndex * 8`.
5. Reads the record's payload offset from directory field `+0`.
6. Reads the payload length from directory field `+4`.
7. Skips to the payload offset and reads the payload length into a byte array.

This establishes that the integer passed to the helper is a **bundle directory entry index**, not a sprite ID.

## Direct static mappings

| Global `f[]` slot | Bundle | Directory entry | Loader call offset in `i.b(I)V` |
|---:|---|---:|---:|
| 10 | `/mmv.f` | 0 | 145 |
| 46 | `/mmv.f` | 5 | 178 |
| 55 | `/mmv.f` | 4 | 258 |
| 18 | `/ui.f` | 3 | 314 |
| 54 | `/mmv.f` | 1 | 348 |
| 53 | `/mmv.f` | 2 | 417 |
| 52 | `/mmv.f` | 3 | 451 |
| 59 | `/cm.f` | 2 | 513 |
| 17 | `/ms.f` | 0 | 584 |
| 9 | `/cm.f` | 7 | 621 |

These are ten direct static assignments, not a complete map of all 61 slots.

## Dynamic assignment inventory

`research/build233_dynamic_sprite_slot_assignments.csv` preserves four additional stores in `i.j()V`:
- slot 21 is assigned a new `f` object populated from a byte buffer read from the current input stream;
- another store uses a runtime local variable as the global slot index;
- slots 43 and 13 receive previously created local objects whose complete source chain is not yet attributed.

These are intentionally not merged into the static bundle map.

## Important decoder limitation

The existing DF03 parser inventory reports parser failures for all ten mapped bundle entries:
- `/mmv.f` entries 0–5 used by the mappings;
- `/ui.f` entry 3;
- `/ms.f` entry 0;
- `/cm.f` entries 2 and 7.

This does **not** invalidate the bytecode mapping. It means the current offline parser has not successfully decoded these exact payloads. Build 234 should investigate the original `f.a(byte[], int)` parsing path and determine whether the current parser's record-layout assumptions are incomplete for these entries.

## New files

- `android/src/main/kotlin/com/diamondrush/legacy/LegacyBundleSpriteSlotCatalog.kt`
- `research/build233_bundle_to_global_sprite_slots.csv`
- `research/build233_dynamic_sprite_slot_assignments.csv`
- `tests/test_build233_bundle_slot_attribution.py`
- `docs/BUILD233_BUNDLE_TO_GLOBAL_SPRITE_SLOT_ATTRIBUTION.md`
- `docs/ROADMAP_THROUGH_BUILD233.md`
- `BUILD233_TEST_RESULTS.txt`
- `BUILD233_KOTLIN_VALIDATION.txt`

## Validation

- Python regression tests: **178 passed, 4 warnings**.
- Kotlin compilation: not run; `kotlinc` is unavailable in this environment.
- Android Gradle build, APK, device runtime, and visual parity: not performed.

The four warnings are existing Pillow deprecation warnings from earlier raster tests.
\n\n## Follow-up from Build 234\n\nThe parser failures listed in this Build233 report were caused by a cursor-alignment mistake in the then-current offline parser, not by malformed mapped payloads. Build234 corrected the `count << 2` table sizing and successfully parsed all ten mapped entries, along with all 94 DF03 entries in the original JAR. See `docs/BUILD234_DF03_SPRITE_RESOURCE_DECODER_RECONSTRUCTION.md`.\n