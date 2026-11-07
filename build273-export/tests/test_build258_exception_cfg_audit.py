import csv
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('b258',ROOT/'research/build258_exception_cfg_audit.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
def test_original_renderer_method_has_no_exception_handlers():
 import zipfile
 with zipfile.ZipFile(ROOT/'original.jar') as z:m=b.parse_class_method(z.read('i.class'))
 assert m['code_length']==8029
 assert m['max_stack']==9 and m['max_locals']==14
 assert m['exception_table']==[]
def test_exception_audit_reachability_is_unchanged():
 import csv
 rows=list(csv.DictReader((ROOT/'research/build258_summary.csv').open()))
 d={r['metric']:r['value'] for r in rows}
 assert d['exception_table_entries']=='0'
 assert d['exception_cfg_edges']=='0'
 assert d['blocks_reachable_after_exception_edge_audit']=='247'
 assert d['unreachable_blocks_after_exception_edge_audit']=='75'
 assert d['renderer_callsites_reachable_after_exception_edge_audit']=='13'
def test_unreachable_region_begins_after_return():
 ins=list(csv.DictReader((ROOT/'research/build255_renderer_instructions.csv').open()))
 by={int(x['offset']):x['instruction'] for x in ins}
 assert by[6170]=='return'
 assert by[6171]=='aload_0'
