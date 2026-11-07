package com.diamondrush.legacy

/** One evidence-preserving cell record assembled from the original room planes. */
data class LegacyAssembledRoomCell(
    val row: Int,
    val column: Int,
    val mapFirst: Int,
    val mapSecond: Int,
    val screenX: Int,
    val screenY: Int,
    val logicalCanvasY: Int,
    val inBounds: Boolean,
    val packedIntegerValue: Int? = null,
    val primarySignedByte: Int? = null,
    val firstPass: LegacyMainDispatchDecision? = null,
    val secondPass: LegacyMainDispatchDecision? = null,
    val overlayRoute: LegacyRenderDispatchCatalog.OverlayRoute? = null,
    val supplementalResources: List<Int> = emptyList()
) {
    fun canonicalLine(): String = listOf(
        row, column, mapFirst, mapSecond, screenX, screenY, logicalCanvasY,
        if (inBounds) "IN" else "OUT",
        packedIntegerValue ?: "-", primarySignedByte ?: "-",
        firstPass?.kind?.name ?: "-", firstPass?.branchTargetOffset ?: "-",
        secondPass?.kind?.name ?: "-", secondPass?.branchTargetOffset ?: "-",
        overlayRoute?.resourceIndex ?: "-", overlayRoute?.frameRule?.name ?: "-",
        supplementalResources.joinToString("+").ifEmpty { "-" }
    ).joinToString(",")
}

data class LegacyAssembledRoomPass(
    val roomIndex: Int,
    val camera: LegacyCameraOffset,
    val cells: List<LegacyAssembledRoomCell>
) {
    val inBoundsCount: Int get() = cells.count { it.inBounds }
    val outOfBoundsCount: Int get() = cells.size - inBoundsCount
    val overlayRouteCount: Int get() = cells.count { it.overlayRoute != null }
    val opaqueFirstPassCount: Int get() = cells.count {
        it.firstPass?.kind in setOf(LegacyMainDispatchKind.EXPLICIT_SWITCH_CASE, LegacyMainDispatchKind.DEFAULT_SHARED_TAIL)
    }
    fun canonicalCsv(): String = (listOf(HEADER) + cells.map { it.canonicalLine() })
        .joinToString("\n", postfix = "\n")
    companion object {
        const val HEADER = "row,column,mapFirst,mapSecond,screenX,screenY,logicalCanvasY,bounds,packedInteger,primarySignedByte,firstKind,firstTarget,secondKind,secondTarget,overlayResource,overlayRule,supplementalResources"
    }
}

/**
 * Build 240: assembles the original room's viewport cell scan into a deterministic
 * ordered render-pass manifest. It intentionally does not assign art semantics to
 * opaque dispatch targets or invent sequence/frame selection for resource 42.
 */
object LegacyRoomRenderAssembly {
    @JvmStatic
    fun assemble(
        room: LegacyDecodedRoom,
        camera: LegacyCameraOffset
    ): LegacyAssembledRoomPass {
        val candidates = LegacyVisibleCellTraversal.candidates(room.planes, camera)
        val cells = candidates.map { candidate ->
            val logicalY = candidate.screenY + LegacyGameplayViewport.VIEWPORT_TRANSLATE_Y
            if (!candidate.inBounds) {
                LegacyAssembledRoomCell(
                    candidate.row, candidate.column, candidate.mapFirst, candidate.mapSecond,
                    candidate.screenX, candidate.screenY, logicalY, false
                )
            } else {
                val packed = room.planes.secondaryIntAt(candidate.mapFirst, candidate.mapSecond)
                val signed = room.planes.primaryByteAt(candidate.mapFirst, candidate.mapSecond).toInt()
                val sample = LegacyRenderCellSample(packed and 0xff, signed, packed)
                LegacyAssembledRoomCell(
                    candidate.row, candidate.column, candidate.mapFirst, candidate.mapSecond,
                    candidate.screenX, candidate.screenY, logicalY, true,
                    packed, signed,
                    LegacyRenderDispatchResolver.selectFirstMainPass(sample.integerPlaneLowByte),
                    LegacyRenderDispatchResolver.selectSecondMainPass(sample.signedBytePlaneValue),
                    LegacyRenderDispatchCatalog.overlayRoute(sample.integerPlaneLowByte),
                    LegacyRenderDispatchResolver.supplementalResources(sample)
                )
            }
        }
        return LegacyAssembledRoomPass(room.roomIndex, camera, cells)
    }
}
