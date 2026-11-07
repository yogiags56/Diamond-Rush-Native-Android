# Build273 — Exact selector dataflow trace

## Scope

Build272's W0 room0 candidate join treated CFG-reachable `f[]` accesses as a
union of possibilities. Build273 traces the six selector values actually
present in the 90 in-bounds W0 room0 cells through the main renderer's
`bJ` switch and the subsequent `a(int)` resource-index resolver.

Bytecode source: `research/build214_bytecode/i_build214_full.javap.txt`.

- Cell selector load: renderer bytecode offsets 692–729. The low byte of
  `a[[I]][bG][bH]` is stored in `bJ` (`iand 255`).
- Main selector switch: offsets 779–935, `tableswitch` at 783.
- Relevant case bodies: 3→1890, 4→1549, 5→1632, 6→1064, 7→1416, 8→1796.
- Dynamic draw resolver: `public static int a(int)`, bytecode offsets 0–206.
- Dynamic draw call: offsets 2017–2055 invoke `a(aJ)` and use its return value
  as the `f[]` index when the cached-image path is not used.

## Results

- 90 room cells traced, 15 per selector.
- Six raw selector values: 3, 4, 5, 6, 7, 8.
- Selector 4 sets `aJ=20` when the cell high-byte meets `this.aC`; helper
  `a(20)` returns resource slot `f[43]`.
- Selector 7 sets `aJ=4`; helper `a(4)` returns `f[56]`. The same case also
  contains a separate direct `f[56]` draw at offset 1501, guarded by the
  left-neighbor low byte not being 8 or 9. These are two distinct draw paths.
- Selector 8 sets `aJ=23`; helper `a(23)` returns `f[45]`.
- Selector 3 can set `aJ=12`; helper default returns -1. Selector 6 sets
  `aJ=26`; helper default returns -1. Selector 5's case body is diagnostic
  output only and does not assign a new `aJ`.
- For these six W0 room0 selectors, no case path proves `f[27]` or `f[30]` as
  the selected resource. Their appearance in Build272's candidate union was
  caused by treating a CFG-reachable union as an exclusive per-case selection.

## Interpretation and limits

This resolves selector-to-`f[]` index dataflow where the bytecode proves it;
it does **not** identify the resource bundle/file loaded into every `f[]` slot.
The selector 4 result depends on the runtime comparison against `this.aC`.
Selector 7's direct draw depends on a left-neighbor value. The runtime values of
those predicates, `aJ`-dependent animation/frame values, cache state, and
actual resource contents are not executed or decoded here. The `f[43]`,
`f[45]`, and `f[56]` indices are exact bytecode-level results, not claims about
resource filenames or rendered pixels.

The new per-selector and per-cell CSVs retain the unresolved resource identity
and runtime predicate values explicitly. No candidate resource path is
promoted to a proven runtime asset.

## Files

- `research/build273_selector_dataflow_trace.py`
- `research/build273_selector_dataflow_trace.csv`
- `research/build273_w0_room0_cell_selector_resolution.csv`
- `tests/test_build273_selector_dataflow_trace.py`

## Validation boundary

This is static bytecode dataflow tracing and CSV generation. It does not execute
the original J2ME game, compile Kotlin or Android, render a room, validate
visual parity, or produce a playable APK.
