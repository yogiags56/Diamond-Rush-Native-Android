package com.example.diamondrush;

/** Logical game viewport. Keeps uniform scale and exposes extra horizontal world space. */
public final class Viewport {
    public static final int LOGICAL_WIDTH = 320;
    public static final int LOGICAL_HEIGHT = 240;
    public static final int TILE_SIZE = 24;
    public static final int PLAYFIELD_TOP = 31;
    public static final int PLAYFIELD_HEIGHT = 178;
    public float scale, left, top, visibleWidth, visibleHeight;

    public void update(int screenWidth, int screenHeight) {
        scale = Math.min(screenHeight / (float) LOGICAL_HEIGHT,
                         screenWidth / (float) LOGICAL_HEIGHT);
        if (scale <= 0f) scale = 1f;
        visibleWidth = screenWidth / scale;
        visibleHeight = screenHeight / scale;
        left = (LOGICAL_WIDTH - visibleWidth) * 0.5f;
        top = (LOGICAL_HEIGHT - visibleHeight) * 0.5f;
    }
    public float screenX(float worldX) { return (worldX - left) * scale; }
    public float screenY(float worldY) { return (worldY - top) * scale; }
    public float worldX(float screenX) { return screenX / scale + left; }
    public float worldY(float screenY) { return screenY / scale + top; }
}
