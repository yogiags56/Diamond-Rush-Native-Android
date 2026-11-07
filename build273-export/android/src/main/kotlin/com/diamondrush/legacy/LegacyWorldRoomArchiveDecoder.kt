package com.diamondrush.legacy

/**
 * Container decoder for the original game's w0.bin / w1.bin / w2.bin room sets.
 * Byte 0 is retained as an opaque marker; byte 1 is the record count. The
 * remaining bytes are concatenated records consumed by LegacyRoomPayloadDecoder.
 */
object LegacyWorldRoomArchiveDecoder {
    data class ArchiveIndex(
        val opaquePrefixByte: Int,
        val declaredRoomCount: Int,
        val records: List<RecordIndex>,
        val consumedBytes: Int,
        val trailingBytes: Int
    )
    data class RecordIndex(
        val roomIndex: Int, val firstDimension: Int, val secondDimension: Int,
        val recordOffset: Int, val payloadOffset: Int, val payloadBytes: Int
    )
    data class DecodedArchiveRoom(
        val archiveName: String, val archiveIndex: ArchiveIndex, val room: LegacyDecodedRoom
    )

    fun index(bytes: ByteArray): ArchiveIndex {
        require(bytes.size >= 2) { "room archive requires two-byte prefix" }
        val count = bytes[1].toInt() and 0xff
        var cursor = 2
        val records = ArrayList<RecordIndex>(count)
        repeat(count) { roomIndex ->
            require(bytes.size - cursor >= 4) { "truncated room header at archive offset $cursor" }
            val first = u16le(bytes, cursor)
            val second = u16le(bytes, cursor + 2)
            val cells = LegacyRoomMapPlanes.checkedCellCount(first, second)
            val payloadLong = cells.toLong() * 3L
            require(payloadLong <= Int.MAX_VALUE) { "room payload too large" }
            val payloadBytes = payloadLong.toInt()
            val payloadOffset = cursor + 4
            require(payloadBytes <= bytes.size - payloadOffset) {
                "truncated payload for room $roomIndex at archive offset $payloadOffset"
            }
            records += RecordIndex(roomIndex, first, second, cursor, payloadOffset, payloadBytes)
            cursor = payloadOffset + payloadBytes
        }
        return ArchiveIndex(bytes[0].toInt() and 0xff, count, records, cursor, bytes.size - cursor)
    }

    fun decode(bytes: ByteArray, archiveName: String, roomIndex: Int): DecodedArchiveRoom {
        require(archiveName in setOf("w0.bin", "w1.bin", "w2.bin")) { "unknown original room archive name" }
        val indexed = index(bytes)
        require(roomIndex in indexed.records.indices) {
            "room index $roomIndex outside declared room count ${indexed.declaredRoomCount}"
        }
        val recordsOnly = bytes.copyOfRange(2, indexed.consumedBytes)
        val decoded = LegacyRoomPayloadDecoder.decodeSelectedRecord(recordsOnly, roomIndex)
        return DecodedArchiveRoom(archiveName, indexed, decoded)
    }

    private fun u16le(bytes: ByteArray, offset: Int): Int =
        (bytes[offset].toInt() and 0xff) or ((bytes[offset + 1].toInt() and 0xff) shl 8)
}
