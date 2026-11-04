package com.example.diamondrush.engine;

/**
 * Strict, platform-neutral port of the indexed-pixel expansion branches in
 * the original Diamond Rush class f. Palette construction and image geometry
 * are intentionally handled by the caller; this class only expands indices
 * into ARGB pixels.
 */
public final class IndexedPixelDecoder {
    public static final int MODE_RLE_INDEXED = 10225;
    public static final int MODE_4BIT = 5632;
    public static final int MODE_2BIT = 1024;
    public static final int MODE_1BIT = 512;
    public static final int MODE_RAW_INDEXED = 22018;
    public static final int MODE_RLE_INDEXED_ALT = 22258;

    private IndexedPixelDecoder() {}

    public static int[] decode(int mode, byte[] source, int offset,
                               int pixelCount, int[] palette) {
        if (source == null || palette == null) throw new IllegalArgumentException("null input");
        if (offset < 0 || pixelCount < 0 || offset > source.length)
            throw new IllegalArgumentException("invalid source range or pixel count");
        if (palette.length == 0) throw new IllegalArgumentException("empty palette");
        int[] out = new int[pixelCount];
        Cursor c = new Cursor(source, offset);
        switch (mode) {
            case MODE_RLE_INDEXED:
            case MODE_RLE_INDEXED_ALT:
                decodeRle(mode, c, out, palette);
                break;
            case MODE_RAW_INDEXED:
                for (int i = 0; i < pixelCount; i++) out[i] = color(palette, c.u8());
                break;
            case MODE_4BIT:
                requireMultiple(pixelCount, 2, "4-bit");
                for (int i = 0; i < pixelCount; i += 2) {
                    int b = c.u8();
                    out[i] = color(palette, b >>> 4);
                    out[i + 1] = color(palette, b & 15);
                }
                break;
            case MODE_2BIT:
                requireMultiple(pixelCount, 4, "2-bit");
                for (int i = 0; i < pixelCount; i += 4) {
                    int b = c.u8();
                    out[i] = color(palette, (b >>> 6) & 3);
                    out[i + 1] = color(palette, (b >>> 4) & 3);
                    out[i + 2] = color(palette, (b >>> 2) & 3);
                    out[i + 3] = color(palette, b & 3);
                }
                break;
            case MODE_1BIT:
                requireMultiple(pixelCount, 8, "1-bit");
                for (int i = 0; i < pixelCount; i += 8) {
                    int b = c.u8();
                    for (int bit = 7; bit >= 0; bit--) out[i + (7 - bit)] = color(palette, (b >>> bit) & 1);
                }
                break;
            default:
                throw new IllegalArgumentException("unsupported pixel mode: " + mode);
        }
        return out;
    }

    private static void decodeRle(int mode, Cursor c, int[] out, int[] palette) {
        int p = 0;
        while (p < out.length) {
            int token = c.u8();
            if (mode == MODE_RLE_INDEXED) {
                if (token <= 127) {
                    out[p++] = color(palette, token);
                } else {
                    int count = token - 128;
                    int index = c.u8();
                    if (count == 0 || count > out.length - p) throw new IllegalArgumentException("invalid RLE run length");
                    int argb = color(palette, index);
                    for (int n = 0; n < count; n++) out[p++] = argb;
                }
            } else {
                if (token <= 127) {
                    int index = c.u8();
                    out[p++] = color(palette, index);
                } else {
                    int count = token - 128;
                    if (count == 0 || count > out.length - p) throw new IllegalArgumentException("invalid alternate RLE run length");
                    int index = c.u8();
                    int argb = color(palette, index);
                    for (int n = 0; n < count; n++) out[p++] = argb;
                }
            }
        }
    }

    private static int color(int[] palette, int index) {
        if (index < 0 || index >= palette.length) throw new IllegalArgumentException("palette index out of range: " + index);
        return palette[index];
    }
    private static void requireMultiple(int pixels, int group, String label) {
        if (pixels % group != 0) throw new IllegalArgumentException(label + " pixel count must be divisible by " + group);
    }
    private static final class Cursor {
        final byte[] data; int pos;
        Cursor(byte[] data, int pos) { this.data = data; this.pos = pos; }
        int u8() {
            if (pos >= data.length) throw new IllegalArgumentException("truncated pixel stream at byte " + pos);
            return data[pos++] & 255;
        }
    }
}
