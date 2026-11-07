package com.diamondrush.legacy

/**
 * Build 210: field-aligned representation of the original obfuscated class `f`.
 * Names are kept as JVM field name + descriptor because source names are obfuscated.
 * This parser mirrors the bytecode's actual allocation/copy order; it does not
 * assign semantic names to opaque tables beyond what their consumers prove.
 */
data class LegacySpriteFieldLayout(
    val fDimensions: ByteArray,       // f:[B — two bytes per sprite, used as width/height
    val hComponents: ByteArray,       // h:[B — four bytes per component
    val gGroupCounts: ByteArray,      // g:[B — one component count per group
    val bGroupStarts: ShortArray,     // b:[S — component-record start per group
    val aGroupRecords: ByteArray,    // a:[B — four bytes per group
    val cFiveByteRecords: ByteArray, // c:[B — five bytes per record
    val bByteTable: ByteArray,       // b:[B — one byte per record
    val aShortTable: ShortArray,     // a:[S — one short per record
    val paletteFormat: Int,
    val paletteCount: Int,
    val colorsPerPalette: Int,
    val palettesArgb: List<IntArray>,
    val pixelFormat: Int,
    val spritePayloadOffsets: IntArray, // c:[S in original, widened here for safe indexing
    val spritePayloads: List<ByteArray>,
    val concatenatedPixelBytes: ByteArray,
    val trailingBytes: ByteArray
) {
    val spriteCount: Int get() = fDimensions.size / 2
    val groupCount: Int get() = gGroupCounts.size
}

object LegacySpriteFieldLayoutParser {
    private val paletteFormats = setOf(-30584, 17476, 21781, 25861)

    /**
     * The original bytecode hardcodes header offsets 6 and 7, despite receiving
     * an int argument. Callers pass a sliced resource beginning at byte zero.
     */
    fun parse(data: ByteArray): LegacySpriteFieldLayout {
        require(data.size >= 8) { "DF03 resource is truncated" }
        require(data[0] == 0xDF.toByte() && data[1] == 0x03.toByte() &&
            data[2] == 0x01.toByte() && data[3] == 0x01.toByte()) { "Unsupported DF03 signature" }
        val c = Cursor(data, 6)
        val spriteCount = c.signedShort().coerceAtLeast(0)
        val f = c.bytes(checkedProduct(spriteCount, 2))

        val hCount = c.signedShort().coerceAtLeast(0)
        val h = c.bytes(checkedProduct(hCount, 4))

        val groupCount = c.signedShort().coerceAtLeast(0)
        val g = ByteArray(groupCount)
        val bStarts = ShortArray(groupCount)
        repeat(groupCount) { i ->
            g[i] = c.byte()
            c.skip(1)
            bStarts[i] = c.signedShort().toShort()
        }
        val aGroups = c.bytes(checkedProduct(groupCount, 4))

        val cCount = c.signedShort().coerceAtLeast(0)
        val cRecords = c.bytes(checkedProduct(cCount, 5))

        val bCount = c.signedShort().coerceAtLeast(0)
        val bTable = ByteArray(bCount)
        val aShorts = ShortArray(bCount)
        repeat(bCount) { i ->
            bTable[i] = c.byte()
            c.skip(1)
            aShorts[i] = c.signedShort().toShort()
        }

        if (spriteCount == 0) {
            return LegacySpriteFieldLayout(f, h, g, bStarts, aGroups, cRecords, bTable,
                aShorts, 0, 0, 0, emptyList(), 0, intArrayOf(), emptyList(),
                byteArrayOf(), c.rest())
        }

        val paletteFormat = c.signedShort()
        val paletteCount = c.unsignedByte()
        val colorsPerPalette = c.unsignedByte()
        require(paletteCount <= 16) { "Original fixed palette array has 16 slots; count=$paletteCount" }
        val palettes = ArrayList<IntArray>(paletteCount)
        repeat(paletteCount) {
            val colors = IntArray(colorsPerPalette)
            if (paletteFormat in paletteFormats) {
                repeat(colorsPerPalette) { i ->
                    colors[i] = when (paletteFormat) {
                        -30584 -> c.intLittleEndian()
                        17476 -> expand4444(c.unsignedShort())
                        21781 -> expand1555(c.unsignedShort())
                        25861 -> expand565(c.unsignedShort())
                        else -> error("unreachable")
                    }
                }
            }
            palettes += colors
        }
        val pixelFormat = c.signedShort()
        // Original bytecode uses a moving cursor: read a short length, skip that
        // sprite's payload, then read the next short. This is interleaved records.
        val lengthStreamStart = c.position
        val offsets = IntArray(spriteCount)
        val lengths = IntArray(spriteCount)
        var total = 0
        repeat(spriteCount) { i ->
            val length = c.signedShort()
            require(length >= 0) { "Negative sprite length $length at index $i" }
            lengths[i] = length
            offsets[i] = total
            c.skip(length)
            total = Math.addExact(total, length)
        }
        // The original second pass copies each payload from after its length word.
        val payloadCursor = Cursor(data, lengthStreamStart)
        val payloads = lengths.map { length -> payloadCursor.skip(2); payloadCursor.bytes(length) }
        val allPixels = ByteArray(total)
        var pixelOut = 0
        for (payload in payloads) { payload.copyInto(allPixels, pixelOut); pixelOut += payload.size }
        return LegacySpriteFieldLayout(f, h, g, bStarts, aGroups, cRecords, bTable,
            aShorts, paletteFormat, paletteCount, colorsPerPalette, palettes,
            pixelFormat, offsets, payloads, allPixels, c.rest())
    }

    private fun checkedProduct(a: Int, b: Int): Int = Math.multiplyExact(a, b)
    private fun expand4444(v: Int): Int =
        (((v ushr 12) and 15) * 17 shl 24) or (((v ushr 8) and 15) * 17 shl 16) or
        (((v ushr 4) and 15) * 17 shl 8) or ((v and 15) * 17)
    private fun expand1555(v: Int): Int =
        (if ((v and 0x8000) != 0) 0xFF000000.toInt() else 0) or
        ((v and 0x7C00) shl 9) or ((v and 0x03E0) shl 6) or ((v and 0x001F) shl 3)
    private fun expand565(v: Int): Int =
        if (v == 0xF81F) 0 else 0xFF000000.toInt() or
            ((v and 0xF800) shl 8) or ((v and 0x07E0) shl 5) or ((v and 0x001F) shl 3)

    private class Cursor(private val data: ByteArray, start: Int) {
        private var p = start
        val position: Int get() = p
        private fun need(n: Int) { require(n >= 0 && p.toLong() + n <= data.size.toLong()) { "Truncated at $p; need $n; size ${data.size}" } }
        fun byte(): Byte { need(1); return data[p++] }
        fun skip(n: Int) { need(n); p += n }
        fun signedShort(): Int { val lo = unsignedByte(); val hi = unsignedByte(); return (lo or (hi shl 8)).toShort().toInt() }
        fun unsignedByte(): Int = byte().toInt() and 255
        fun unsignedShort(): Int { val lo = unsignedByte(); val hi = unsignedByte(); return lo or (hi shl 8) }
        fun intLittleEndian(): Int { val lo = unsignedShort(); val hi = unsignedShort(); return lo or (hi shl 16) }
        fun bytes(n: Int): ByteArray { need(n); return data.copyOfRange(p, p + n).also { p += n } }
        fun rest(): ByteArray = bytes(data.size - p)
    }
}
