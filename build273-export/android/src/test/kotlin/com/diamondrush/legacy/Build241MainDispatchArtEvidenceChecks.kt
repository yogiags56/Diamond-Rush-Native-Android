package com.diamondrush.legacy

object Build241MainDispatchArtEvidenceChecks {
    fun runAll() {
        val row = LegacyMainDispatchArtEvidenceCatalog.fromCfgAudit(
            LegacyMainDispatchArtEvidence.MainPass.BJ, 6, 1064, 462,
            listOf(1501, 1930, 1957), listOf(27, 30, 56), 2
        )
        check(row.confidence == LegacyMainDispatchArtEvidence.Confidence.CFG_REACHABLE_CANDIDATES_ONLY)
        check(row.candidateResourceIndices == listOf(27, 30, 56))
        check(row.canonicalLine().endsWith("NOT_AN_EXCLUSIVE_BINDING"))

        val empty = LegacyMainDispatchArtEvidenceCatalog.fromCfgAudit(
            LegacyMainDispatchArtEvidence.MainPass.BJ, 10, 1995, 0,
            emptyList(), emptyList(), 0
        )
        check(empty.confidence == LegacyMainDispatchArtEvidence.Confidence.NO_REACHABLE_ART_EVIDENCE)
        check(LegacyMainDispatchArtEvidenceCatalog.canonicalCsv(listOf(row, empty)).lines().size == 4)

        var rejected = false
        try {
            LegacyMainDispatchArtEvidenceCatalog.fromCfgAudit(
                LegacyMainDispatchArtEvidence.MainPass.BI, 3, 5676, 0,
                emptyList(), listOf(-1), 0
            )
        } catch (_: IllegalArgumentException) { rejected = true }
        check(rejected)
    }
}
