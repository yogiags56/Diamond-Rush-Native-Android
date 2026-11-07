from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAVAP = ROOT / "research" / "build214_bytecode" / "i_build214_full.javap.txt"
TEXT = JAVAP.read_text(errors="replace")


def method_slice(start_marker: str, end_marker: str) -> str:
    start = TEXT.index(start_marker)
    end = TEXT.index(end_marker, start)
    return TEXT[start:end]


def test_paint_state_one_dispatches_to_gameplay_d():
    paint = method_slice("public final void paint(javax.microedition.lcdui.Graphics);", "private static java.lang.String a(java.lang.String);")
    assert "1: 2804" in paint
    assert "2804: aload_0" in paint
    assert "Method D:()V" in paint


def test_gameplay_viewport_translation_and_clip():
    gameplay = method_slice("private void D();", "private void E();")
    assert "Graphics.translate:(II)V" in gameplay
    assert "bipush        31" in gameplay
    assert "sipush        320" in gameplay
    assert "sipush        178" in gameplay
    assert "Field cI:I" in gameplay and "Field cJ:I" in gameplay
    assert "Field cK:I" in gameplay and "Field cL:I" in gameplay


def test_camera_uses_24_pixel_tile_units():
    gameplay = method_slice("private void D();", "private void E();")
    assert gameplay.count("bipush        24") >= 8
    assert "Field cK:I" in gameplay and "Field cL:I" in gameplay


def test_visible_grid_bounds_are_ten_by_sixteen_candidates():
    gameplay = method_slice("private void D();", "private void E();")
    assert "bipush        9" in gameplay
    assert "bipush        15" in gameplay
    assert "Field e:I" in gameplay and "Field f:I" in gameplay


def test_map_region_helper_reads_both_map_planes_and_base_tile():
    helper = method_slice("private void a(int, int, int, int, boolean);", "private void C();")
    assert "Field a:[[B" in helper
    assert "Field a:[[I" in helper
    assert "Field b:[[Ljavax/microedition/lcdui/Image;" in helper
    assert "bipush        8" in helper
    assert "Graphics.drawImage" in helper


def test_second_visible_cell_pass_exists_after_first_pass_and_effect_call():
    gameplay = method_slice("private void D();", "private void E();")
    first = gameplay.index("614: iconst_m1")
    second = gameplay.index("6490: istore_3")
    assert first < second
    assert "Method P:()V" in gameplay


def test_normal_gameplay_path_restores_origin_before_hud():
    gameplay = method_slice("private void D();", "private void E();")
    assert "bipush        -31" in gameplay
    assert "Method G:()V" in gameplay


def test_hud_method_uses_resource_zero_and_lower_strip_translation():
    hud = method_slice("private void G();", "private void H();")
    assert "iconst_0" in hud
    assert "sipush        240" in hud
    assert "Graphics.translate:(II)V" in hud
    assert "Graphics.drawImage" in hud
