package com.diamondrush.legacy

/**
 * Structural index for nested composite references.
 *
 * The original draw overload treats byte-0 as a composite-group index only
 * when control bit 0x10 is set. Leaf sprite indices remain a separate namespace.
 * This class deliberately does not resolve leaf descriptors or assign meaning
 * to the two opaque pass-through draw arguments.
 */
class CompositeSpriteGraphIndex(
    private val componentCounts: ByteArray,
    private val componentStarts: ShortArray,
    private val componentRecords: ByteArray
) {
    data class Group(val index: Int, val records: List<CompositeSpriteRecord>)
    data class Edge(val fromGroup: Int, val toGroup: Int, val componentIndex: Int)
    data class Inspection(
        val groups: List<Group>,
        val nestedEdges: List<Edge>,
        val invalidNestedTargets: List<Edge>,
        val cycles: List<List<Int>>,
        val maximumDepth: Int
    )

    fun inspect(): Inspection {
        require(componentCounts.size == componentStarts.size) {
            "component count/start table size mismatch"
        }
        val groups = componentCounts.indices.map { group ->
            val count = componentCounts[group].toInt() and 0xff
            val records = (0 until count).map { component ->
                val base = CompositeSpriteRecord.recordBase(componentStarts, group, component)
                CompositeSpriteRecord.parse(componentRecords, base)
            }
            Group(group, records)
        }

        val edges = mutableListOf<Edge>()
        val invalid = mutableListOf<Edge>()
        for (group in groups) {
            group.records.forEachIndexed { component, record ->
                if (record.isNestedComposite) {
                    val edge = Edge(group.index, record.spriteIndex, component)
                    if (record.spriteIndex in groups.indices) edges += edge else invalid += edge
                }
            }
        }

        val adjacency = groups.indices.associateWith { g ->
            edges.filter { it.fromGroup == g }.map { it.toGroup }
        }
        val color = IntArray(groups.size) // 0 unseen, 1 active, 2 complete
        val stack = mutableListOf<Int>()
        val cycles = mutableListOf<List<Int>>()
        var maxDepth = 0

        fun visit(node: Int, depth: Int) {
            maxDepth = maxOf(maxDepth, depth)
            color[node] = 1
            stack += node
            for (next in adjacency[node].orEmpty()) {
                when (color[next]) {
                    0 -> visit(next, depth + 1)
                    1 -> {
                        val start = stack.indexOf(next)
                        if (start >= 0) cycles += (stack.subList(start, stack.size) + next).toList()
                    }
                }
            }
            stack.removeAt(stack.lastIndex)
            color[node] = 2
        }

        groups.indices.forEach { if (color[it] == 0) visit(it, 1) }
        return Inspection(groups, edges, invalid, cycles, maxDepth)
    }
}
