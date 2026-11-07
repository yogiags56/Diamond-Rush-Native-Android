# Build 214 — Animation Records, Palette State, and Viewport Geometry

## Executive result

Build 214 resolves the original five-byte `c:[B` table as an animation-frame indirection table and adds a Kotlin model for it. It also confirms the logical screen and gameplay viewport dimensions directly from original renderer bytecode.

This build is a bytecode-backed data-model milestone. It does not yet reconstruct every gameplay/menu layer or claim an Android screenshot.

## 1. Five-byte animation records

Original `f.class` parser allocation:
- reads a signed-short record count;
- allocates `count * 5` bytes for `c:[B`;
- copies the five-byte records without changing their order.

The adjacent tables are:
- `b:[B`: one unsigned frame count per animation sequence;
- `a:[S`: one signed-short first-record index per sequence.

The original accessors prove the table relationships:
- `a(int)` returns `b[sequence]` as an unsigned byte;
- `a(int,int)` returns byte 1 from `c[(a[sequence] + frame) * 5 + 1]`, unsigned.

Game class `i` uses the second accessor in elapsed-counter loops: it subtracts the returned value while advancing the frame index. Byte 1 is therefore a frame duration / countdown unit. Its conversion to milliseconds or a fixed frame rate is not inferred here.

### Record layout established by the draw method

| Byte | Meaning | Evidence |
|---:|---|---|
| 0 | Composite group index; `0xFF` is a no-group sentinel | Passed into composite group drawing; original resource references validate |
| 1 | Frame duration units | Accessor returns it unsigned; game uses it in elapsed-counter subtraction |
| 2 | Signed X offset | Loaded with JVM `baload`, then used in coordinate arithmetic |
| 3 | Signed Y offset | Loaded with JVM `baload`, then used in coordinate arithmetic |
| 4 | Control flags; low nibble XORed with incoming flags | Original renderer masks with `0x0F` and XORs |

Do not confuse this fifth byte with flag `0x20`: `0x20` is a bit in the *incoming renderer flags argument*, not a bit observed in the five-byte record control byte.

## 2. Flag `0x20` and frame offsets

The original seven-integer frame draw wrapper tests `incomingFlags & 0x20`.

- If bit `0x20` is clear, the wrapper preserves its inherited X/Y offset arguments.
- If bit `0x20` is set, it replaces those offsets with the current record's signed X/Y values.
- Incoming flag bit 0 chooses the X-offset sign.
- Incoming flag bit 1 chooses the Y-offset sign.
- The renderer subtracts the effective offsets from the supplied X/Y coordinates.
- The record's low control nibble is XORed with incoming flags before the composite group is drawn.

Equivalent placement logic:

```text
if flags & 0x20:
    effectiveX = recordX if flags & 1 else -recordX
    effectiveY = recordY if flags & 2 else -recordY
else:
    effectiveX = inheritedX
    effectiveY = inheritedY

drawX = baseX - effectiveX
drawY = baseY - effectiveY
drawFlags = flags XOR (recordControl & 0x0F)
```

This behavior is represented by `LegacySpriteAnimationTable.placement(...)`.

## 3. Full original-JAR inventory

| Measurement | Result |
|---|---:|
| DF03 resources parsed | 94 |
| Resources containing animation records | 37 |
| Animation sequences | 188 |
| Five-byte frame records | 1,238 |
| Valid composite-group references | 1,235 |
| Explicit no-group sentinel records | 3 |
| Invalid group references | 0 |
| Sequence range/count mismatches | 0 |

The three `0xFF` no-group frames occur at the second frame of sequence 0 in `mmv.f` entries 1, 2, and 3. They are preserved as sentinel frames, not treated as invalid group indices.

The sequence frame-count table partitions the record table exactly: the sum of all per-sequence frame counts equals the number of five-byte records in every resource.

### Duration and control distributions

- Duration units range from 1 to 90.
- All 1,238 durations are nonzero.
- Control byte values in the original records are 0 (1,007 records) and 1 (231 records).
- Signed X offsets range from -100 to 48.
- Signed Y offsets range from -24 to 120.

The largest five-byte record sets include:
- `o.f`, entry 0: 281 records across 49 sequences.
- `b1.f`, entry 0: 175 records across 14 sequences.
- `mm1.f`, entry 0: 185 records.

