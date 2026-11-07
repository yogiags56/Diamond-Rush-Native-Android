# Diamond Rush Native Android Port — Roadmap Through Build 215

## Completed foundations

- Build 210: original field consumer audit.
- Build 211: native sprite pixel decode validation (1,372/1,372).
- Build 212: composite sprite rasterization baseline.
- Build 213: draw-flag semantics and palette selection; Kotlin/Python raster parity 1,125/1,125.
- Build 214: animation-record layout and 320×178 gameplay viewport confirmation; 69/69 Python tests.
- Build 215: gameplay paint dispatch, viewport/camera setup, 24×24 map-region redraw helper, visible map traversal, multiple render passes, and HUD boundary audit.

## Build 215 findings

- `paint` state `b == 1` dispatches to `D()`.
- `D()` translates the gameplay origin by y=31 and clips to 320×178.
- Camera position is decomposed into 24-pixel tile coordinates and pixel remainders.
- The map renderer scans a 10×16 candidate window, clipped by actual room dimensions.
- The visible map is traversed in at least two distinct passes.
- `G()` is called after returning to the full-canvas origin in the normal path and begins drawing the lower-screen HUD resource `f[0]`.

## Next milestone — Build 216: Tile-ID and Render-Pass Attribution

1. Enumerate every tile-byte dispatch branch in `D()` and its referenced composite/image resources.
2. Correlate map byte/int planes with room initialization and gameplay update methods.
3. Identify the second-pass purpose and its relation to animated objects, actors, and occlusion.
4. Trace `P()` and the state-specific helpers invoked between passes.
5. Produce per-resource/per-tile draw inventory and tests without guessing semantic labels.
6. Only after attribution, define the first deterministic gameplay scene fixture.

## Still pending

- Full gameplay layer/occlusion semantics.
- Animation-to-object ownership mapping.
- Camera motion and room transition parity.
- Deterministic full gameplay scene renderer.
- HUD/menu/hint visual reconstruction.
- Kotlin Android runtime integration and Android Gradle build.
- Device testing, visual parity, and APK.

## Build discipline

The project remains a native Android port, not an emulator wrapper. Logical canvas is 320×240; original gameplay viewport is 320×178 at y=31; tile target is 24×24. Original assets and behavior remain authoritative. Static bytecode analysis and Python reference tests must not be described as device-runtime success.
