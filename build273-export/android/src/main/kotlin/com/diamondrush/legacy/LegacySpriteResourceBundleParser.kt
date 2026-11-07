package com.diamondrush.legacy

/**
 * Bytecode-aligned reader for the original .f bundle directory and DF03 sprite
 * payload consumed by i.f.a(byte[], int).
 *
 * Resource directory entry indexes are not sprite indexes. The parser keeps
 * opaque tables intact rather than assigning gameplay meaning to them.
 */
object LegacySpriteResourceBundleParser {
    private val signature = byteArrayOf(0xDF.toByte(), 0x03, 0x01, 0x01)

    data class BundleEntry(
        val index: Int,
        val offset: Long,
        val length: Long,
        val payload: ByteArray
    )

    data class SpritePayload(
        val index: Int,
        val width: Int,
        val height: Int,
        val encodedPixels: ByteArray
    )

    data class ParsedDf03(
        val headerTail: ByteArray,
        val spriteDimensions: ByteArray,
        val fourByteTable: ByteArray,
        val metadataRows: List<MetadataRow>,
        val pairedFourByteTable: ByteArray,
        val fiveByteTable: ByteArray,
        val byteShortRows: List<ByteShortRow>,
        val paletteFormat: Int?,
        val paletteCount: Int,
        val colorsPerPalette: Int,
        val palettes: List<IntArray>,
        val pixelFormat: Int?,
        val sprites: List<SpritePayload>,
        val trailingBytes: ByteArray,
        val hasTransparency: Boolean
    )

    data class MetadataRow(val first: Int, val skipped: Int, val value: Int)
    data class ByteShortRow(val first: Int, val skipped: Int, val value: Int)

    @JvmStatic
    fun readBundleEntries(bundle: ByteArray): List<BundleEntry> {
        require(bundle.isNotEmpty()) { "Empty resource bundle" }
        val count = bundle[0].toInt() and 0xff
        val directoryEnd = 1L + count.toLong() * 8L
        require(directoryEnd <= bundle.size.toLong()) { "Truncated resource directory" }
        val out = ArrayList<BundleEntry>(count)
        repeat(count) { index ->
            val record = 1 + index * 8
            val offset = u32(bundle, record)
            val length = u32(bundle, record + 4)
            val start = directoryEnd + offset
            val end = start + length
            require(start >= directoryEnd && end >= start && end <= bundle.size.toLong()) {
                "Bundle entry $index is outside the resource bundle"
            }
            out += BundleEntry(index, offset, length, bundle.copyOfRange(start.toInt(), end.toInt()))
        }
        return out
    }

