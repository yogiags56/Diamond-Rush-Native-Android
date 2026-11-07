import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(name):
 with (ROOT/'research'/name).open(newline='') as f:return list(csv.DictReader(f))
def test_actual_graphics_renderer_invocations_are_extracted():
 r=[x for x in rows('build261_actual_renderer_invocations.csv') if 'Graphics;' in x['target_descriptor']]
 assert len(r)==111
 assert sum(x['caller_class']!='i' for x in r)==8
 assert {x['caller_class'] for x in r if x['caller_class']!='i'}=={'b','c','g'}
def test_external_invocation_offsets_and_families():
 r=[x for x in rows('build261_actual_renderer_invocations.csv') if x['caller_class']!='i' and 'Graphics;' in x['target_descriptor']]
 got={(x['caller_class'],int(x['bytecode_offset']),x['renderer_family']) for x in r}
 expected={('b',87,'component_7int'),('b',113,'leaf_4int'),('b',141,'composite_6int'),('c',873,'composite_6int'),('c',280,'component_7int'),('c',304,'composite_6int'),('c',382,'composite_6int'),('g',80,'composite_6int')}
 assert got==expected
def test_only_graphics_overloads_are_classified_as_renderers():
 r=rows('build261_actual_renderer_invocations.csv')
 assert all(x['renderer_family']=='other' for x in r if 'Graphics;' not in x['target_descriptor'])
