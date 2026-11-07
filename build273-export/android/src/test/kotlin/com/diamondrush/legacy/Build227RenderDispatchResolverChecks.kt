package com.diamondrush.legacy

object Build227RenderDispatchResolverChecks {
    private fun fixtureTable(): LegacySpriteAnimationTable {
        // one sequence, two frames; first record is zero
        val layout = LegacySpriteFieldLayout(
            fDimensions = byteArrayOf(1, 1),
            hComponents = byteArrayOf(0, 0, 0, 0),
            gGroupCounts = byteArrayOf(0),
            bGroupStarts = shortArrayOf(0),
            aGroupRecords = ByteArray(4),
            cFiveByteRecords = byteArrayOf(
                0, 3, 1, 2, 0,
                0xff.toByte(), 5, 0, 0, 0,
                0, 3, 0, 0, 0,
                0, 3, 0, 0, 0,
                0, 3, 0, 0, 0,
                0, 3, 0, 0, 0,
                0, 3, 0, 0, 0
            ),
            bByteTable = byteArrayOf(2, 1, 1, 1, 1, 1),
            aShortTable = shortArrayOf(0, 2, 3, 4, 5, 6),
            paletteFormat = 0,
            paletteCount = 0,
            colorsPerPalette = 0,
            palettesArgb = emptyList(),
            pixelFormat = 0,
            spritePayloadOffsets = intArrayOf(),
            spritePayloads = emptyList(),
            concatenatedPixelBytes = byteArrayOf(),
            trailingBytes = byteArrayOf()
        )
        return LegacySpriteAnimationTable.fromFieldLayout(layout)
    }

    @JvmStatic fun main(args: Array<String>) {
        // Repair check: Build 226 catalog source must contain actual Kotlin lines.
        check(LegacyRenderDispatchCatalog.bJCases.size == 35)
        check(LegacyRenderDispatchCatalog.bICases.size == 50)

        check(LegacyRenderDispatchResolver.selectFirstMainPass(3).branchTargetOffset == 1890)
        check(LegacyRenderDispatchResolver.selectFirstMainPass(255).kind ==
            LegacyMainDispatchKind.DEFAULT_SHARED_TAIL)
        check(LegacyRenderDispatchResolver.selectFirstMainPass(255).branchTargetOffset == 1995)

        check(LegacyRenderDispatchResolver.selectSecondMainPass(-1).kind ==
            LegacyMainDispatchKind.SKIP_CELL)
        check(LegacyRenderDispatchResolver.selectSecondMainPass(0).branchTargetOffset == 5644)
        check(LegacyRenderDispatchResolver.selectSecondMainPass(50).kind ==
            LegacyMainDispatchKind.DEFAULT_SHARED_TAIL)
        check(LegacyRenderDispatchResolver.selectSecondMainPass(80).kind ==
            LegacyMainDispatchKind.SIGNED_BYTE_BYPASS_TO_SHARED_TAIL)
        check(LegacyRenderDispatchResolver.selectSecondMainPass(-49).kind ==
            LegacyMainDispatchKind.SIGNED_BYTE_BYPASS_TO_SHARED_TAIL)
        check(LegacyRenderDispatchResolver.selectSecondMainPass(-48).kind ==
            LegacyMainDispatchKind.DEFAULT_SHARED_TAIL)

        val table = fixtureTable()
        val tables = mapOf(3 to table, 15 to table, 16 to table, 20 to table)
        val cell20 = LegacyRenderCellSample(20, 0, 20)
        val sel20 = LegacyRenderDispatchResolver.resolveOverlayFrame(cell20, 8, tables)!!
        check(sel20.resourceIndex == 3 && sel20.sequenceIndex == 0 && sel20.frameIndex == 0 && sel20.directDrawArgument == null)

        val cell25 = LegacyRenderCellSample(25, 0, 25)
        check(LegacyRenderDispatchResolver.resolveOverlayFrame(cell25, 4, tables)!!.sequenceIndex == 5)
        val cell31 = LegacyRenderCellSample(31, 0, (1 shl 8) or 31)
        val sel31 = LegacyRenderDispatchResolver.resolveOverlayFrame(cell31, 4, tables)!!
        check(sel31.resourceIndex == 15 && sel31.sequenceIndex == 1 && sel31.frameIndex == 0)

        val cell32 = LegacyRenderCellSample(32, 0, (1 shl 8) or 32)
        val sel32 = LegacyRenderDispatchResolver.resolveOverlayFrame(cell32, 0, tables)!!
        check(sel32.resourceIndex == 16 && sel32.sequenceIndex == 0 && sel32.frameIndex == 1)

        val cell36 = LegacyRenderCellSample(36, 0, (3 shl 8) or 36)
        val sel36 = LegacyRenderDispatchResolver.resolveOverlayFrame(cell36, 0, tables)!!
        check(sel36.resourceIndex == 20 && sel36.frameIndex == 0)

        val cell80 = LegacyRenderCellSample(80, 0, 80)
        val sel80 = LegacyRenderDispatchResolver.resolveOverlayFrame(cell80, 0, emptyMap())!!
        check(sel80.kind == LegacyOverlaySelectionKind.DIRECT_DRAW_ARGUMENT)
        check(sel80.resourceIndex == 42 && sel80.frameIndex == null && sel80.directDrawArgument == 0)
        check(LegacyRenderDispatchResolver.selectSecondaryOverlay(
            LegacyRenderCellSample(50, 0, 50)) == null)

        check(LegacyRenderDispatchResolver.supplementalResources(
            LegacyRenderCellSample(1, 54, 1)) == listOf(7))
        check(LegacyRenderDispatchResolver.supplementalResources(
            LegacyRenderCellSample(1, 0, 0x10000001)) == listOf(13))
        check(LegacyRenderDispatchResolver.supplementalResources(
            LegacyRenderCellSample(1, 54, 0x10000001)) == listOf(13, 7))
        check(LegacyRenderDispatchResolver.supplementalResources(
            LegacyRenderCellSample(1, 54, 0xF0000001u.toInt())) == listOf(7))

        println("BUILD227_KOTLIN_CHECKS_PASSED")
    }
}
