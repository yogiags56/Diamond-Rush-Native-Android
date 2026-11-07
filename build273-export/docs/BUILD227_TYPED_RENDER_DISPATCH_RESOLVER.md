# Build 227 — Typed Render Dispatch and Animation Resolver

## Scope

Build 227 adds an executable pure-Kotlin decision layer over the raw bytecode metadata from Build 226. It connects the two main selector domains, secondary overlay routing, the five-byte animation table, and the existing composite object resolver.

It does not claim a complete renderer and does not assign semantic names to numeric cell IDs or resource indices.

## Main pass selectors

`LegacyRenderCellSample` preserves three separate values:
- `integerPlaneLowByte`: the unsigned low byte of the packed integer map plane;
- `signedBytePlaneValue`: the signed JVM byte from the serialized byte map plane;
- `packedIntegerPlaneValue`: the full integer value for packed metadata.

The first main pass (`bJ`) selects one of 35 explicit switch cases. Unknown values go to the shared tail at offset 1995.

The second main pass (`bI`) reproduces the bytecode prechecks:
1. `-1` skips the current cell to offset 5976.
2. `(bI - 80).toByte().toInt() >= 0` bypasses the switch and enters the shared tail at 5676.
3. Otherwise, values 0..49 use their explicit switch targets; all other values take the default shared tail.

The narrowing step is deliberately JVM signed-byte behavior, not an ordinary integer comparison.

## Secondary overlay pass

The secondary traversal considers only raw low-byte values `<38` or `>=80`. The existing Build 226 catalog then identifies specific resource routes.

For animation-table routes, Build 227 resolves the sequence and frame expressions:
- Resource `f[3]`: sequence `rawLowByte - 20`, frame `(aS >> 2) % frameCount`.
- Resource `f[15]`: sequence `packedIntegerPlaneValue >> 8`, frame `(aS >> 1) % frameCount`.
- Resource `f[16]`: sequence 0, frame `(packedIntegerPlaneValue >> 8) & 255`.
- Resource `f[20]`: sequence 0, frame `((packedIntegerPlaneValue >> 8) - 1) * 7 / 16`, using JVM/Kotlin truncation toward zero.

Resource `f[42]` is kept separate. Bytecode calls a six-int overload with the signed-byte-narrowed `(rawLowByte - 80)` value. The resolver calls this an opaque direct draw argument, not an animation frame or a composite sequence.

Missing animation tables, invalid sequence indices, zero-frame sequences, and invalid frame indices fail explicitly instead of silently substituting another route.

## Composite integration

`resolveCompositeOverlay()` takes a resolved animation selection, the corresponding `LegacySpriteAnimationTable`, and `LegacySpriteCompositeSection`. It applies the existing frame placement rules and expands the frame's composite group through `CompositeSpriteObjectResolver`.

The `0xFF` no-group sentinel yields no leaf commands. Rasterization remains a later operation because actual decoded resource assets are not bound to this numeric resolver yet.

## Supplemental resources

The two post-branch conditions remain independent:
- high packed nibble arithmetic-shifted right 28 is positive → resource 13;
- signed byte-plane value equals 54 → resource 7.

The arithmetic shift is intentional: high nibbles 8..15 produce a negative signed result and do not satisfy the positive test.

## Build 226 source correction

The inherited generated `LegacyRenderDispatchCatalog.kt` contained literal `\\n` text between case rows, which would make it invalid Kotlin. Build 227 repairs this to actual line breaks and adds a regression test. The archive now contains the corrected source.

## Validation boundaries

Python tests: 152 passed, 4 Pillow deprecation warnings.

Kotlin test source was added, but `kotlinc` is not installed in this environment; therefore the Kotlin tests were not compiled or executed. No Android Gradle build, device runtime, visual parity, or APK is claimed.

## Next — Build 228

Add a deterministic trace layer that records, per visible cell:
- logical map coordinates and raw plane values;
- first and second main-pass decisions;
- secondary overlay route and selected sequence/frame or opaque draw argument;
- supplemental resource conditions;
- composite group expansion and resulting leaf commands.

Use synthetic fixtures and compare trace output against the bytecode-derived expected paths before attempting real room rendering.
