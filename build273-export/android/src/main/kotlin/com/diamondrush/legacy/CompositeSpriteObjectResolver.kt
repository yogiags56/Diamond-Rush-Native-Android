package com.diamondrush.legacy

/**
 * Expands one composite group into ordered leaf draw commands.
 *
 * Flag channels are kept separate because the original recursive overload
 * passes both the incoming flags and the XOR-adjusted flags to its child.
 */
class CompositeSpriteObjectResolver(
    private val section: LegacySpriteCompositeSection,
    private val maxDepth: Int = 128
) {
    data class LeafDrawCommand(
        val spriteIndex: Int,
        val x: Int,
        val y: Int,
        val incomingFlags: Int,
        val drawFlags: Int,
        val opaqueArgumentA: Int,
        val opaqueArgumentB: Int,
        val sourceGroupPath: List<Int>,
        val sourceComponentPath: List<Int>
    )

    fun resolve(
        rootGroup: Int,
        x: Int,
        y: Int,
        incomingFlags: Int,
        opaqueArgumentA: Int = 0,
        opaqueArgumentB: Int = 0
    ): List<LeafDrawCommand> {
        require(rootGroup in 0 until section.groupCount) { "Composite group $rootGroup out of range" }
        require(maxDepth > 0) { "maxDepth must be positive" }

        val output = ArrayList<LeafDrawCommand>()
        val active = BooleanArray(section.groupCount)
        val groupPath = ArrayList<Int>()
        val componentPath = ArrayList<Int>()

        fun expand(group: Int, originX: Int, originY: Int, flags: Int, depth: Int) {
            require(depth <= maxDepth) { "Composite nesting exceeds maxDepth=$maxDepth at group $group" }
            require(!active[group]) { "Composite cycle detected: ${(groupPath + group).joinToString(" -> ")}" }
            active[group] = true
            groupPath += group
            try {
                val count = section.componentCounts[group].toInt() and 0xff
                repeat(count) { component ->
                    val recordBase = CompositeSpriteRecord.recordBase(
                        section.componentStarts, group, component
                    )
                    val record = CompositeSpriteRecord.parse(section.componentRecords, recordBase)
                    val (childX, childY) = CompositeSpriteRules.componentPosition(
                        originX, originY, flags, record
                    )
                    val drawFlags = CompositeSpriteRules.adjustedFlags(flags, record)
                    componentPath += component
                    try {
                        if (record.isNestedComposite) {
                            require(record.spriteIndex in 0 until section.groupCount) {
                                "Nested target ${record.spriteIndex} out of range in group $group component $component"
                            }
                            expand(record.spriteIndex, childX, childY, drawFlags, depth + 1)
                        } else {
                            val dimBase = Math.multiplyExact(record.spriteIndex, 2)
                            require(dimBase >= 0 && dimBase + 1 < section.spriteDimensionBytes.size) {
                                "Leaf sprite ${record.spriteIndex} has no two-byte dimension entry"
                            }
                            val drawX = if ((flags and 0x01) != 0)
                                childX - (section.spriteDimensionBytes[dimBase].toInt() and 0xff)
                            else childX
                            val drawY = if ((flags and 0x02) != 0)
                                childY - (section.spriteDimensionBytes[dimBase + 1].toInt() and 0xff)
                            else childY
                            output += LeafDrawCommand(
                                record.spriteIndex, drawX, drawY, flags, drawFlags,
                                opaqueArgumentA, opaqueArgumentB,
                                groupPath.toList(), componentPath.toList()
                            )
                        }
                    } finally {
                        componentPath.removeAt(componentPath.lastIndex)
                    }
                }
            } finally {
                groupPath.removeAt(groupPath.lastIndex)
                active[group] = false
            }
        }

        expand(rootGroup, x, y, incomingFlags, 1)
        return output
    }
}
