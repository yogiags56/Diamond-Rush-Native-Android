package com.diamondrush.legacy

/**
 * Build 226: bytecode-derived raw dispatch metadata.
 * Numeric IDs remain opaque; this catalog does not name gameplay objects.
 */
data class LegacyRawDispatchCase(val rawValue: Int, val branchTargetOffset: Int)

object LegacyRenderDispatchCatalog {
    const val MAIN_PASS_BJ_SWITCH_OFFSET = 783
    const val MAIN_PASS_BI_SWITCH_OFFSET = 2239
    const val MAIN_PASS_BJ_SHARED_TAIL_OFFSET = 1995
    const val MAIN_PASS_BI_SHARED_TAIL_OFFSET = 5676
    const val SECONDARY_OVERLAY_LOOP_START = 6490
    const val SECONDARY_OVERLAY_LOOP_END = 6988

    val bJCases: List<LegacyRawDispatchCase> = listOf(
        LegacyRawDispatchCase(3, 1890),
        LegacyRawDispatchCase(4, 1549),
        LegacyRawDispatchCase(5, 1632),
        LegacyRawDispatchCase(6, 1064),
        LegacyRawDispatchCase(7, 1416),
        LegacyRawDispatchCase(8, 1796),
        LegacyRawDispatchCase(9, 1796),
        LegacyRawDispatchCase(10, 1995),
        LegacyRawDispatchCase(11, 1995),
        LegacyRawDispatchCase(12, 1995),
        LegacyRawDispatchCase(13, 1995),
        LegacyRawDispatchCase(14, 967),
        LegacyRawDispatchCase(15, 1324),
        LegacyRawDispatchCase(16, 1363),
        LegacyRawDispatchCase(17, 1995),
        LegacyRawDispatchCase(18, 1995),
        LegacyRawDispatchCase(19, 1995),
        LegacyRawDispatchCase(20, 1995),
        LegacyRawDispatchCase(21, 1995),
        LegacyRawDispatchCase(22, 1995),
        LegacyRawDispatchCase(23, 1995),
        LegacyRawDispatchCase(24, 1995),
        LegacyRawDispatchCase(25, 1995),
        LegacyRawDispatchCase(26, 1995),
        LegacyRawDispatchCase(27, 1995),
        LegacyRawDispatchCase(28, 1640),
        LegacyRawDispatchCase(29, 1995),
        LegacyRawDispatchCase(30, 1995),
        LegacyRawDispatchCase(31, 1995),
        LegacyRawDispatchCase(32, 1995),
        LegacyRawDispatchCase(33, 967),
        LegacyRawDispatchCase(34, 940),
        LegacyRawDispatchCase(35, 936),
        LegacyRawDispatchCase(36, 1995),
        LegacyRawDispatchCase(37, 1930),
    )

    val bICases: List<LegacyRawDispatchCase> = listOf(
        LegacyRawDispatchCase(0, 5644),
        LegacyRawDispatchCase(1, 5614),
        LegacyRawDispatchCase(2, 5611),
        LegacyRawDispatchCase(3, 5676),
        LegacyRawDispatchCase(4, 5605),
        LegacyRawDispatchCase(5, 5608),
        LegacyRawDispatchCase(6, 5666),
        LegacyRawDispatchCase(7, 5669),
        LegacyRawDispatchCase(8, 5672),
        LegacyRawDispatchCase(9, 5551),
        LegacyRawDispatchCase(10, 5544),
        LegacyRawDispatchCase(11, 5083),
        LegacyRawDispatchCase(12, 3767),
        LegacyRawDispatchCase(13, 5676),
        LegacyRawDispatchCase(14, 4582),
        LegacyRawDispatchCase(15, 5676),
        LegacyRawDispatchCase(16, 4400),
        LegacyRawDispatchCase(17, 5676),
        LegacyRawDispatchCase(18, 3991),
        LegacyRawDispatchCase(19, 5532),
        LegacyRawDispatchCase(20, 5676),
        LegacyRawDispatchCase(21, 2871),
        LegacyRawDispatchCase(22, 5497),
        LegacyRawDispatchCase(23, 5474),
        LegacyRawDispatchCase(24, 5676),
        LegacyRawDispatchCase(25, 5676),
        LegacyRawDispatchCase(26, 5676),
        LegacyRawDispatchCase(27, 5676),
        LegacyRawDispatchCase(28, 4152),
        LegacyRawDispatchCase(29, 5676),
        LegacyRawDispatchCase(30, 5417),
        LegacyRawDispatchCase(31, 5676),
        LegacyRawDispatchCase(32, 4912),
        LegacyRawDispatchCase(33, 5676),
        LegacyRawDispatchCase(34, 4060),
        LegacyRawDispatchCase(35, 4101),
        LegacyRawDispatchCase(36, 3915),
        LegacyRawDispatchCase(37, 5450),
        LegacyRawDispatchCase(38, 5676),
        LegacyRawDispatchCase(39, 5676),
        LegacyRawDispatchCase(40, 5676),
        LegacyRawDispatchCase(41, 5676),
        LegacyRawDispatchCase(42, 5676),
        LegacyRawDispatchCase(43, 5520),
        LegacyRawDispatchCase(44, 3609),
        LegacyRawDispatchCase(45, 3386),
        LegacyRawDispatchCase(46, 3173),
        LegacyRawDispatchCase(47, 5547),
        LegacyRawDispatchCase(48, 2720),
        LegacyRawDispatchCase(49, 2452),
    )

    enum class OverlayFrameRule {
        LOW_ID_MINUS_20_ANIMATED_BY_AS_SHIFT_2,
        PACKED_HIGH_BYTE_ANIMATED_BY_AS_SHIFT_1,
        PACKED_HIGH_BYTE_RAW,
        PACKED_HIGH_BYTE_MINUS_ONE_TIMES_7_DIV_16,
        LOW_ID_MINUS_80_SIGNED_BYTE
    }

    data class OverlayRoute(
        val resourceIndex: Int,
        val frameRule: OverlayFrameRule
    )

    /** Mirrors the secondary overlay branch selection without rendering. */
    fun overlayRoute(rawLowByte: Int): OverlayRoute? {
        require(rawLowByte in 0..255)
        return when {
            rawLowByte in 20..25 -> OverlayRoute(3, OverlayFrameRule.LOW_ID_MINUS_20_ANIMATED_BY_AS_SHIFT_2)
            rawLowByte == 31 -> OverlayRoute(15, OverlayFrameRule.PACKED_HIGH_BYTE_ANIMATED_BY_AS_SHIFT_1)
            rawLowByte == 32 -> OverlayRoute(16, OverlayFrameRule.PACKED_HIGH_BYTE_RAW)
            rawLowByte == 36 -> OverlayRoute(20, OverlayFrameRule.PACKED_HIGH_BYTE_MINUS_ONE_TIMES_7_DIV_16)
            rawLowByte >= 80 && ((rawLowByte - 80).toByte().toInt() >= 0) ->
                OverlayRoute(42, OverlayFrameRule.LOW_ID_MINUS_80_SIGNED_BYTE)
            else -> null
        }
    }

    /** Independent post-branch overlays; returned IDs are still raw resource indices. */
    fun supplementalResourceIndices(packedCellValue: Int, bytePlaneValue: Int): List<Int> {
        val result = ArrayList<Int>(2)
        if (((packedCellValue and -268435456) shr 28) > 0) result += 13
        if (bytePlaneValue == 54) result += 7
        return result
    }
}
