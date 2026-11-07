# Build 245 — Render Callsite Descriptor Provenance

## Goal

Advance Build244's cell/resource candidate join by inventorying exact sprite-render invocation points in original `i.D()V` bytecode.

## Exact result

`research/build245_render_callsite_provenance.csv` records 60 renderer-related invocation sites. Among them are 25 calls to the sprite object's overloaded `f.a(Graphics, ...)` methods:
- 16 calls with descriptor `(Ljavax/microedition/lcdui/Graphics;IIIIIII)V` (seven integer arguments after the Graphics reference);
- 9 calls with descriptor `(Ljavax/microedition/lcdui/Graphics;IIIIII)V` (six integer arguments after the Graphics reference).

The exact bytecode offsets and nearby original `javap -c -p i` excerpts are stored in:
- `research/build245_render_callsite_provenance.csv`
- `research/build245_render_callsite_bytecode_excerpts.txt`

Kotlin mirror: `LegacyRenderCallsiteProvenance.kt`.

## Evidence boundary

This milestone proves invocation locations and JVM method descriptors only. It does not prove the runtime receiver's global `f[]` slot, composite group, sprite index, palette, or actual argument values. Those are marked unresolved. The static descriptor count must not be confused with runtime argument provenance. Build244 candidate rows remain candidate-only and are not sent to the rasterizer.

## Validation

- Python regression suite: 229 passed, 4 existing Pillow deprecation warnings.
- All Kotlin production and test sources compiled together.
- Kotlin regression runner through Build245 passed, including the Build242 DF03 fixtures and Build243 composite checks.

## Next: Build246 — Producer-to-Call Stack Slice

Select a small number of callsites whose control-flow predecessors are bounded and reconstruct the operand stack backward from each invocation. Preserve all branches and merge points. Resolve receiver and argument expressions only where the producer chain is complete; otherwise retain explicit unknown values. Prioritize the first main-pass calls near offsets 960, 1057, 1526, 1950, and 2054, then trace the shared tail and direct six-argument path separately.

## Not performed

No Android Gradle build, device runtime, complete room rasterization, screenshot parity, or APK packaging is claimed.