    @JvmStatic
    fun parse(payload: ByteArray): ParsedDf03 {
        require(payload.size >= 8) { "DF03 payload shorter than fixed header" }
        require(payload.copyOfRange(0, 4).contentEquals(signature)) { "Invalid DF03 signature" }
        val c = Cursor(payload, 6)
        val spriteCount = c.s16("sprite count").coerceAtLeast(0)
        val spriteDimensions = c.take(spriteCount * 2, "sprite dimensions")

        val fourByteCount = c.s16("four-byte table count").coerceAtLeast(0)
        val fourByteTable = c.take(fourByteCount * 4, "four-byte table")

        val metadataCount = c.s16("metadata row count").coerceAtLeast(0)
        val metadataRows = ArrayList<MetadataRow>(metadataCount)
        repeat(metadataCount) {
            val first = c.u8("metadata first byte")
            val skipped = c.u8("metadata skipped byte")
            val value = c.s16("metadata short")
            metadataRows += MetadataRow(first, skipped, value)
        }
        // The original allocates this byte array as count << 2, not count << 1.
        val pairedFourByteTable = c.take(metadataCount * 4, "paired four-byte table")

        val fiveCount = c.s16("five-byte table count").coerceAtLeast(0)
        val fiveByteTable = c.take(fiveCount * 5, "five-byte table")

        val byteShortCount = c.s16("byte/short table count").coerceAtLeast(0)
        val byteShortRows = ArrayList<ByteShortRow>(byteShortCount)
        repeat(byteShortCount) {
            val first = c.u8("byte/short first byte")
            val skipped = c.u8("byte/short skipped byte")
            val value = c.s16("byte/short value")
            byteShortRows += ByteShortRow(first, skipped, value)
        }

        if (spriteCount == 0) {
            return ParsedDf03(
                payload.copyOfRange(4, 6), spriteDimensions, fourByteTable,
                metadataRows, pairedFourByteTable, fiveByteTable, byteShortRows,
                null, 0, 0, emptyList(), null, emptyList(), c.remaining(), false
            )
        }

        val paletteFormat = c.s16("palette format")
        val paletteCount = c.u8("palette count")
        val colorsPerPalette = c.u8("colors per palette")
        require(paletteCount <= 16) {
            "Original decoder has a 16-row palette array; count $paletteCount would overflow it"
        }
        val palettes = ArrayList<IntArray>(paletteCount)
        var hasTransparency = false
        // The original lookupswitch default branch consumes no palette bytes.
        if (paletteFormat == -30584 || paletteFormat == 17476 ||
            paletteFormat == 21781 || paletteFormat == 25861) {
            repeat(paletteCount) {
                val colors = IntArray(colorsPerPalette)
                repeat(colorsPerPalette) { colorIndex ->
                    when (paletteFormat) {
                        -30584 -> {
                            val value = c.i32("ARGB8888 palette entry")
                            if ((value and -0x1000000) != -0x1000000) hasTransparency = true
                            colors[colorIndex] = value
                        }
                        17476 -> {
                            val value = c.u16("ARGB4444 palette entry")
                            if ((value and 0xF000) != 0xF000) hasTransparency = true
                            colors[colorIndex] = value
                        }
                        21781 -> {
                            val value = c.u16("ARGB1555 palette entry")
                            if ((value and 0x8000) != 0x8000) hasTransparency = true
                            colors[colorIndex] = value
                        }
                        25861 -> {
                            val value = c.u16("RGB565 palette entry")
                            if (value == 63519) hasTransparency = true
                            colors[colorIndex] = value
                        }
                    }
                }
                palettes += colors
            }
        }

        val pixelFormat = c.s16("pixel format")
        // The original bytecode consumes an interleaved stream:
        // [signed-short length][that sprite's encoded bytes], repeated per sprite.
        // Reading all lengths first silently misaligns every multi-sprite resource.
        var totalPixelBytes = 0L
        val sprites = ArrayList<SpritePayload>(spriteCount)
        repeat(spriteCount) { index ->
            val length = c.s16("sprite $index encoded length")
            require(length >= 0) { "Negative sprite length $length at sprite $index" }
            totalPixelBytes += length.toLong()
            require(totalPixelBytes <= Int.MAX_VALUE) { "Sprite payload aggregate is too large" }
            val width = spriteDimensions[index * 2].toInt() and 0xff
            val height = spriteDimensions[index * 2 + 1].toInt() and 0xff
            val encoded = c.take(length, "sprite $index pixel payload")
            sprites += SpritePayload(index, width, height, encoded)
        }

        return ParsedDf03(
            payload.copyOfRange(4, 6), spriteDimensions, fourByteTable,
            metadataRows, pairedFourByteTable, fiveByteTable, byteShortRows,
            paletteFormat, paletteCount, colorsPerPalette, palettes, pixelFormat,
            sprites, c.remaining(), hasTransparency
        )
    }

    private class Cursor(private val data: ByteArray, start: Int) {
        private var position = start
        fun u8(label: String): Int {
            require(position < data.size) { "Truncated $label at byte $position" }
            return data[position++].toInt() and 0xff
        }
        fun u16(label: String): Int = u8(label).or(u8(label) shl 8)
        fun s16(label: String): Int = u16(label).toShort().toInt()
        fun i32(label: String): Int =
            u8(label) or (u8(label) shl 8) or (u8(label) shl 16) or (u8(label) shl 24)
        fun take(length: Int, label: String): ByteArray {
            require(length >= 0 && position.toLong() + length <= data.size.toLong()) {
                "Truncated $label at byte $position, need $length, size ${data.size}"
            }
            val out = data.copyOfRange(position, position + length)
            position += length
            return out
        }
        fun remaining(): ByteArray = data.copyOfRange(position, data.size)
    }

    private fun u32(data: ByteArray, offset: Int): Long =
        (data[offset].toLong() and 0xffL) or
            ((data[offset + 1].toLong() and 0xffL) shl 8) or
            ((data[offset + 2].toLong() and 0xffL) shl 16) or
            ((data[offset + 3].toLong() and 0xffL) shl 24)
}
