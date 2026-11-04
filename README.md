# Diamond Rush Android — native port foundation

This is the Android Studio source scaffold for a native port of the supplied
`DMR320x240-Celsius.jar` (MIDP 2.0 / CLDC 1.0).

## Current status

- Android Activity, immersive landscape host and native `SurfaceView` render loop: implemented as a diagnostic shell.
- Viewport geometry: uniform scale, original 320×240 logical frame and expanded horizontal visibility on wide screens.
- Original JAR: preserved unchanged in `reference/` for reverse-engineering; it is not executed by the Android app.
- `.f` asset container extraction: verified. 121 payload sections across 24 resources have been extracted with a reproducible tool.
- Original simulation, level parser, sprite decoder integration, audio, menus and touch controls: not yet ported.
- The current screen is a renderer diagnostic grid, not playable Diamond Rush.

## Open in Android Studio

Open this directory as a Gradle project. It uses Android Gradle Plugin 8.7.3,
compile SDK 35 and min SDK 23. A compatible Android SDK and Gradle installation
are required to build. This environment has not built an APK.

## Architecture direction

1. Keep original game logic/data semantics isolated from Android APIs.
2. Port the original `.f` asset loading rules and sprite composition. The outer
   section table is documented in `docs/ASSET_CONTAINER_FORMAT.md`.
3. Render original 24×24 world tiles with nearest-neighbour filtering and
   original per-frame offsets/transforms.
4. Keep HUD and touch controls in separate screen-space layers.
5. Implement multi-pointer input with independent pointer-to-action tracking.
6. Add expanded horizontal camera visibility only where level bounds permit;
   never stretch or crop sprites.

No APK has been built or tested. This is a source scaffold and renderer
 diagnostic, not a completed port.
- Multi-touch input bridge: implemented as a reusable pointer-to-mask adapter with per-bit reference counts. Gameplay key mapping remains intentionally unassigned pending input-path verification.
- Multi-touch transition logic: standalone regression test passes for shared holds, overlapping masks, independent release and cleanup.

### Build 04 — asset integrity audit

Added `tools/audit_asset_sections.py` and regression tests. The audit re-reads
the original JAR, validates section table bounds/non-overlap, cross-checks the
manifest, and verifies all extracted section bytes exactly. Current result:
121 sections / 24 resources / 250,742 bytes verified. The internal sprite
payload decoder is still a separate unfinished milestone.


## Build 05 — Sprite decoder reverse-engineering

Added `docs/SPRITE_DECODER_RESEARCH.md` and `tools/inspect_sprite_payload.py`. The research traces the original `f` decoder from bytecode: its staged table parsing, sprite dimension lookup, ARGB pixel materialization, alpha handling, and confirmed packed-pixel branches (10225, 5632, 1024, 512). The inspector reports only header fields whose boundaries are currently verified; it deliberately does not claim to decode PNG/Bitmap output.

Validation: the 121-section byte-for-byte asset audit still passes. Example payload `gen0_section_00.bin` reports a first table count of 5 and a following 4-byte-record count of 5, both in bounds. Android bitmap decoding and APK generation remain future work.

### Build 06 — sprite payload corpus probe

Added `tools/audit_sprite_headers.py` to classify payload sections using the
verified initial sprite-decoder table prefix. Of 121 extracted sections, 96
match the prefix and 25 are intentionally left unclassified (many are audio or
other resource types); they are not reported as corrupt. Added regression
tests for valid and truncated headers. All 7 Python tests pass. No sprite
pixels/Android Bitmaps have been decoded yet.

### Build 07 research tools

- `tools/parse_sprite_header.py <payload>`: bounds-checked parser for the
  verified initial three metadata table groups. It deliberately stops before
  unresolved later fields; it is not a sprite or palette decoder.
- Run regression tests with `python -m unittest discover -s tools/tests -v`.

### Build 08 — later metadata boundary investigation

Attempted to extend the sprite metadata parser beyond its verified prefix.
The next count interpretation did not fit the known gen0 fixture, so the
extension was deliberately rolled back. This exposed an unresolved caller /
resource-offset assumption rather than a valid new parser stage. The parser
remains at the verified prefix; no palette or pixel decoding is claimed.
Regression suite: 12 tests pass.

