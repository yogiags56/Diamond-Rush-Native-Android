package com.diamondrush.legacy

object Build230DrawCommandPlannerChecks {
    private fun sampleTrace(low: Int, signed: Int, packed: Int): LegacyCellRenderTrace {
        val sample = LegacyRenderCellSample(low, signed, packed)
        return LegacyPerCellRenderTrace.traceCell(
            LegacyCellTraceInput(2, 3, 4, 5, 72, 96, sample), 0, emptyMap()
        )
    }

    fun verifyMainPassOrderAndOpaqueTarget() {
        val trace = sampleTrace(3, 0, 3)
        val commands = LegacyCellDrawCommandPlanner.plan(trace)
        check(commands.size >= 2)
        check(commands[0].pass == LegacyCellDrawPass.FIRST_MAIN)
        check(commands[0].kind == LegacyCellDrawCommandKind.OPAQUE_BRANCH)
        check(commands[0].branchTargetOffset == 1890)
        check(commands[1].pass == LegacyCellDrawPass.SECOND_MAIN)
        check(commands[1].kind == LegacyCellDrawCommandKind.OPAQUE_BRANCH)
        check(commands.map { it.ordinal } == commands.indices.toList())
    }

    fun verifySkipAndSharedTailRemainDistinct() {
        val skip = LegacyCellDrawCommandPlanner.plan(sampleTrace(0, -1, 0))
        check(skip[1].kind == LegacyCellDrawCommandKind.SKIP_CELL)
        val tail = LegacyCellDrawCommandPlanner.plan(sampleTrace(10, 3, 10))
        check(tail[0].kind == LegacyCellDrawCommandKind.SHARED_COMPOSITE_OR_CACHE_TAIL)
        check(tail[0].branchTargetOffset == 1995)
    }

    fun verifySceneCommandCsvIsStable() {
        val room = LegacyRoomMapPlanes(1, 1, byteArrayOf(3), intArrayOf(10), intArrayOf(3))
        val scene = LegacyRoomSceneTraceBuilder.build(room, LegacyCameraOffset(0, 0), 0, emptyMap())
        val csv = scene.canonicalDrawCommandCsv()
        check(csv.startsWith(LegacyCellDrawCommandPlanner.HEADER + "\n"))
        check(csv.endsWith("\n"))
        check(csv.contains("OPAQUE_BRANCH"))
        check(csv.contains("SHARED_COMPOSITE_OR_CACHE_TAIL"))
    }

    fun runAll() {
        verifyMainPassOrderAndOpaqueTarget()
        verifySkipAndSharedTailRemainDistinct()
        verifySceneCommandCsvIsStable()
    }
}
