package com.diamondrush.legacy

object Build223RoomDecoderChecks {
    @JvmStatic
    fun main(args: Array<String>) {
        selectedRecordDecodesUnsignedLittleEndianDimensionsAndSignedPlanes()
        skipsEarlierRoomByThreePlanePayloadSize()
        overlaysAreIndependentAndZeroInitialized()
        setterUpdatesOnlyProvenPlanePair()
        rejectsTruncatedHeaderAndPayload()
        rejectsMissingRoomAndOutOfBoundsAccess()
        println("BUILD223_KOTLIN_CHECKS: 6 passed")
    }

    private fun selectedRecordDecodesUnsignedLittleEndianDimensionsAndSignedPlanes() {
        val record = roomRecord(2, 2, byteArrayOf(1, 2, 3, 4),
            byteArrayOf(0xFF.toByte(), 0x80.toByte(), 0x7F, 0),
            byteArrayOf(0xFE.toByte(), 0x81.toByte(), 5, 6))
        val decoded = LegacyRoomPayloadDecoder.decodeSelectedRecord(record, 0)
        check(decoded.planes.firstDimension == 2 && decoded.planes.secondDimension == 2)
        check(decoded.planes.primaryByteAt(0, 1) == 2.toByte())
        check(decoded.planes.serializedIntAt(0, 0) == -1)
        check(decoded.planes.serializedIntAt(0, 1) == -128)
        check(decoded.planes.secondaryIntAt(0, 0) == -2)
    }

    private fun skipsEarlierRoomByThreePlanePayloadSize() {
        val first = roomRecord(1, 2, byteArrayOf(1, 2), byteArrayOf(3, 4), byteArrayOf(5, 6))
        val second = roomRecord(2, 1, byteArrayOf(7, 8), byteArrayOf(9, 10), byteArrayOf(11, 12))
        val decoded = LegacyRoomPayloadDecoder.decodeSelectedRecord(first + second, 1)
        check(decoded.roomIndex == 1)
        check(decoded.skippedRecords.size == 1)
        check(decoded.skippedRecords[0].payloadByteCount == 6)
        check(decoded.planes.primaryByteAt(1, 0) == 8.toByte())
    }

    private fun overlaysAreIndependentAndZeroInitialized() {
        val decoded = LegacyRoomPayloadDecoder.decodeSelectedRecord(
            roomRecord(1, 2, byteArrayOf(1, 2), byteArrayOf(3, 4), byteArrayOf(5, 6)), 0)
        val p = decoded.planes
        check(p.runtimeOverlayBAt(0, 0) == 0.toByte())
        check(p.runtimeOverlayCAt(0, 0) == 0.toByte())
        check(p.copyRuntimeOverlayB().contentEquals(p.copyRuntimeOverlayC()))
    }

    private fun setterUpdatesOnlyProvenPlanePair() {
        val p = LegacyRoomPayloadDecoder.decodeSelectedRecord(
            roomRecord(1, 1, byteArrayOf(1), byteArrayOf(2), byteArrayOf(3)), 0).planes
        p.setPrimaryAndSerializedInt(0, 0, 0xFE.toByte(), -1234)
        check(p.primaryByteAt(0, 0) == 0xFE.toByte())
        check(p.serializedIntAt(0, 0) == -1234)
        check(p.secondaryIntAt(0, 0) == 3)
        check(p.runtimeOverlayBAt(0, 0) == 0.toByte())
        check(p.runtimeOverlayCAt(0, 0) == 0.toByte())
    }

    private fun rejectsTruncatedHeaderAndPayload() {
        check(runCatching { LegacyRoomPayloadDecoder.decodeSelectedRecord(byteArrayOf(1, 2, 3), 0) }.isFailure)
        check(runCatching { LegacyRoomPayloadDecoder.decodeSelectedRecord(
            byteArrayOf(1, 0, 1, 0, 1, 2), 0) }.isFailure)
    }

    private fun rejectsMissingRoomAndOutOfBoundsAccess() {
        val p = LegacyRoomPayloadDecoder.decodeSelectedRecord(
            roomRecord(1, 1, byteArrayOf(1), byteArrayOf(2), byteArrayOf(3)), 0).planes
        check(runCatching { LegacyRoomPayloadDecoder.decodeSelectedRecord(
            roomRecord(1, 1, byteArrayOf(1), byteArrayOf(2), byteArrayOf(3)), 1) }.isFailure)
        check(runCatching { p.primaryByteAt(1, 0) }.isFailure)
    }

    private fun roomRecord(w: Int, h: Int, a: ByteArray, b: ByteArray, c: ByteArray): ByteArray {
        require(a.size == w*h && b.size == w*h && c.size == w*h)
        return byteArrayOf(w.toByte(), (w ushr 8).toByte(), h.toByte(), (h ushr 8).toByte()) + a + b + c
    }
}
