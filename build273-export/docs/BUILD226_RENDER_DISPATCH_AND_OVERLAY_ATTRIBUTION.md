# Build 226 — Render Dispatch and Secondary Overlay Attribution

## Scope

Build 226 inspects the two cell loops inside `i.D()` and turns bytecode branch facts into reproducible raw dispatch metadata. It deliberately avoids naming cell IDs as gameplay objects.

## Main visible-cell loop (offsets 609–5988)

The loop scans row values `-1..8` and column values `-1..14` (10×16 candidate positions), then rejects coordinates outside room dimensions. For each in-bounds cell:

- `bG = cI + column` (first/X map dimension).
- `bH = cJ + row` (second/Y map dimension).
- `bI` receives the signed byte from `a:[[B]`.
- `bJ` receives `a:[[I] & 255`.
- `bx = column*24 - cK`; `by = row*24 - cL`.

The `bJ` switch at offset 783 has 35 explicit raw values 3..37. The `bI` switch at offset 2239 has 50 explicit raw values 0..49. The selectors and tables remain separate.

Before the `bI` switch, the method checks `bI == -1`, then applies the JVM `i2b` signed-byte test to `(bI - 80)`; qualifying values jump to the shared tail at 5676. The method also reads `b:[[I` into a local before the switch, but this read is not the selector.

## Shared render tails

- Offset 1995–2201: first-pass queued composite/cached-image draw using `aJ/aK`, then restores the gameplay clip.
- Offset 5676–5976: second queued composite/cached-image draw using `aL/aM`, then resets pending offsets and conditionally draws the current composite.

These tails are recorded separately from switch branch attribution. A switch target equal to a shared-tail offset does not mean “no draw.”

## CFG-based branch attribution

`research/build226_main_dispatch_cfg_attribution.csv` records every explicit case value, target, reachable instruction count before the shared tail, direct constant `a:[Lf;` resource access sites, candidate resource indices, and render-call/cache access counts.

The reachability calculation follows conditional branches, gotos, and nested switches. It computes the union of possible branch paths. Therefore:
- a candidate resource index is reachable from that case, not necessarily used on every execution;
- shared code and conditional alternatives can appear in several case rows;
- raw switch values are not semantic tile names;
- dynamic resource indices are not converted into constants.

## Secondary overlay loop (offsets 6490–6988)

A second 10×16 traversal reads:
- `rawLowByte = a:[[I] & 255`;
- `bytePlaneValue = a:[[B]`;
- packed high-byte/metadata bits from `a:[[I]`.

It continues only for raw low-byte values below 38 or at least 80; values 38..79 are skipped. Within that filter, the exact resource routes are:

| Raw low-byte condition | Resource | Frame/index calculation |
|---|---:|---|
| 20..25 | `f[3]` | `rawLowByte - 20`; animation phase uses `(aS >> 2)` and the selected frame duration |
| 31 | `f[15]` | packed high byte; animation phase uses `(aS >> 1)` and frame duration |
| 32 | `f[16]` | packed high byte masked to 8 bits |
| 36 | `f[20]` | `((highByte - 1) * 7) / 16` |
| 80..207 | `f[42]` | `(rawLowByte - 80)` converted to signed byte; nonnegative required |

The default path computes `(rawLowByte - 80)` and applies `i2b`; a negative signed result skips `f[42]`. Thus 208..255 do not draw through that path.

Two independent supplemental branches follow:
- `((packedCellValue & 0xF0000000) >> 28) > 0` draws `f[13]`.
- `bytePlaneValue == 54` draws `f[7]` using the integer-plane value through the helper.

No semantic names are assigned to these IDs or resources.

## Implementation

- `LegacyRenderDispatchCatalog.kt`: exact main switch offsets and 85 raw case/target pairs, secondary overlay route descriptors, supplemental resource conditions.
- CSV inventories in `research/` preserve the CFG evidence and exact overlay conditions.
- Standalone Kotlin checks cover case counts/edge entries and overlay routing boundaries.
- Python tests verify all case values, numeric route tables, and independent supplemental overlays.

## Validation boundaries

Python tests and archive integrity are recorded in the build files. Kotlin compilation is attempted only if `kotlinc` is present. No Android Gradle build, device runtime, visual parity, or APK is claimed.

## Next — Build 227

Connect the now-attributed resource/frame selectors to the existing `LegacySpriteResource` and `LegacySpriteAnimationTable` abstractions through a typed, evidence-backed resolver. Keep the first-pass queued composites, second-pass queued composites, and secondary overlay pass separate. Add fixture-driven trace output before drawing any actual scene.
