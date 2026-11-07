from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_build230_planner_preserves_order_and_opaque_branches():
    source = (ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyCellDrawCommandPlanner.kt").read_text()
    assert "OPAQUE_BRANCH" in source
    assert "SHARED_COMPOSITE_OR_CACHE_TAIL" in source
    assert "branchTargetOffset" in source
    assert "FIRST_MAIN" in source and "SECOND_MAIN" in source
    assert source.index("main(LegacyCellDrawPass.FIRST_MAIN") < source.index("main(LegacyCellDrawPass.SECOND_MAIN")
    assert source.index("main(LegacyCellDrawPass.SECOND_MAIN") < source.index("trace.secondaryOverlay?.let")
    assert "SUPPLEMENTAL" in source


def test_build230_scene_exposes_separate_command_csv():
    source = (ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyRoomSceneTrace.kt").read_text()
    assert "drawCommands: List<LegacyCellDrawCommand>" in source
    assert "canonicalDrawCommandCsv" in source
    assert "candidates.flatMap { it.drawCommands }" in source


def test_build230_does_not_assign_gameplay_names_to_unknown_branches():
    source = (ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyCellDrawCommandPlanner.kt").read_text()
    for forbidden in ("DIAMOND", "ENEMY", "ROCK", "PLAYER"):
        assert forbidden not in source
