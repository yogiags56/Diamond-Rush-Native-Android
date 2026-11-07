import csv, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_build241_evidence_rows_never_claim_exclusive_art_binding():
    path=ROOT/'research/build241_main_dispatch_art_evidence.csv'
    with path.open(newline='') as f: rows=list(csv.DictReader(f))
    assert len(rows)==88
    assert all(r['execution_status'] in ('NOT_AN_EXCLUSIVE_BINDING','CONTROL_FLOW_ONLY') for r in rows)
    assert all(r['confidence'] in ('CFG_REACHABLE_CANDIDATES_ONLY','NO_REACHABLE_ART_EVIDENCE','SKIP_SENTINEL','SIGNED_BYTE_BYPASS_BOUNDARY','SIGNED_BYTE_BYPASS_UPPER_EDGE') for r in rows)
    assert any(r['pass']=='BJ' and r['selector']=='6' and r['candidate_resource_indices']=='27;30;56' for r in rows)

def test_build241_room_frequency_is_grounded_in_all_original_room_archives():
    path=ROOT/'research/build241_main_dispatch_art_evidence.csv'
    with path.open(newline='') as f: rows=list(csv.DictReader(f))
    assert sum(int(r['original_room_occurrences']) for r in rows if r['pass']=='BJ') > 0
    assert sum(int(r['original_room_occurrences']) for r in rows if r['pass']=='BI') > 0
    with zipfile.ZipFile(ROOT/'original.jar') as z:
        assert all(name in z.namelist() for name in ('w0.bin','w1.bin','w2.bin'))
