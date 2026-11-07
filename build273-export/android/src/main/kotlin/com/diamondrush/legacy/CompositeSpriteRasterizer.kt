package com.diamondrush.legacy

/**
 * Build 213 rasterizer for the transform values actually emitted by f.a(Graphics,...).
 *
 * Original bytecode passes (drawFlags & 3) directly to MIDP Graphics.drawRegion.
 * MIDP 2.0 constants are: 0 NONE, 1 MIRROR_ROT180, 2 MIRROR, 3 ROT180.
 * Therefore all supported transforms preserve the source width and height.
 */
object CompositeSpriteRasterizer {
    data class RasterizedComposite(
        val width: Int,
        val height: Int,
        val originX: Int,
        val originY: Int,
        val argb: IntArray,
        val drawnSprites: Int
    )

    fun rasterize(
        commands: List<CompositeSpriteObjectResolver.LeafDrawCommand>,
        sprites: List<LegacySpriteDecoder.DecodedSprite>,
        maxDimension: Int = 4096
    ): RasterizedComposite {
        require(commands.isNotEmpty()) { "Composite has no leaf commands" }
        var minX = Int.MAX_VALUE
        var minY = Int.MAX_VALUE
        var maxX = Int.MIN_VALUE
        var maxY = Int.MIN_VALUE
        for (command in commands) {
            require(command.spriteIndex in sprites.indices) {
                "Sprite index ${command.spriteIndex} out of range"
            }
            val sprite = sprites[command.spriteIndex]
            minX = minOf(minX, command.x)
            minY = minOf(minY, command.y)
            maxX = maxOf(maxX, Math.addExact(command.x, sprite.width))
            maxY = maxOf(maxY, Math.addExact(command.y, sprite.height))
        }
        val width = maxX - minX
        val height = maxY - minY
        require(width in 1..maxDimension && height in 1..maxDimension) {
            "Composite bounds ${width}x${height} exceed safety limit $maxDimension"
        }
        val out = IntArray(Math.multiplyExact(width, height))
        for (command in commands) {
            val sprite = sprites[command.spriteIndex]
            val dx = command.x - minX
            val dy = command.y - minY
            val transform = command.drawFlags and 0x03
            for (sy in 0 until sprite.height) {
                for (sx in 0 until sprite.width) {
                    // MIDP TRANS_MIRROR_ROT180 (1): horizontal mirror then 180° rotation = vertical flip.
                    // MIDP TRANS_MIRROR (2): reflection about the vertical center = horizontal flip.
                    // MIDP TRANS_ROT180 (3): both axes reversed.
                    val tx = if ((transform and 0x02) != 0) sprite.width - 1 - sx else sx
                    val ty = if ((transform and 0x01) != 0) sprite.height - 1 - sy else sy
                    val src = sprite.argb[sy * sprite.width + sx]
                    if ((src ushr 24) == 0) continue
                    val di = (dy + ty) * width + dx + tx
                    out[di] = sourceOver(out[di], src)
                }
            }
        }
        return RasterizedComposite(width, height, minX, minY, out, commands.size)
    }

    private fun sourceOver(dst: Int, src: Int): Int {
        val sa = src ushr 24
        if (sa == 255) return src
        if (sa == 0) return dst
        val da = dst ushr 24
        val outA = sa + (da * (255 - sa) + 127) / 255
        if (outA == 0) return 0
        fun channel(shift: Int): Int {
            val sc = (src ushr shift) and 255
            val dc = (dst ushr shift) and 255
            val premul = sc * sa + (dc * da * (255 - sa) + 127) / 255
            return ((premul + outA / 2) / outA).coerceIn(0, 255)
        }
        return (outA shl 24) or (channel(16) shl 16) or
            (channel(8) shl 8) or channel(0)
    }
}
