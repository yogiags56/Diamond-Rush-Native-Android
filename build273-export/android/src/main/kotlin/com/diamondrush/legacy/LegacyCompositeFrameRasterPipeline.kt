package com.diamondrush.legacy

/**
 * Build 239: end-to-end bridge from an already-resolved animation frame and
 * composite graph to the deterministic logical-canvas rasterizer.
 *
 * This class deliberately does not choose a palette, infer a resource slot,
 * calculate animation time, or interpret direct-draw arguments. Those decisions
 * must be supplied by the bytecode-backed upstream stages.
 */
data class LegacyCompositeFrameRasterResult(
    val selection: LegacyOverlayFrameSelection,
    val placement: LegacySpriteAnimationFramePlacement,
    val operations: List<LegacyConcreteSpriteDrawOperation>,
    val boundDraws: List<LegacyPaletteBoundSpriteDraw>,
    val surface: LegacyRasterizedSurface
)

object LegacyCompositeFrameRasterPipeline {
    @JvmStatic
    fun rasterize(
        resource: LegacyBoundSpriteResource,
        resolved: LegacyResolvedCompositeOverlay,
        decodedSprites: List<LegacyDecodedSpriteRecord>,
        paletteIndex: Int,
        width: Int = 320,
        height: Int = 240,
        clip: LegacyRasterClip = LegacyRasterClip(0, 0, width, height)
    ): LegacyCompositeFrameRasterResult {
        require(resolved.selection.kind == LegacyOverlaySelectionKind.ANIMATION_SEQUENCE_FRAME) {
            "Direct-draw argument path cannot enter composite-frame raster pipeline"
        }
        require(resolved.selection.resourceIndex == resource.globalArraySlot) {
            "Selection f[${resolved.selection.resourceIndex}] does not match bound f[${resource.globalArraySlot}]"
        }
        require(decodedSprites.all { it.globalArraySlot == resource.globalArraySlot }) {
            "Decoded sprite list contains pixels from another global resource slot"
        }
        val operations = if (resolved.placement.frame.compositeGroupIndex == null) {
            require(resolved.leafCommands.isEmpty()) {
                "No-group animation frame unexpectedly contains composite leaves"
            }
            emptyList()
        } else {
            LegacyConcreteSpriteDrawOperationResolver.expand(resource, resolved)
        }
        val boundDraws = LegacyPaletteAwareSpriteDecoder.bindOperations(
            operations, decodedSprites, paletteIndex
        )
        val surface = LegacySpriteRasterExecution.rasterize(
            boundDraws, width, height, clip
        )
        return LegacyCompositeFrameRasterResult(
            resolved.selection, resolved.placement, operations, boundDraws, surface
        )
    }
}
