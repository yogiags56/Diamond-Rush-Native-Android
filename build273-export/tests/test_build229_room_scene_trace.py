from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyRoomSceneTrace.kt"


def test_scene_builder_uses_proven_viewport_candidate_traversal():
    s = SRC.read_text()
    assert "LegacyVisibleCellTraversal.candidates(room, camera)" in s
    assert "candidate.inBounds" in s
    assert "LegacyGameplayViewport.VIEWPORT_TRANSLATE_Y" in s


def test_scene_builder_keeps_plane_mapping_explicit_and_does_not_use_serialized_plane():
    s = SRC.read_text()
    assert "room.primaryByteAt(candidate.mapFirst, candidate.mapSecond).toInt()" in s
    assert "room.secondaryIntAt(candidate.mapFirst, candidate.mapSecond)" in s
    assert "serializedIntPlane" in s


def test_out_of_bounds_candidates_are_preserved_without_plane_reads():
    s = SRC.read_text()
    assert "LegacyRoomSceneCellTrace(candidate, logicalY, null)" in s
    assert "OUT_OF_BOUNDS" in s


def test_scene_trace_keeps_deterministic_order_and_explicit_bounds_status():
    s = SRC.read_text()
    assert "candidates.map { it.canonicalLine() }" in s
    assert "IN_BOUNDS" in s
    assert "boundsStatus" in s
