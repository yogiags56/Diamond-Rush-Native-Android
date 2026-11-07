package com.diamondrush.legacy

/**
 * Composite view backed by the field-aligned Build 210 parser.
 * The trailing per-group auxiliary bytes are retained without assigning meaning.
 * Use [fromFieldLayout] for real resources. The old [parse] convenience parser is
 * deprecated because it consumes the auxiliary table with an obsolete width.
 */
data class LegacySpriteCompositeSection(
    val spriteDimensionBytes: ByteArray,
    val componentRecords: ByteArray,
    val componentCounts: ByteArray,
    val componentStarts: ShortArray,
    val groupAuxiliaryBytes: ByteArray,
    val consumedBytes: Int
) {
    val groupCount: Int get() = componentCounts.size
    val componentRecordCount: Int get() = componentRecords.size / CompositeSpriteRecord.RECORD_SIZE

    @Deprecated("Use groupAuxiliaryBytes; this is an opaque four-byte-per-group table, not dimensions.")
    val groupDimensionBytes: ByteArray get() = groupAuxiliaryBytes

    fun graphIndex(): CompositeSpriteGraphIndex =
        CompositeSpriteGraphIndex(componentCounts, componentStarts, componentRecords)

    companion object {
        /** Build 210+ factory: consume the field-aligned parser, never the historical partial parser. */
        fun fromFieldLayout(layout: LegacySpriteFieldLayout): LegacySpriteCompositeSection =
            LegacySpriteCompositeSection(
                spriteDimensionBytes = layout.fDimensions,
                componentRecords = layout.hComponents,
                componentCounts = layout.gGroupCounts,
                componentStarts = layout.bGroupStarts,
                groupAuxiliaryBytes = layout.aGroupRecords,
                consumedBytes = 0
            )

        private const val DF03_MAGIC_0 = 0xdf
        private const val DF03_MAGIC_1 = 0x03
        private const val DF03_VERSION_0 = 0x01
        private const val DF03_VERSION_1 = 0x01

        @Deprecated("Build 206 real-resource table alignment is under re-audit after Build 209.")
        fun parse(payload: ByteArray): LegacySpriteCompositeSection {
            require(payload.size >= 8) { "Truncated DF03 payload header" }
            require((payload[0].toInt() and 0xff) == DF03_MAGIC_0 &&
                (payload[1].toInt() and 0xff) == DF03_MAGIC_1 &&
                (payload[2].toInt() and 0xff) == DF03_VERSION_0 &&
                (payload[3].toInt() and 0xff) == DF03_VERSION_1) {
                "Unsupported sprite payload signature/version"
            }

            var p = 6
            fun readSignedCount(label: String): Int {
                require(p >= 0 && p <= payload.size - 2) { "Truncated $label count at $p" }
                val raw = (payload[p].toInt() and 0xff) or
                    ((payload[p + 1].toInt() and 0xff) shl 8)
                p += 2
                return raw.toShort().toInt().coerceAtLeast(0)
            }
            fun take(length: Int, label: String): ByteArray {
                require(length >= 0 && p.toLong() + length.toLong() <= payload.size.toLong()) {
                    "Truncated $label at $p (length=$length)"
                }
                return payload.copyOfRange(p, p + length).also { p += length }
            }

            val dimensionCount = readSignedCount("sprite dimension")
            val dimensions = take(Math.multiplyExact(dimensionCount, 2), "sprite dimensions")

            val componentCount = readSignedCount("component record")
            val records = take(Math.multiplyExact(componentCount, CompositeSpriteRecord.RECORD_SIZE),
                "component records")

            val groupCount = readSignedCount("composite group")
            val counts = ByteArray(groupCount)
            val starts = ShortArray(groupCount)
            repeat(groupCount) { index ->
                require(p <= payload.size - 4) { "Truncated composite group entry $index at $p" }
                counts[index] = payload[p]
                // Byte p+1 is skipped by the original parser; retain no guessed meaning.
                val rawStart = (payload[p + 2].toInt() and 0xff) or
                    ((payload[p + 3].toInt() and 0xff) shl 8)
                starts[index] = rawStart.toShort()
                p += 4
            }
            val groupDimensions = take(Math.multiplyExact(groupCount, 2), "group dimension table")

            return LegacySpriteCompositeSection(
                dimensions, records, counts, starts, groupDimensions, p
            )
        }
    }
}