### Build 10 — sprite animation state groundwork

Inspected the original `b` class bytecode and added a platform-neutral Java
`SpriteAnimationState` port for animation selection/reset, per-frame tick
advancement and wraparound, and signed frame-offset accumulation with the two
observed flip bits. A standalone Java test passes 6 checks; the existing Python
suite passes 12 tests. This is not yet wired to decoded sprite metadata or the
Android renderer; the `f` decoder and `SequenceData` adapter remain unfinished.
See `docs/SPRITE_ANIMATION_STATE.md`.

### Build 11 — sprite rendering adapter groundwork

Added `SpriteFrame`, a decoder-independent atlas-frame descriptor,
`SpriteDrawGeometry` for logical placement/origin/animation offsets, and
`AndroidSpriteRenderer` for nearest-neighbour Canvas drawing with alpha and
horizontal/vertical flips. The pure Java geometry test passes 10 checks. The
existing Python regression suite passes 12 tests. The Android Canvas adapter
has not been compiled in this environment (Android SDK unavailable), and no
original `.f` payload has yet been decoded into a Bitmap. See
`docs/SPRITE_RENDER_ADAPTER.md`.

### Build 12 — decoder layout probe

Added `tools/probe_decoder_layout.py` and `docs/DECODER_LAYOUT_PROBE.md`.
The probe mirrors the class-f bytecode's early tables and palette selection,
then checks the cumulative image-offset table. This caught an important false
positive: `gen0_section_00.bin` matches the initial table prefix and palette
stage but its later cumulative offsets exceed the payload length. It is not
safe to treat this section as a complete sprite decoder input. The tool rejects
it explicitly. No pixel decoder, Bitmap output, playable scene, or APK is
claimed. Python regression suite: 15 tests pass; asset audit: 121 payloads / 24
resources / 250,742 bytes match the original JAR byte-for-byte.

## Build 13 — Indexed pixel expansion

Added `engine/IndexedPixelDecoder.java`, a platform-neutral Java implementation
of the six indexed-pixel expansion branches identified in the original `f`
decoder (10225, 5632, 1024, 512, 22018, 22258). It expands a supplied ARGB
palette and pixel byte stream into ARGB pixels with strict bounds checking.

Validation: 11 Java decoder tests passed; the existing Python regression suite
passes 15 tests. This does not yet decode a complete `.f` sprite resource or
produce Android Bitmaps. See `docs/PIXEL_DECODER_BUILD13.md`.

## Build 24 resource foundation

The app now packages the original 24 `.f` resource containers in `app/src/main/assets/original/`. `engine/ResourceSectionReader` extracts one indexed payload using the original little-endian section table format. See `docs/BUILD24_RESOURCE_SECTION_READER.md` for verification and current limitations.


## Build 26 — decoder metadata corpus audit

Build 26 adds `tools/audit_decoder_layout.py` and a machine-readable
`reference/decoder_layout_audit.json`. The audit applies the bounded class-f
metadata probe to all 121 extracted resource sections.

Results: 29 sections have a structurally bounded image metadata/palette/
cumulative-offset layout for this decoder entrypoint; 92 sections remain
unclassified for this entrypoint. Unclassified does not mean corrupt: these
may be non-image sections or use another loader/decoder path.

The 29 accepted sections use palette format value 21781 (0x5515) and include
1–8 images per section. The audit records palette group/color counts and the
number of bytes remaining after the metadata prefix. Those remaining bytes
are NOT yet claimed to be fully decoded pixels. Build 26 does not add a
pixel decoder or claim that original sprites are rendered in the Android app.


## Build 27 — RGB565 palette conversion

Build 27 adds the platform-neutral `Rgb565Palette` utility. It converts an
already-read unsigned 16-bit RGB565 palette word into opaque ARGB8888, using
bit replication when expanding 5-bit and 6-bit channels to 8-bit channels.
It also converts complete arrays of palette words.

Important boundary: this utility does not assume or choose the resource
byte order. The resource reader must supply the word in the byte order
confirmed by the original class-f decoder. Build 27 does not claim that
pixel-data offsets or image dimensions are fully reconstructed, and does
not yet render a decoded original sprite.

Verification:
- RGB565 palette tests: 9 passed.
- Existing indexed pixel decoder tests: 11 passed.
- Java compilation for both platform-neutral test targets succeeded.


