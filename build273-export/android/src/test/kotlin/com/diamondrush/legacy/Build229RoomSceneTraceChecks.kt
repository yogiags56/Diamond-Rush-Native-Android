package com.diamondrush.legacy

object Build229RoomSceneTraceChecks {
    fun verifyCandidateJoinAndBounds() {
        val room = LegacyRoomMapPlanes(
            firstDimension = 4, secondDimension = 4,
            primaryByte = ByteArray(16) { (-1).toByte() },
            serializedIntPlane = IntArray(16) { 1234 },
            secondaryIntPlane = IntArray(16) { 0 }
        )
        val scene = LegacyRoomSceneTraceBuilder.build(
            room, LegacyCameraOffset(0, 0), 0, emptyMap()
        )
        check(scene.candidates.size == 160)
        check(scene.inBoundsCount == 16)
        check(scene.outOfBoundsCount == 144)
        val firstInBounds = scene.candidates.first { !it.isOutOfBounds }
        check(firstInBounds.candidate.mapFirst == 0)
        check(firstInBounds.candidate.mapSecond == 0)
        check(firstInBounds.cellTrace?.secondPass?.kind == LegacyMainDispatchKind.SKIP_CELL)
        check(firstInBounds.logicalCanvasY == firstInBounds.candidate.screenY + 31)
    }

    fun verifyCanonicalSceneTraceIsStable() {
        val room = LegacyRoomMapPlanes(1, 1, byteArrayOf((-1).toByte()), intArrayOf(9), intArrayOf(0))
        val scene = LegacyRoomSceneTraceBuilder.build(room, LegacyCameraOffset(0, 0), 0, emptyMap())
        val csv = scene.canonicalCsv()
        check(csv.startsWith(LegacyPerCellRenderTrace.HEADER + ",logicalCanvasY,boundsStatus\n"))
        check(csv.endsWith("\n"))
        check(csv.contains("OUT_OF_BOUNDS"))
        check(csv.contains("IN_BOUNDS"))
    }

    fun runAll() {
        verifyCandidateJoinAndBounds()
        verifyCanonicalSceneTraceIsStable()
    }
}
