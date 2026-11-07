import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'research'
def rows(n):
 with (R/n).open(newline='') as f:return list(csv.DictReader(f))
def test_one_detached_region_after_return():
 s={x['metric']:int(x['value']) for x in rows('build259_summary.csv')}
 assert s['unreachable_component_count']==1
 assert s['unreachable_block_count']==75
 assert s['unreachable_instruction_count']==926
 assert s['detached_region_start']==6171
 assert s['boundary_return_offset']==6170
 assert s['reachable_to_unreachable_cfg_edges']==0
def test_all_renderer_callsites_partitioned():
 r=rows('build259_callsite_region_audit.csv')
 assert len(r)==25
 assert sum(x['reachability']=='ENTRY_REACHABLE' for x in r)==13
 assert sum(x['reachability']=='UNREACHABLE_FROM_ENTRY' for x in r)==12
def test_cross_edge_audit_explicitly_empty():
 r=rows('build259_cross_region_edges.csv')
 assert len(r)==1 and r[0]['edge_type']=='NO_REACHABLE_TO_UNREACHABLE_EDGE'
def test_boundary_contains_return_then_detached_start():
 r=rows('build259_region_boundary_instructions.csv')
 d={int(x['offset']):x['instruction'] for x in r}
 assert d[6170]=='return'
 assert d[6171]=='aload_0'
 assert 'invokespecial' in d[6172]
