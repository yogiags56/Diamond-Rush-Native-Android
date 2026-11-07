package com.diamondrush.legacy

object Build236ConcreteSpriteDrawOperationChecks {
    private fun resource(slot: Int = 10) = LegacyBoundSpriteResource(
        globalArraySlot = slot,
        bundlePath = "/mmv.f",
        bundleEntryIndex = 0,
        renderConsumer = null,
        sprites = listOf(
            LegacyBoundSpriteRecord(slot, "/mmv.f", 0, 0, 12, 16, 24, 5632),
            LegacyBoundSpriteRecord(slot, "/mmv.f", 0, 1, 8, 9, 12, 5632)
        ),
        components = emptyList(),
        animationFrames = emptyList()
    )

    private fun resolved(slot: Int = 10) = LegacyResolvedCompositeOverlay(
        selection = LegacyOverlayFrameSelection(
            slot, LegacyOverlaySelectionKind.ANIMATION_SEQUENCE_FRAME,
            3, 1, null, 20, 0
        ),
        placement = LegacySpriteAnimationFramePlacement(
            3, 1, LegacySpriteAnimationFrame(2, 4, -1, 2, 5),
            100, 200, 0, 0, 5
        ),
        leafCommands = listOf(
            CompositeSpriteObjectResolver.LeafDrawCommand(
                0, 97, 203, 5, 5, 11, 12, listOf(2, 4), listOf(0, 3)
            ),
            CompositeSpriteObjectResolver.LeafDrawCommand(
                1, 110, 190, 5, 4, 11, 12, listOf(2, 4), listOf(1, 2)
            )
        )
    )

    fun verifyLeafCommandsBindToSpriteDimensionsAndProvenance() {
        val ops = LegacyConcreteSpriteDrawOperationResolver.expand(resource(), resolved())
        check(ops.size == 2)
        check(ops[0].ordinal == 0 && ops[1].ordinal == 1)
        check(ops[0].globalArraySlot == 10 && ops[0].spriteIndex == 0)
        check(ops[0].spriteWidth == 12 && ops[0].spriteHeight == 16)
        check(ops[0].x == 97 && ops[0].y == 203)
        check(ops[0].incomingFlags == 5 && ops[0].drawFlags == 5)
        check(ops[0].sourceGroupPath == listOf(2, 4))
        check(ops[0].sourceComponentPath == listOf(0, 3))
        check(ops[1].spriteWidth == 8 && ops[1].spriteHeight == 9)
    }

    fun verifyMismatchedGlobalSlotIsRejected() {
        check(runCatching {
            LegacyConcreteSpriteDrawOperationResolver.expand(resource(9), resolved(10))
        }.isFailure)
    }

    fun verifyUnknownLeafSpriteIsRejected() {
        val bad = resolved().copy(
            leafCommands = listOf(resolved().leafCommands.first().copy(spriteIndex = 99))
        )
        check(runCatching {
            LegacyConcreteSpriteDrawOperationResolver.expand(resource(), bad)
        }.isFailure)
    }

    fun verifyCanonicalCsvIsStable() {
        val csv = LegacyConcreteSpriteDrawOperationResolver.canonicalCsv(
            LegacyConcreteSpriteDrawOperationResolver.expand(resource(), resolved())
        )
        check(csv.startsWith(LegacyConcreteSpriteDrawOperationResolver.CSV_HEADER + "\n"))
        check(csv.contains("0,10,3,1,2,0,12,16,97,203,5,5,11,12,2/4,0/3"))
        check(csv.endsWith("\n"))
    }

    fun runAll() {
        verifyLeafCommandsBindToSpriteDimensionsAndProvenance()
        verifyMismatchedGlobalSlotIsRejected()
        verifyUnknownLeafSpriteIsRejected()
        verifyCanonicalCsvIsStable()
    }
}
