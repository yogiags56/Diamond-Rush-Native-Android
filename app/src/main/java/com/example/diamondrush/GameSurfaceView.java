package com.example.diamondrush;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

/** Diagnostic Android render host. It is intentionally not the game renderer yet. */
public final class GameSurfaceView extends SurfaceView implements SurfaceHolder.Callback, Runnable {
    private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Viewport viewport = new Viewport();
    private Thread renderThread;
    private volatile boolean running;

    public GameSurfaceView(Context context) { super(context); getHolder().addCallback(this); setFocusable(true); }
    @Override public void surfaceCreated(SurfaceHolder holder) { running = true; renderThread = new Thread(this, "DiamondRushRender"); renderThread.start(); }
    @Override public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) { viewport.update(width, height); }
    @Override public void surfaceDestroyed(SurfaceHolder holder) {
        running = false;
        if (renderThread != null) { try { renderThread.join(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); } }
    }
    @Override public void run() {
        while (running) {
            Canvas canvas = null;
            try {
                canvas = getHolder().lockCanvas();
                if (canvas != null) drawDiagnostic(canvas);
            } finally { if (canvas != null) getHolder().unlockCanvasAndPost(canvas); }
            try { Thread.sleep(16); } catch (InterruptedException e) { Thread.currentThread().interrupt(); return; }
        }
    }
    private void drawDiagnostic(Canvas c) {
        c.drawColor(0xff101820);
        float s = viewport.scale;
        paint.setColor(0xff263746); paint.setStrokeWidth(1f);
        for (int x = 0; x <= viewport.visibleWidth + Viewport.TILE_SIZE; x += Viewport.TILE_SIZE)
            c.drawLine(viewport.screenX(x), 0, viewport.screenX(x), getHeight(), paint);
        for (int y = 0; y <= Viewport.LOGICAL_HEIGHT; y += Viewport.TILE_SIZE)
            c.drawLine(0, viewport.screenY(y), getWidth(), viewport.screenY(y), paint);
        paint.setColor(0xfff5c542); paint.setTextSize(18f * Math.max(1f, s / 4f));
        c.drawText("DIAMOND RUSH — ANDROID PORT FOUNDATION", 24, 48, paint);
        paint.setColor(0xffd7e0e8); paint.setTextSize(13f * Math.max(1f, s / 4f));
        c.drawText("Native renderer host ready; original game engine not integrated.", 24, 76, paint);
    }
}
