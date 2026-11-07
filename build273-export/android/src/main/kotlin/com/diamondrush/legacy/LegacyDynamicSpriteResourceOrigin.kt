package com.diamondrush.legacy

/** Bytecode-backed origin of one global f[] resource slot in i.j()V. */
data class LegacyDynamicSpriteResourceOrigin(
    val globalSlot: Int,
    val resourcePath: String,
    val recordIndex: Int,
    val localRecordIndex: Int,
    val lengthHeaderOffset: Int,
    val branchBytecodeOffset: Int,
    val condition: String,
    val evidence: String = "BYTECODE_CONFIRMED"
) {
    fun canonicalLine(): String = listOf(
        globalSlot, resourcePath, recordIndex, localRecordIndex,
        lengthHeaderOffset, branchBytecodeOffset, condition, evidence
    ).joinToString(",")
}

/**
 * Evidence catalog only. It does not load assets or claim that a dispatch branch
 * unconditionally draws a resource. The original loader's runtime flag gates remain
 * explicit in [condition].
 */
object LegacyDynamicSpriteResourceOriginCatalog {
    private fun gen(index: Int, slot: Int, branchOffset: Int, condition: String = "record-enabled-by-c-bit") =
        LegacyDynamicSpriteResourceOrigin(
            globalSlot = slot,
            resourcePath = "/gen${index / 10}.f",
            recordIndex = index,
            localRecordIndex = index % 10,
            lengthHeaderOffset = 1 + (index % 10) * 8 + 4,
            branchBytecodeOffset = branchOffset,
            condition = condition
        )

    val confirmedOrigins: List<LegacyDynamicSpriteResourceOrigin> = listOf(
        LegacyDynamicSpriteResourceOrigin(60, "/{aA}.f", 0, 0, 5, 5672, "d-bit-0-enabled"),
        LegacyDynamicSpriteResourceOrigin(16, "/{aA}.f", 1, 1, 13, 5693, "d-bit-1-enabled"),
        LegacyDynamicSpriteResourceOrigin(42, "/{aA}.f", 2, 2, 21, 5716, "record-2-direct-slot-assignment"),
        gen(23, 30, 6262),
        gen(34, 27, 6283),
        LegacyDynamicSpriteResourceOrigin(
            globalSlot = 56, resourcePath = "/cm.f", recordIndex = 1,
            localRecordIndex = 1, lengthHeaderOffset = 1 + 1 * 8 + 4,
            branchBytecodeOffset = 6964,
            condition = "record-enabled-by-bu-bit; aA==1-or-2-applies-extra-initialization"
        ),
        LegacyDynamicSpriteResourceOrigin(
            globalSlot = 59, resourcePath = "/cm.f", recordIndex = 2,
            localRecordIndex = 2, lengthHeaderOffset = 1 + 2 * 8 + 4,
            branchBytecodeOffset = 6945,
            condition = "record-enabled-by-bu-bit"
        ),
        LegacyDynamicSpriteResourceOrigin(
            globalSlot = 13, resourcePath = "/cm.f", recordIndex = 3,
            localRecordIndex = 3, lengthHeaderOffset = 1 + 3 * 8 + 4,
            branchBytecodeOffset = 7040,
            condition = "record-enabled-by-bu-bit; invokes-r()"
        ),
        LegacyDynamicSpriteResourceOrigin(
            globalSlot = 43, resourcePath = "/cm.f", recordIndex = 6,
            localRecordIndex = 6, lengthHeaderOffset = 1 + 6 * 8 + 4,
            branchBytecodeOffset = 6920,
            condition = "record-enabled-by-bu-bit"
        )
    )

    fun originForGlobalSlot(slot: Int): LegacyDynamicSpriteResourceOrigin? =
        confirmedOrigins.firstOrNull { it.globalSlot == slot }

    fun canonicalCsv(): String = buildString {
        appendLine("global_slot,resource_path,record_index,local_record_index,length_header_offset,branch_bytecode_offset,condition,evidence")
        confirmedOrigins.forEach { appendLine(it.canonicalLine()) }
    }
}
