package com.diamondrush.legacy

/** Build 229: one viewport candidate joined to room-plane data when in bounds. */
data class LegacyRoomSceneCellTrace(
    val candidate: LegacyVisibleCellCandidate,
    val logicalCanvasY: Int,
    val cellTrace: LegacyCellRenderTrace?
) {
    val drawCommands: List<LegacyCellDrawCommand> = cellTrace?.let { LegacyCellDrawCommandPlanner.plan(it) } ?: emptyList()
    val isOutOfBounds: Boolean get() = cellTrace == null

    fun canonicalLine(): String = if (cellTrace == null) {
        listOf(candidate.row, candidate.column, candidate.mapFirst, candidate.mapSecond,
            candidate.screenX, candidate.screenY, logicalCanvasY, "OUT_OF_BOUNDS").joinToString(",")
    } else {
        "${cellTrace.canonicalLine()},$logicalCanvasY,IN_BOUNDS"
    }
}

/** Ordered scene trace; preserves the source traversal's row-major candidate order. */
data class LegacyRoomSceneTrace(
    val camera: LegacyCameraOffset,
    val candidates: List<LegacyRoomSceneCellTrace>
) {
    val inBoundsCount: Int get() = candidates.count { !it.isOutOfBounds }
    val outOfBoundsCount: Int get() = candidates.count { it.isOutOfBounds }

    fun canonicalCsv(): String = (listOf(
        LegacyPerCellRenderTrace.HEADER + ",logicalCanvasY,boundsStatus"
    ) + candidates.map { it.canonicalLine() }).joinToString("\n", postfix = "\n")

    /** Separate ordered command stream; raw scene trace remains backward compatible. */
    fun canonicalDrawCommandCsv(): String = LegacyCellDrawCommandPlanner.canonicalCsv(
        candidates.flatMap { it.drawCommands }
    )
}

/** Joins the proven room-plane storage model with the observed camera candidate scan. */
object LegacyRoomSceneTraceBuilder {
    /**
     * Plane mapping follows the recovered renderer reads: primary byte plane supplies
     * the signed bI selector; secondary integer plane supplies packed bJ metadata.
     * serializedIntPlane is retained in the room model but is not substituted here.
     * Out-of-room candidates remain explicit and never trigger an array read.
     */
    fun build(
        room: LegacyRoomMapPlanes,
        camera: LegacyCameraOffset,
        animationClock: Int,
        animationTables: Map<Int, LegacySpriteAnimationTable>
    ): LegacyRoomSceneTrace {
        val cells = LegacyVisibleCellTraversal.candidates(room, camera).map { candidate ->
            val logicalY = candidate.screenY + LegacyGameplayViewport.VIEWPORT_TRANSLATE_Y
            if (!candidate.inBounds) {
                LegacyRoomSceneCellTrace(candidate, logicalY, null)
            } else {
                val packed = room.secondaryIntAt(candidate.mapFirst, candidate.mapSecond)
                val signed = room.primaryByteAt(candidate.mapFirst, candidate.mapSecond).toInt()
                val sample = LegacyRenderCellSample(
                    integerPlaneLowByte = packed and 0xff,
                    signedBytePlaneValue = signed,
                    packedIntegerPlaneValue = packed
                )
                val trace = LegacyPerCellRenderTrace.traceCell(
                    LegacyCellTraceInput(
                        row = candidate.row,
                        column = candidate.column,
                        mapX = candidate.mapFirst,
                        mapY = candidate.mapSecond,
                        screenX = candidate.screenX,
                        screenY = candidate.screenY,
                        sample = sample
                    ), animationClock, animationTables
                )
                LegacyRoomSceneCellTrace(candidate, logicalY, trace)
            }
        }
        return LegacyRoomSceneTrace(camera, cells)
    }
}
