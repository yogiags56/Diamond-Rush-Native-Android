import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):
    with (ROOT/'research'/name).open() as f: return list(csv.DictReader(f))
def test_eight_cross_class_renderer_callsites_are_catalogued():
    rows=read('build262_cross_class_callsite_summary.csv')
    assert len(rows)==8
    assert {r['caller_class'] for r in rows}=={'b','c','g'}
def test_descriptor_stack_contract_includes_receiver_and_graphics():
    rows=read('build262_cross_class_callsite_summary.csv')
    for r in rows:
        assert int(r['receiver_plus_argument_slots'])==2+int(r['integer_arguments'])
        assert r['operand_values_decoded']=='False'
def test_instruction_windows_end_at_the_actual_invoke():
    rows=read('build262_cross_class_instruction_windows.csv')
    assert len(rows)==152
    calls=[r for r in rows if r['is_renderer_invoke']=='True']
    assert len(calls)==8
    assert all(r['opcode'] in {'invokevirtual','invokestatic','invokespecial','invokeinterface'} for r in calls)