## Build 28 — decoded sprite pixel container

Build 28 adds `DecodedSpritePixels`, a platform-neutral validated bridge
between the existing indexed pixel decoder and a future Android Bitmap
adapter. It accepts dimensions, compression mode, a located pixel stream,
and a decoded ARGB palette from its caller; it does not infer these values
from an unverified resource payload.

The class validates positive dimensions and multiplication overflow, invokes
`IndexedPixelDecoder`, retains row-major ARGB pixels, and provides bounds-
checked pixel access. This creates a clean integration boundary for the
Android renderer without pretending that original payload offsets are solved.

Verification:
- Decoded sprite pixel tests: 9 passed.
- RGB565 palette tests: 9 passed.
- Indexed pixel decoder tests: 11 passed.
- Java compilation for these platform-neutral classes succeeded.
- This build does not yet decode a complete original sprite or generate an APK.


## Build 29 — first verified original sprite decode

A resource-specific decoder, `tools/decode_verified_gen0_sprite.py`, now
decodes `reference/sections/gen0_section_04.bin` from the original JAR.
The section's observed metadata is validated before decoding:
- 8 frames, each 24x24 pixels;
- RGB565 palette with 16 colors;
- 4-bit indexed pixel stream;
- metadata ends at byte 238;
- 2,304 pixel bytes (8 x 288 bytes).

The decoder writes eight transparent PNG frames and a nearest-neighbor
contact sheet under `reference/previews/`. The same eight PNGs are copied
into Android `drawable-nodpi` resources for inspection and later integration.
The decoder is intentionally specific to this verified payload; it is not
presented as a universal `.f` parser. Frame identity/animation meaning still
needs mapping against the original game's draw calls.

Verification: all 21 Python tests pass, including three new tests against the
original extracted payload. The Android project still needs an Android SDK
and Gradle build to produce an installable APK; this build does not claim APK
generation or full gameplay integration.


## Build 30 — first original sprite in the Android preview

The Android gameplay preview now loads the eight decoded `gen0_section_04`
PNG frames from `drawable-nodpi`. The moving preview marker displays frames
0–3 as the user moves with the touch HUD, so the original decoded pixel art
is now part of the Android gameplay view rather than only a reference image.

Important: the original class/resource draw-call mapping has not yet proven
the semantic identity of this particular 8-frame group. It is therefore
labelled "ORIGINAL SPRITE SAMPLE" and is not claimed to be the protagonist's
confirmed animation. The cave arena, gem collection and movement simulation
remain a native preview, not original level/gameplay logic.

All 21 Python tests from Build 29 still pass. The eight PNG resources are
included in `app/src/main/res/drawable-nodpi/`. Android SDK/Gradle are not
available in this build environment, so no installable APK is produced.


## Build 31 — deterministic decoded-frame stepping

Build 31 adds `SpriteFrameSequence`, a platform-neutral deterministic
sequence controller with configurable frame count and frame duration.
The Android preview now steps through all eight decoded sample frames when
the user moves with the touch controls and displays the selected frame number.

This is an inspection/preview sequence, not a recovered original animation:
the exact frame order, timing, and semantic association must still be mapped
from the original game's draw/update calls. It intentionally advances on
input rather than running a guessed autonomous animation loop.

Verification:
- SpriteFrameSequence Java tests: 10 passed.
- Existing Python reverse-engineering suite: 21 passed.
- Java sequence class and test compiled successfully.
- No Android APK is produced; Android SDK/Gradle remain unavailable here.


## Build 32 — reproducible APK build workflow

This project now includes `.github/workflows/android-debug-apk.yml`.
After the source archive is pushed to a GitHub repository, the workflow can
build a debug APK on GitHub-hosted Ubuntu using JDK 17, Gradle 8.9, and the
Android Gradle Plugin 8.7.3. It runs on pushes to `main`/`master` and can also
be started manually from the Actions tab. The APK is uploaded as a workflow
artifact named `diamond-rush-android-debug` for 14 days.

This workflow is a build route, not a prebuilt APK. It has not been executed
from this environment and its first hosted run must confirm dependency
resolution and Android compilation. The app remains a native prototype with
original sprite sample integration; original levels and game simulation are
not yet ported.
