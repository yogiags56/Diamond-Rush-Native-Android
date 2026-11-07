from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyGameplayViewport.kt"
TEXT = SRC.read_text()

def test_canvas_viewport_constants_are_source_backed():
    for token in ("CANVAS_WIDTH = 320", "CANVAS_HEIGHT = 240",
                  "TILE_SIZE = 24", "VIEWPORT_TRANSLATE_Y = 31",
                  "VIEWPORT_WIDTH = 320", "VIEWPORT_HEIGHT = 178"):
        assert token in TEXT

def test_render_switch_domains_remain_separate():
    assert "val bJ: Int, val bI: Int" in TEXT
    assert "BJ_CASE_COUNT = 35" in TEXT
    assert "BI_CASE_COUNT = 50" in TEXT
    assert "enum class" not in TEXT

def test_camera_matches_jvm_integer_division_and_remainder():
    assert "rawX / LegacyGameplayViewport.TILE_SIZE" in TEXT
    assert "rawX % LegacyGameplayViewport.TILE_SIZE" in TEXT
    assert "rawY / LegacyGameplayViewport.TILE_SIZE" in TEXT
    assert "rawY % LegacyGameplayViewport.TILE_SIZE" in TEXT

def test_visible_cell_bounds_are_explicit():
    assert "FIRST_ROW = -1" in TEXT and "LAST_ROW = 8" in TEXT
    assert "FIRST_COLUMN = -1" in TEXT and "LAST_COLUMN = 14" in TEXT
    assert "inBounds = mapFirst in 0 until room.firstDimension" in TEXT

def test_logical_surface_clips_blits():
    assert "class LegacyLogicalSurface" in TEXT
    assert "clip.rightExclusive" in TEXT
    assert "clip.bottomExclusive" in TEXT
