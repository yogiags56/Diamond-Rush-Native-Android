package com.diamondrush.legacy

object Build238SpriteRasterExecutionChecks {
    private fun draw(
        x: Int,
        y: Int,
        width: Int,
        height: Int,
        pixels: IntArray,
        flags: Int = 0
    ) = LegacyPaletteBoundSpriteDraw(
        LegacyConcreteSpriteDrawOperation(
            0, 10, 0, 0, 0, 0, width, height, x, y,
            0, flags, 0, 0, listOf(0), listOf(0)
        ), 0, pixels, pixels.any { (it ushr 24) != 0xff }
    )

    fun verifyUntransformedBlitAndPainterOrder() {
        val red = 0xffff0000.toInt()
        val blue = 0xff0000ff.toInt()
        val surface = LegacySpriteRasterExecution.rasterize(
            listOf(draw(1, 1, 2, 1, intArrayOf(red, red)), draw(2, 1, 1, 1, intArrayOf(blue))),
            4, 3
        )
        check(surface.argb[1 * 4 + 1] == red)
        check(surface.argb[1 * 4 + 2] == blue)
        check(surface.executedOperations == 2)
    }

    fun verifyMidpHorizontalVerticalAndCombinedTransforms() {
        val a = 0xff000001.toInt(); val b = 0xff000002.toInt()
        val c = 0xff000003.toInt(); val d = 0xff000004.toInt()
        val source = intArrayOf(a, b, c, d)
        fun result(flags: Int) = LegacySpriteRasterExecution.rasterize(
            listOf(draw(0, 0, 2, 2, source, flags)), 2, 2
        ).argb
        check(result(0).contentEquals(intArrayOf(a, b, c, d)))
        check(result(1).contentEquals(intArrayOf(c, d, a, b))) // vertical
        check(result(2).contentEquals(intArrayOf(b, a, d, c))) // horizontal
        check(result(3).contentEquals(intArrayOf(d, c, b, a))) // both
    }

    fun verifyTransparentPixelsDoNotOverwriteDestination() {
        val base = 0xff123456.toInt()
        val surface = LegacySpriteRasterExecution.rasterize(
            listOf(draw(0, 0, 1, 1, intArrayOf(base)), draw(0, 0, 1, 1, intArrayOf(0x00112233))),
            1, 1
        )
        check(surface.argb.single() == base)
        check(surface.skippedTransparentPixels == 1L)
    }

    fun verifyPartialAlphaUsesSourceOver() {
        val dst = 0xff0000ff.toInt()
        val src = 0x80ff0000.toInt()
        val blended = LegacySpriteRasterExecution.sourceOver(dst, src)
        check(blended ushr 24 == 0xff)
        check((blended ushr 16 and 0xff) in 127..129)
        check((blended and 0xff) in 126..128)
    }

    fun verifyClippingAndNegativeCoordinates() {
        val pixels = intArrayOf(0xff000001.toInt(), 0xff000002.toInt(), 0xff000003.toInt(), 0xff000004.toInt())
        val surface = LegacySpriteRasterExecution.rasterize(
            listOf(draw(-1, 0, 2, 2, pixels)), 2, 2,
            LegacyRasterClip(0, 0, 2, 2)
        )
        check(surface.argb.contentEquals(intArrayOf(pixels[1], 0, pixels[3], 0)))
        check(surface.clippedPixels == 2L)
    }

    fun verifyViewportClipAndSurfaceSafety() {
        val white = 0xffffffff.toInt()
        val surface = LegacySpriteRasterExecution.rasterize(
            listOf(draw(0, 0, 1, 1, intArrayOf(white)), draw(319, 239, 1, 1, intArrayOf(white))),
            320, 240, LegacyRasterClip(0, 31, 320, 209)
        )
        check(surface.argb[0] == 0)
        check(surface.argb[239 * 320 + 319] == 0)
        check(runCatching { LegacySpriteRasterExecution.rasterize(emptyList(), 5000, 5000) }.isFailure)
    }

    fun verifyInvalidPixelPayloadIsRejectedAtBindingBoundary() {
        val op = LegacyConcreteSpriteDrawOperation(
            0, 10, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, listOf(0), listOf(0)
        )
        check(runCatching {
            LegacyPaletteBoundSpriteDraw(op, 0, intArrayOf(0xffffffff.toInt()), false)
        }.isFailure)
    }

    fun runAll() {
        verifyUntransformedBlitAndPainterOrder()
        verifyMidpHorizontalVerticalAndCombinedTransforms()
        verifyTransparentPixelsDoNotOverwriteDestination()
        verifyPartialAlphaUsesSourceOver()
        verifyClippingAndNegativeCoordinates()
        verifyViewportClipAndSurfaceSafety()
        verifyInvalidPixelPayloadIsRejectedAtBindingBoundary()
    }
}
