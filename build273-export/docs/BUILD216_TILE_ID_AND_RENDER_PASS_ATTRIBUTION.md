# Build 216 — Tile-ID and Render-Pass Attribution

## Scope

This milestone continues the static bytecode reconstruction from Build 215. It identifies the two tile/cell dispatch switches in `i.D()` and records their explicit case values, branch targets, and conservative direct references to the original `f[]` composite-resource table.

This is **not** a semantic tile catalogue yet. A numeric cell value is retained as a raw dispatch ID; it is not renamed as a wall, gem, enemy, exit, water, or other game object unless a separate producer/consumer trace proves that meaning.

## 1. Two distinct dispatch domains

- First visible-cell pass: switch at bytecode offset `783`, dispatches the value held in instance field `bJ`, with 35 explicit cases (3–37).
- Second visible-cell pass: switch at bytecode offset `2239`, dispatches the value held in instance field `bI`, with 50 explicit cases (0–49).

The two switches are not interchangeable. Their input fields and surrounding code differ. The first pass also includes a preceding special branch for values outside the 3–37 switch interval; the second pass first checks a low-byte value and then dispatches values 0–49.

## 2. First-pass branch facts

The first-pass switch includes special direct composite calls at several branches. For example, case 34 reaches a direct call to `f[27]`; cases 14 and 33 derive an animation/resource selector from the high byte of the integer map plane and select `f[8]` or `f[22]`. Case 6 performs state/neighbor checks and can alter the object's draw position before continuing to later common rendering logic.

These are control-flow facts, not final gameplay labels. Resource-table index use can be conditional, and a branch can jump to shared code.

## 3. Second-pass branch facts

The second-pass switch has 50 explicit case values (0–49). It includes distinct paths for values such as 49, 48, 46, 45, 44, 36, 34, 32, 31, and 30, while many values share the default path. Several branches invoke `f[]` entries directly. Case 30 selects `f[20]`; cases 22 and 23 select `f[12]` and call the byte-parameter helper with distinct values (22 and 23). Cases 31, 32, and 36 have separate animation/resource paths. The generic path can resolve an index into `f[42]` for values at or above 80 after subtracting 80 and converting to a signed byte.

The second pass also reads the upper metadata nibble of the integer plane (`value & 0xF0000000`) and, when nonzero, invokes `f[13]`. A byte-plane value of 54 triggers an additional `f[7]` call. These are additional per-cell draw operations, not standalone tile-ID meanings.

## 4. Direct resource attribution inventory

The CSV `research/build216_tile_dispatch_attribution.csv` records each switch case and a deliberately conservative local branch-window scan. It found 23 first-pass cases and 28 second-pass cases with direct `f[]` table references in their bounded branch windows.

The local scan is only a navigation aid: compiler-generated branches can jump over the next case target, and shared blocks can be reached from multiple cases. Therefore the CSV's `direct_f_resource_indices` must not be treated as a complete control-flow graph or as an exclusive one-to-one mapping.

## 5. Important data-plane distinction

The renderer reads multiple cell planes:
- `a:[[B]` (byte plane), used for cell values and special value checks;
- `a:[[I]` (integer plane), used for low-byte dispatch values and packed metadata/high-byte selectors.

The bytecode demonstrates that the integer plane is not merely an independent tile ID. Its packed high bits are consumed for additional rendering metadata. Preserve the complete integer value when reconstructing map cells; do not discard it after extracting the low byte.

## 6. Confirmed render ordering update

Build 215 established:
1. camera setup and exposed-strip redraw;
2. first visible-cell pass;
3. `P()` and conditional state/effect calls (`O()`, `M()`, `N()`, or `L()`);
4. second visible-cell pass;
5. viewport restoration and HUD `G()`.

Build 216 adds dispatch-domain evidence but does not yet resolve the semantic identity of every cell value, the exact actor/effect ordering inside the first pass, or full occlusion behavior.

## 7. Next milestone — Build 217

1. Trace map-plane initialization and map-cell writes to identify the producers of `a:[[B]` and `a:[[I]`.
2. Trace mutation sites for representative values (including 6, 14, 20–25, 31, 32, 34, 36, 49, and byte-plane 54).
3. Resolve the high-byte/packed metadata layout without losing unknown bits.
4. Build a control-flow-aware branch graph instead of relying on local instruction windows.
5. Only then assign semantic names and create a deterministic scene fixture.

## Validation boundaries

- Static bytecode extraction and switch-table consistency checks: performed.
- Python regression tests: see `BUILD216_TEST_RESULTS.txt`.
- Kotlin compilation: not performed.
- Android Gradle build, emulator/device runtime, original-game visual parity, and APK: not performed.
