# Build 215 — Gameplay Scene Layer Reconstruction (Bytecode Audit)

## Scope and evidence

Build 215 audits the original `i.class` rendering path in `research/build214_bytecode/i_build214_full.javap.txt`, using the original JAR already retained in this repository. This is a static bytecode reconstruction. It does not claim Android runtime rendering, device parity, or a finished gameplay renderer.

## 1. Gameplay dispatch

`i.paint(Graphics)` first applies a 320×240 clip and dispatches on static byte field `b`. The switch case `1` branches to offset 2804, which invokes private `D()`. This establishes `D()` as the gameplay paint path for state value 1. Other states dispatch to separate menu, transition, loading, or overlay methods; they must not be mixed into the gameplay scene pipeline.

## 2. Gameplay viewport and camera

At entry, `D()`:

1. Retains the current `Graphics` and reads the frame counter `aS`.
2. Computes `bQ` from a flag in `k` and `l`.
3. Calls `Graphics.translate(0, 31)`.
4. Resets `bk` and calls `C()`, whose body sets clip `(0, 0, 320, 178)`.
5. Derives camera tile coordinates and pixel remainders:
   - `cI = a / 24`
   - `cJ = b / 24`
   - `cK = a % 24`
   - `cL = b % 24`

The 31-pixel translation plus the 320×178 local clip matches Build 214's independently established gameplay viewport at canvas y=31..208. The camera is therefore represented in tile coordinates plus sub-tile pixel offsets, with a 24-pixel tile unit.

## 3. Map-region redraw helper

Private `a(int,int,int,int,boolean)` is a map-region painter. It iterates in 24-pixel increments, wraps map indices using the map dimensions (`cC`, `cD`), reads the map's byte and integer planes (`a:[[B]`, `a:[[I]`), and draws the base tile image from `b[8][0]` when the byte-plane value is below 80. It also handles cell-specific tile/composite cases, including references into the `a:[Lf;` resource table and cached images in `b:[[Image;`.

`D()` computes camera-aligned boundaries and invokes this helper for exposed horizontal/vertical strips when the camera crosses a tile boundary. The calls are not a one-time full-map draw: they are incremental redraws to keep the scrolling background aligned with camera movement.

## 4. Visible map-cell traversal

After camera setup, `D()` performs a bounded visible-cell traversal. The loop indices range from -1 through 8 for rows and -1 through 14 for columns (10×16 candidate cells), with explicit checks against map width (`e`) and height (`f`). For each in-bounds cell it loads:

- `bI` from byte map plane `a:[[B]`;
- `bJ` from the low byte of integer map plane `a:[[I]`;
- `bx = column*24 - cK` and `by = row*24 - cL`.

It then dispatches by tile/cell values and metadata. The bytecode contains distinct cases for static composite groups, cached animation images, animated composite frames, and clipping behavior. Values are retained as raw IDs in this audit; semantic names are not assigned without further evidence from map construction and update consumers.

The first traversal is not the only scene pass. After it completes, `D()` calls `P()` and performs additional conditional rendering and state-specific actor/effect work. A second traversal of the visible map region begins at bytecode offset 6490, proving that the renderer separates at least two passes over the same map area. The second pass must be analyzed independently before assigning definitive labels such as foreground, actors, or occlusion layer.

## 5. Scene tail and HUD boundary

In the normal branch, after the map/effect/actor passes, `D()` restores the canvas clip, translates by `(0, -31)`, and calls `G()` when no separate `c` overlay object is present. `G()` translates to the lower screen strip and draws resource `f[0]` plus additional HUD-related images and indicators. This establishes a clear boundary between the gameplay viewport pass and a later full-canvas HUD pass.

The debug/alternate branch guarded by static boolean `a:Z` has a different tail and must be treated separately; it is not used as evidence for the normal frame order.

## 6. Evidence-backed scene pipeline (partial)

For state `b == 1`, the confirmed high-level sequence is:

1. `paint`: establish 320×240 canvas clip and dispatch state 1.
2. `D`: translate gameplay origin down by 31 pixels; apply 320×178 viewport clip.
3. Camera/tile-boundary calculations; redraw exposed map strips via `a(IIIIZ)`.
4. First visible-cell traversal: base map tile and cell-specific rendering/animation handling.
5. `P()` and conditional map/effect/state work.
6. Second visible-cell traversal and additional per-cell rendering.
7. Finish gameplay viewport, restore canvas origin/clip.
8. `G()` HUD path (subject to overlay/state conditions).

This is a partial high-level order. Exact sub-layer names, actor ordering, animation ownership, and overlap/occlusion semantics remain open.

## 7. Next work

1. Decode the two visible-cell passes by mapping each tile ID branch to the original resource/animation table and to map update code.
2. Identify the purpose and draw ordering of `P()`, `E()`, `F()`, `O()`, `M()`, `N()`, `L()`, and `G()` using callers and field consumers.
3. Trace camera update methods and validate camera offsets against actual room/map dimensions.
4. Build a deterministic 320×240 reference scene only after room data, map resource indices, and draw ordering are grounded.
5. Add object-bound and overlap tests; only then move the reconstructed passes into Android Kotlin runtime code.

## Validation boundaries

- Static bytecode assertions: covered by Build 215 tests.
- Python test suite: run and reported in `BUILD215_TEST_RESULTS.txt`.
- Kotlin compilation: not performed in this milestone.
- Android Gradle build, emulator/device runtime, visual parity, and APK: not performed.
