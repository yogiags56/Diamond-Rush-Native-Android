# Build 235 — Sprite-to-Room/Composite Binding

## Result

Build 235 connects the ten statically attributed `f[]` global slots from Build233 to their local DF03 sprite records, composite component records, animation sequences, and the previously audited original resource consumers.

The audit produces:

- **10** static global-slot bindings.
- **87** decoded sprite records across those slots.
- **843** composite component references.
- **843** expanded composite-group-to-leaf sprite references.
- **85** animation frame records referenced by sequence tables.
- **82** animation-frame references to valid composite groups.
- **3** explicit `0xFF` no-group sentinels.
- **719** expanded leaf sprite references reached from animation frames.
- **0** invalid component record positions, component targets, or animation group references in this mapped set.

One component edge is a nested-composite reference, in `/ui.f` entry 3. It is preserved as a group reference and expanded through the referenced group; it is not misreported as a sprite record.

## Important consumer distinction

The static loader map and the gameplay render consumer map are different evidence sets. Of the ten static slots, only **`f[9]` and `f[10]`** are directly referenced by the audited `i.D()V` render method (at offsets `6107, 7236` and `6348, 6357, 6369`, respectively). The other eight static slots have original consumer sites in other methods, but are not relabeled as direct `i.D()` room-render consumers.

This prevents a common false join: a resource being loaded into global `f[]` does not by itself prove that `i.D()` draws it as a room-cell resource. The catalog retains the exact slot, bundle, directory entry, and all indexed consumer sites separately.

## Generated research catalogs

- `research/build235_resource_binding_summary.csv` — per-slot bundle/entry, consumer sites, and aggregate counts.
- `research/build235_composite_component_bindings.csv` — group/component record to sprite-or-group references, including signed offsets and control byte.
- `research/build235_composite_group_leaf_expansion.csv` — ordered leaf sprite references for every composite group.
- `research/build235_animation_group_bindings.csv` — sequence/frame to composite-group references, preserving duration, offsets, flags, and sentinel state.
- `research/build235_animation_leaf_draw_bindings.csv` — leaf sprite references expanded from animation frame groups.
- `research/build235_sprite_room_composite_binding_audit.py` — reproducible audit against `original.jar` and the checked-in Build232/233 catalogs.

## Kotlin implementation

`LegacySpriteResourceBindingCatalog.kt` adds typed binding records for:

- static global slot to bundle path and directory entry;
- local sprite record to dimensions and encoded payload length;
- composite group/component to a leaf sprite or nested group;
- animation sequence/frame to a composite group or the explicit `0xFF` no-group sentinel;
- optional direct `i.D()V` consumer evidence.

The implementation does not invent semantic names for sprite IDs, table fields, or global slots. Missing/invalid references remain explicit rather than being silently coerced.

`Build235SpriteResourceBindingChecks.kt` adds synthetic checks for the slot binding, component leaf, animation group, and unknown-slot rejection.

## Validation

- Python regression suite: **191 passed, 4 warnings**.
- Mapped static slot bindings: **10/10**.
- Sprite records: **87**.
- Composite component edges: **843**, with no out-of-range targets.
- Animation frames: **85**, comprising 82 valid group references and 3 explicit no-group sentinels.
- Animation-derived leaf references: **719**, all in range.
- Kotlin compilation: targeted Build234/235 source set compiled successfully with `kotlinc`; parser and binding checks executed successfully (`BUILD235_KOTLIN_VALIDATION.txt`).
- Android Gradle build, device runtime, visual parity, and APK packaging: not performed.

## Interpretation and next step

Build235 establishes a static resource-binding layer. It does not yet prove that all 719 animation-derived leaves are visible in a particular room at a particular time; the original animation clock, room-cell dispatch, visibility, and draw ordering still gate runtime emission.

**Build236** should join the proven `i.D()` cell dispatch results to these resource/group/sprite bindings and emit concrete, deterministic sprite draw operations. It must preserve the distinction between the two main dispatch domains, secondary overlays, direct draw paths, and supplemental resources.
