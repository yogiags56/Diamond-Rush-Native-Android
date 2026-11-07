import csv
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

def transform(im,flags):
    t=flags&3
    if t==0:return im
    if t==1:return im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    if t==2:return im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if t==3:return im.transpose(Image.Transpose.ROTATE_180)
    raise ValueError(t)

def test_midp_transform_constants_have_correct_mapping():
    # 2x2 asymmetric pixels: top-left red, top-right green, bottom-left blue, bottom-right white.
    im=Image.new("RGBA",(2,2))
    im.putdata([(255,0,0,255),(0,255,0,255),(0,0,255,255),(255,255,255,255)])
    assert list(transform(im,0).getdata()) == [
        (255,0,0,255),(0,255,0,255),(0,0,255,255),(255,255,255,255)]
    assert list(transform(im,1).getdata()) == [
        (0,0,255,255),(255,255,255,255),(255,0,0,255),(0,255,0,255)]
    assert list(transform(im,2).getdata()) == [
        (0,255,0,255),(255,0,0,255),(255,255,255,255),(0,0,255,255)]
    assert list(transform(im,3).getdata()) == [
        (255,255,255,255),(0,0,255,255),(0,255,0,255),(255,0,0,255)]

def test_all_original_composite_roots_have_inventory_rows_except_empty_groups():
    rows=list(csv.DictReader((ROOT/"research/build213_composite_inventory.csv").open()))
    assert len(rows)==1125
    assert all(int(r["width"])>0 and int(r["height"])>0 for r in rows)
    assert all(int(r["leaf_commands"])>0 for r in rows)

def test_every_leaf_transform_is_one_of_the_four_original_midp_values():
    rows=list(csv.DictReader((ROOT/"research/build213_transform_histogram.csv").open()))
    assert {r["midp_transform"] for r in rows}=={"0","1","2","3"}
    assert sum(int(r["leaf_command_count"]) for r in rows)==10258

def test_all_multi_palette_resources_are_listed_and_previewed():
    rows=list(csv.DictReader((ROOT/"research/build213_multi_palette_resources.csv").open()))
    assert len(rows)==10
    assert all(int(r["palette_count"])>1 for r in rows)
    assert (ROOT/"previews/palette_1_cm_f_e1_g0.png").is_file()
    assert (ROOT/"previews/palette_1_cm_f_e2_g0.png").is_file()

def test_nested_flag_propagation_regression_is_present():
    source=(ROOT/"android/src/main/kotlin/com/diamondrush/legacy/CompositeSpriteObjectResolver.kt").read_text()
    assert "expand(record.spriteIndex, childX, childY, drawFlags, depth + 1)" in source

def test_kotlin_rasterizer_supports_midp_transforms_and_palette_selector_exists():
    source=(ROOT/"android/src/main/kotlin/com/diamondrush/legacy/CompositeSpriteRasterizer.kt").read_text()
    assert "TRANS_MIRROR_ROT180" in source
    assert "TRANS_MIRROR" in source
    assert "TRANS_ROT180" in source
    assert (ROOT/"android/src/main/kotlin/com/diamondrush/legacy/LegacySpritePaletteSelector.kt").is_file()


def test_kotlin_and_python_composite_rgba_match_for_all_nonempty_groups():
    kotlin_dir = ROOT / "previews/kotlin_rasters"
    kotlin_rows = list(csv.DictReader((kotlin_dir / "build213_kotlin_composite_inventory.csv").open()))
    python_rows = list(csv.DictReader((ROOT / "research/build213_composite_inventory.csv").open()))
    assert len(kotlin_rows) == len(python_rows) == 1125
    pmap = {(r["bundle"], r["entry"], r["group"]): r for r in python_rows}
    for kr in kotlin_rows:
        key = (kr["bundle"], kr["entry"], kr["group"])
        pr = pmap[key]
        stem = f'{key[0].replace(".", "_")}_e{key[1]}_g{key[2]}'
        raw = (kotlin_dir / f"{stem}.rgba").read_bytes()
        with Image.open(ROOT / pr["preview"]) as im:
            assert im.convert("RGBA").tobytes() == raw
        assert (kr["width"], kr["height"], kr["origin_x"], kr["origin_y"], kr["leaf_commands"]) == (
            pr["width"], pr["height"], pr["origin_x"], pr["origin_y"], pr["leaf_commands"]
        )

def test_kotlin_palette_selector_matches_all_five_o_bundle_palette_rows():
    kotlin_dir = ROOT / "previews/kotlin_rasters"
    for palette in range(5):
        stem = f"palette_{palette}_o_f_e0_g0"
        raw = (kotlin_dir / f"{stem}.rgba").read_bytes()
        with Image.open(ROOT / "previews" / f"{stem}.png") as im:
            assert im.convert("RGBA").tobytes() == raw
