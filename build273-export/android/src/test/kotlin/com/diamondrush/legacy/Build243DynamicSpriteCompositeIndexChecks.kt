package com.diamondrush.legacy

object Build243DynamicSpriteCompositeIndexChecks {
    fun runAll() {
        fun layout(name: String) = javaClass.getResourceAsStream("/build242/$name")!!.use {
            LegacySpriteFieldLayoutParser.parse(it.readBytes())
        }
        val cases = listOf(
            Triple(27, "slot27.bin", listOf(7, 7, 3, 4, 5, 3, 2)),
            Triple(30, "slot30.bin", listOf(2, 1, 2, 2, 2, 1, 1, 1)),
            Triple(56, "slot56.bin", listOf(1, 2, 2, 1, 1, 1))
        )
        val expectedSpriteCounts = mapOf(27 to 11, 30 to 11, 56 to 6)
        val expectedComponents = mapOf(27 to 31, 30 to 12, 56 to 8)
        for ((slot, file, expectedGroups) in cases) {
            val parsed = layout(file)
            val paletteVariants = if (slot == 56) parsed.palettesArgb.indices else 0..0
            for (palette in paletteVariants) {
                val index = LegacyDynamicSpriteCompositeIndex.build(slot, parsed, palette)
                check(index.groups.map { it.componentCount } == expectedGroups)
                check(index.componentRecordCount == expectedComponents.getValue(slot))
                check(index.decodedSprites.size == expectedSpriteCounts.getValue(slot))
                check(index.groups.all { group ->
                    group.components.all { component ->
                        if (component.isNestedComposite) component.spriteIndex in index.groups.indices
                        else component.spriteIndex in index.decodedSprites.indices
                    }
                })
                check(index.decodedSprites.all { it.argb.size == it.width * it.height })
                check(index.decodedSprites.all { it.paletteIndex == palette })
            }
        }
        val p27 = LegacyDynamicSpriteCompositeIndex.build(27, layout("slot27.bin"), 0)
        val p30 = LegacyDynamicSpriteCompositeIndex.build(30, layout("slot30.bin"), 0)
        val p56 = LegacyDynamicSpriteCompositeIndex.build(56, layout("slot56.bin"), 0)
        check(p27.referencedSpriteIndices == (0..10).toSet())
        check(p30.referencedSpriteIndices == setOf(0, 1, 2, 3, 4, 8, 9, 10))
        check(p56.referencedSpriteIndices == (0..5).toSet())
        check(p27.groups.sumOf { it.components.count { c -> c.isNestedComposite } } == 0)
        check(p30.groups.sumOf { it.components.count { c -> c.isNestedComposite } } == 0)
        check(p56.groups.sumOf { it.components.count { c -> c.isNestedComposite } } == 0)
        println("BUILD243_DYNAMIC_COMPOSITE_INDEX_PASS: f27=7g/31c/11s f30=8g/12c/11s f56=6g/8c/6s")
    }
}
