package com.diamondrush.legacy

object Build237PaletteAwareSpriteChecks {
    private fun parsed(
        paletteFormat: Int = 21781,
        paletteRows: List<IntArray> = listOf(intArrayOf(0xFFFF, 0xFC00)),
        pixelFormat: Int = 5632,
        sprite: LegacySpriteResourceBundleParser.SpritePayload =
            LegacySpriteResourceBundleParser.SpritePayload(0, 2, 1, byteArrayOf(0x01))
    ) = LegacySpriteResourceBundleParser.ParsedDf03(
        byteArrayOf(0, 0), byteArrayOf(2, 1), byteArrayOf(), emptyList(), byteArrayOf(),
        byteArrayOf(), emptyList(), paletteFormat, paletteRows.size, paletteRows.first().size,
        paletteRows, pixelFormat, listOf(sprite), byteArrayOf(), true
    )

    private fun operation(slot: Int = 10, sprite: Int = 0, width: Int = 2, height: Int = 1) =
        LegacyConcreteSpriteDrawOperation(
            0, slot, 0, 0, 0, sprite, width, height, 11, 12, 0, 0, 0, 0,
            listOf(0), listOf(0)
        )

    fun verifyExplicitPaletteDecodesIndicesIntoArgb() {
        val decoded = LegacyPaletteAwareSpriteDecoder.decodeResource(parsed(), 10, 0)
        check(decoded.size == 1)
        check(decoded[0].argbPixels.contentEquals(intArrayOf(0xFFF8F8F8.toInt(), 0xFFF80000.toInt())))
        check(decoded[0].paletteIndex == 0)
    }

    fun verifyDifferentPaletteRowsRemainExplicit() {
        val source = parsed(paletteRows = listOf(
            intArrayOf(0xFFFF, 0xFC00), intArrayOf(0x801F, 0x83E0)
        ))
        val row0 = LegacyPaletteAwareSpriteDecoder.decodeResource(source, 10, 0).single()
        val row1 = LegacyPaletteAwareSpriteDecoder.decodeResource(source, 10, 1).single()
        check(!row0.argbPixels.contentEquals(row1.argbPixels))
        check(row1.paletteIndex == 1)
    }

    fun verifyOperationBindingPreservesGeometryAndFlags() {
        val op = operation().copy(x = -7, y = 31, incomingFlags = 5, drawFlags = 9)
        val decoded = LegacyPaletteAwareSpriteDecoder.decodeResource(parsed(), 10, 0)
        val bound = LegacyPaletteAwareSpriteDecoder.bindOperations(listOf(op), decoded, 0).single()
        check(bound.operation.x == -7 && bound.operation.y == 31)
        check(bound.operation.incomingFlags == 5 && bound.operation.drawFlags == 9)
        check(bound.argbPixels.contentEquals(decoded.single().argbPixels))
    }

    fun verifyInvalidPaletteAndMissingPixelsAreRejected() {
        check(runCatching {
            LegacyPaletteAwareSpriteDecoder.decodeResource(parsed(), 10, 1)
        }.isFailure)
        val decoded = LegacyPaletteAwareSpriteDecoder.decodeResource(parsed(), 10, 0)
        check(runCatching {
            LegacyPaletteAwareSpriteDecoder.bindOperations(listOf(operation(11)), decoded, 0)
        }.isFailure)
    }

    fun verifyUnsupportedPaletteFormatIsRejectedWithoutGuessing() {
        check(runCatching {
            LegacyPaletteAwareSpriteDecoder.decodeResource(parsed(paletteFormat = 1234), 10, 0)
        }.isFailure)
    }

    fun verifyDimensionMismatchIsRejected() {
        val decoded = LegacyPaletteAwareSpriteDecoder.decodeResource(parsed(), 10, 0)
        check(runCatching {
            LegacyPaletteAwareSpriteDecoder.bindOperations(listOf(operation(width = 1)), decoded, 0)
        }.isFailure)
    }

    fun runAll() {
        verifyExplicitPaletteDecodesIndicesIntoArgb()
        verifyDifferentPaletteRowsRemainExplicit()
        verifyOperationBindingPreservesGeometryAndFlags()
        verifyInvalidPaletteAndMissingPixelsAreRejected()
        verifyUnsupportedPaletteFormatIsRejectedWithoutGuessing()
        verifyDimensionMismatchIsRejected()
    }
}
