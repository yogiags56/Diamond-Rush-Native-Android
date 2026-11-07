package com.diamondrush.legacy

/**
 * Four-byte component record read from f.h in the original composite-sprite path.
 * Names describe observed operations, not assumed game semantics.
 */
data class CompositeSpriteRecord(
    val spriteIndex: Int,
    val offsetX: Int,
    val offsetY: Int,
    val controlByte: Int
) {
    /** Original code tests bit 0x10 to choose nested-composite vs leaf-sprite drawing. */
    val isNestedComposite: Boolean get() = (controlByte and 0x10) != 0

    /** Original code XORs only the low nibble into the incoming draw flags. */
    val transformXor: Int get() = controlByte and 0x0f

    companion object {
        const val RECORD_SIZE = 4

        fun parse(data: ByteArray, base: Int): CompositeSpriteRecord {
            require(base >= 0) { "negative component record offset" }
            require(base <= data.size - RECORD_SIZE) { "truncated four-byte component record" }
            return CompositeSpriteRecord(
                spriteIndex = data[base].toInt() and 0xff,
                offsetX = data[base + 1].toInt(), // JVM byte sign extension matches baload
                offsetY = data[base + 2].toInt(),
                controlByte = data[base + 3].toInt() and 0xff
            )
        }

        /** Original table lookup: (shortTable[group] + componentIndex) * 4. */
        fun recordBase(shortTable: ShortArray, group: Int, componentIndex: Int): Int {
            require(group in shortTable.indices) { "composite group out of range" }
            require(componentIndex >= 0) { "negative component index" }
            val slot = shortTable[group].toInt() + componentIndex
            require(slot >= 0) { "negative component slot" }
            return Math.multiplyExact(slot, RECORD_SIZE)
        }
    }
}

/** Pure helpers for reproducing the branch decisions of the original composite draw loop. */
object CompositeSpriteRules {
    fun adjustedFlags(incomingFlags: Int, record: CompositeSpriteRecord): Int =
        incomingFlags xor record.transformXor

    /**
     * Component-local placement is signed and conditional on incoming flag bits.
     * The original code uses subtraction when the corresponding bit is set.
     */
    fun componentPosition(
        x: Int,
        y: Int,
        incomingFlags: Int,
        record: CompositeSpriteRecord
    ): Pair<Int, Int> {
        val outX = if ((incomingFlags and 0x01) != 0) x - record.offsetX
                   else x + record.offsetX
        val outY = if ((incomingFlags and 0x02) != 0) y - record.offsetY
                   else y + record.offsetY
        return outX to outY
    }
}
