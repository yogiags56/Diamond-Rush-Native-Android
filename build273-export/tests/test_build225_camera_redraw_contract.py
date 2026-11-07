from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMERA = ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyCameraRedrawPlanner.kt"
VIEWPORT = ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyGameplayViewport.kt"
CAMERA_TEXT = CAMERA.read_text()
VIEWPORT_TEXT = VIEWPORT.read_text()

def test_aligned_bounds_preserve_source_remainder_formula():
    assert "cameraX + mapPixelWidth - tile" in CAMERA_TEXT
    assert "cameraY + mapPixelHeight - tile" in CAMERA_TEXT
    assert "rightEdge - rightEdge % tile" in CAMERA_TEXT
    assert "bottomEdge - bottomEdge % tile" in CAMERA_TEXT

def test_initial_redraw_is_full_aligned_region():
    assert "LegacyRedrawAxis.INITIAL" in CAMERA_TEXT
    assert "current.left, current.top, current.right, current.bottom" in CAMERA_TEXT

def test_x_and_y_strips_are_independent():
    assert "LegacyRedrawAxis.X_STRIP" in CAMERA_TEXT
    assert "LegacyRedrawAxis.Y_STRIP" in CAMERA_TEXT
    assert "old.right + LegacyGameplayViewport.TILE_SIZE" in CAMERA_TEXT
    assert "old.bottom + LegacyGameplayViewport.TILE_SIZE" in CAMERA_TEXT

def test_camera_step_matches_bytecode_remainder_chain():
    assert "((smoothingParameterBj * frameCounter) %" in CAMERA_TEXT
    assert "((smoothingParameterBj shr 1) + 1)) % 12" in CAMERA_TEXT
    assert "if (delta > currentOffset) delta = currentOffset" in CAMERA_TEXT

def test_map_coordinate_orientation_matches_original_d_loop():
    assert "val mapFirst = camera.tileX + column" in VIEWPORT_TEXT
    assert "val mapSecond = camera.tileY + row" in VIEWPORT_TEXT
