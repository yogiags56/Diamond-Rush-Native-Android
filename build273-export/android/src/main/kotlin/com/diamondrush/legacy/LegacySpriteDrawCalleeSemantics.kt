package com.diamondrush.legacy

/** Bytecode-proven structural roles of the original f.a(Graphics, ...) overloads. */
enum class LegacySpriteDrawRoutineRole {
    COMPOSITE_COMPONENT_ENTRY,
    COMPOSITE_GROUP_EXPANSION,
    LEAF_SPRITE_DRAW
}

data class LegacySpriteDrawRoutineDescriptor(
    val integerArgumentCount: Int,
    val role: LegacySpriteDrawRoutineRole,
    val delegatesToArgumentCount: Int?,
    val canRecurse: Boolean
)

object LegacySpriteDrawCalleeSemantics {
    val routines = listOf(
        LegacySpriteDrawRoutineDescriptor(7, LegacySpriteDrawRoutineRole.COMPOSITE_COMPONENT_ENTRY, 6, false),
        LegacySpriteDrawRoutineDescriptor(6, LegacySpriteDrawRoutineRole.COMPOSITE_GROUP_EXPANSION, 6, true),
        LegacySpriteDrawRoutineDescriptor(4, LegacySpriteDrawRoutineRole.LEAF_SPRITE_DRAW, null, false)
    )

    fun routine(argumentCount: Int): LegacySpriteDrawRoutineDescriptor? =
        routines.firstOrNull { it.integerArgumentCount == argumentCount }
}
