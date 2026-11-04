package com.example.diamondrush.engine;

import com.example.diamondrush.ui.DiamondRushKeyMap;

/**
 * Platform-neutral reproduction of the original game's input bitmask
 * operations in i.keyPressed(int), i.keyReleased(int), and a(int).
 *
 * This models input storage only. Game-state-specific meaning is still owned
 * by the original gameplay state machine.
 */
public final class OriginalInputMask {
    private int mask;
    private final int gameState;

    public OriginalInputMask(int gameState) {
        this.gameState = gameState;
    }

    public void keyPressed(int keyCode) {
        if (keyCode == DiamondRushKeyMap.IGNORED_KEY) return;
        int bit = DiamondRushKeyMap.toInputBit(keyCode);
        if (bit == 0 && gameState == 30) {
            bit = DiamondRushKeyMap.toInputBit(53);
        }
        mask |= bit;
    }

    public void keyReleased(int keyCode) {
        if (keyCode == DiamondRushKeyMap.IGNORED_KEY) return;
        int bit = DiamondRushKeyMap.toInputBit(keyCode);
        if (bit == 0 && gameState == 30) {
            bit = DiamondRushKeyMap.toInputBit(53);
        }
        mask &= ~bit;
    }

    /** Mirrors the original private static a(int) bit-test helper. */
    public boolean isDown(int bitMask) {
        return (mask & bitMask) != 0;
    }

    public int snapshot() {
        return mask;
    }

    public void clear() {
        mask = 0;
    }
}
