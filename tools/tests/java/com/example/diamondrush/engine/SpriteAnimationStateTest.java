package com.example.diamondrush.engine;

public final class SpriteAnimationStateTest {
    private static final class Data implements SpriteAnimationState.SequenceData {
        final byte[] records = new byte[15];
        Data() {
            records[2] = 3; records[3] = -2;
            records[7] = 1; records[8] = 4;
        }
        public int frameCount(int a) { return 2; }
        public int frameDuration(int a, int f) { return 2; }
        public byte[] frameRecords() { return records; }
        public short[] animationRecordOffsets() { return new short[]{0}; }
    }
    private static void check(boolean value, String message) {
        if (!value) throw new AssertionError(message);
    }
    public static void main(String[] args) {
        SpriteAnimationState s = new SpriteAnimationState(new Data());
        s.setAnimation(0);
        check(!s.tick() && s.frame() == 0, "duration first tick");
        check(s.tick() && s.frame() == 1, "advance on duration");
        s.setTransformFlags(1);
        s.accumulateFrameOffset();
        check(s.offsetX() == -1 && s.offsetY() == 4, "flip-aware frame delta");
        check(!s.tick() && s.tick() && s.frame() == 0, "wrap after final frame");
        check(s.offsetX() == 0 && s.offsetY() == 0, "offset reset on wrap");
        s.setAnimation(-1);
        check(!s.tick(), "negative animation is paused");
        System.out.println("SpriteAnimationStateTest: 6 checks passed");
    }
}
