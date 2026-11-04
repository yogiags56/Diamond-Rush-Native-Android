package com.example.diamondrush.engine;

/**
 * Converts the original game's 16-bit RGB565 palette words to Android-style
 * opaque ARGB8888 colors. The caller is responsible for reading the word using
 * the byte order established by the resource decoder.
 */
public final class Rgb565Palette {
    private Rgb565Palette() {}

    public static int toArgb(int word) {
        if ((word & ~0xffff) != 0) {
            throw new IllegalArgumentException("RGB565 word must be unsigned 16-bit");
        }
        int r5 = (word >>> 11) & 0x1f;
        int g6 = (word >>> 5) & 0x3f;
        int b5 = word & 0x1f;
        int r8 = (r5 << 3) | (r5 >>> 2);
        int g8 = (g6 << 2) | (g6 >>> 4);
        int b8 = (b5 << 3) | (b5 >>> 2);
        return 0xff000000 | (r8 << 16) | (g8 << 8) | b8;
    }

    public static int[] decodeWords(int[] words) {
        if (words == null) throw new IllegalArgumentException("null palette words");
        int[] colors = new int[words.length];
        for (int i = 0; i < words.length; i++) colors[i] = toArgb(words[i]);
        return colors;
    }
}
