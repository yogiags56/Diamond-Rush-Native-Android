package com.example.diamondrush.engine;

import java.util.Arrays;

public final class Rgb565PaletteTest {
    private static void eq(int actual, int expected) {
        if (actual != expected) throw new AssertionError(
            String.format("0x%08X != 0x%08X", actual, expected));
    }
    private static void fails(Runnable r) {
        try { r.run(); throw new AssertionError("expected rejection"); }
        catch (IllegalArgumentException expected) {}
    }
    public static void main(String[] args) {
        eq(Rgb565Palette.toArgb(0xf800), 0xffff0000);
        eq(Rgb565Palette.toArgb(0x07e0), 0xff00ff00);
        eq(Rgb565Palette.toArgb(0x001f), 0xff0000ff);
        eq(Rgb565Palette.toArgb(0xffff), 0xffffffff);
        eq(Rgb565Palette.toArgb(0x0000), 0xff000000);
        eq(Rgb565Palette.toArgb(0x8410), 0xff848284);
        int[] actual = Rgb565Palette.decodeWords(new int[]{0xf800,0x07e0,0x001f});
        if (!Arrays.equals(actual, new int[]{0xffff0000,0xff00ff00,0xff0000ff}))
            throw new AssertionError("palette array conversion mismatch");
        fails(() -> Rgb565Palette.toArgb(-1));
        fails(() -> Rgb565Palette.toArgb(0x10000));
        fails(() -> Rgb565Palette.decodeWords(null));
        System.out.println("PASS: 9 RGB565 palette tests");
    }
}
