package com.diamondrush.legacy

/** Build 230: an ordered, deliberately conservative command representation. */
enum class LegacyCellDrawCommandKind {
    OPAQUE_BRANCH,
    SHARED_COMPOSITE_OR_CACHE_TAIL,
    SKIP_CELL,
    ANIMATION_COMPOSITE_REQUEST,
    DIRECT_DRAW_REQUEST,
    SUPPLEMENTAL_RESOURCE_REQUEST
}

enum class LegacyCellDrawPass { FIRST_MAIN, SECOND_MAIN, SECONDARY_OVERLAY, SUPPLEMENTAL }

data class LegacyCellDrawCommand(
    val ordinal: Int,
    val row: Int,
    val column: Int,
    val pass: LegacyCellDrawPass,
    val kind: LegacyCellDrawCommandKind,
    val rawSelector: Int,
    val branchTargetOffset: Int? = null,
    val resourceIndex: Int? = null,
    val sequenceIndex: Int? = null,
    val frameIndex: Int? = null,
    val directDrawArgument: Int? = null
) {
    fun canonicalLine(): String = listOf(
        ordinal, row, column, pass.name, kind.name, rawSelector,
        branchTargetOffset ?: "-", resourceIndex ?: "-", sequenceIndex ?: "-",
        frameIndex ?: "-", directDrawArgument ?: "-"
    ).joinToString(",")
}

/**
 * Converts resolver outcomes into ordered records, not pixels. Unknown switch
 * branches remain opaque and retain their bytecode target offset. Shared tails
 * are identified only by their known control-flow target, not by guessed art.
 */
object LegacyCellDrawCommandPlanner {
    const val HEADER = "ordinal,row,column,pass,kind,rawSelector,branchTarget,resource,sequence,frame,directArgument"
    private val sharedTailOffsets = setOf(
        LegacyRenderDispatchCatalog.MAIN_PASS_BJ_SHARED_TAIL_OFFSET,
        LegacyRenderDispatchCatalog.MAIN_PASS_BI_SHARED_TAIL_OFFSET
    )

    fun plan(trace: LegacyCellRenderTrace): List<LegacyCellDrawCommand> {
        val out = ArrayList<LegacyCellDrawCommand>(5)
        fun add(
            pass: LegacyCellDrawPass,
            kind: LegacyCellDrawCommandKind,
            selector: Int,
            target: Int? = null,
            resource: Int? = null,
            sequence: Int? = null,
            frame: Int? = null,
            direct: Int? = null
        ) {
            out += LegacyCellDrawCommand(
                out.size, trace.row, trace.column, pass, kind, selector,
                target, resource, sequence, frame, direct
            )
        }
        fun main(pass: LegacyCellDrawPass, decision: LegacyMainDispatchDecision) {
            val kind = when (decision.kind) {
                LegacyMainDispatchKind.SKIP_CELL -> LegacyCellDrawCommandKind.SKIP_CELL
                else -> if (decision.branchTargetOffset in sharedTailOffsets)
                    LegacyCellDrawCommandKind.SHARED_COMPOSITE_OR_CACHE_TAIL
                else LegacyCellDrawCommandKind.OPAQUE_BRANCH
            }
            add(pass, kind, decision.rawSelector, decision.branchTargetOffset)
        }
        main(LegacyCellDrawPass.FIRST_MAIN, trace.firstPass)
        main(LegacyCellDrawPass.SECOND_MAIN, trace.secondPass)
        trace.secondaryOverlay?.let { selection ->
            val kind = if (selection.kind == LegacyOverlaySelectionKind.ANIMATION_SEQUENCE_FRAME)
                LegacyCellDrawCommandKind.ANIMATION_COMPOSITE_REQUEST
            else LegacyCellDrawCommandKind.DIRECT_DRAW_REQUEST
            add(
                LegacyCellDrawPass.SECONDARY_OVERLAY, kind, selection.rawLowByte,
                resource = selection.resourceIndex, sequence = selection.sequenceIndex,
                frame = selection.frameIndex, direct = selection.directDrawArgument
            )
        }
        trace.supplementalResourceIndices.forEach { resource ->
            add(LegacyCellDrawPass.SUPPLEMENTAL,
                LegacyCellDrawCommandKind.SUPPLEMENTAL_RESOURCE_REQUEST,
                trace.integerPlaneLowByte, resource = resource)
        }
        return out
    }

    fun canonicalCsv(commands: List<LegacyCellDrawCommand>): String =
        (listOf(HEADER) + commands.map { it.canonicalLine() }).joinToString("\n", postfix = "\n")
}
