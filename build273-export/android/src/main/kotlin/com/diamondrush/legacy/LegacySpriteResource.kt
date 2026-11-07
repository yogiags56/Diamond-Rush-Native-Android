package com.diamondrush.legacy

/** Historical Build 208 model. Its table alignment is superseded by Build 209; do not use as authoritative original-JAR parsing. */
data class LegacySpriteResource(
    val compositeSection: LegacySpriteCompositeSection,
    val spriteDimensions: ByteArray,
    val opaqueFiveByteRecords: ByteArray,
    val opaqueByteShortRecords: ByteArray,
    val paletteFormat: Int,
    val palettes: List<IntArray>,
    val pixelFormat: Int,
    val spritePayloadOffsets: IntArray,
    val spritePayloads: List<ByteArray>,
    val trailingBytes: ByteArray
) {
    val spriteCount: Int get() = spriteDimensions.size / 2
    fun width(index: Int): Int = spriteDimensions[index * 2].toInt() and 0xff
    fun height(index: Int): Int = spriteDimensions[index * 2 + 1].toInt() and 0xff
}

/** Provisional Build 208 parser; superseded by LegacySpriteBytecodeTraceParser pending Build 210 field-consumer audit. */
@Deprecated("Build 208 table alignment was superseded by Build 209; use LegacySpriteBytecodeTraceParser for positional tracing.")
object LegacySpriteResourceParser {
    private const val MAGIC = 0xDF030101.toInt()

    fun parse(data: ByteArray): LegacySpriteResource {
        require(data.size >= 8) { "DF03 resource is truncated" }
        val header = ((data[0].toInt() and 255) shl 24) or
            ((data[1].toInt() and 255) shl 16) or
            ((data[2].toInt() and 255) shl 8) or (data[3].toInt() and 255)
        require(header == MAGIC) { "Unsupported resource signature" }
        val c = Cursor(data, 6)
        val spriteCount = c.signedShort()
        require(spriteCount >= 0) { "Negative sprite count" }
        val dimensions = c.bytes(spriteCount * 2)
        val recordCount = c.signedShort()
        require(recordCount >= 0) { "Negative component record count" }
        val records = c.bytes(recordCount * 4)
        val groupCount = c.signedShort()
        require(groupCount >= 0) { "Negative composite group count" }
        val counts = ByteArray(groupCount)
        val starts = ShortArray(groupCount)
        repeat(groupCount) { i ->
            counts[i] = c.byte()
            c.byte() // Reserved/unknown byte; preserved only by the raw source in this version.
            starts[i] = c.signedShort().toShort()
        }
        val groupDimensions = c.bytes(groupCount * 2)
        val fiveCount = c.signedShort()
        require(fiveCount >= 0) { "Negative five-byte record count" }
        val fiveRecords = c.bytes(fiveCount * 5)
        val pairCount = c.signedShort()
        require(pairCount >= 0) { "Negative byte/short record count" }
        val pairRecords = c.bytes(pairCount * 4)
        val paletteFormat = c.signedShort()
        val paletteCount = c.byte().toInt() and 0xff
        val colorCount = c.byte().toInt() and 0xff
        require(paletteCount in 0..16) { "Palette count outside original 16-slot table" }
        val paletteEntryBytes = if (paletteFormat == -30584) 4 else 2
        val palettes = List(paletteCount) {
            IntArray(colorCount) { if (paletteEntryBytes == 4) c.intLittleEndian() else c.unsignedShort() }
        }
        val pixelFormat = c.signedShort()
        val lengths = IntArray(spriteCount) { c.signedShort().also { n -> require(n >= 0) { "Negative sprite payload length" } } }
        val offsets = IntArray(spriteCount)
        var total = 0
        for (i in lengths.indices) { offsets[i] = total; total = Math.addExact(total, lengths[i]) }
        val payloads = List(spriteCount) { c.bytes(lengths[it]) }
        val trailing = c.remainingBytes()
        val section = LegacySpriteCompositeSection(
            spriteDimensionBytes = dimensions,
            componentRecords = records,
            componentCounts = counts,
            componentStarts = starts,
            groupAuxiliaryBytes = groupDimensions,
            consumedBytes = c.position
        )
        return LegacySpriteResource(section, dimensions, fiveRecords, pairRecords,
            paletteFormat, palettes, pixelFormat, offsets, payloads, trailing)
    }

    private class Cursor(private val data: ByteArray, start: Int) {
        private var p = start
        val position: Int get() = p
        private fun need(n: Int) { require(n >= 0 && p.toLong() + n <= data.size) { "Truncated DF03 resource at $p (need $n)" } }
        fun byte(): Byte { need(1); return data[p++] }
        fun signedShort(): Int { val lo = byte().toInt() and 255; val hi = byte().toInt() and 255; return (lo or (hi shl 8)).toShort().toInt() }
        fun bytes(n: Int): ByteArray { need(n); return data.copyOfRange(p, p + n).also { p += n } }
        fun unsignedShort(): Int { val lo=byte().toInt() and 255; val hi=byte().toInt() and 255; return lo or (hi shl 8) }
        fun intLittleEndian(): Int { val a=unsignedShort(); val b=unsignedShort(); return a or (b shl 16) }
        fun remainingBytes(): ByteArray = bytes(data.size - p)
    }
}
