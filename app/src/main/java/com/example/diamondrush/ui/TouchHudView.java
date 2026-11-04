package com.example.diamondrush.ui;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.RectF;
import android.view.MotionEvent;
import android.view.View;
import java.util.HashMap;
import java.util.Map;

/**
 * Initial touch HUD overlay. Draws translucent stone/gold controls and tracks
 * independent pointers so movement and action can be held simultaneously.
 */
public final class TouchHudView extends View {
    public interface Listener {
        void onControlChanged(int control, boolean pressed);
    }

    private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Map<Integer, Integer> pointerControls = new HashMap<>();
    private Listener listener;
    private float density;
    private final RectF left = new RectF();
    private final RectF right = new RectF();
    private final RectF up = new RectF();
    private final RectF down = new RectF();
    private final RectF action = new RectF();
    private final RectF pause = new RectF();

    public TouchHudView(Context context) {
        super(context);
        density = getResources().getDisplayMetrics().density;
        setLayerType(View.LAYER_TYPE_SOFTWARE, null);
    }

    public void setListener(Listener listener) { this.listener = listener; }

    @Override protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        float size = 58f * density;
        float gap = 7f * density;
        float margin = 18f * density;
        float baseX = margin;
        float baseY = getHeight() - margin - size * 2 - gap;
        left.set(baseX, baseY + size + gap, baseX + size, baseY + size * 2 + gap);
        right.set(baseX + size * 2 + gap * 2, baseY + size + gap,
                baseX + size * 3 + gap * 2, baseY + size * 2 + gap);
        up.set(baseX + size + gap, baseY, baseX + size * 2 + gap,
                baseY + size);
        down.set(baseX + size + gap, baseY + size + gap * 2,
                baseX + size * 2 + gap, baseY + size * 2 + gap * 2);

        float actionSize = 72f * density;
        float ax = getWidth() - margin - actionSize;
        float ay = getHeight() - margin - actionSize;
        action.set(ax, ay, ax + actionSize, ay + actionSize);
        float pauseSize = 42f * density;
        pause.set(getWidth() - margin - pauseSize, margin,
                getWidth() - margin, margin + pauseSize);

        drawButton(canvas, left, "◀", TouchControlState.LEFT);
        drawButton(canvas, right, "▶", TouchControlState.RIGHT);
        drawButton(canvas, up, "▲", TouchControlState.UP);
        drawButton(canvas, down, "▼", TouchControlState.DOWN);
        drawButton(canvas, action, "A", TouchControlState.ACTION);
        drawButton(canvas, pause, "Ⅱ", TouchControlState.PAUSE);
    }

    private void drawButton(Canvas canvas, RectF rect, String label, int control) {
        boolean pressed = pointerControls.containsValue(control);
        paint.setColor(pressed ? 0xdd80612f : 0xaa30271f);
        paint.setStyle(Paint.Style.FILL);
        canvas.drawRoundRect(rect, 13f * density, 13f * density, paint);
        paint.setColor(0xffd6a84b);
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(1.6f * density);
        canvas.drawRoundRect(rect, 13f * density, 13f * density, paint);
        paint.setStyle(Paint.Style.FILL);
        paint.setColor(0xfffff0d0);
        paint.setTextAlign(Paint.Align.CENTER);
        paint.setTextSize((control == TouchControlState.ACTION ? 25f : 19f) * density);
        Paint.FontMetrics fm = paint.getFontMetrics();
        float cy = rect.centerY() - (fm.ascent + fm.descent) / 2f;
        canvas.drawText(label, rect.centerX(), cy, paint);
    }

    private int hit(float x, float y) {
        if (pause.contains(x, y)) return TouchControlState.PAUSE;
        if (action.contains(x, y)) return TouchControlState.ACTION;
        if (left.contains(x, y)) return TouchControlState.LEFT;
        if (right.contains(x, y)) return TouchControlState.RIGHT;
        if (up.contains(x, y)) return TouchControlState.UP;
        if (down.contains(x, y)) return TouchControlState.DOWN;
        return TouchControlState.NONE;
    }

    @Override public boolean onTouchEvent(MotionEvent event) {
        int masked = event.getActionMasked();
        int index = event.getActionIndex();
        if (masked == MotionEvent.ACTION_DOWN || masked == MotionEvent.ACTION_POINTER_DOWN) {
            int id = event.getPointerId(index);
            int control = hit(event.getX(index), event.getY(index));
            if (control != TouchControlState.NONE) {
                pointerControls.put(id, control);
                notifyChange(control, true);
                invalidate();
            }
            return true;
        }
        if (masked == MotionEvent.ACTION_UP || masked == MotionEvent.ACTION_POINTER_UP) {
            int id = event.getPointerId(index);
            Integer control = pointerControls.remove(id);
            if (control != null) {
                notifyChange(control, false);
                invalidate();
            }
            return true;
        }
        if (masked == MotionEvent.ACTION_CANCEL) {
            for (int control : pointerControls.values()) notifyChange(control, false);
            pointerControls.clear();
            invalidate();
            return true;
        }
        return true;
    }

    private void notifyChange(int control, boolean pressed) {
        if (listener != null) listener.onControlChanged(control, pressed);
    }
}
