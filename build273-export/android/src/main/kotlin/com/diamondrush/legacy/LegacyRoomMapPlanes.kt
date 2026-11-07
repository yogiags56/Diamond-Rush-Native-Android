package com.diamondrush.legacy

/**
 * Faithful storage model for the five room map planes established by the
 * original room-loader bytecode. The source dimensions are preserved in order:
 * firstDimension is the outer JVM array dimension; secondDimension is each row.
 *
 * Integer planes intentionally retain sign-extended source-byte values.
 * No tile/object semantics are assigned here.
 */
class LegacyRoomMapPlanes(
    val firstDimension: Int,
    val secondDimension: Int,
    primaryByte: ByteArray,
    serializedIntPlane: IntArray,
    secondaryIntPlane: IntArray,
    runtimeByteOverlayB: ByteArray = ByteArray(primaryByte.size),
    runtimeByteOverlayC: ByteArray = ByteArray(primaryByte.size)
) {
    val cellCount: Int = checkedCellCount(firstDimension, secondDimension)

    private val primary = primaryByte.copyOf()
    private val serializedInt = serializedIntPlane.copyOf()
    private val secondaryInt = secondaryIntPlane.copyOf()
    private val overlayB = runtimeByteOverlayB.copyOf()
    private val overlayC = runtimeByteOverlayC.copyOf()

    init {
        require(primary.size == cellCount) { "primary byte plane length mismatch" }
        require(serializedInt.size == cellCount) { "serialized integer plane length mismatch" }
        require(secondaryInt.size == cellCount) { "secondary integer plane length mismatch" }
        require(overlayB.size == cellCount) { "runtime overlay B length mismatch" }
        require(overlayC.size == cellCount) { "runtime overlay C length mismatch" }
    }

    fun primaryByteAt(first: Int, second: Int): Byte = primary[index(first, second)]
    fun serializedIntAt(first: Int, second: Int): Int = serializedInt[index(first, second)]
    fun secondaryIntAt(first: Int, second: Int): Int = secondaryInt[index(first, second)]
    fun runtimeOverlayBAt(first: Int, second: Int): Byte = overlayB[index(first, second)]
    fun runtimeOverlayCAt(first: Int, second: Int): Byte = overlayC[index(first, second)]

    /**
     * Mirrors the proven setter contract: a:[[B and b:[[I are updated together.
     * Other planes are deliberately untouched.
     */
    fun setPrimaryAndSerializedInt(first: Int, second: Int, byteValue: Byte, intValue: Int) {
        val i = index(first, second)
        primary[i] = byteValue
        serializedInt[i] = intValue
    }

    fun copyPrimaryBytePlane(): ByteArray = primary.copyOf()
    fun copySerializedIntPlane(): IntArray = serializedInt.copyOf()
    fun copySecondaryIntPlane(): IntArray = secondaryInt.copyOf()
    fun copyRuntimeOverlayB(): ByteArray = overlayB.copyOf()
    fun copyRuntimeOverlayC(): ByteArray = overlayC.copyOf()

    private fun index(first: Int, second: Int): Int {
        require(first in 0 until firstDimension) { "first coordinate out of bounds: $first" }
        require(second in 0 until secondDimension) { "second coordinate out of bounds: $second" }
        return first * secondDimension + second
    }

    companion object {
        internal fun checkedCellCount(first: Int, second: Int): Int {
            require(first > 0) { "first dimension must be positive" }
            require(second > 0) { "second dimension must be positive" }
            val product = first.toLong() * second.toLong()
            require(product <= Int.MAX_VALUE) { "room dimensions overflow addressable array size" }
            return product.toInt()
        }
    }
}

/** A decoded selected room plus its original record index and skipped-record audit. */
data class LegacyDecodedRoom(
    val roomIndex: Int,
    val planes: LegacyRoomMapPlanes,
    val skippedRecords: List<LegacySkippedRoomRecord>
)

data class LegacySkippedRoomRecord(
    val roomIndex: Int,
    val firstDimension: Int,
    val secondDimension: Int,
    val payloadByteCount: Int
)
