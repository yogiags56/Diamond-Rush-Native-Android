package com.example.diamondrush.engine;

/**
 * Small deterministic frame sequencer for previewing decoded sprite frames.
 * It does not infer animation timing or frame order from the original game.
 */
public final class SpriteFrameSequence {
    private final int frameCount;
    private final long frameDurationMs;
    private int frameIndex;
    private long remainderMs;

    public SpriteFrameSequence(int frameCount, long frameDurationMs) {
        if (frameCount <= 0) throw new IllegalArgumentException("frameCount must be positive");
        if (frameDurationMs <= 0) throw new IllegalArgumentException("frameDurationMs must be positive");
        this.frameCount = frameCount;
        this.frameDurationMs = frameDurationMs;
    }

    public int currentFrame() { return frameIndex; }

    public void reset() { frameIndex = 0; remainderMs = 0; }

    public void advance(long elapsedMs) {
        if (elapsedMs < 0) throw new IllegalArgumentException("elapsed time cannot be negative");
        long total = remainderMs + elapsedMs;
        long steps = total / frameDurationMs;
        remainderMs = total % frameDurationMs;
        if (steps != 0) frameIndex = (int)((frameIndex + (steps % frameCount)) % frameCount);
    }
}
