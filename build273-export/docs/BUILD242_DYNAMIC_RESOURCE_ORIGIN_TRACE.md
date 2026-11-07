# Build 242 — Dynamic f[] Resource Origin Trace

## Objective

Trace runtime-created global `f[]` resources in the original `i.j()V` loader to their exact resource bundle, record index, bytecode assignment branch, and serialized payload. This closes the resource-origin gap raised by Build241 without turning CFG candidate unions into unconditional draw commands.

## Confirmed loader streams

### State-10 `/{aA}.f` stream

The loader builds the path `"/" + aA + ".f"`, reads the first byte as record count, then reads `count << 3` directory bytes. The four records map as follows:
- record 0 → `f[60]` only when bit 0 of `d` is set;
- record 1 → `f[16]` only when bit 1 of `d` is set;
- record 2 → `f[42]`;
- record 3 → image cache `b[8]`, not an `f[]` slot.

The original archive contains variants `/0.f`, `/1.f`, and `/2.f`; each has four records.

### `/genN.f` stream

The loader walks 43 global record indices, switching to a new `genN.f` every ten records. For each file it reads a count byte and `count << 3` directory bytes. The record payload length is read from the 4-byte little-endian field at directory offset `1 + 8*localIndex + 4`. The loop's global record index is mapped through the original 0..42 tableswitch.

Important confirmed origins include:
- global record 23 → `f[30]`, `/gen2.f`, local record 3;
- global record 34 → `f[27]`, `/gen3.f`, local record 4.

Additional special cases are retained: records 15 and 17 conditionally create `f[21]` and/or bind `f[4]` according to `bu` bits; record 26 assigns static field `d`, not `f[]`; image-cache destinations remain distinct from sprite-resource slots.

### `/cm.f` stream

The loader reads eight directory records using the same 8-byte header-entry layout:
- record 1 → `f[56]`;
- record 2 → `f[59]`;
- record 3 → `f[13]` and calls `r()`;
- record 6 → `f[43]`.

Other records populate image caches rather than `f[]` slots.

## Build241 candidate join

The three candidate slots from Build241's `bJ=6` CFG evidence now have exact resource origins:

| Global slot | Original bundle | Global record | Local record | Payload bytes |
|---:|---|---:|---:|---:|
| 27 | `/gen3.f` | 34 | 4 | 754 |
| 30 | `/gen2.f` | 23 | 3 | 1,846 |
| 56 | `/cm.f` | 1 | 1 | 1,258 |

All three payloads start with DF03 signature `DF 03 01 01` and were parsed by the existing Kotlin DF03 parser:
- `f[27]`: 11 sprites, 1 palette, 9 colors/palette, ARGB1555 palette, pixel format 5632, no trailing bytes.
- `f[30]`: 11 sprites, 1 palette, 16 colors/palette, ARGB1555 palette, pixel format 5632, no trailing bytes.
- `f[56]`: 6 sprites, 3 palettes, 15 colors/palette, ARGB1555 palette, pixel format 5632, no trailing bytes.

Across all three loader families, the audit covers 63 directory records: 12 from `/{aA}.f` variants, 43 from `gen0.f`–`gen4.f`, and 8 from `cm.f`. All 63 payloads have the DF03 signature, and all bundle length totals exactly match the bytes remaining after each directory.

## Validation

- Python regression: 219 passed, 4 existing Pillow `Image.getdata()` deprecation warnings.
- Kotlin: all production and test Kotlin sources compiled together.
- Kotlin regression runner: Build223–Build242 passed.
- New Kotlin checks parse the three exact original payload fixtures for `f[27]`, `f[30]`, and `f[56]` and verify sprite/palette metadata and zero trailing bytes.

## Evidence boundary

Build242 proves the origin and DF03 structure of the three candidate resource objects. It does **not** prove that every candidate is selected for every `bJ=6` cell, nor that their local sprite indices or transforms have been resolved for each room cell. Conditional flags, dispatch path selection, and the direct `f[42]` six-argument route remain distinct. No full-room raster, Android runtime, screenshot parity, or APK is claimed.
