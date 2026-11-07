package com.diamondrush.legacy

object Build240RoomRenderAssemblyChecks {
    @JvmStatic fun main(args: Array<String>) = runAll()
    fun runAll() {
        val room = LegacyRoomMapPlanes(
            3, 2,
            byteArrayOf(0, 54, -1, 1, -1, 20),
            IntArray(6),
            intArrayOf(20, 31 shl 8 or 31, 32, 36, 80, 0)
        )
        val pass = LegacyRoomRenderAssembly.assemble(LegacyDecodedRoom(7, room, emptyList()), LegacyCameraOffset(0, 0))
        check(pass.cells.size == 160)
        check(pass.inBoundsCount == 6)
        check(pass.outOfBoundsCount == 154)
        val cell01 = pass.cells.single { it.mapFirst == 0 && it.mapSecond == 1 }
        check(cell01.overlayRoute?.resourceIndex == 15)
        check(cell01.overlayRoute?.frameRule == LegacyRenderDispatchCatalog.OverlayFrameRule.PACKED_HIGH_BYTE_ANIMATED_BY_AS_SHIFT_1)
        val cell10 = pass.cells.single { it.mapFirst == 1 && it.mapSecond == 0 }
        check(cell10.overlayRoute?.resourceIndex == 16)
        check(cell10.overlayRoute?.frameRule == LegacyRenderDispatchCatalog.OverlayFrameRule.PACKED_HIGH_BYTE_RAW)
        val cell11 = pass.cells.single { it.mapFirst == 1 && it.mapSecond == 1 }
        check(cell11.overlayRoute?.resourceIndex == 20)
        val cell20 = pass.cells.single { it.mapFirst == 2 && it.mapSecond == 0 }
        check(cell20.overlayRoute?.resourceIndex == 42)
        check(cell20.secondPass?.kind == LegacyMainDispatchKind.SKIP_CELL)
        check(pass.canonicalCsv().trimEnd().lineSequence().count() == 161)
        check(pass.cells.first().row == -1 && pass.cells.first().column == -1)
        check(pass.cells.first().logicalCanvasY == 7)
    }
}
