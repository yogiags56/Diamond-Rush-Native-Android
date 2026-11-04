package com.example.diamondrush.engine.render;

/** Platform-neutral placement math shared by Android rendering and unit tests. */
public final class SpriteDrawGeometry {
    public final float left, top, right, bottom;
    public final boolean flipX, flipY;

    private SpriteDrawGeometry(float left, float top, float right, float bottom,
                               boolean flipX, boolean flipY) {
        this.left = left; this.top = top; this.right = right; this.bottom = bottom;
        this.flipX = flipX; this.flipY = flipY;
    }

    /** Destination keeps native pixel dimensions; origin is the frame's anchor point. */
    public static SpriteDrawGeometry at(SpriteFrame frame, float anchorX, float anchorY,
                                        float accumulatedOffsetX, float accumulatedOffsetY,
                                        float scale) {
        if (frame == null) throw new IllegalArgumentException("frame == null");
        if (!(scale > 0f) || Float.isInfinite(scale) || Float.isNaN(scale))
            throw new IllegalArgumentException("scale must be finite and positive");
        float x = anchorX + accumulatedOffsetX - frame.originX;
        float y = anchorY + accumulatedOffsetY - frame.originY;
        return new SpriteDrawGeometry(x, y, x + frame.width, y + frame.height,
                (frame.transformFlags & SpriteFrame.FLIP_X) != 0,
                (frame.transformFlags & SpriteFrame.FLIP_Y) != 0);
    }
}
