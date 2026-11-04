package com.example.diamondrush.engine.render;

/** Immutable, decoder-independent description of one rectangular sprite frame. */
public final class SpriteFrame {
    public static final int FLIP_X = 1;
    public static final int FLIP_Y = 2;

    public final int atlasIndex;
    public final int sourceX;
    public final int sourceY;
    public final int width;
    public final int height;
    public final int originX;
    public final int originY;
    public final int transformFlags;

    public SpriteFrame(int atlasIndex, int sourceX, int sourceY, int width, int height,
                       int originX, int originY, int transformFlags) {
        if (atlasIndex < 0 || sourceX < 0 || sourceY < 0 || width <= 0 || height <= 0)
            throw new IllegalArgumentException("Invalid atlas rectangle");
        if ((transformFlags & ~(FLIP_X | FLIP_Y)) != 0)
            throw new IllegalArgumentException("Unsupported transform flags: " + transformFlags);
        this.atlasIndex = atlasIndex;
        this.sourceX = sourceX;
        this.sourceY = sourceY;
        this.width = width;
        this.height = height;
        this.originX = originX;
        this.originY = originY;
        this.transformFlags = transformFlags;
    }

    public int sourceRight() { return sourceX + width; }
    public int sourceBottom() { return sourceY + height; }
}
