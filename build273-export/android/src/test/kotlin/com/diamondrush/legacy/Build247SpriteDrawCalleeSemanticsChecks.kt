package com.diamondrush.legacy

object Build247SpriteDrawCalleeSemanticsChecks {
    fun runAll() {
        check(LegacySpriteDrawCalleeSemantics.routine(7)?.role == LegacySpriteDrawRoutineRole.COMPOSITE_COMPONENT_ENTRY)
        check(LegacySpriteDrawCalleeSemantics.routine(7)?.delegatesToArgumentCount == 6)
        check(LegacySpriteDrawCalleeSemantics.routine(6)?.role == LegacySpriteDrawRoutineRole.COMPOSITE_GROUP_EXPANSION)
        check(LegacySpriteDrawCalleeSemantics.routine(6)?.canRecurse == true)
        check(LegacySpriteDrawCalleeSemantics.routine(4)?.role == LegacySpriteDrawRoutineRole.LEAF_SPRITE_DRAW)
        check(LegacySpriteDrawCalleeSemantics.routine(5) == null)
    }
}
