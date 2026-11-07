package com.diamondrush.legacy

/**
 * Build 214 model for the original f-class five-byte animation-frame table.
 *
 * Evidence from f.class:
 * - b:[B stores the unsigned frame count for each animation sequence.
 * - a:[S stores the first five-byte record index for each sequence.
 * - c:[B stores five bytes per animation frame.
 * - a(int) returns b[sequence] unsigned.
 * - a(int,int) returns c[(a[sequence] + frame) * 5 + 1] unsigned;
 *   the game subtracts this value from an elapsed counter when selecting a frame.
 * - a(Graphics, seven ints) reads the frame's composite group, X/Y offsets,
 *   and low-nibble control flags. Incoming flag 0x20 enables the stored offsets.
 */
data class LegacySpriteAnimationFrame(
    val rawCompositeGroupIndex: Int,
    val durationUnits: Int,
    val offsetX: Int,
    val offsetY: Int,
    val controlFlags: Int
) {
    /** 0xFF is retained as an explicit no-group sentinel seen in mmv.f. */
    val compositeGroupIndex: Int?
        get() = rawCompositeGroupIndex.takeUnless { it == NO_GROUP }

    companion object {
        const val RECORD_SIZE = 5
        const val NO_GROUP = 0xFF
    }
}

data class LegacySpriteAnimationSequence(
    val sequenceIndex: Int,
    val frameCount: Int,
    val firstRecordIndex: Int
)

data class LegacySpriteAnimationFramePlacement(
    val sequenceIndex: Int,
    val frameIndex: Int,
    val frame: LegacySpriteAnimationFrame,
    val drawX: Int,
    val drawY: Int,
    val effectiveOffsetX: Int,
    val effectiveOffsetY: Int,
    val drawFlags: Int
)

class LegacySpriteAnimationTable private constructor(
    private val records: ByteArray,
    private val frameCounts: ByteArray,
    private val firstRecordIndices: ShortArray,
    val compositeGroupCount: Int
) {
    val sequenceCount: Int get() = frameCounts.size
    val recordCount: Int get() = records.size / LegacySpriteAnimationFrame.RECORD_SIZE

    fun sequence(sequenceIndex: Int): LegacySpriteAnimationSequence {
        require(sequenceIndex in 0 until sequenceCount) {
            "Animation sequence $sequenceIndex out of range"
        }
        return LegacySpriteAnimationSequence(
            sequenceIndex = sequenceIndex,
            frameCount = frameCounts[sequenceIndex].toInt() and 0xff,
            firstRecordIndex = firstRecordIndices[sequenceIndex].toInt()
        )
    }

    fun frame(sequenceIndex: Int, frameIndex: Int): LegacySpriteAnimationFrame {
        val sequence = sequence(sequenceIndex)
        require(frameIndex in 0 until sequence.frameCount) {
            "Frame $frameIndex out of range for sequence $sequenceIndex"
        }
        val recordIndex = Math.addExact(sequence.firstRecordIndex, frameIndex)
        val p = Math.multiplyExact(recordIndex, LegacySpriteAnimationFrame.RECORD_SIZE)
        return LegacySpriteAnimationFrame(
            rawCompositeGroupIndex = records[p].toInt() and 0xff,
            durationUnits = records[p + 1].toInt() and 0xff,
            offsetX = records[p + 2].toInt(),
            offsetY = records[p + 3].toInt(),
            controlFlags = records[p + 4].toInt() and 0xff
        )
    }

    /**
     * Mirrors the original seven-int frame draw wrapper.
     *
     * The final two arguments are inherited offsets. When incomingFlags contains
     * 0x20, the frame's signed offsets replace them. Bits 0 and 1 choose the sign:
     * set => stored offset; clear => negated stored offset. The original renderer
     * then subtracts the effective offsets from the supplied X/Y coordinates.
     */
    fun placement(
        sequenceIndex: Int,
        frameIndex: Int,
        baseX: Int,
        baseY: Int,
        incomingFlags: Int,
        inheritedOffsetX: Int = 0,
        inheritedOffsetY: Int = 0
    ): LegacySpriteAnimationFramePlacement {
        val frame = frame(sequenceIndex, frameIndex)
        val useRecordOffsets = (incomingFlags and 0x20) != 0
        val effectiveX = if (!useRecordOffsets) inheritedOffsetX
            else if ((incomingFlags and 0x01) != 0) frame.offsetX else -frame.offsetX
        val effectiveY = if (!useRecordOffsets) inheritedOffsetY
            else if ((incomingFlags and 0x02) != 0) frame.offsetY else -frame.offsetY
        return LegacySpriteAnimationFramePlacement(
            sequenceIndex = sequenceIndex,
            frameIndex = frameIndex,
            frame = frame,
            drawX = baseX - effectiveX,
            drawY = baseY - effectiveY,
            effectiveOffsetX = effectiveX,
            effectiveOffsetY = effectiveY,
            drawFlags = incomingFlags xor (frame.controlFlags and 0x0f)
        )
    }

    fun validateGroupReferences(): List<Pair<Int, Int>> {
        val invalid = ArrayList<Pair<Int, Int>>()
        for (sequenceIndex in 0 until sequenceCount) {
            val sequence = sequence(sequenceIndex)
            for (frameIndex in 0 until sequence.frameCount) {
                val group = frame(sequenceIndex, frameIndex).compositeGroupIndex ?: continue
                if (group !in 0 until compositeGroupCount) {
                    invalid += sequenceIndex to frameIndex
                }
            }
        }
        return invalid
    }

    companion object {
        fun fromFieldLayout(layout: LegacySpriteFieldLayout): LegacySpriteAnimationTable {
            require(layout.cFiveByteRecords.size % LegacySpriteAnimationFrame.RECORD_SIZE == 0) {
                "Five-byte animation record table has a partial record"
            }
            require(layout.bByteTable.size == layout.aShortTable.size) {
                "Animation frame-count and start-index tables differ in length"
            }
            val table = LegacySpriteAnimationTable(
                records = layout.cFiveByteRecords,
                frameCounts = layout.bByteTable,
                firstRecordIndices = layout.aShortTable,
                compositeGroupCount = layout.groupCount
            )
            for (index in 0 until table.sequenceCount) {
                val sequence = table.sequence(index)
                require(sequence.firstRecordIndex >= 0 &&
                    sequence.firstRecordIndex.toLong() + sequence.frameCount <= table.recordCount.toLong()) {
                    "Animation sequence $index exceeds five-byte record table"
                }
            }
            return table
        }
    }
}
