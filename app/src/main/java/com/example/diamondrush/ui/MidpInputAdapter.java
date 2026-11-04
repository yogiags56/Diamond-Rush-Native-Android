package com.example.diamondrush.ui;

/**
 * Converts Android touch-HUD states into Java ME Canvas key codes.
 *
 * Mapping is centralized so it can be corrected after the original game's
 * keyPressed/keyReleased dispatch is fully traced. The standard MIDP game
 * game-action key codes are normalized by the original game to bit flags:
 * UP=1, DOWN=2, LEFT=4, RIGHT=8, FIRE=16.
 * Pause is an Android-side command, not a Canvas key.
 */
public final class MidpInputAdapter {
    public static final int KEY_UP = DiamondRushKeyMap.UP;
    public static final int KEY_LEFT = DiamondRushKeyMap.LEFT;
    public static final int KEY_RIGHT = DiamondRushKeyMap.RIGHT;
    public static final int KEY_DOWN = DiamondRushKeyMap.DOWN;
    public static final int KEY_FIRE = DiamondRushKeyMap.FIRE;

    public interface Sink {
        void keyPressed(int keyCode);
        void keyReleased(int keyCode);
        void pauseRequested();
    }

    private final Sink sink;
    private final boolean[] sent = new boolean[7];

    public MidpInputAdapter(Sink sink) {
        if (sink == null) throw new IllegalArgumentException("sink is null");
        this.sink = sink;
    }

    public void update(TouchControlState state) {
        if (state == null) throw new IllegalArgumentException("state is null");
        transition(TouchControlState.UP, KEY_UP, state.isPressed(TouchControlState.UP));
        transition(TouchControlState.DOWN, KEY_DOWN, state.isPressed(TouchControlState.DOWN));
        transition(TouchControlState.LEFT, KEY_LEFT, state.isPressed(TouchControlState.LEFT));
        transition(TouchControlState.RIGHT, KEY_RIGHT, state.isPressed(TouchControlState.RIGHT));
        transition(TouchControlState.ACTION, KEY_FIRE, state.isPressed(TouchControlState.ACTION));
        if (state.isPressed(TouchControlState.PAUSE) && !sent[TouchControlState.PAUSE]) {
            sink.pauseRequested();
        }
        sent[TouchControlState.PAUSE] = state.isPressed(TouchControlState.PAUSE);
    }

    public void releaseAll() {
        release(TouchControlState.UP, KEY_UP);
        release(TouchControlState.DOWN, KEY_DOWN);
        release(TouchControlState.LEFT, KEY_LEFT);
        release(TouchControlState.RIGHT, KEY_RIGHT);
        release(TouchControlState.ACTION, KEY_FIRE);
        sent[TouchControlState.PAUSE] = false;
    }

    private void transition(int slot, int key, boolean now) {
        if (now == sent[slot]) return;
        if (now) sink.keyPressed(key);
        else sink.keyReleased(key);
        sent[slot] = now;
    }

    private void release(int slot, int key) {
        if (sent[slot]) sink.keyReleased(key);
        sent[slot] = false;
    }
}
