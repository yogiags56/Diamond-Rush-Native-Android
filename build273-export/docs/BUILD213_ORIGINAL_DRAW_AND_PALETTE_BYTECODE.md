# Build 213 — Original `f.class` draw and palette evidence

## Audited method signatures

- `a(Graphics, int, int, int, int)` — leaf sprite drawing.
- `a(Graphics, int, int, int, int, int, int)` — composite group traversal.
- `a(int, int, int, int)` — palette image preloader / palette selection.
- `a(int)` — one of the sprite-table accessors; not the palette setter.

## Composite recursion and flag propagation

In the composite renderer, the control byte is read from the fourth byte of each four-byte component record. The renderer computes `drawFlags = incomingFlags XOR (control & 0x0F)`.

For a nested group (control bit `0x10` set), the recursive invocation receives `drawFlags`, not the unchanged incoming flags. The Build 207/212 resolver had retained the old incoming flags on this recursive edge. Build 213 corrects that propagation. The component X/Y offsets are still evaluated using the incoming flags before the XOR, matching the bytecode order.

For a leaf sprite, the renderer calls the leaf draw method with the same XOR-adjusted flags.

## Leaf draw transform

The leaf method checks bit 0 and bit 1 of its flags and passes the resulting integer `flags & 3` directly to `Graphics.drawRegion`.

The MIDP 2.0 constants are:
- 0 = `TRANS_NONE`
- 1 = `TRANS_MIRROR_ROT180`
- 2 = `TRANS_MIRROR`
- 3 = `TRANS_ROT180`

Important correction: the initial Build 213 progress note incorrectly described value 1 as `TRANS_MIRROR_ROT90`. That was wrong. The official MIDP constant is value 7; value 1 is `TRANS_MIRROR_ROT180`. The implementation in this build uses the correct values.

For the four values emitted by this game, the pixel mappings are:
- 0: unchanged.
- 1: mirror horizontally, then rotate 180°; equivalent to vertical flip.
- 2: reflect about the vertical center; horizontal flip.
- 3: rotate 180°; both axes reversed.

All four preserve source width and height.

## Palette selection

The `a(int, int, int, int)` method:
- stores its first integer argument in field `a:I` as the selected palette index;
- temporarily sets that field while decoding/cache-building images;
- iterates sprite indices from zero through its third integer argument;
- restores the previous palette index afterward.

The second and fourth integer arguments are not read in the audited method body. The selected palette index is therefore caller-controlled state, not an intrinsic property of each composite group. Build 213 exposes it as an explicit argument to `LegacySpritePaletteSelector.decodeSprites`.

## Group auxiliary table

The four-byte-per-group `a:[B` table is not read by the audited composite traversal or leaf drawing methods. Its semantic role remains unresolved; it is preserved as opaque data and is not repurposed as a transform or palette table.
