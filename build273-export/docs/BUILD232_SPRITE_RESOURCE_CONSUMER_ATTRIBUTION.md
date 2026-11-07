# Build 232 — Sprite Resource Consumer Attribution

## Scope

This build inventories references to the original game's global `f[]` sprite-resource array in the preserved `i_build214_full.javap.txt` disassembly. It adds an evidence-backed numeric consumer catalog for the main render method `i.D()V`.

## Bytecode evidence

- Original `i` class allocates a global `f[]` array with **61 slots** (`bipush 61`, `anewarray class f`).
- The disassembly contains **248** references to fields with descriptor `[Lf;`.
- Classified nearby instruction patterns: **190 reads**, **17 writes**, and **41 references whose immediate use is not resolved by the bounded local scan**.
- `i.D()V` contains **42** array-index references with a statically visible integer constant, spanning **23 distinct resource-array indices**: 0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 20, 27, 28, 29, 30, 32, 38, 42, 56.
- Previously attributed secondary-overlay resource indices remain numeric: **3, 7, 13, 15, 16, 20, 42**.

## New files

- `android/src/main/kotlin/com/diamondrush/legacy/LegacySpriteResourceConsumerCatalog.kt`
- `research/build232_sprite_resource_array_accesses.csv`
- `tests/test_build232_sprite_resource_consumers.py`
- `docs/BUILD232_SPRITE_RESOURCE_CONSUMER_ATTRIBUTION.md`
- `docs/ROADMAP_THROUGH_BUILD232.md`
- `BUILD232_TEST_RESULTS.txt`
- `BUILD232_KOTLIN_VALIDATION.txt`

## Interpretation boundaries

This is **consumer attribution**, not a complete asset-to-room binding:

1. A numeric `f[index]` reference does not by itself identify a sprite's visual meaning.
2. A `getstatic f[]` access followed by `aaload` is evidence of a read, not proof that the loaded object is drawn at that exact point.
3. `ARRAY_REF` rows intentionally retain ambiguous nearby stack patterns.
4. The CSV records all observed field references and nearby instructions so future analysis can refine unresolved accesses without losing original bytecode offsets.
5. Resource bundle filenames from Build 231 are not mapped to individual `f[]` slots in this build.

## Validation

- Python regression suite: **171 passed, 4 warnings**.
- Kotlin compilation: **not run in this environment** (`kotlinc` unavailable). The new Kotlin catalog is source-only in this build.
- Android Gradle build, APK, device runtime, and visual parity: **not performed**.

The four Python warnings are existing Pillow deprecation warnings from earlier raster tests.
