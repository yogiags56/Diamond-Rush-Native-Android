package com.example.diamondrush;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Paint;
import android.graphics.RectF;
import android.view.View;
import android.os.SystemClock;

import com.example.diamondrush.engine.SpriteFrameSequence;

/**
 * Native Android visual prototype for the gameplay screen.
 *
 * This is intentionally a preview scene with placeholder geometry. It is not
 * the original Diamond Rush level renderer or game simulation.
 */
public final class GameplayPreviewView extends View {
    private final Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Bitmap originalGem;
    private final Bitmap[] originalSpriteFrames = new Bitmap[8];
    private final SpriteFrameSequence spriteSequence = new SpriteFrameSequence(8, 140);
    private long lastFrameTimeMs = -1L;
    private final RectF tile = new RectF();
    private int playerX = 2;
    private int playerY = 3;
    private int collected = 0;
    private boolean paused;

    private static final int COLS = 14;
    private static final int ROWS = 8;
    private static final int[][] GEMS = {
            {5, 2}, {9, 4}, {11, 1}, {7, 6}
    };
    private final boolean[] taken = new boolean[GEMS.length];

    public GameplayPreviewView(Context context) {
        super(context);
        originalGem = BitmapFactory.decodeResource(
                context.getResources(), com.example.diamondrush.R.drawable.diamond_rush_gem);
        for (int i = 0; i < originalSpriteFrames.length; i++) {
            int id = context.getResources().getIdentifier(
                    String.format(java.util.Locale.ROOT, "dmr_gen0_frame_%02d", i),
                    "drawable", context.getPackageName());
            if (id != 0) originalSpriteFrames[i] = BitmapFactory.decodeResource(
                    context.getResources(), id);
        }
        setLayerType(View.LAYER_TYPE_SOFTWARE, null);
    }

    public void onControlChanged(int control, boolean pressed) {
        if (!pressed || paused) return;
        switch (control) {
            case 1: playerX = Math.max(1, playerX - 1); spriteSequence.advance(140); break;
            case 2: playerX = Math.min(COLS - 2, playerX + 1); spriteSequence.advance(140); break;
            case 3: playerY = Math.max(1, playerY - 1); spriteSequence.advance(140); break;
            case 4: playerY = Math.min(ROWS - 2, playerY + 1); spriteSequence.advance(140); break;
            case 5: collectAtPlayer(); break;
            case 6: paused = !paused; break;
        }
        invalidate();
    }

    public void togglePause() {
        paused = !paused;
        invalidate();
    }

    private void collectAtPlayer() {
        for (int i = 0; i < GEMS.length; i++) {
            if (!taken[i] && GEMS[i][0] == playerX && GEMS[i][1] == playerY) {
                taken[i] = true;
                collected++;
            }
        }
    }

    @Override protected void onDraw(Canvas c) {
        super.onDraw(c);
        float cell = Math.min(getWidth() / (float) COLS, getHeight() / (float) ROWS);
        float ox = (getWidth() - cell * COLS) / 2f;
        float oy = (getHeight() - cell * ROWS) / 2f;
        c.drawColor(0xff171512);

        // Deep cave backdrop and a stone-tile arena.
        for (int y = 0; y < ROWS; y++) {
            for (int x = 0; x < COLS; x++) {
                float l = ox + x * cell, t = oy + y * cell;
                tile.set(l + 1, t + 1, l + cell - 1, t + cell - 1);
                boolean wall = x == 0 || y == 0 || x == COLS - 1 || y == ROWS - 1
                        || ((x == 4 && y == 3) || (x == 8 && y == 2) || (x == 8 && y == 3));
                p.setColor(wall ? 0xff62503a : ((x + y) % 2 == 0 ? 0xff3b3329 : 0xff302a23));
                c.drawRoundRect(tile, cell * .08f, cell * .08f, p);
                p.setColor(wall ? 0xff88704e : 0xff514536);
                p.setStyle(Paint.Style.STROKE);
                p.setStrokeWidth(Math.max(1f, cell * .025f));
                c.drawRoundRect(tile, cell * .08f, cell * .08f, p);
                p.setStyle(Paint.Style.FILL);
            }
        }

        // Gems.
        for (int i = 0; i < GEMS.length; i++) {
            if (taken[i]) continue;
            float cx = ox + (GEMS[i][0] + .5f) * cell;
            float cy = oy + (GEMS[i][1] + .5f) * cell;
            if (originalGem != null) {
                float gemSize = cell * .62f;
                RectF gemRect = new RectF(cx - gemSize / 2f, cy - gemSize / 2f,
                        cx + gemSize / 2f, cy + gemSize / 2f);
                p.setFilterBitmap(false);
                c.drawBitmap(originalGem, null, gemRect, p);
            } else {
                p.setColor(0xff46d9e9);
                PathUtil.drawDiamond(c, p, cx, cy, cell * .24f);
            }
        }

        // Simple placeholder adventurer.
        float px = ox + (playerX + .5f) * cell;
        float py = oy + (playerY + .5f) * cell;
        Bitmap originalFrame = originalSpriteFrames[spriteSequence.currentFrame()];
        if (originalFrame != null) {
            float spriteSize = cell * 1.15f;
            RectF spriteRect = new RectF(px - spriteSize / 2f, py - spriteSize / 2f,
                    px + spriteSize / 2f, py + spriteSize / 2f);
            p.setFilterBitmap(false);
            c.drawBitmap(originalFrame, null, spriteRect, p);
        } else {
            // Safe fallback if a decoded original PNG is unavailable.
            p.setColor(0xffc58a42);
            c.drawCircle(px, py, cell * .30f, p);
            p.setColor(0xfff1d4a0);
            c.drawCircle(px, py - cell * .06f, cell * .20f, p);
        }

        p.setColor(0xffffe3a0);
        p.setTextSize(Math.max(14f, cell * .34f));
        p.setShadowLayer(3f, 1f, 1f, 0xff000000);
        c.drawText("DIAMONDS  " + collected + " / " + GEMS.length, ox + cell * .5f, oy + cell * .55f, p);
        p.clearShadowLayer();
        p.setTextSize(Math.max(10f, cell * .20f));
        p.setColor(0xffcbb995);
        c.drawText("ORIGINAL SPRITE SAMPLE  •  FRAME " + (spriteSequence.currentFrame() + 1)
                + " / 8", ox + cell * .5f, oy + ROWS * cell - cell * .25f, p);

        if (paused) {
            p.setColor(0xaa000000);
            c.drawRect(0, 0, getWidth(), getHeight(), p);
            p.setColor(0xffffd477);
            p.setTextAlign(Paint.Align.CENTER);
            p.setTextSize(Math.max(24f, cell * .8f));
            c.drawText("PAUSED", getWidth() / 2f, getHeight() / 2f, p);
            p.setTextAlign(Paint.Align.LEFT);
        }
    }
}
