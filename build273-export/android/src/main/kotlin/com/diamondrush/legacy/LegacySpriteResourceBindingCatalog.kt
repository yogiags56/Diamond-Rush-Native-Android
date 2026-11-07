package com.diamondrush.legacy

/**
 * Build 235: evidence-backed bridge from the ten statically loaded global f[]
 * slots to their local sprite records, composite component graph, and animation
 * frame group references. Resource/slot names remain numeric and opaque.
 */
data class LegacyBoundSpriteRecord(
    val globalArraySlot: Int,
    val bundlePath: String,
    val bundleEntryIndex: Int,
    val spriteIndex: Int,
    val width: Int,
    val height: Int,
    val encodedPixelBytes: Int,
    val pixelFormat: Int?
)

data class LegacyBoundCompositeComponent(
    val globalArraySlot: Int,
    val groupIndex: Int,
    val componentIndex: Int,
    val componentRecordIndex: Int,
    val targetIndex: Int,
    val targetIsNestedGroup: Boolean,
    val targetInRange: Boolean
)

data class LegacyBoundAnimationFrame(
    val globalArraySlot: Int,
    val sequenceIndex: Int,
    val frameIndex: Int,
    val animationRecordIndex: Int,
    val animationRecordInRange: Boolean,
    val rawGroupIndex: Int?,
    val durationUnits: Int?,
    val offsetX: Int?,
    val offsetY: Int?,
    val controlFlags: Int?,
    val groupInRange: Boolean?
)

data class LegacyBoundSpriteResource(
    val globalArraySlot: Int,
    val bundlePath: String,
    val bundleEntryIndex: Int,
    val renderConsumer: LegacySpriteResourceConsumerEvidence?,
    val sprites: List<LegacyBoundSpriteRecord>,
    val components: List<LegacyBoundCompositeComponent>,
    val animationFrames: List<LegacyBoundAnimationFrame>
)

object LegacySpriteResourceBindingCatalog {
    /**
     * `parsedByGlobalSlot` must be keyed by the exact slot from the original
     * `i.b(I)V` aastore evidence. It is deliberately not keyed by sprite ID.
     */
    @JvmStatic
    fun bind(parsedByGlobalSlot: Map<Int, LegacySpriteResourceBundleParser.ParsedDf03>): List<LegacyBoundSpriteResource> {
        val knownBindings = LegacyBundleSpriteSlotCatalog.staticBindings.associateBy { it.globalArraySlot }
        require(parsedByGlobalSlot.keys.all { it in knownBindings }) {
            "Parsed resource map contains a slot without static bundle/entry evidence"
        }

        return LegacyBundleSpriteSlotCatalog.staticBindings.mapNotNull { binding ->
            val parsed = parsedByGlobalSlot[binding.globalArraySlot] ?: return@mapNotNull null
            val spriteRows = parsed.sprites.map { sprite ->
                LegacyBoundSpriteRecord(
                    binding.globalArraySlot, binding.bundlePath, binding.entryIndex,
                    sprite.index, sprite.width, sprite.height, sprite.encodedPixels.size,
                    parsed.pixelFormat
                )
            }

            val componentRecords = ArrayList<CompositeSpriteRecord>(parsed.fourByteTable.size / 4)
            require(parsed.fourByteTable.size % CompositeSpriteRecord.RECORD_SIZE == 0) {
                "Slot ${binding.globalArraySlot} has a partial component record"
            }
            for (offset in parsed.fourByteTable.indices step CompositeSpriteRecord.RECORD_SIZE) {
                componentRecords += CompositeSpriteRecord.parse(parsed.fourByteTable, offset)
            }

            val componentRows = ArrayList<LegacyBoundCompositeComponent>()
            parsed.metadataRows.forEachIndexed { groupIndex, metadata ->
                val start = metadata.value
                val count = metadata.first
                repeat(count) { componentIndex ->
                    val recordIndex = start + componentIndex
                    if (recordIndex !in componentRecords.indices) {
                        componentRows += LegacyBoundCompositeComponent(
                            binding.globalArraySlot, groupIndex, componentIndex, recordIndex,
                            -1, false, false
                        )
                    } else {
                        val record = componentRecords[recordIndex]
                        val nested = record.isNestedComposite
                        val targetLimit = if (nested) parsed.metadataRows.size else parsed.sprites.size
                        componentRows += LegacyBoundCompositeComponent(
                            binding.globalArraySlot, groupIndex, componentIndex, recordIndex,
                            record.spriteIndex, nested, record.spriteIndex in 0 until targetLimit
                        )
                    }
                }
            }

            require(parsed.fiveByteTable.size % LegacySpriteAnimationFrame.RECORD_SIZE == 0) {
                "Slot ${binding.globalArraySlot} has a partial five-byte animation record"
            }
            val animationRecordCount = parsed.fiveByteTable.size / LegacySpriteAnimationFrame.RECORD_SIZE
            val animationRows = ArrayList<LegacyBoundAnimationFrame>()
            parsed.byteShortRows.forEachIndexed { sequenceIndex, sequence ->
                repeat(sequence.first) { frameIndex ->
                    val recordIndex = sequence.value + frameIndex
                    if (recordIndex !in 0 until animationRecordCount) {
                        animationRows += LegacyBoundAnimationFrame(
                            binding.globalArraySlot, sequenceIndex, frameIndex, recordIndex,
                            false, null, null, null, null, null, null
                        )
                    } else {
                        val base = recordIndex * LegacySpriteAnimationFrame.RECORD_SIZE
                        val rawGroup = parsed.fiveByteTable[base].toInt() and 0xff
                        val groupInRange = if (rawGroup == LegacySpriteAnimationFrame.NO_GROUP) null
                            else rawGroup in parsed.metadataRows.indices
                        animationRows += LegacyBoundAnimationFrame(
                            binding.globalArraySlot, sequenceIndex, frameIndex, recordIndex,
                            true, rawGroup,
                            parsed.fiveByteTable[base + 1].toInt() and 0xff,
                            parsed.fiveByteTable[base + 2].toInt(),
                            parsed.fiveByteTable[base + 3].toInt(),
                            parsed.fiveByteTable[base + 4].toInt() and 0xff,
                            groupInRange
                        )
                    }
                }
            }

            LegacyBoundSpriteResource(
                binding.globalArraySlot, binding.bundlePath, binding.entryIndex,
                LegacySpriteResourceConsumerCatalog.consumersFor(binding.globalArraySlot),
                spriteRows, componentRows, animationRows
            )
        }
    }
}
