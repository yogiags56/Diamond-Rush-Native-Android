package com.example.diamondrush;

import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Path;

final class PathUtil {
    private PathUtil() {}
    static void drawDiamond(Canvas canvas, Paint paint, float cx, float cy, float radius) {
        Path path = new Path();
        path.moveTo(cx, cy - radius);
        path.lineTo(cx + radius * .72f, cy);
        path.lineTo(cx, cy + radius);
        path.lineTo(cx - radius * .72f, cy);
        path.close();
        canvas.drawPath(path, paint);
    }
}
