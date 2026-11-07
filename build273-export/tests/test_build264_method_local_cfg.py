import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'research'
def read(name):
    with (R/name).open(newline='') as f: return list(csv.DictReader(f))
def test_all_eight_cross_class_renderer_sites_are_present_and_reachable():
    rows=read('build264_callsite_reachability.csv')
    assert len(rows)==8
    assert all(r['reachable']=='True' for r in rows)
def test_expected_callsite_offsets_are_preserved():
    rows=read('build264_callsite_reachability.csv')
    assert {(r['class'],int(r['callsite_offset'])) for r in rows}=={
        ('b',87),('b',113),('b',141),('c',280),('c',304),('c',382),('c',873),('g',80)}
def test_cfg_edges_point_to_decoded_instructions():
    blocks=read('build264_method_basic_blocks.csv')
    edges=read('build264_method_cfg_edges.csv')
    starts={(r['class'],r['method'],int(r['block_start'])) for r in blocks}
    # Edges are instruction-level; validate each endpoint is covered by a block interval.
    for e in edges:
        src=int(e['source_offset']); dst=int(e['target_offset'])
        same=[r for r in blocks if r['class']==e['class'] and r['method']==e['method']]
        assert any(int(r['block_start'])<=src<=int(r['block_end']) for r in same)
        assert any(int(r['block_start'])<=dst<=int(r['block_end']) for r in same)
def test_method_cfg_outputs_are_nonempty():
    assert len(read('build264_method_basic_blocks.csv'))>0
    assert len(read('build264_method_cfg_edges.csv'))>0
def test_g_renderer_site_is_reachable_through_both_conditional_paths():
    edges=read('build264_method_cfg_edges.csv')
    g=[e for e in edges if e['class']=='g' and e['method']=='public static void a(javax.microedition.lcdui.Graphics)']
    assert any(e['source_offset']=='24' and e['target_offset']=='42' for e in g)
    assert any(e['source_offset']=='50' and e['target_offset']=='83' for e in g)
