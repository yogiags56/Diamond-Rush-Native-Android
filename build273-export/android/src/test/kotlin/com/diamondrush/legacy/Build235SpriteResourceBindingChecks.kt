package com.diamondrush.legacy

object Build235SpriteResourceBindingChecks {
    private fun s16(value: Int): ByteArray =
        byteArrayOf(value.toByte(), (value ushr 8).toByte())

    private fun syntheticResource(): ByteArray =
        byteArrayOf(0xDF.toByte(), 3, 1, 1, 1, 1) +
            s16(1) + byteArrayOf(2, 3) + // one 2x3 sprite
            s16(1) + byteArrayOf(0, 0, 0, 0) + // one leaf component record
            s16(1) + byteArrayOf(1, 0) + s16(0) + // one group: count=1, start=0
            byteArrayOf(0, 0, 0, 0) + // opaque four-byte-per-group table
            s16(1) + byteArrayOf(0, 2, 3, 4, 5) + // one animation frame -> group 0
            s16(1) + byteArrayOf(1, 0) + s16(0) + // one sequence -> record 0
            s16(21781) + byteArrayOf(1, 2) + s16(0x8000) + s16(0x7C00) +
            s16(5632) + s16(1) + byteArrayOf(0x10)

    fun verifyStaticSlotBindsSpriteAndCompositeLeaf() {
        val parsed = LegacySpriteResourceBundleParser.parse(syntheticResource())
        val bound = LegacySpriteResourceBindingCatalog.bind(mapOf(10 to parsed)).single()
        check(bound.globalArraySlot == 10)
        check(bound.bundlePath == "/mmv.f")
        check(bound.bundleEntryIndex == 0)
        check(bound.sprites.single().spriteIndex == 0)
        check(bound.sprites.single().width == 2 && bound.sprites.single().height == 3)
        check(bound.components.single().targetIndex == 0)
        check(!bound.components.single().targetIsNestedGroup)
        check(bound.components.single().targetInRange)
        check(bound.renderConsumer?.bytecodeOffsets == listOf(6348, 6357, 6369))
    }

    fun verifyAnimationFrameBindsToCompositeGroup() {
        val parsed = LegacySpriteResourceBundleParser.parse(syntheticResource())
        val bound = LegacySpriteResourceBindingCatalog.bind(mapOf(10 to parsed)).single()
        val frame = bound.animationFrames.single()
        check(frame.sequenceIndex == 0 && frame.frameIndex == 0)
        check(frame.rawGroupIndex == 0 && frame.groupInRange == true)
        check(frame.durationUnits == 2)
        check(frame.offsetX == 3 && frame.offsetY == 4)
        check(frame.controlFlags == 5)
    }

    fun verifyUnknownGlobalSlotIsRejected() {
        val parsed = LegacySpriteResourceBundleParser.parse(syntheticResource())
        val rejected = runCatching { LegacySpriteResourceBindingCatalog.bind(mapOf(999 to parsed)) }
        check(rejected.isFailure)
    }

    fun runAll() {
        verifyStaticSlotBindsSpriteAndCompositeLeaf()
        verifyAnimationFrameBindsToCompositeGroup()
        verifyUnknownGlobalSlotIsRejected()
    }
}
