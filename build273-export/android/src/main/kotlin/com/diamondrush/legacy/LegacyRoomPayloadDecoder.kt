package com.diamondrush.legacy

/**
 * Decoder for the room-record layout proven by the original i.j() bytecode:
 * 4-byte header (two unsigned little-endian 16-bit dimensions), followed by
 * three width*height byte planes. Records are concatenated without extra tags.
 *
 * The second and third serialized byte planes are sign-extended to Int values,
 * matching JVM baload -> iastore behavior. Two runtime byte overlays are
 * allocated independently and initialized to zero.
 */
object LegacyRoomPayloadDecoder {
    private const val HEADER_BYTES = 4
    private const val SERIALIZED_PLANES = 3

    @JvmStatic
    fun decodeSelectedRecord(streamBytes: ByteArray, selectedRoomIndex: Int): LegacyDecodedRoom {
        require(selectedRoomIndex >= 0) { "selectedRoomIndex must be non-negative" }
        var cursor = 0
        var roomIndex = 0
        val skipped = ArrayList<LegacySkippedRoomRecord>()

        while (cursor < streamBytes.size) {
            require(streamBytes.size - cursor >= HEADER_BYTES) {
                "truncated room header at byte offset $cursor"
            }
            val first = readUnsignedLittleEndian16(streamBytes, cursor)
            val second = readUnsignedLittleEndian16(streamBytes, cursor + 2)
            cursor += HEADER_BYTES
            val cells = LegacyRoomMapPlanes.checkedCellCount(first, second)
            val payloadBytes = cells.toLong() * SERIALIZED_PLANES
            require(payloadBytes <= Int.MAX_VALUE) { "room payload too large" }
            require(payloadBytes <= streamBytes.size.toLong() - cursor) {
                "truncated room payload for record $roomIndex"
            }

            if (roomIndex == selectedRoomIndex) {
                val primary = streamBytes.copyOfRange(cursor, cursor + cells)
                val secondPlaneBytes = streamBytes.copyOfRange(cursor + cells, cursor + cells * 2)
                val thirdPlaneBytes = streamBytes.copyOfRange(cursor + cells * 2, cursor + cells * 3)
                val secondInts = IntArray(cells) { secondPlaneBytes[it].toInt() }
                val thirdInts = IntArray(cells) { thirdPlaneBytes[it].toInt() }
                val planes = LegacyRoomMapPlanes(
                    firstDimension = first,
                    secondDimension = second,
                    primaryByte = primary,
                    serializedIntPlane = secondInts,
                    secondaryIntPlane = thirdInts,
                    runtimeByteOverlayB = ByteArray(cells),
                    runtimeByteOverlayC = ByteArray(cells)
                )
                return LegacyDecodedRoom(roomIndex, planes, skipped.toList())
            }

            skipped += LegacySkippedRoomRecord(roomIndex, first, second, payloadBytes.toInt())
            cursor += payloadBytes.toInt()
            roomIndex++
        }

        throw IllegalArgumentException("selected room index $selectedRoomIndex not found; records read: $roomIndex")
    }

    private fun readUnsignedLittleEndian16(bytes: ByteArray, offset: Int): Int {
        val low = bytes[offset].toInt() and 0xFF
        val high = bytes[offset + 1].toInt() and 0xFF
        return low or (high shl 8)
    }
}
