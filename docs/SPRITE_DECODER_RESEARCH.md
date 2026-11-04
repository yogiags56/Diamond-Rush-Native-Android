# Sprite decoder research — class `f`

This note records facts verified directly from `f.class` bytecode in the supplied JAR. It is not a completed Android decoder.

## Confirmed decoder stages

1. `f.a(byte[], int)` parses one already-extracted section payload. It begins by advancing the supplied cursor by six bytes, then reads little-endian unsigned 16-bit values (interpreted as signed `short` in the original code) to size/copy several internal tables.
2. The first table length is read at payload offsets 6–7. When positive, that many 16-bit entries are copied from offset 8 into an internal byte table.
3. The next length controls a table of four-byte records. A later table stores per-entry byte and 16-bit values, and a further table stores five-byte records. More header fields follow; a complete field map still needs to be transcribed before writing a replacement parser.
4. `f.a(int,int,int,int)` materializes image groups. For each sprite index it reads width and height from a two-byte-per-entry dimension table, asks the pixel decoder for `width * height` ARGB pixels, then calls `Image.createRGBImage`.
5. The original image constructor's final boolean is selected by scanning decoded pixels: it is true if at least one pixel has an alpha byte other than `0xFF`. Therefore transparency is meaningful and must not be flattened.
6. The private pixel routine `f.a(int)` reads width and height from the sprite-dimension table, obtains the compressed pixel-data offset from a short-offset table, and decodes according to a format code stored in the decoder.

## Confirmed pixel encodings

The bytecode contains explicit branches for format identifiers `10225`, `5632`, `1024`, and `512` (additional branches exist later in the method). These are decoding modes, not resource filenames. At least these branches implement:

- `10225`: run/literal style indexed-color stream. Values above 127 begin a repeated-color run; the next byte selects the palette entry.
- `5632`: two 4-bit palette indices per byte, high nibble then low nibble.
- `1024`: four 2-bit palette indices per byte, from most-significant to least-significant pair.
- `512`: bit-packed 1-bit palette indices (the full loop is in the original method).

Palette lookup is performed before writing each ARGB pixel. The original method reuses a static integer pixel buffer, so an Android implementation should use an owned buffer per decode or a carefully synchronized pool rather than sharing mutable storage across concurrent render/decode threads.

## Android port implications

- Preserve ARGB alpha exactly; do not premultiply or force opaque colors in the decoder.
- Validate `width * height` and every compressed-data read before allocating or indexing.
- Keep the original sprite index and group index stable; animations and composite sprites refer to these indices.
- Keep decoding off the render thread and publish immutable `Bitmap` objects to the renderer.
- Do not infer that every section is an image section. Resource roles and decoder parameters must be traced through the original loader.

## Current milestone

The bytecode-level decode pipeline and several compression branches are now identified. No Android bitmap has yet been produced by a verified replacement decoder, and no APK/gameplay build is claimed.

## Corpus probe — Build 06

Added `tools/audit_sprite_headers.py`, which applies the currently verified
initial-table prefix to every extracted section and labels non-matching entries
as *unclassified*, not corrupt. On the present 121-section corpus, 96 sections
fit this prefix (including the 10 `gen0` sections); 25 do not. Most of those
are audio (`snd_*`) or other resource sections and must be traced to their own
loader before interpretation. This prevents the sprite parser from being
blindly applied to every `.f` payload.

Regression coverage: 7 Python tests pass, including known `gen0` header counts
and truncated-header bounds checks. This remains a structural classifier; it
does not yet decode pixel data or produce Android Bitmaps.

## Verified metadata-prefix parser — Build 07

Added `tools/parse_sprite_header.py`. It independently bounds-checks the first
three table groups read by `f.a(byte[], int)` and stops at the next unresolved
field boundary rather than guessing. On `gen0_section_00.bin` it reports 5
entries in table 0, 5 records in table 1, 1 record in table 2, and a verified
cursor at byte 48. All ten `gen0` section payloads pass this prefix parser.

The parser is intentionally not a full decoder. An attempted extension into
later header fields did not align consistently with the real payload corpus,
so those fields remain unresolved and were excluded. No palette or pixel data
is claimed to have been decoded. The full Python test suite currently passes
11 tests.

## Build 08 — later-header boundary check

A controlled attempt was made to extend the metadata parser beyond the verified
48-byte prefix using the subsequent table-copy sequence in `f.a(byte[], int)`.
It did not validate against `gen0_section_00.bin`: interpreting the next two
bytes as the next table count yields an implausible 32,115-entry table that
cannot fit in the 323-byte payload. The extension was therefore reverted.

This is an important negative result: the later decoder cursor cannot yet be
mapped onto this extracted payload with the current assumptions. Possible
causes include resource-specific loader offsets or a different section role;
these must be resolved by tracing the exact caller and arguments before
extending the parser. The stable parser remains limited to the verified first
three table groups (48-byte cursor in the known fixture). No pixel decoding or
Bitmap output is claimed. Regression suite: 12 tests pass.

## Build 09 — caller/loader trace

Disassembly of the original `i` class confirms the exact resource handoff. The
helper `i.a(String, int)` reads the one-byte section count, reads the `count * 8`
index table, selects the record at `sectionIndex * 8`, reads its little-endian
offset and length, skips to that payload, and returns exactly that payload.
The sprite-loading overload passes the returned byte array at cursor zero to
`f.a(byte[], 0)`, then calls `f.a(group, 0, -1, -1)` for requested groups.

Concrete call sites and resource/section pairs are recorded in
`RESOURCE_CALL_TRACE.md`. In the traced dispatcher, `/mmv.f` sections 0–5,
`/ui.f` section 3, `/0.f` section 3, `/cm.f` sections 2 and 7, and `/ms.f`
section 0 are sent through the sprite loader. `/cr.f` section 0 is also loaded
as raw bytes, not as a sprite decoder input. This is a partial call-site map,
not a complete semantic asset catalogue.

The earlier failed extension of the Python header parser remains unresolved;
this call trace clarifies the resource selection boundary but does not by itself
explain every later header field. The parser remains intentionally limited to
its validated prefix. Full regression suite: 12 tests pass. No Bitmap decode or
APK build is claimed.
