package com.diamondrush.legacy

/**
 * A conservative structural trace of f.a(byte[], int), reconstructed from the
 * original JVM bytecode. Table names are positional only: no gameplay meaning
 * is assigned to the opaque tables until their consumers are audited.
 *
 * Important: this is not yet a replacement production resource parser. Some
 * DF03 entries do not satisfy this method's control-flow and palette checks.
 */
data class LegacySpriteBytecodeTrace(
    val spriteDimensions: ByteArray,
    val secondaryTwoByteTable: ByteArray,
    val table3Descriptors: ByteArray,
    val table3FourByteRecords: ByteArray,
    val fiveByteTable: ByteArray,
    val table5Descriptors: ByteArray,
    val paletteFormat: Int,
    val paletteCount: Int,
    val colorsPerPalette: Int,
    val paletteBytes: ByteArray,
    val pixelFormat: Int,
    val spritePayloadOffsets: IntArray,
    val spritePayloads: List<ByteArray>,
    val trailingBytes: ByteArray
) {
    val spriteCount: Int get() = spriteDimensions.size / 2
}

@Deprecated("Build 209 field widths were misidentified; use LegacySpriteFieldLayoutParser from Build 210.")
object LegacySpriteBytecodeTraceParser {
    private val supportedPaletteFormats = setOf(-30584, 17476, 21781, 25861)

    fun parse(data: ByteArray, startOffset: Int = 0): LegacySpriteBytecodeTrace {
        require(startOffset >= 0 && startOffset.toLong() + 8L <= data.size.toLong()) {
            "DF03 header/count region is truncated"
        }
        require(data[0] == 0xDF.toByte() && data[1] == 0x03.toByte() &&
            data[2] == 0x01.toByte() && data[3] == 0x01.toByte()) {
            "Unsupported DF03 signature/version"
        }
        val c = Cursor(data, startOffset + 6)
        // The original method only enters each allocation/copy branch for count > 0.
        // Zero and negative signed-short counts therefore consume no table bytes.
        val spriteCount = c.signedShort().coerceAtLeast(0)
        val dimensions = if (spriteCount > 0) c.bytes(Math.multiplyExact(spriteCount, 2)) else byteArrayOf()

        val secondaryCount = c.signedShort().coerceAtLeast(0)
        val secondary = if (secondaryCount > 0) c.bytes(Math.multiplyExact(secondaryCount, 2)) else byteArrayOf()

        val table3Count = c.signedShort().coerceAtLeast(0)
        // The original method reads byte, skips byte, then reads a signed short.
        val descriptors3 = c.bytes(Math.multiplyExact(table3Count, 4))
        val records3 = c.bytes(Math.multiplyExact(table3Count, 4))

        val fiveCount = c.signedShort().coerceAtLeast(0)
        val five = if (fiveCount > 0) c.bytes(Math.multiplyExact(fiveCount, 5)) else byteArrayOf()

        val table5Count = c.signedShort().coerceAtLeast(0)
        // The original method reads one byte, skips one byte, then reads a short.
        val descriptors5 = if (table5Count > 0) c.bytes(Math.multiplyExact(table5Count, 4)) else byteArrayOf()

        // The original method returns here when spriteCount <= 0.
        if (spriteCount == 0) {
            return LegacySpriteBytecodeTrace(dimensions, secondary, descriptors3, records3,
                five, descriptors5, 0, 0, 0, byteArrayOf(), 0, intArrayOf(), emptyList(), c.rest())
        }

        val paletteFormat = c.signedShort()
        val paletteCount = c.unsignedByte()
        val colorsPerPalette = c.unsignedByte()
        require(paletteCount <= 16) { "Palette count $paletteCount exceeds original 16-slot array" }
        val paletteBytes = if (paletteFormat in supportedPaletteFormats) {
            val entryBytes = if (paletteFormat == -30584) 4 else 2
            c.bytes(Math.multiplyExact(Math.multiplyExact(paletteCount, colorsPerPalette), entryBytes))
        } else {
            // The original lookupswitch default branch consumes no palette data.
            byteArrayOf()
        }
        val pixelFormat = c.signedShort()

        // Each sprite is encoded as [signed-short length][payload], not as a
        // separate length table followed by a concatenated payload block.
        val offsets = IntArray(spriteCount)
        val payloads = ArrayList<ByteArray>(spriteCount)
        var total = 0
        repeat(spriteCount) { index ->
            val length = c.signedShort()
            require(length >= 0) { "Negative sprite payload length $length at index $index" }
            offsets[index] = total
            payloads += c.bytes(length)
            total = Math.addExact(total, length)
        }
        return LegacySpriteBytecodeTrace(dimensions, secondary, descriptors3, records3,
            five, descriptors5, paletteFormat, paletteCount, colorsPerPalette,
            paletteBytes, pixelFormat, offsets, payloads, c.rest())
    }

    private class Cursor(private val bytes: ByteArray, start: Int) {
        private var p = start
        private fun need(n: Int) {
            require(n >= 0 && p.toLong() + n.toLong() <= bytes.size.toLong()) {
                "Truncated at $p, need $n, size ${bytes.size}"
            }
        }
        fun signedShort(): Int {
            val lo = unsignedByte(); val hi = unsignedByte()
            return (lo or (hi shl 8)).toShort().toInt()
        }
        fun unsignedByte(): Int { need(1); return bytes[p++].toInt() and 0xFF }
        fun bytes(n: Int): ByteArray { need(n); return bytes.copyOfRange(p, p + n).also { p += n } }
        fun rest(): ByteArray = bytes(bytes.size - p)
    }
}
