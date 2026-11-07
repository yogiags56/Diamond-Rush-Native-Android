import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows():
    return list(csv.DictReader((ROOT/'research/build245_render_callsite_provenance.csv').open()))
def test_build245_catalog_has_exact_callsite_descriptors():
    r=rows(); assert len(r)==60
    assert all(x['evidence_status']=='EXACT_CALLSITE_DESCRIPTOR_ONLY' for x in r)
def test_build245_sprite_draw_callsite_counts():
    r=rows()
    assert sum(x['family']=='SPRITE_DRAW_7_INT_ARGS' for x in r)==16
    assert sum(x['family']=='SPRITE_DRAW_6_INT_ARGS' for x in r)==9
def test_build245_runtime_receiver_and_group_remain_unresolved():
    assert all(x['receiver_f_array_slot']=='UNRESOLVED_FROM_THIS_CALLSITE_AUDIT' for x in rows())
    assert all(x['composite_group_argument']=='UNRESOLVED_FROM_THIS_CALLSITE_AUDIT' for x in rows())
def test_build245_bytecode_excerpts_present():
    p=ROOT/'research/build245_render_callsite_bytecode_excerpts.txt'
    assert p.exists() and 'f.a:(Ljavax/microedition/lcdui/Graphics;' in p.read_text()
