package com.diamondrush.legacy

object Build231WorldRoomArchiveChecks {
    private fun u16(value: Int) = byteArrayOf(value.toByte(), (value ushr 8).toByte())

    fun verifyArchivePrefixAndMultiRoomIndex() {
        val bytes = byteArrayOf(1, 2) + u16(2) + u16(3) + ByteArray(18) { it.toByte() } +
            u16(1) + u16(2) + ByteArray(6) { (20 + it).toByte() }
        val index = LegacyWorldRoomArchiveDecoder.index(bytes)
        check(index.opaquePrefixByte == 1)
        check(index.declaredRoomCount == 2)
        check(index.records.map { it.firstDimension to it.secondDimension } == listOf(2 to 3, 1 to 2))
        check(index.consumedBytes == bytes.size)
        check(index.trailingBytes == 0)
    }

    fun verifySelectedRoomUsesExistingPlaneDecoder() {
        val firstPayload = ByteArray(6) { 7 }
        val secondPayload = byteArrayOf(1, 2, 3, 4) +
            byteArrayOf((-1).toByte(), 2, 3, 4) +
            byteArrayOf(9, 8, 7, 6)
        val bytes = byteArrayOf(1, 2) + u16(2) + u16(1) + firstPayload +
            u16(2) + u16(2) + secondPayload
        val decoded = LegacyWorldRoomArchiveDecoder.decode(bytes, "w0.bin", 1)
        check(decoded.room.roomIndex == 1)
        check(decoded.room.planes.firstDimension == 2)
        check(decoded.room.planes.secondDimension == 2)
        check(decoded.room.planes.primaryByteAt(0, 0).toInt() == 1)
        check(decoded.room.planes.serializedIntAt(0, 0) == -1)
        check(decoded.room.planes.secondaryIntAt(1, 1) == 6)
        check(decoded.room.skippedRecords.single().roomIndex == 0)
    }

    fun verifyMalformedArchiveRejected() {
        check(runCatching { LegacyWorldRoomArchiveDecoder.index(byteArrayOf(1)) }.isFailure)
        check(runCatching { LegacyWorldRoomArchiveDecoder.index(byteArrayOf(1, 1, 2, 0, 2, 0)) }.isFailure)
    }

    fun runAll() {
        verifyArchivePrefixAndMultiRoomIndex()
        verifySelectedRoomUsesExistingPlaneDecoder()
        verifyMalformedArchiveRejected()
    }
}
