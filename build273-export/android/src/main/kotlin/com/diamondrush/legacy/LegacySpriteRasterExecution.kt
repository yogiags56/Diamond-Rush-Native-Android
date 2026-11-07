package com.diamondrush.legacy

/** Half-open clipping rectangle in logical-canvas coordinates. */
data class LegacyRasterClip(
    val left: Int,
    val top: Int,
    val rightExclusive: Int,
    val bottomExclusive: Int
) {
    init {
        require(rightExclusive >= left) { "Clip right edge precedes left edge" }
        require(bottomExclusive >= top) { "Clip bottom edge precedes top edge" }
    }
}

/** Deterministic ARGB surface produced by executing palette-bound sprite draws. */
data class LegacyRasterizedSurface(
    val width: Int,
    val height: Int,
    val argb: IntArray,
    val executedOperations: Int,
    val skippedTransparentPixels: Long,
    val clippedPixels: Long
) {
    init {
        require(width > 0 && height > 0)
        require(argb.size == width * height)
    }
}

/**
 * Build 238: execute concrete sprite draw operations onto a bounded ARGB surface.
 *
 * Transform semantics are the MIDP Graphics.drawRegion values proven in Build 213:
 * bit 1 (value 1) flips vertically, bit 2 (value 2) flips horizontally, and 3
 * flips both axes. The operation list order is preserved as painter's order.
 * Coordinates are already in logical-canvas space; camera translation and scene
 * composition remain upstream responsibilities.
 */
object LegacySpriteRasterExecution {
    @JvmStatic
    fun rasterize(
        draws: List<LegacyPaletteBoundSpriteDraw>,
        width: Int = 320,
        height: Int = 240,
        clip: LegacyRasterClip = LegacyRasterClip(0, 0, width, height),
        maxPixels: Int = 16 * 1024 * 1024
    ): LegacyRasterizedSurface {
        require(width > 0 && height > 0) { "Surface dimensions must be positive" }
        val pixelCount = Math.multiplyExact(width, height)
        require(pixelCount <= maxPixels) { "Surface exceeds safety limit of $maxPixels pixels" }
        val out = IntArray(pixelCount)
        val clipLeft = maxOf(0, clip.left)
        val clipTop = maxOf(0, clip.top)
        val clipRight = minOf(width, clip.rightExclusive)
        val clipBottom = minOf(height, clip.bottomExclusive)
        var transparentSkipped = 0L
        var clipped = 0L

        for (draw in draws) {
            val op = draw.operation
            require(op.spriteWidth > 0 && op.spriteHeight > 0)
            require(draw.argbPixels.size == Math.multiplyExact(op.spriteWidth, op.spriteHeight)) {
                "Pixel payload does not match f[${op.globalArraySlot}] sprite ${op.spriteIndex}"
            }
            val right = Math.addExact(op.x, op.spriteWidth)
            val bottom = Math.addExact(op.y, op.spriteHeight)
            val visibleLeft = maxOf(op.x, clipLeft)
            val visibleTop = maxOf(op.y, clipTop)
            val visibleRight = minOf(right, clipRight)
            val visibleBottom = minOf(bottom, clipBottom)
            val visibleWidth = maxOf(0, visibleRight - visibleLeft)
            val visibleHeight = maxOf(0, visibleBottom - visibleTop)
            clipped += op.spriteWidth.toLong() * op.spriteHeight - visibleWidth.toLong() * visibleHeight
            if (visibleWidth == 0 || visibleHeight == 0) continue

            val transform = op.drawFlags and 0x03
            for (dy in visibleTop until visibleBottom) {
                val localY = dy - op.y
                val sourceY = if ((transform and 0x01) != 0) op.spriteHeight - 1 - localY else localY
                for (dx in visibleLeft until visibleRight) {
                    val localX = dx - op.x
                    val sourceX = if ((transform and 0x02) != 0) op.spriteWidth - 1 - localX else localX
                    val source = draw.argbPixels[sourceY * op.spriteWidth + sourceX]
                    val alpha = source ushr 24
                    if (alpha == 0) {
                        transparentSkipped++
                        continue
                    }
                    val destinationIndex = dy * width + dx
                    out[destinationIndex] = sourceOver(out[destinationIndex], source)
                }
            }
        }
        return LegacyRasterizedSurface(
            width, height, out, draws.size, transparentSkipped, clipped
        )
    }

    /** Straight-alpha source-over blend with deterministic integer rounding. */
    @JvmStatic
    fun sourceOver(destination: Int, source: Int): Int {
        val sourceAlpha = source ushr 24
        if (sourceAlpha == 0) return destination
        if (sourceAlpha == 255) return source
        val destinationAlpha = destination ushr 24
        val inverseSourceAlpha = 255 - sourceAlpha
        val outputAlpha = sourceAlpha + (destinationAlpha * inverseSourceAlpha + 127) / 255
        if (outputAlpha == 0) return 0

        fun channel(shift: Int): Int {
            val sourceChannel = (source ushr shift) and 0xff
            val destinationChannel = (destination ushr shift) and 0xff
            val premultiplied = sourceChannel * sourceAlpha +
                (destinationChannel * destinationAlpha * inverseSourceAlpha + 127) / 255
            return ((premultiplied + outputAlpha / 2) / outputAlpha).coerceIn(0, 255)
        }
        return (outputAlpha shl 24) or (channel(16) shl 16) or
            (channel(8) shl 8) or channel(0)
    }
}
