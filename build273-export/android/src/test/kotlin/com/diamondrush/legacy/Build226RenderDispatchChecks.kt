package com.diamondrush.legacy

object Build226RenderDispatchChecks {
    @JvmStatic fun main(args: Array<String>) {
        check(LegacyRenderDispatchCatalog.bJCases.size == 35)
        check(LegacyRenderDispatchCatalog.bICases.size == 50)
        check(LegacyRenderDispatchCatalog.bJCases.first() == LegacyRawDispatchCase(3, 1890))
        check(LegacyRenderDispatchCatalog.bJCases.last() == LegacyRawDispatchCase(37, 1930))
        check(LegacyRenderDispatchCatalog.bICases.first() == LegacyRawDispatchCase(0, 5644))
        check(LegacyRenderDispatchCatalog.bICases.last() == LegacyRawDispatchCase(49, 2452))

        check(LegacyRenderDispatchCatalog.overlayRoute(20) ==
            LegacyRenderDispatchCatalog.OverlayRoute(3,
                LegacyRenderDispatchCatalog.OverlayFrameRule.LOW_ID_MINUS_20_ANIMATED_BY_AS_SHIFT_2))
        check(LegacyRenderDispatchCatalog.overlayRoute(25)?.resourceIndex == 3)
        check(LegacyRenderDispatchCatalog.overlayRoute(31)?.resourceIndex == 15)
        check(LegacyRenderDispatchCatalog.overlayRoute(32)?.resourceIndex == 16)
        check(LegacyRenderDispatchCatalog.overlayRoute(36)?.resourceIndex == 20)
        check(LegacyRenderDispatchCatalog.overlayRoute(80)?.resourceIndex == 42)
        check(LegacyRenderDispatchCatalog.overlayRoute(207)?.resourceIndex == 42)
        check(LegacyRenderDispatchCatalog.overlayRoute(208) == null)
        check(LegacyRenderDispatchCatalog.overlayRoute(37) == null)
        check(LegacyRenderDispatchCatalog.overlayRoute(38) == null)

        check(LegacyRenderDispatchCatalog.supplementalResourceIndices(0x10000000, 0) == listOf(13))
        check(LegacyRenderDispatchCatalog.supplementalResourceIndices(0, 54) == listOf(7))
        check(LegacyRenderDispatchCatalog.supplementalResourceIndices(0x10000000, 54) == listOf(13, 7))
        check(LegacyRenderDispatchCatalog.supplementalResourceIndices(0, 0).isEmpty())
        check(LegacyRenderDispatchCatalog.supplementalResourceIndices(0xF0000000.toInt(), 54) == listOf(7))

        println("BUILD226_KOTLIN_CHECKS_PASSED")
    }
}
