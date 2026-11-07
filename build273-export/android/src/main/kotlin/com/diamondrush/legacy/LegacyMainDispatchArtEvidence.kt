package com.diamondrush.legacy

/**
 * Build 241: preserves the CFG-reachable resource candidates for a main-pass
 * switch branch without pretending that a reachability union is an exclusive
 * semantic binding. Candidates are diagnostic evidence only; they are not
 * executable sprite draw commands.
 */
data class LegacyMainDispatchArtEvidence(
    val pass: MainPass,
    val selector: Int,
    val branchTargetOffset: Int,
    val reachableInstructionCount: Int,
    val directArrayAccessOffsets: List<Int>,
    val candidateResourceIndices: List<Int>,
    val reachableRenderCallCount: Int,
    val confidence: Confidence
) {
    enum class MainPass { BJ, BI }
    enum class Confidence { NO_REACHABLE_ART_EVIDENCE, CFG_REACHABLE_CANDIDATES_ONLY }

    init {
        require(selector >= 0)
        require(branchTargetOffset >= 0)
        require(reachableInstructionCount >= 0)
        require(reachableRenderCallCount >= 0)
        require(directArrayAccessOffsets.distinct().size == directArrayAccessOffsets.size)
        require(candidateResourceIndices.distinct().size == candidateResourceIndices.size)
        require(candidateResourceIndices.all { it >= 0 })
        require(confidence == if (candidateResourceIndices.isEmpty())
            Confidence.NO_REACHABLE_ART_EVIDENCE else Confidence.CFG_REACHABLE_CANDIDATES_ONLY)
    }

    fun canonicalLine(): String = listOf(
        pass.name, selector, branchTargetOffset, reachableInstructionCount,
        directArrayAccessOffsets.joinToString(";"),
        candidateResourceIndices.joinToString(";"), reachableRenderCallCount,
        confidence.name, "NOT_AN_EXCLUSIVE_BINDING"
    ).joinToString(",")
}

object LegacyMainDispatchArtEvidenceCatalog {
    /**
     * Inputs are copied from Build226's CFG-reachability audit. Candidate sets
     * are unions across conditional paths and must never be used to select art.
     */
    fun fromCfgAudit(
        pass: LegacyMainDispatchArtEvidence.MainPass,
        selector: Int,
        branchTargetOffset: Int,
        reachableInstructionCount: Int,
        directArrayAccessOffsets: List<Int>,
        candidateResourceIndices: List<Int>,
        reachableRenderCallCount: Int
    ): LegacyMainDispatchArtEvidence = LegacyMainDispatchArtEvidence(
        pass, selector, branchTargetOffset, reachableInstructionCount,
        directArrayAccessOffsets, candidateResourceIndices,
        reachableRenderCallCount,
        if (candidateResourceIndices.isEmpty())
            LegacyMainDispatchArtEvidence.Confidence.NO_REACHABLE_ART_EVIDENCE
        else LegacyMainDispatchArtEvidence.Confidence.CFG_REACHABLE_CANDIDATES_ONLY
    )

    fun canonicalCsv(rows: List<LegacyMainDispatchArtEvidence>): String =
        (listOf("pass,selector,branchTarget,reachableInstructions,directArrayAccessOffsets,candidateResourceIndices,reachableRenderCalls,confidence,executionStatus") +
            rows.map { it.canonicalLine() }).joinToString("\n", postfix = "\n")
}
