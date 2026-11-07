# Build 225 — Camera Motion and Redraw-Strip Reconstruction

## Scope

This milestone traces original `i.D()` camera calculations and its calls to `a(int,int,int,int,boolean)`. It adds a deterministic Kotlin planner for the aligned redraw rectangles and corrects the visible-cell map-coordinate orientation in the Build 224 scaffold.

## Bytecode facts

From `research/build214_bytecode/i_build214_full.javap.txt`, method `private void D()`:

1. Camera pixel offsets are instance fields `a` (X) and `b` (Y).
2. The source derives:
   - `cI = a / 24`, `cJ = b / 24`;
   - `cK = a % 24`, `cL = b % 24`.
3. Aligned world-pixel bounds are calculated as:
   - `left = a - cK`;
   - `top = b - cL`;
   - `rightEdge = a + cC - 24`, then `right = rightEdge - (rightEdge % 24)`;
   - `bottomEdge = b + cD - 24`, then `bottom = bottomEdge - (bottomEdge % 24)`.
4. The first frame calls `a(left, top, right, bottom, false)` and caches these four bounds in `cE/cF/cG/cH`.
5. When the aligned X bounds change, D() calls the helper for only the newly exposed vertical strip. Moving right starts at `oldRight + 24`; moving left ends at `oldLeft - 24`.
6. When the aligned Y bounds change, D() calls the helper for only the newly exposed horizontal strip. Moving down starts at `oldBottom + 24`; moving up ends at `oldTop - 24`.
7. X and Y changes are evaluated independently, so a diagonal tile-boundary crossing can emit two redraw strips.
8. The helper `a(IIIIZ)` iterates in 24-pixel increments, reads `a:[[B]` and `a:[[I]`, and checks cell coordinates against `e` and `f`. Its screen-space tile origins begin at `(x1 % cC)-24` and `(y1 % cD)-24`, then advance by 24. Screen coordinates wrap at the map pixel extent; cell coordinates are separately checked against map dimensions.
9. D() then derives viewport wrap coordinates using `a % cC`, `b % cD`, `(a+320) % cC`, and `(b+178) % cD`. The subsequent Graphics helper argument patterns are retained in the bytecode audit; their visual source/destination semantics are not assigned in this milestone.

## Vertical camera step

At D() bytecode offsets 48–109:
- if `bj > 0`, calculate `bk = ((bj * aS) % ((bj >> 1) + 1)) % 12`;
- clamp `bk` to `b` when `bk > b`;
- update `b = b - bk`.

`LegacyCameraMotion.applyVerticalStep` mirrors this integer expression. Kotlin `Int` arithmetic retains JVM 32-bit overflow behavior. The formula is preserved as observed; its design intent is not inferred.

## Corrected visible-cell coordinate orientation

Build 224's initial candidate iterator had X/Y dimension axes reversed. The original D() loop proves:
- outer column index contributes to `bG = cI + column`, checked against `e` (first room dimension);
- inner row index contributes to `bH = cJ + row`, checked against `f` (second room dimension).

Build 225 corrects this to:
- `mapFirst = camera.tileX + column`;
- `mapSecond = camera.tileY + row`.

Screen positions remain `column*24-cK` and `row*24-cL`.

## Implementation

- `LegacyCameraRedrawPlanner.kt`: aligned bounds, stateful initial/X/Y strip plan, exact vertical camera-step formula.
- `LegacyGameplayViewport.kt`: corrected map dimension orientation.
- Kotlin standalone checks: initial full region, X strip, Y strip, diagonal crossing, reverse movement, stable camera, smoothing expression, and coordinate orientation.
- Python source-contract tests: bytecode formula and orientation invariants.

## Deliberate limitations

- This is a planner, not a tile renderer. It returns the world-pixel rectangle arguments for the proven map-region helper.
- It does not invent semantics for the later `Graphics` wrap/copy helper calls.
- Map edge handling, negative camera offsets, map sizes smaller than the viewport, and multiple-wrap jumps require separate fixture/reference validation.
- The `cC/cD` values are treated as map pixel extents because the bytecode uses them as modulo divisors and aligned redraw bounds; no UI labels or gameplay meaning are attached.
- No full scene rendering or tile semantics are added.

## Validation boundaries

The Python suite result and Kotlin tool availability are recorded in `BUILD225_TEST_RESULTS.txt` and `BUILD225_KOTLIN_VALIDATION.txt`. No Android Gradle build, device runtime, visual parity, or APK is claimed.

## Next — Build 226

Decode the two visible-cell passes at bytecode offsets 609–5988 and 6490 onward. Build a branch-to-resource/frame attribution table using full control-flow edges and exact `f[]`/cached-image accesses. Keep raw dispatch IDs and avoid assigning layer names until producer/consumer evidence supports them.
