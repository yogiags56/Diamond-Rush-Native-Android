package com.diamondrush.legacy

object Build225CameraChecks {
    @JvmStatic fun main(args: Array<String>) {
        val planner = LegacyCameraRedrawPlanner()
        val initial = planner.plan(25, 49, 240, 192)
        check(initial.size == 1)
        check(initial[0].axis == LegacyRedrawAxis.INITIAL)
        check(initial[0] == LegacyMapRedrawRegion(
            LegacyRedrawAxis.INITIAL, 24, 48, 240, 216
        ))
        check(initial[0].columns == 10 && initial[0].rows == 8)

        // Move one tile to the right: only the newly exposed right strip.
        val xMove = planner.plan(49, 49, 240, 192)
        check(xMove.size == 1)
        check(xMove[0] == LegacyMapRedrawRegion(
            LegacyRedrawAxis.X_STRIP, 264, 48, 264, 216
        ))

        // Move one tile down: only the newly exposed bottom strip.
        val yMove = planner.plan(49, 73, 240, 192)
        check(yMove.size == 1)
        check(yMove[0] == LegacyMapRedrawRegion(
            LegacyRedrawAxis.Y_STRIP, 48, 240, 264, 240
        ))

        // Simultaneous diagonal movement emits independent X and Y strips.
        val diagonal = planner.plan(73, 97, 240, 192)
        check(diagonal.size == 2)
        check(diagonal[0].axis == LegacyRedrawAxis.X_STRIP)
        check(diagonal[1].axis == LegacyRedrawAxis.Y_STRIP)

        // A one-tile movement in the opposite direction exposes the left/top strips.
        val reverse = planner.plan(49, 73, 240, 192)
        check(reverse.size == 2)
        check(reverse[0] == LegacyMapRedrawRegion(
            LegacyRedrawAxis.X_STRIP, 48, 72, 48, 240
        ))
        check(reverse[1] == LegacyMapRedrawRegion(
            LegacyRedrawAxis.Y_STRIP, 48, 72, 264, 72
        ))

        val stable = planner.plan(49, 73, 240, 192)
        check(stable.isEmpty())

        val motion = LegacyCameraMotion.applyVerticalStep(50, 7, 11)
        check(motion.appliedDelta == ((7 * 11) % ((7 shr 1) + 1)) % 12)
        check(motion.resultingOffset == 50 - motion.appliedDelta)
        val clamped = LegacyCameraMotion.applyVerticalStep(0, 7, 11)
        check(clamped.appliedDelta == 0 && clamped.resultingOffset == 0)
        val disabled = LegacyCameraMotion.applyVerticalStep(20, 0, 11)
        check(disabled.appliedDelta == 0 && disabled.resultingOffset == 20)

        // D() indexes map dimension 1 with camera X + column,
        // and dimension 2 with camera Y + row.
        val room = LegacyRoomMapPlanes(6, 7, ByteArray(42), IntArray(42), IntArray(42))
        val cells = LegacyVisibleCellTraversal.candidates(
            room, LegacyCameraOffset(48, 24)
        )
        val center = cells.first { it.row == 0 && it.column == 0 }
        check(center.mapFirst == 2 && center.mapSecond == 1)
        check(center.screenX == 0 && center.screenY == 0)
        val right = cells.first { it.row == 0 && it.column == 1 }
        check(right.mapFirst == 3 && right.mapSecond == 1)
        val below = cells.first { it.row == 1 && it.column == 0 }
        check(below.mapFirst == 2 && below.mapSecond == 2)

        println("BUILD225_KOTLIN_CHECKS_PASSED")
    }
}
