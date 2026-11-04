package com.example.diamondrush.engine;

/**
 * Semantic names for input masks observed in the original Diamond Rush
 * central update method. Values are the exact integer masks passed to its
 * private a(int) bit-test helper.
 *
 * Names describe observed usage/context, not a claim that each mask has one
 * universal meaning in every game state.
 */
public final class OriginalGameplayInput {
    private OriginalGameplayInput() {}

    // Single input flags used by the original update state machine.
    public static final int FLAG_64 = 64;
    public static final int FLAG_256 = 256;
    public static final int FLAG_512 = 512;
    public static final int FLAG_1024 = 1024;
    public static final int FLAG_65536 = 65536;
    public static final int FLAG_131072 = 131072;
    public static final int FLAG_262144 = 262144;
    public static final int FLAG_524288 = 524288;

    // Composite masks explicitly tested by the original code.
    public static final int MASK_4097 = 4097;
    public static final int MASK_262146 = 262146;
    public static final int MASK_16388 = 16388;
    public static final int MASK_65544 = 65544;
    public static final int MASK_32784 = 32784;
    public static final int MASK_32944 = 32944;
    public static final int MASK_33008 = 33008;
    public static final int MASK_1048575 = 1048575;

    public static boolean contains(int currentInput, int mask) {
        return (currentInput & mask) != 0;
    }
}
