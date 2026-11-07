# Build 224 — Logical Canvas, Camera, and Render Scaffolding

## Objective

Introduce the evidence-backed 320×240 logical surface and gameplay viewport, preserve the original camera's tile/pixel decomposition, keep the two render dispatch selectors independent, and provide a conservative visible-cell candidate iterator plus a deterministic clipped pixel surface.

## Evidence basis

Build 215's original `i.class` bytecode audit establishes:
- full logical canvas clip: 320×240;
- gameplay origin translation: `(0, 31)`;
- local gameplay clip: `(0, 0, 320, 178)` after translation, i.e. canvas rectangle `(0,31,320,178)`;
- tile size: 24;
- camera decomposition: `cI=a/24`, `cJ=b/24`, `cK=a%24`, `cL=b%24`;
- visible candidate loops: rows `-1..8`, columns `-1..14`;
- per-cell screen placement: `column*24-cK`, `row*24-cL`;
- distinct selectors `bJ` (35 switch cases) and `bI` (50 switch cases).

## Implemented

`LegacyGameplayViewport.kt` adds:
- named logical canvas, gameplay viewport, and tile constants;
- raw camera pixel offsets with tile and sub-tile decomposition;
- separate raw `bJ`/`bI` selectors and case-count metadata;
- 160-candidate visible-cell scan with in-bounds flags, preserving room dimension orientation;
- minimal deterministic ARGB logical surface with explicit clip-aware blitting.

## Conservative choices / limitations

- Candidate map coordinates are not wrapped. Build 215 proves map-dimension checks and tile traversal, while full wrap semantics are handled in a separate map-region redraw helper; this scaffold intentionally reports out-of-range candidates rather than inventing wrapping.
- Selector values remain raw integers. No semantic labels or cross-domain enum was introduced.
- The surface blitter copies non-transparent pixels; it is a testable compositing scaffold, not yet a full reproduction of MIDP Graphics blend/clip state or original pass ordering.
- No fake tile art, guessed tile IDs, actor ordering, or gameplay behavior is added.
- Camera offsets remain raw signed pixel values and use Kotlin/JVM integer `/` and `%`, matching the original bytecode's `idiv`/`irem` truncation-toward-zero behavior for negative offsets.

## Tests

- Standalone Kotlin checks cover viewport bounds, camera decomposition, candidate count/coordinates, selector independence, and clipping.
- Python source-contract tests cover constants, independent selectors, camera decomposition, traversal bounds, and clip-aware blitting.

## Validation boundaries

This milestone adds source and deterministic contract tests. It does not claim Kotlin compilation unless the standalone compiler check recorded below succeeds. It does not claim Android Gradle integration, emulator/device runtime, original-game visual parity, or APK output.

## Next — Build 225

Trace the camera update and redraw-strip callers against the original bytecode, then tighten coordinate orientation and map boundary behavior. In parallel, decode the two visible-cell passes without assigning speculative layer names; connect only the branches whose resource and animation indices are proven.
