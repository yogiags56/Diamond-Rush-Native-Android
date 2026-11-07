package com.diamondrush.legacy

/**
 * Build 232: evidence-backed references to the global f[] sprite-resource array
 * observed inside the original i.D() render method.
 *
 * Offsets are original JVM bytecode offsets. This catalog records array-index
 * references, not semantic object names or proof that every reference draws.
 */
data class LegacySpriteResourceConsumerEvidence(
    val resourceArrayIndex: Int,
    val bytecodeOffsets: List<Int>,
    val consumerMethod: String = "i.D()V"
)

object LegacySpriteResourceConsumerCatalog {
    @JvmField
    val renderMethodConsumers: List<LegacySpriteResourceConsumerEvidence> = listOf(
        LegacySpriteResourceConsumerEvidence(0, listOf(3853, 3898)),
        LegacySpriteResourceConsumerEvidence(1, listOf(4442)),
        LegacySpriteResourceConsumerEvidence(2, listOf(6083, 7212)),
        LegacySpriteResourceConsumerEvidence(3, listOf(6636, 6647)),
        LegacySpriteResourceConsumerEvidence(5, listOf(3944)),
        LegacySpriteResourceConsumerEvidence(6, listOf(3994)),
        LegacySpriteResourceConsumerEvidence(7, listOf(6939, 6947, 7643, 7655)),
        LegacySpriteResourceConsumerEvidence(9, listOf(6107, 7236)),
        LegacySpriteResourceConsumerEvidence(10, listOf(6348, 6357, 6369)),
        LegacySpriteResourceConsumerEvidence(11, listOf(4239)),
        LegacySpriteResourceConsumerEvidence(12, listOf(5474, 5497)),
        LegacySpriteResourceConsumerEvidence(13, listOf(6912, 7045)),
        LegacySpriteResourceConsumerEvidence(15, listOf(6279, 6769)),
        LegacySpriteResourceConsumerEvidence(16, listOf(6820)),
        LegacySpriteResourceConsumerEvidence(20, listOf(5417, 6732)),
        LegacySpriteResourceConsumerEvidence(27, listOf(940, 1930, 3636, 3725)),
        LegacySpriteResourceConsumerEvidence(28, listOf(3406)),
        LegacySpriteResourceConsumerEvidence(29, listOf(2894, 3176)),
        LegacySpriteResourceConsumerEvidence(30, listOf(1957)),
        LegacySpriteResourceConsumerEvidence(32, listOf(2747)),
        LegacySpriteResourceConsumerEvidence(38, listOf(2528)),
        LegacySpriteResourceConsumerEvidence(42, listOf(4300, 4347, 6872)),
        LegacySpriteResourceConsumerEvidence(56, listOf(1501)),
    )

    /** Resource indices with specifically attributed secondary-overlay paths. */
    @JvmField
    val secondaryOverlayIndices: Set<Int> = setOf(3, 7, 13, 15, 16, 20, 42)

    @JvmStatic
    fun consumersFor(resourceArrayIndex: Int): LegacySpriteResourceConsumerEvidence? =
        renderMethodConsumers.firstOrNull { it.resourceArrayIndex == resourceArrayIndex }
}
