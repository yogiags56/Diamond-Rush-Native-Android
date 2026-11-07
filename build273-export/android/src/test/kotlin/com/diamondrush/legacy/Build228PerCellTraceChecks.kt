package com.diamondrush.legacy

/** Framework-free checks; compile/run with the project's Kotlin test harness when available. */
object Build228PerCellTraceChecks {
    fun verifyCanonicalLinePreservesIndependentPasses() {
        val trace = LegacyCellRenderTrace(
            row = 2, column = 3, mapX = 7, mapY = 9, screenX = 48, screenY = 79,
            integerPlaneLowByte = 10, signedBytePlaneValue = -1, packedIntegerPlaneValue = 266,
            firstPass = LegacyRenderDispatchResolver.selectFirstMainPass(10),
            secondPass = LegacyRenderDispatchResolver.selectSecondMainPass(-1),
            secondaryOverlay = null,
            supplementalResourceIndices = emptyList()
        )
        val expected = "2,3,7,9,48,79,10,-1,266,EXPLICIT_SWITCH_CASE,1995,SKIP_CELL,5976,-,-,-,-,-,-"
        check(trace.canonicalLine() == expected)
    }

    fun verifyCsvHeaderAndStableNewline() {
        val csv = LegacyPerCellRenderTrace.canonicalCsv(emptyList())
        check(csv == LegacyPerCellRenderTrace.HEADER + "\n")
    }

    fun runAll() {
        verifyCanonicalLinePreservesIndependentPasses()
        verifyCsvHeaderAndStableNewline()
    }
}
