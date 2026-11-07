package com.diamondrush.legacy

object Build234SpriteResourceParserChecks {
    private fun s16(value: Int): ByteArray =
        byteArrayOf(value.toByte(), (value ushr 8).toByte())

    private fun minimalPayload(paletteFormat: Int = 21781): ByteArray =
        byteArrayOf(0xDF.toByte(), 0x03, 0x01, 0x01, 0x01, 0x01) +
            s16(1) + byteArrayOf(2, 1) +
            s16(0) + // four-byte table
            s16(0) + // metadata rows
            s16(0) + // five-byte table
            s16(0) + // byte/short rows
            s16(paletteFormat) + byteArrayOf(1, 2) +
            s16(0x8000) + s16(0x7C00) +
            s16(5632) + s16(1) + byteArrayOf(0x10)

    fun verifyMinimalDf03Payload() {
        val parsed = LegacySpriteResourceBundleParser.parse(minimalPayload())
        check(parsed.paletteFormat == 21781)
        check(parsed.pixelFormat == 5632)
        check(parsed.paletteCount == 1)
        check(parsed.colorsPerPalette == 2)
        check(parsed.palettes.single().contentEquals(intArrayOf(0x8000, 0x7C00)))
        check(parsed.sprites.single().width == 2)
        check(parsed.sprites.single().height == 1)
        check(parsed.sprites.single().encodedPixels.contentEquals(byteArrayOf(0x10)))
        check(parsed.trailingBytes.isEmpty())
    }

    fun verifyFourByteTableLengthsUseShiftByTwo() {
        val payload = byteArrayOf(0xDF.toByte(), 3, 1, 1, 1, 1) +
            s16(1) + byteArrayOf(1, 1) +
            s16(1) + byteArrayOf(1, 2, 3, 4) +
            s16(1) + byteArrayOf(5, 6, 7, 8) + byteArrayOf(9, 10, 11, 12) +
            s16(0) + s16(0) + s16(0x1234) + byteArrayOf(1, 1) +
            s16(5632) + s16(1) + byteArrayOf(0x10)
        val parsed = LegacySpriteResourceBundleParser.parse(payload)
        check(parsed.fourByteTable.size == 4)
        check(parsed.metadataRows.size == 1)
        check(parsed.pairedFourByteTable.size == 4)
        check(parsed.paletteFormat == 0x1234)
        check(parsed.palettes.isEmpty())
        check(parsed.sprites.size == 1)
    }

    fun verifyBundleDirectoryLittleEndian32BitRecords() {
        val payload = minimalPayload()
        val directory = byteArrayOf(1) +
            byteArrayOf(0, 0, 0, 0) +
            byteArrayOf(payload.size.toByte(), (payload.size ushr 8).toByte(),
                (payload.size ushr 16).toByte(), (payload.size ushr 24).toByte())
        val entries = LegacySpriteResourceBundleParser.readBundleEntries(directory + payload)
        check(entries.size == 1)
        check(entries.single().index == 0)
        check(entries.single().offset == 0L)
        check(entries.single().length == payload.size.toLong())
        check(entries.single().payload.contentEquals(payload))
    }


    fun verifySpriteLengthAndPayloadRecordsAreInterleaved() {
        val payload = byteArrayOf(0xDF.toByte(), 3, 1, 1, 1, 1) +
            s16(2) + byteArrayOf(1, 1, 2, 1) +
            s16(0) + s16(0) + s16(0) + s16(0) +
            s16(21781) + byteArrayOf(1, 2) +
            s16(0x8000) + s16(0x7C00) +
            s16(5632) +
            s16(1) + byteArrayOf(0x10) +
            s16(2) + byteArrayOf(0x01, 0x23)
        val parsed = LegacySpriteResourceBundleParser.parse(payload)
        check(parsed.sprites.size == 2)
        check(parsed.sprites[0].encodedPixels.contentEquals(byteArrayOf(0x10)))
        check(parsed.sprites[1].encodedPixels.contentEquals(byteArrayOf(0x01, 0x23)))
        check(parsed.trailingBytes.isEmpty())
    }

    fun runAll() {
        verifyMinimalDf03Payload()
        verifyFourByteTableLengthsUseShiftByTwo()
        verifyBundleDirectoryLittleEndian32BitRecords()
        verifySpriteLengthAndPayloadRecordsAreInterleaved()
    }
}
