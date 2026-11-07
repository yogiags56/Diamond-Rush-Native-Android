# Build 247 — Original Sprite Draw Callee Semantics

## Objective

Resolve the roles of the overloaded `f.a(Graphics, ...)` methods by inspecting the original JAR's callee bytecode, rather than guessing from caller descriptors.

## Confirmed call hierarchy

### `a(Graphics, int, int, int, int, int, int, int)` — seven integer arguments

- Reads the composite offset/index table `a:[S`.
- Selects a component record from `c:[B`.
- Applies component flags and signed offsets.
- Delegates to the six-integer overload.

Role: composite-component entry/selection.

### `a(Graphics, int, int, int, int, int, int)` — six integer arguments

- Reads the component count from `g:[B`.
- Iterates component references using `b:[S`.
- Reads component metadata and offsets from `h:[B`.
- Recursively invokes the six-integer overload for nested composite components.
- Dispatches leaf sprite components to the four-integer overload.

Role: composite-group expansion.

### `a(Graphics, int, int, int, int)` — four integer arguments

- Resolves sprite dimensions from `f:[B` and pixel/image data.
- Selects the MIDP transform from flag bits.
- Calls `Graphics.drawRegion`.

Role: leaf-sprite drawing.

## Implementation

- `LegacySpriteDrawCalleeSemantics.kt` records the proven overload roles and delegation relationships.
- `Build247SpriteDrawCalleeSemanticsChecks.kt` checks the role catalog.
- `research/build247_sprite_draw_callee_semantics.py` audits the original JAR using `javap` and asserts the key field accesses/delegations.
- `research/build247_sprite_draw_callee_semantics.csv` and `.txt` contain machine-readable and human-readable results.

## Validation

- 11 original-bytecode structural assertions passed.
- Python regression: 234 passed, 4 pre-existing Pillow deprecation warnings.
- All Kotlin production and test sources compile together.
- Build223–247 Kotlin regression runner passes, including original DF03 fixtures and composite attribution checks.

## Evidence boundary

Build247 proves what the three callee overloads do structurally. It does not yet prove the caller-side integer values at every `i.D()V` callsite, nor the runtime-selected composite group for each room cell. No candidate cell mapping is promoted to a concrete raster operation in this milestone.

## Next: Build248 — Caller Argument Stack Reconstruction

1. Reconstruct the operand stack at each of the 25 sprite callsites in `i.D()V`.
2. Use control-flow predecessor states and local-variable definitions rather than a bounded textual lookback.
3. Identify the seven-int component-entry arguments versus six-int composite-group arguments.
4. Trace the group index and destination coordinates back to map-cell dispatch variables.
5. Preserve unresolved merges as explicit unknowns.
6. Keep the separate `f[42]` direct-draw path isolated until its call semantics are proven.

No Android Gradle build, device runtime, full-room raster, screenshot parity, or APK packaging is claimed.
