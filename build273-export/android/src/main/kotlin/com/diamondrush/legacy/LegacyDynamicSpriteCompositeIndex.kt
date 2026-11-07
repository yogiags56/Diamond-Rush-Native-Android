package com.diamondrush.legacy

/** Build243: component-to-sprite attribution for bytecode-confirmed dynamic f[] resources. */
data class LegacyDynamicCompositeGroup(
    val groupIndex: Int,
    val firstComponentRecord: Int,
    val componentCount: Int,
    val components: List<CompositeSpriteRecord>
) {
    val leafSpriteIndices: List<Int>
        get() = components.filterNot { it.isNestedComposite }.map { it.spriteIndex }
    val nestedGroupIndices: List<Int>
        get() = components.filter { it.isNestedComposite }.map { it.spriteIndex }
}

data class LegacyDynamicSpritePixelRecord(
    val spriteIndex: Int,
    val width: Int,
    val height: Int,
    val argb: IntArray,
    val paletteIndex: Int,
    val hasTransparency: Boolean
)

data class LegacyDynamicSpriteCompositeIndex(
    val globalSlot: Int,
    val resourcePath: String,
    val groups: List<LegacyDynamicCompositeGroup>,
    val decodedSprites: List<LegacyDynamicSpritePixelRecord>,
    val componentRecordCount: Int
) {
    val referencedSpriteIndices: Set<Int>
        get() = groups.flatMap { it.leafSpriteIndices }.toSortedSet()

    companion object {
        /**
         * Group count/start and four-byte component tables are read from the
         * bytecode-aligned f-field layout. Palette selection remains explicit.
         * Nested references are retained as group references; no recursive
         * expansion is assumed here.
         */
        @JvmStatic
        fun build(
            globalSlot: Int,
            layout: LegacySpriteFieldLayout,
            paletteIndex: Int
        ): LegacyDynamicSpriteCompositeIndex {
            val origin = LegacyDynamicSpriteResourceOriginCatalog.originForGlobalSlot(globalSlot)
                ?: error("No bytecode-confirmed dynamic origin for f[$globalSlot]")
            require(origin.globalSlot == globalSlot)
            require(paletteIndex in layout.palettesArgb.indices) {
                "Palette $paletteIndex unavailable for f[$globalSlot]"
            }
            require(layout.hComponents.size % CompositeSpriteRecord.RECORD_SIZE == 0) {
                "Partial four-byte component table"
            }
            val recordCount = layout.hComponents.size / CompositeSpriteRecord.RECORD_SIZE
            val groups = layout.gGroupCounts.indices.map { group ->
                val count = layout.gGroupCounts[group].toInt() and 0xff
                val start = layout.bGroupStarts[group].toInt()
                require(start >= 0 && start.toLong() + count <= recordCount.toLong()) {
                    "Group $group component range exceeds table for f[$globalSlot]"
                }
                val records = List(count) { component ->
                    CompositeSpriteRecord.parse(
                        layout.hComponents,
                        CompositeSpriteRecord.recordBase(layout.bGroupStarts, group, component)
                    )
                }
                records.forEach { record ->
                    if (record.isNestedComposite) {
                        require(record.spriteIndex in layout.gGroupCounts.indices) {
                            "Nested group ${record.spriteIndex} outside f[$globalSlot]"
                        }
                    } else {
                        require(record.spriteIndex in 0 until layout.spriteCount) {
                            "Sprite ${record.spriteIndex} outside f[$globalSlot]"
                        }
                    }
                }
                LegacyDynamicCompositeGroup(group, start, count, records)
            }
            val palette = layout.palettesArgb[paletteIndex]
            val decoded = layout.spritePayloads.mapIndexed { index, bytes ->
                val width = layout.fDimensions[index * 2].toInt() and 0xff
                val height = layout.fDimensions[index * 2 + 1].toInt() and 0xff
                val indices = LegacySpriteDecoder.decodeIndices(bytes, width, height, layout.pixelFormat)
                val pixels = IntArray(indices.size)
                var transparent = false
                indices.forEachIndexed { pixel, colorIndex ->
                    require(colorIndex in palette.indices) {
                        "Sprite $index pixel $pixel palette index $colorIndex outside ${palette.size}"
                    }
                    pixels[pixel] = palette[colorIndex]
                    if ((palette[colorIndex] ushr 24) != 0xff) transparent = true
                }
                LegacyDynamicSpritePixelRecord(index, width, height, pixels, paletteIndex, transparent)
            }
            return LegacyDynamicSpriteCompositeIndex(
                globalSlot, origin.resourcePath, groups, decoded, recordCount
            )
        }
    }
}
