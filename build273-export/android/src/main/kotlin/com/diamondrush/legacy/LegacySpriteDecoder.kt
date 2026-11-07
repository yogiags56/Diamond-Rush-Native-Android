package com.diamondrush.legacy

/**
 * Pure Kotlin implementation of the pixel-index and palette operations
 * identified in the original J2ME class f bytecode.
 *
 * This module deliberately does not parse the full .f container yet.
 */
object LegacySpriteDecoder {
    data class DecodedSprite(
        val width: Int,
        val height: Int,
        val argb: IntArray,
        val hasTransparency: Boolean
    )

    fun decodeIndices(data: ByteArray, width: Int, height: Int, format: Int): IntArray {
        require(width > 0 && height > 0) { "Sprite dimensions must be positive" }
        val countLong = width.toLong() * height.toLong()
        require(countLong <= Int.MAX_VALUE) { "Sprite is too large" }
        val count = countLong.toInt()
        val out = IntArray(count)
        var outPos = 0
        var p = 0

        fun nextByte(): Int {
            require(p < data.size) { "Truncated pixel payload at byte $p" }
            return data[p++].toInt() and 0xff
        }

        when (format) {
            10225 -> { // 0x27F1: indexed RLE
                while (outPos < count) {
                    val token = nextByte()
                    if (token >= 128) {
                        val run = token - 128
                        require(run > 0) { "Zero-length RLE run at byte ${p - 1}" }
                        val index = nextByte()
                        require(run <= count - outPos) { "RLE run exceeds sprite dimensions" }
                        repeat(run) { out[outPos++] = index }
                    } else {
                        out[outPos++] = token
                    }
                }
            }
            5632 -> { // 0x1600: indexed 4bpp, high nibble first
                while (outPos < count) {
                    val b = nextByte()
                    out[outPos++] = (b ushr 4) and 0x0f
                    if (outPos < count) out[outPos++] = b and 0x0f
                }
            }
            1024 -> { // 0x0400: indexed 2bpp, most significant pair first
                while (outPos < count) {
                    val b = nextByte()
                    for (shift in intArrayOf(6, 4, 2, 0)) {
                        if (outPos < count) out[outPos++] = (b ushr shift) and 0x03
                    }
                }
            }
            512 -> { // 0x0200: indexed 1bpp, most significant bit first
                while (outPos < count) {
                    val b = nextByte()
                    for (shift in 7 downTo 0) {
                        if (outPos < count) out[outPos++] = (b ushr shift) and 1
                    }
                }
            }
            22018 -> { // 0x5602: direct 8-bit palette indices
                while (outPos < count) out[outPos++] = nextByte()
            }
            22258 -> { // 0x56F2: RLE; run token then repeated palette index, literal token otherwise
                while (outPos < count) {
                    val token = nextByte()
                    if (token > 127) {
                        val literalCount = token - 128
                        require(literalCount > 0 && literalCount <= count - outPos) { "Invalid 0x56F2 literal run" }
                        repeat(literalCount) { out[outPos++] = nextByte() }
                    } else {
                        val run = token
                        require(run > 0 && run <= count - outPos) { "Invalid 0x56F2 repeated run" }
                        val index = nextByte()
                        repeat(run) { out[outPos++] = index }
                    }
                }
            }
            else -> throw IllegalArgumentException("Unsupported pixel format: $format")
        }
        return out
    }

    fun decodePalette(raw: IntArray, format: Int): IntArray {
        return IntArray(raw.size) { i ->
            val v = raw[i]
            when (format) {
                -30584 -> v // 0x8888: ARGB8888, stored directly
                17476 -> { // 0x4444: each nibble is shifted into its channel
                    ((v and 0xf000) shl 16) or ((v and 0xf000) shl 12) or
                    ((v and 0x0f00) shl 12) or ((v and 0x0f00) shl 8) or
                    ((v and 0x00f0) shl 8) or ((v and 0x00f0) shl 4) or
                    ((v and 0x000f) shl 4) or (v and 0x000f)
                }
                21781 -> { // 0x5515: ARGB1555
                    val alpha = if ((v and 0x8000) != 0) 0xff000000.toInt() else 0
                    alpha or ((v and 0x7c00) shl 9) or
                    ((v and 0x03e0) shl 6) or ((v and 0x001f) shl 3)
                }
                25861 -> { // 0x6505: RGB565; magenta key is transparent
                    if (v == 0xf81f) 0
                    else 0xff000000.toInt() or ((v and 0xf800) shl 8) or
                        ((v and 0x07e0) shl 5) or ((v and 0x001f) shl 3)
                }
                else -> throw IllegalArgumentException("Unsupported palette format: $format")
            }
        }
    }

    fun decode(
        data: ByteArray,
        width: Int,
        height: Int,
        pixelFormat: Int,
        rawPalette: IntArray,
        paletteFormat: Int
    ): DecodedSprite {
        val indices = decodeIndices(data, width, height, pixelFormat)
        val palette = decodePalette(rawPalette, paletteFormat)
        val pixels = IntArray(indices.size)
        var transparent = false
        for (i in indices.indices) {
            val index = indices[i]
            require(index < palette.size) {
                "Palette index $index at pixel $i exceeds palette size ${palette.size}"
            }
            val color = palette[index]
            pixels[i] = color
            if ((color ushr 24) != 0xff) transparent = true
        }
        return DecodedSprite(width, height, pixels, transparent)
    }
}