## 4. Example animation sequence

`b1.f`, entry 0, sequence 0 contains eight frames. The first records map to composite groups 7, 8, 9, 10, 11, 12, 13, and 6. Their durations are three units each. X offsets progress across the sequence and the control byte remains zero for these frames.

Reference contact sheet:
- `previews/build214_b1_animation_sequence0.png`

This is a reconstructed reference preview using decoded original sprite resources, not a screenshot from the original game.

## 5. Palette-state mapping

The game-level state field `i.aA:I` is explicitly assigned values 0, 1, and 2 in game-state transitions.

In the original resource initialization method `i.j()`:
- the state is tested for values 1 and 2;
- when either branch is active, its value is passed as the first argument to `f.a(int, int, int, int)`;
- the sprite object's selected-palette field `f.a:I` is then set to the same state value.

This confirms that `aA` acts as a dynamic palette-row selector in this resource initialization path. It does not establish a universal semantic name (such as a specific character skin or game mode) for each value.

## 6. Logical screen and gameplay viewport

Two independent original renderer paths establish the logical dimensions:

1. `i.paint(Graphics)` sets the drawing clip to `(0, 0, 320, 240)`.
2. `c.a(Graphics)` paints the top strip at `(0, 0, 320, 31)` and the bottom strip at `(0, 209, 320, 31)`.

Therefore the central gameplay window is:

- logical canvas: **320×240**;
- top strip: y = 0 through 30;
- gameplay viewport: y = 31 through 208, **320×178**;
- bottom strip: y = 209 through 239.

This directly confirms the project's previously selected gameplay viewport target.

The global `i.paint` method dispatches among multiple game states before invoking state-specific drawing paths. The exact ordering of all background, tile, actor, HUD, and foreground layers remains to be reconstructed from those state-specific branches; Build 214 does not claim that layer ordering is complete.

## 7. Source additions

- `android/src/main/kotlin/com/diamondrush/legacy/LegacySpriteAnimationTable.kt`
  - Typed five-byte animation records and sequence metadata.
  - Preserves raw group index and `0xFF` no-group sentinel.
  - Exposes unsigned frame duration.
  - Decodes signed X/Y offsets.
  - Models incoming flag `0x20`, inherited offsets, and low-nibble XOR.
  - Validates sequence ranges and composite group references.
- `tools/Build214OriginalAnimationAudit.kt`
  - Kotlin runtime audit harness for all original `.f` bundles.
- `research/build214_animation_resource_inventory.csv`
  - Resource-level animation table counts.
- `research/build214_animation_sequence_inventory.csv`
  - Per-sequence frame counts and start indices.
- `research/build214_animation_frame_histogram.csv`
  - Duration and control-byte distributions.
- `research/build214_bytecode/c_build214_full.javap.txt`
  - Full disassembly of original class `c`.
- `research/build214_bytecode/f_build214_full.javap.txt`
  - Full disassembly of original class `f`.
- `research/build214_bytecode/i_build214_full.javap.txt`
  - Full disassembly of original class `i`.

## 8. Validation boundary

- Python regression suite: **69/69 passed**.
- Original bytecode audit: completed for classes `c`, `f`, and `i`.
- All 1,238 frame records accounted for by 188 sequences.
- All 1,235 non-sentinel group references valid.
- All three `0xFF` sentinel frames retained.
- Kotlin source was added but not compiled in this environment because `kotlinc` is unavailable.
- No Android Gradle build, device rendering, original-game visual parity, or playable APK is claimed.

## Next build — Build 215: Gameplay Scene Layer Reconstruction

1. Map the gameplay branch of `i.paint(Graphics)` and its called render helpers.
2. Separate background, map/tile, composite actors, effects, HUD, and overlay draw passes.
3. Trace the 24×24 tile placement and camera offsets against the confirmed 320×178 viewport.
4. Map the five-byte animation sequences to the actual gameplay objects that consume them.
5. Assemble one deterministic gameplay scene at 320×240 using original resource data.
6. Compare object bounds, layer order, and camera movement against original bytecode-derived expectations.

Menu and hint scenes will be handled as separate state branches after the gameplay pass is understood.
