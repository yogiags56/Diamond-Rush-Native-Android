package com.example.diamondrush.engine.render;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.RectF;

/** Android Canvas adapter. It consumes decoded atlas bitmaps; it does not decode J2ME data. */
public final class AndroidSpriteRenderer {
    private final Paint paint = new Paint();
    private final Rect source = new Rect();
    private final RectF destination = new RectF();

    public AndroidSpriteRenderer() {
        paint.setAntiAlias(false);
        paint.setFilterBitmap(false);
        paint.setDither(false);
    }

    public void draw(Canvas canvas, Bitmap atlas, SpriteFrame frame,
                     float anchorX, float anchorY,
                     float accumulatedOffsetX, float accumulatedOffsetY,
                     float scale, int alpha) {
        if (canvas == null || atlas == null || frame == null)
            throw new IllegalArgumentException("canvas, atlas and frame are required");
        if (frame.sourceRight() > atlas.getWidth() || frame.sourceBottom() > atlas.getHeight())
            throw new IllegalArgumentException("Sprite frame exceeds atlas bounds");
        if (alpha < 0 || alpha > 255) throw new IllegalArgumentException("alpha out of range");

        SpriteDrawGeometry g = SpriteDrawGeometry.at(frame, anchorX, anchorY,
                accumulatedOffsetX, accumulatedOffsetY, scale);
        source.set(frame.sourceX, frame.sourceY, frame.sourceRight(), frame.sourceBottom());
        destination.set(g.left * scale, g.top * scale, g.right * scale, g.bottom * scale);
        paint.setAlpha(alpha);

        int save = canvas.save();
        try {
            float cx = destination.centerX();
            float cy = destination.centerY();
            canvas.scale(g.flipX ? -1f : 1f, g.flipY ? -1f : 1f, cx, cy);
            canvas.drawBitmap(atlas, source, destination, paint);
        } finally {
            canvas.restoreToCount(save);
        }
    }
}
