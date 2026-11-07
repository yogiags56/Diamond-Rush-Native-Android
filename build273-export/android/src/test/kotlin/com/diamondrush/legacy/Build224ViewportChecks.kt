package com.diamondrush.legacy

object Build224ViewportChecks {
    @JvmStatic fun main(args: Array<String>) {
        check(LegacyGameplayViewport.canvas == LegacyRect(0, 0, 320, 240))
        check(LegacyGameplayViewport.gameplayClipInCanvas == LegacyRect(0, 31, 320, 178))
        check(LegacyGameplayViewport.gameplayClipInCanvas.bottomExclusive == 209)

        val camera = LegacyCameraOffset(49, 26)
        check(camera.tileX == 2 && camera.tileY == 1)
        check(camera.pixelRemainderX == 1 && camera.pixelRemainderY == 2)
        val negativeCamera = LegacyCameraOffset(-25, -1)
        check(negativeCamera.tileX == -1 && negativeCamera.pixelRemainderX == -1)
        check(negativeCamera.tileY == 0 && negativeCamera.pixelRemainderY == -1)

        val room = LegacyRoomMapPlanes(
            4, 5, ByteArray(20), IntArray(20), IntArray(20)
        )
        val cells = LegacyVisibleCellTraversal.candidates(room, camera)
        check(cells.size == 160)
        check(cells.first().row == -1 && cells.first().column == -1)
        check(cells.first().screenX == -25 && cells.first().screenY == -26)
        check(cells.any { it.inBounds })
        check(cells.none { it.row !in -1..8 || it.column !in -1..14 })

        val selectors = LegacyRenderDispatchSelectors(bJ = 34, bI = 49)
        check(selectors.bJ == 34 && selectors.bI == 49)
        check(LegacyRenderDispatchSelectors.BJ_CASE_COUNT == 35)
        check(LegacyRenderDispatchSelectors.BI_CASE_COUNT == 50)

        val surface = LegacyLogicalSurface()
        val opaqueRed = 0xffff0000.toInt()
        val opaqueBlue = 0xff0000ff.toInt()
        surface.blit(intArrayOf(opaqueRed, opaqueRed, opaqueRed, opaqueRed), 2, 2,
            0, 30, LegacyGameplayViewport.gameplayClipInCanvas)
        check(surface.pixelAt(0, 30) == 0)
        check(surface.pixelAt(0, 31) == opaqueRed)
        check(surface.pixelAt(1, 31) == opaqueRed)
        check(surface.pixelAt(0, 32) == 0)
        surface.blit(intArrayOf(opaqueBlue), 1, 1, 319, 208,
            LegacyGameplayViewport.gameplayClipInCanvas)
        check(surface.pixelAt(319, 208) == opaqueBlue)
        surface.blit(intArrayOf(opaqueBlue), 1, 1, 0, 209,
            LegacyGameplayViewport.gameplayClipInCanvas)
        check(surface.pixelAt(0, 209) == 0)
        check(surface.copyPixels().size == 320 * 240)
        println("BUILD224_KOTLIN_CHECKS_PASSED")
    }
}
