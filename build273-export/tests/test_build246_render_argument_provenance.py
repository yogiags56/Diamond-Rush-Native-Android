import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_build246_retains_all_25_sprite_draw_callsites():
    rows=list(csv.DictReader((ROOT/'research/build246_render_argument_provenance.csv').open()))
    assert len(rows)==25
    assert sum(r['integer_argument_count']=='7' for r in rows)==16
    assert sum(r['integer_argument_count']=='6' for r in rows)==9

def test_build246_explicit_receiver_slots_are_evidence_tagged():
    rows=list(csv.DictReader((ROOT/'research/build246_render_argument_provenance.csv').open()))
    expected={961:'f[27]',1058:'UNRESOLVED',1527:'f[56]',1951:'f[27]',6131:'f[9]',6749:'f[20]',6888:'f[42]',6929:'f[13]'}
    got={int(r['bytecode_offset']):r['receiver_slot'] for r in rows}
    for off,slot in expected.items(): assert got[off]==slot
    for r in rows:
        if r['receiver_slot']!='UNRESOLVED':
            assert r['receiver_evidence']=='EXPLICIT_GETSTATIC_ARRAY_CONSTANT_AALOAD_IN_LOCAL_SLICE'

def test_build246_does_not_promote_unknown_composite_arguments():
    rows=list(csv.DictReader((ROOT/'research/build246_render_argument_provenance.csv').open()))
    assert all(r['composite_group']=='UNRESOLVED_RAW_ARGUMENTS_RETAINED' for r in rows)
