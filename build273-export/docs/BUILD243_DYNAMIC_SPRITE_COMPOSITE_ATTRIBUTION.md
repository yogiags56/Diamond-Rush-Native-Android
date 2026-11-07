# Build 243 — Dynamic Sprite and Composite Attribution

## Objective

Continue from Build242's bytecode-confirmed dynamic resource origins by parsing the field-aligned DF03 payloads for `f[27]`, `f[30]`, and `f[56]`, validating each composite group/component reference, and decoding every sprite under explicit palette selection.

## Implementation

New Kotlin source: `LegacyDynamicSpriteCompositeIndex.kt`.

`LegacyDynamicSpriteCompositeIndex.build(globalSlot, layout, paletteIndex)`:
- requires a bytecode-confirmed origin from `LegacyDynamicSpriteResourceOriginCatalog`;
- consumes the bytecode-aligned `LegacySpriteFieldLayout` tables;
- builds group ranges from `gGroupCounts` and `bGroupStarts`;
- parses four-byte component records using the existing `CompositeSpriteRecord` model;
- distinguishes leaf sprite indices from nested group indices using the already audited `0x10` control bit;
- validates all referenced indices;
- decodes every sprite's indexed pixels using `LegacySpriteDecoder.decodeIndices`;
- binds one explicitly selected palette from the field layout;
- retains signed component offsets and the original control byte.

The builder intentionally does not choose a palette, assign gameplay meaning to sprite art, decide which group a room cell selects, or recursively reinterpret any unknown flags.

## Confirmed results

| Global slot | Resource | Groups | Component records | Sprites | Palette rows |
|---:|---|---:|---:|---:|---:|
| 27 | `/gen3.f` record 4 | 7 | 31 | 11 | 1 |
| 30 | `/gen2.f` record 3 | 8 | 12 | 11 | 1 |
| 56 | `/cm.f` record 1 | 6 | 8 | 6 | 3 |
| **Total** | | **21** | **51** | **28** | **5** |

Across these resources, all 51 component records are leaf-sprite references; no nested-composite component is present in these three exact payloads. This is a property of these payloads only, not a general statement about the original game's composite format.

Sprite index coverage:
- `f[27]`: all 11 sprite indices (0–10) referenced.
- `f[30]`: sprite indices 0, 1, 2, 3, 4, 8, 9, 10 referenced; sprites 5, 6, 7 are not referenced by these composite groups.
- `f[56]`: all 6 sprite indices (0–5) referenced.

All 28 sprite records decoded successfully. With explicit palette selection, this yields 40 sprite/palette decode instances (11 + 11 + 6×3), comprising 10,256 decoded pixels. The Python audit records 2,117 transparent pixels using the original ARGB1555 alpha bit.

## Research artifacts

- `research/build243_dynamic_composite_component_attribution.csv`: 51 component-to-sprite/group rows.
- `research/build243_dynamic_sprite_pixel_decode_audit.csv`: 40 sprite/palette rows with dimensions, decoded pixel counts, transparency counts, and payload SHA-256.
- `research/build243_dynamic_sprite_composite_audit.py`: reproducible fixture audit.
- `research/build243_sprite_contact_sheets/`: five visual contact sheets (one palette for `f[27]`, one for `f[30]`, all three for `f[56]`).

Contact sheets are diagnostic views of decoded source sprites. They are not room renders and do not assign names or gameplay semantics to the artwork.

## Validation

- Python regression: **222 passed, 4 warnings**. The four warnings are pre-existing Pillow `Image.getdata()` deprecations in Build213 tests.
- Kotlin: all production and test sources compiled together.
- Kotlin regression runner: **Build223–Build243 passed**.
- Build243 Kotlin checks validate group sizes, component counts, leaf/nested index bounds, decoded dimensions, explicit palette variants, and referenced sprite sets.

## Evidence boundary

Build243 proves the composite-group structure and sprite references inside the three already-confirmed dynamic resources, and proves that all their sprite pixel payloads can be decoded. It does not yet prove which composite group or sprite index is selected by each particular room cell. Build240/241 room dispatch evidence still needs to be joined to these per-resource group tables. Palette selection for runtime cells remains unresolved unless separately established by bytecode. The `f[42]` direct-draw path remains separate.

No complete original-room raster, Android Gradle build, device runtime, screenshot parity, or APK is claimed.

## Next: Build244 — Room Cell to Dynamic Composite Group Join

1. Join Build240's original-room cell manifest and Build241's branch evidence with Build242's confirmed dynamic resource origins.
2. Trace the exact arguments passed from each dispatch branch into the composite/frame draw methods.
3. Establish group-index derivation separately from local sprite index.
4. Resolve runtime palette selection only where the bytecode proves it.
5. Produce a room-cell → `f[]` slot → group → component → sprite provenance table.
6. Rasterize only fully resolved operations; keep unresolved cells explicitly unresolved.
