package com.example.diamondrush.ui;

/**
 * Verified mapping of Java ME game-action key codes to Diamond Rush's
 * internal input bit flags, recovered from the original i.g(int) bytecode.
 *
 * The original game normalizes negative Canvas game-action constants using
 * abs(), then maps 1..7 to powers of two. In particular:
 * UP=-1 -> 1, DOWN=-2 -> 2, LEFT=-3 -> 4,
 * RIGHT=-4 -> 8, FIRE=-5 -> 16.
 */
public final class DiamondRushKeyMap {
    private DiamondRushKeyMap() {}

    public static final int UP = -1;
    public static final int DOWN = -2;
    public static final int LEFT = -3;
    public static final int RIGHT = -4;
    public static final int FIRE = -5;
    public static final int IGNORED_KEY = -10;

    public static int toInputBit(int keyCode) {
        if (keyCode == IGNORED_KEY) return IGNORED_KEY;
        int key = keyCode < 0 ? Math.abs(keyCode) : keyCode;
        switch (key) {
            case 1: return 1;
            case 2: return 2;
            case 3: return 4;
            case 4: return 8;
            case 5: return 16;
            case 6: return 32;
            case 7: return 64;
            case 23: return 128;
            case 42: return 256;
            case 116: return 256;
            case 35: return 512;
            case 106: return 512;
            case 48: return 1024;
            case 109: return 1024;
            case 49: return 2048;
            case 114: return 2048;
            case 50: return 4096;
            case 115: return 4096;
            case 51: return 8192;
            case 121: return 8192;
            case 52: return 16384;
            case 102: return 16384;
            case 53: return 32768;
            case 103: return 32768;
            case 54: return 65536;
            case 104: return 65536;
            case 55: return 131072;
            case 118: return 131072;
            case 56: return 262144;
            case 98: return 262144;
            case 57: return 524288;
            case 110: return 524288;
            default: return 0;
        }
    }
}
