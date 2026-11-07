import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_build244_join_has_explicit_nonproof_status():
 p=ROOT/'research/build244_w0_room0_dynamic_candidate_join.csv'
 rows=list(csv.DictReader(p.open()))
 assert rows
 assert all(r['join_status']=='CANDIDATE_ONLY_NO_RUNTIME_SELECTION_PROOF' for r in rows)
def test_build244_candidates_have_origin_and_group_data():
 rows=list(csv.DictReader((ROOT/'research/build244_w0_room0_dynamic_candidate_join.csv').open()))
 assert all(int(r['component_count'])>0 and r['resource_path'].startswith('/') for r in rows)
def test_build244_does_not_promote_candidates_to_draw_operations():
 rows=list(csv.DictReader((ROOT/'research/build244_w0_room0_dynamic_candidate_join.csv').open()))
 assert all('candidate' in r['global_f_slot_candidate'] or r['global_f_slot_candidate'].isdigit() for r in rows)
 assert not any('RASTERIZED' in r['join_status'] for r in rows)
