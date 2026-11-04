package com.example.diamondrush.engine.render;

public final class SpriteDrawGeometryTest {
    private static int checks;
    private static void eq(float expected, float actual) {
        if (Math.abs(expected - actual) > 0.0001f) throw new AssertionError(expected + " != " + actual);
        checks++;
    }
    private static void yes(boolean value) { if (!value) throw new AssertionError("expected true"); checks++; }
    public static void main(String[] args) {
        SpriteFrame f = new SpriteFrame(0, 4, 8, 16, 20, 3, 5, 0);
        SpriteDrawGeometry g = SpriteDrawGeometry.at(f, 100, 80, 2, -1, 1f);
        eq(99f, g.left); eq(74f, g.top); eq(115f, g.right); eq(94f, g.bottom);
        yes(!g.flipX && !g.flipY);
        SpriteFrame flipped = new SpriteFrame(1, 0, 0, 8, 10, 0, 0, 3);
        SpriteDrawGeometry fg = SpriteDrawGeometry.at(flipped, 20, 30, 0, 0, 2f);
        eq(20f, fg.left); eq(30f, fg.top); eq(28f, fg.right); eq(40f, fg.bottom);
        yes(fg.flipX && fg.flipY);
        System.out.println("SpriteDrawGeometryTest: " + checks + " checks passed");
    }
}
