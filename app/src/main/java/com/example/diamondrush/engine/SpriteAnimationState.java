package com.example.diamondrush.engine;

/**
 * Platform-neutral port of the timing/offset state in the original J2ME
 * animation helper (class b). Sprite data access stays behind SequenceData
 * until the original class f payload decoder is fully ported.
 */
public final class SpriteAnimationState {
    public interface SequenceData {
        int frameCount(int animationIndex);
        /** Duration returned by the original f.a(animation, frame) in ticks. */
        int frameDuration(int animationIndex, int frameIndex);
        /** Five-byte frame record table, same ordering as original f.c. */
        byte[] frameRecords();
        /** Short offsets into frameRecords, same ordering as original f.a. */
        short[] animationRecordOffsets();
    }

    private final SequenceData data;
    private int animation = -1;
    private int frame;
    private int elapsed;
    private int transformFlags;
    private int offsetX;
    private int offsetY;

    public SpriteAnimationState(SequenceData data) {
        if (data == null) throw new IllegalArgumentException("data == null");
        this.data = data;
    }

    /** Equivalent to original b.a(int): changing animation resets its cursor. */
    public void setAnimation(int index) {
        if (animation != index) {
            animation = index;
            frame = 0;
            elapsed = 0;
            offsetX = 0;
            offsetY = 0;
        }
    }

    /**
     * Equivalent to original b.b(): one game tick. Returns true if the frame
     * cursor advanced. A negative animation disables automatic advancement.
     */
    public boolean tick() {
        if (animation < 0) return false;
        int duration = data.frameDuration(animation, frame);
        if (duration == 0) return false;
        elapsed++;
        if (duration > elapsed) return false;
        elapsed = 0;
        frame++;
        if (frame >= data.frameCount(animation)) {
            frame = 0;
            offsetX = 0;
            offsetY = 0;
        }
        return true;
    }

    /**
     * Applies the current frame's signed x/y delta, respecting horizontal and
     * vertical flip bits (1 and 2) observed in original b.a().
     */
    public void accumulateFrameOffset() {
        short[] starts = data.animationRecordOffsets();
        byte[] records = data.frameRecords();
        if (animation < 0 || animation >= starts.length) return;
        int record = (starts[animation] + frame) * 5;
        if (record < 0 || record + 3 >= records.length) {
            throw new IllegalStateException("Frame record outside decoded sprite metadata");
        }
        int dx = records[record + 2];
        int dy = records[record + 3];
        if ((transformFlags & 1) != 0) dx = -dx;
        if ((transformFlags & 2) != 0) dy = -dy;
        offsetX += dx;
        offsetY += dy;
    }

    public void setTransformFlags(int flags) { transformFlags = flags; }
    public int animation() { return animation; }
    public int frame() { return frame; }
    public int elapsedTicks() { return elapsed; }
    public int offsetX() { return offsetX; }
    public int offsetY() { return offsetY; }
}
