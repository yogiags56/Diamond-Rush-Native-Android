# Build 13 — Indexed pixel expansion

## What was implemented

`app/src/main/java/com/example/diamondrush/engine/IndexedPixelDecoder.java` is a
platform-neutral Java port of the six pixel-expansion branches in the original
`f` class's image decode routine. It accepts a decoded ARGB palette and a
bounded byte stream and returns ARGB pixels. It deliberately does not parse
resource containers, build palettes, infer image dimensions, or create Android
`Bitmap` objects.

## Modes confirmed in original bytecode

| Original mode word | Expansion |
|---:|---|
| 10225 | RLE: token 0–127 is one literal palette index; 128–255 repeats the following palette index `token - 128` times |
| 5632 | Two 4-bit palette indices per byte, high nibble first |
| 1024 | Four 2-bit palette indices per byte, most-significant pair first |
| 512 | Eight 1-bit palette indices per byte, most-significant bit first |
| 22018 | One palette index per byte |
| 22258 | RLE variant: token 0–127 is followed by one literal palette index; 128–255 repeats the following palette index `token - 128` times |

The implementation rejects truncated streams, out-of-range palette indices,
unsupported modes, and packed-mode pixel counts that are not aligned to the
number of pixels represented by one byte. The strict alignment is intentional:
the original branches write a full packed group each iteration.

## Verification

- `IndexedPixelDecoderTest.java`: 11 standalone Java tests passed.
- Existing Python regression suite: 15 tests passed.
- The Java test covers raw indices, all packed widths, both RLE variants,
  truncated data, invalid palette indices, and unsupported modes.

## Not yet achieved

This is a verified pixel-expansion component, not a complete resource decoder.
The original resource loader's call context, palette construction, image
metadata/offset tables, and pixel stream boundaries still need to be joined
before a real game sprite can be decoded. No Android Bitmap or playable APK has
been produced by this build.
