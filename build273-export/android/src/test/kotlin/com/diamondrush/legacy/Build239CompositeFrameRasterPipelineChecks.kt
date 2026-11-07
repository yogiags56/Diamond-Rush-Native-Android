package com.diamondrush.legacy

object Build239CompositeFrameRasterPipelineChecks {
    private fun resource(): LegacyBoundSpriteResource = LegacyBoundSpriteResource(
        globalArraySlot = 10,
        bundlePath = "mmv.f",
        bundleEntryIndex = 0,
        renderConsumer = null,
        sprites = listOf(LegacyBoundSpriteRecord(10, "mmv.f", 0, 0, 2, 2, 4, 0)),
        components = emptyList(),
        animationFrames = emptyList()
    )

    private fun resolved(): LegacyResolvedCompositeOverlay {
        val frame = LegacySpriteAnimationFrame(0, 1, 0, 0, 0)
        val placement = LegacySpriteAnimationFramePlacement(0, 0, frame, 1, 1, 0, 0, 0)
        val selection = LegacyOverlayFrameSelection(
            10, LegacyOverlaySelectionKind.ANIMATION_SEQUENCE_FRAME,
            0, 0, null, 20, 0
        )
        val leaf = CompositeSpriteObjectResolver.LeafDrawCommand(
            0, 1, 1, 0, 0, 0, 0, listOf(0), listOf(0)
        )
        return LegacyResolvedCompositeOverlay(selection, placement, listOf(leaf))
    }

    fun verifyResolvedFrameRunsThroughBindingAndRasterizer() {
        val colors = intArrayOf(
            0xffff0000.toInt(), 0xff00ff00.toInt(),
            0xff0000ff.toInt(), 0xffffffff.toInt()
        )
        val decoded = listOf(LegacyDecodedSpriteRecord(10, 0, 2, 2, 0, 0, 0, colors, false))
        val result = LegacyCompositeFrameRasterPipeline.rasterize(
            resource(), resolved(), decoded, paletteIndex = 0, width = 4, height = 4
        )
        check(result.operations.size == 1)
        check(result.boundDraws.size == 1)
        check(result.surface.executedOperations == 1)
        check(result.surface.argb[1 * 4 + 1] == colors[0])
        check(result.surface.argb[1 * 4 + 2] == colors[1])
        check(result.surface.argb[2 * 4 + 1] == colors[2])
        check(result.surface.argb[2 * 4 + 2] == colors[3])
    }

    fun verifyEmptyNoGroupFrameProducesBlankSurface() {
        val base = resolved()
        val noGroup = base.copy(
            placement = base.placement.copy(
                frame = base.placement.frame.copy(rawCompositeGroupIndex = 0xff)
            ),
            leafCommands = emptyList()
        )
        val result = LegacyCompositeFrameRasterPipeline.rasterize(
            resource(), noGroup, emptyList(), paletteIndex = 0, width = 3, height = 2
        )
        check(result.operations.isEmpty())
        check(result.surface.executedOperations == 0)
        check(result.surface.argb.all { it == 0 })
    }

    fun verifyResourceMismatchAndDirectDrawAreRejected() {
        val wrongResource = resource().copy(globalArraySlot = 9)
        val decoded = listOf(LegacyDecodedSpriteRecord(10, 0, 2, 2, 0, 0, 0, IntArray(4), false))
        check(runCatching {
            LegacyCompositeFrameRasterPipeline.rasterize(wrongResource, resolved(), decoded, 0)
        }.isFailure)
        val direct = resolved().copy(selection = resolved().selection.copy(
            kind = LegacyOverlaySelectionKind.DIRECT_DRAW_ARGUMENT
        ))
        check(runCatching {
            LegacyCompositeFrameRasterPipeline.rasterize(resource(), direct, decoded, 0)
        }.isFailure)
    }

    fun runAll() {
        verifyResolvedFrameRunsThroughBindingAndRasterizer()
        verifyEmptyNoGroupFrameProducesBlankSurface()
        verifyResourceMismatchAndDirectDrawAreRejected()
    }
}
