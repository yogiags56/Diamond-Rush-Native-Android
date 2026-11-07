package com.diamondrush.legacy

/**
 * Build 236: a resource-bound, concrete leaf-sprite draw operation.
 *
 * This is still a renderer-neutral command, not a pixel blit. It preserves the
 * original local sprite index, global f[] slot, frame/group provenance, signed
 * coordinates, and both flag channels. Palette selection and raster execution
 * remain responsibilities of later pipeline stages.
 */
data class LegacyConcreteSpriteDrawOperation(
    val ordinal: Int,
    val globalArraySlot: Int,
    val sequenceIndex: Int,
    val frameIndex: Int,
    val compositeGroupIndex: Int,
    val spriteIndex: Int,
    val spriteWidth: Int,
    val spriteHeight: Int,
    val x: Int,
    val y: Int,
    val incomingFlags: Int,
    val drawFlags: Int,
    val opaqueArgumentA: Int,
    val opaqueArgumentB: Int,
    val sourceGroupPath: List<Int>,
    val sourceComponentPath: List<Int>
) {
    fun canonicalLine(): String = listOf(
        ordinal, globalArraySlot, sequenceIndex, frameIndex, compositeGroupIndex,
        spriteIndex, spriteWidth, spriteHeight, x, y, incomingFlags, drawFlags,
        opaqueArgumentA, opaqueArgumentB,
        sourceGroupPath.joinToString("/"), sourceComponentPath.joinToString("/")
    ).joinToString(",")
}

object LegacyConcreteSpriteDrawOperationResolver {
    const val CSV_HEADER = "ordinal,globalSlot,sequence,frame,rootGroup,sprite,width,height,x,y,incomingFlags,drawFlags,opaqueA,opaqueB,groupPath,componentPath"

    /**
     * Bind already-expanded composite leaves to the exact global resource slot.
     * No sprite is inferred from a sequence number: the leaf's local sprite index
     * must exist in the supplied Build235 resource binding.
     */
    @JvmStatic
    fun expand(
        resource: LegacyBoundSpriteResource,
        resolved: LegacyResolvedCompositeOverlay
    ): List<LegacyConcreteSpriteDrawOperation> {
        require(resolved.selection.resourceIndex == resource.globalArraySlot) {
            "Resolved resource f[${resolved.selection.resourceIndex}] does not match bound f[${resource.globalArraySlot}]"
        }
        require(resolved.selection.kind == LegacyOverlaySelectionKind.ANIMATION_SEQUENCE_FRAME) {
            "Direct-draw requests do not expand through composite groups"
        }
        val sequence = requireNotNull(resolved.selection.sequenceIndex)
        val frame = requireNotNull(resolved.selection.frameIndex)
        val rootGroup = requireNotNull(resolved.placement.frame.compositeGroupIndex) {
            "No-group animation frame has no concrete composite leaves"
        }
        val spritesByIndex = resource.sprites.associateBy { it.spriteIndex }
        return resolved.leafCommands.mapIndexed { ordinal, leaf ->
            val sprite = spritesByIndex[leaf.spriteIndex]
                ?: throw IllegalArgumentException(
                    "Leaf sprite ${leaf.spriteIndex} is absent from bound f[${resource.globalArraySlot}]"
                )
            require(sprite.width > 0 && sprite.height > 0) {
                "Sprite ${leaf.spriteIndex} has invalid dimensions ${sprite.width}x${sprite.height}"
            }
            LegacyConcreteSpriteDrawOperation(
                ordinal = ordinal,
                globalArraySlot = resource.globalArraySlot,
                sequenceIndex = sequence,
                frameIndex = frame,
                compositeGroupIndex = rootGroup,
                spriteIndex = leaf.spriteIndex,
                spriteWidth = sprite.width,
                spriteHeight = sprite.height,
                x = leaf.x,
                y = leaf.y,
                incomingFlags = leaf.incomingFlags,
                drawFlags = leaf.drawFlags,
                opaqueArgumentA = leaf.opaqueArgumentA,
                opaqueArgumentB = leaf.opaqueArgumentB,
                sourceGroupPath = leaf.sourceGroupPath.toList(),
                sourceComponentPath = leaf.sourceComponentPath.toList()
            )
        }
    }

    @JvmStatic
    fun canonicalCsv(operations: List<LegacyConcreteSpriteDrawOperation>): String =
        (listOf(CSV_HEADER) + operations.map { it.canonicalLine() })
            .joinToString("\n", postfix = "\n")
}
