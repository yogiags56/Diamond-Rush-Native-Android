package com.example.diamondrush.engine;

/**
 * Validated, platform-neutral decoded sprite pixels.
 * The caller supplies a pixel stream and palette already located by the
 * resource-specific metadata reader. This class deliberately does not guess
 * image dimensions, stream offsets, or compression mode.
 */
public final class DecodedSpritePixels {
    public final int width;
    public final int height;
    public final int[] argb;

    private DecodedSpritePixels(int width, int height, int[] argb) {
        this.width = width;
        this.height = height;
        this.argb = argb;
    }

    public static DecodedSpritePixels decode(int width, int height, int mode,
                                             byte[] stream, int streamOffset,
                                             int[] palette) {
        if (width <= 0 || height <= 0)
            throw new IllegalArgumentException("sprite dimensions must be positive");
        long count = (long) width * (long) height;
        if (count > Integer.MAX_VALUE)
            throw new IllegalArgumentException("sprite pixel count overflows Java array size");
        int[] pixels = IndexedPixelDecoder.decode(mode, stream, streamOffset,
                (int) count, palette);
        return new DecodedSpritePixels(width, height, pixels);
    }

    public int pixelAt(int x, int y) {
        if (x < 0 || x >= width || y < 0 || y >= height)
            throw new IndexOutOfBoundsException("pixel outside sprite");
        return argb[y * width + x];
    }
}
