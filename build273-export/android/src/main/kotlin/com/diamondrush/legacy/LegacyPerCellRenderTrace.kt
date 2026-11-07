package com.diamondrush.legacy

/** Build 228: deterministic, side-effect-free trace for one supplied room cell. */
data class LegacyCellTraceInput(
    val row: Int,
    val column: Int,
    val mapX: Int,
    val mapY: Int,
    val screenX: Int,
    val screenY: Int,
    val sample: LegacyRenderCellSample
)

data class LegacyCellRenderTrace(
    val row: Int,
    val column: Int,
    val mapX: Int,
    val mapY: Int,
    val screenX: Int,
    val screenY: Int,
    val integerPlaneLowByte: Int,
    val signedBytePlaneValue: Int,
    val packedIntegerPlaneValue: Int,
    val firstPass: LegacyMainDispatchDecision,
    val secondPass: LegacyMainDispatchDecision,
    val secondaryOverlay: LegacyOverlayFrameSelection?,
    val supplementalResourceIndices: List<Int>
) {
    /** Stable, locale-independent record suitable for golden fixtures and CSVs. */
    fun canonicalLine(): String = listOf(
        row, column, mapX, mapY, screenX, screenY,
        integerPlaneLowByte, signedBytePlaneValue, packedIntegerPlaneValue,
        firstPass.kind.name, firstPass.branchTargetOffset,
        secondPass.kind.name, secondPass.branchTargetOffset,
        secondaryOverlay?.resourceIndex ?: "-",
        secondaryOverlay?.kind?.name ?: "-",
        secondaryOverlay?.sequenceIndex ?: "-",
        secondaryOverlay?.frameIndex ?: "-",
        secondaryOverlay?.directDrawArgument ?: "-",
        supplementalResourceIndices.joinToString("+").ifEmpty { "-" }
    ).joinToString(",")
}

object LegacyPerCellRenderTrace {
    const val HEADER = "row,column,mapX,mapY,screenX,screenY,lowByte,signedByte,packedInt,firstKind,firstTarget,secondKind,secondTarget,overlayResource,overlayKind,sequence,frame,directArg,supplemental"

    /**
     * Trace one explicitly supplied cell. Coordinates are caller-provided because
     * the exact relationship between room axes and viewport iteration is not
     * inferred here. This preserves the two main dispatch passes as separate
     * ordered decisions and records the secondary overlay pass independently.
     */
    fun traceCell(
        input: LegacyCellTraceInput,
        animationClock: Int,
        animationTables: Map<Int, LegacySpriteAnimationTable>
    ): LegacyCellRenderTrace {
        val sample = input.sample
        return LegacyCellRenderTrace(
            row = input.row,
            column = input.column,
            mapX = input.mapX,
            mapY = input.mapY,
            screenX = input.screenX,
            screenY = input.screenY,
            integerPlaneLowByte = sample.integerPlaneLowByte,
            signedBytePlaneValue = sample.signedBytePlaneValue,
            packedIntegerPlaneValue = sample.packedIntegerPlaneValue,
            firstPass = LegacyRenderDispatchResolver.selectFirstMainPass(sample.integerPlaneLowByte),
            secondPass = LegacyRenderDispatchResolver.selectSecondMainPass(sample.signedBytePlaneValue),
            secondaryOverlay = LegacyRenderDispatchResolver.resolveOverlayFrame(sample, animationClock, animationTables),
            supplementalResourceIndices = LegacyRenderDispatchResolver.supplementalResources(sample)
        )
    }

    fun canonicalCsv(traces: List<LegacyCellRenderTrace>): String =
        (listOf(HEADER) + traces.map { it.canonicalLine() }).joinToString("\n", postfix = "\n")
}
