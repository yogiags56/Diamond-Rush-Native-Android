import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'research'
def rows(name):
    with (R/name).open(newline='') as f:return list(csv.DictReader(f))
def test_all_eight_renderer_callsites_reached_with_descriptor_stack_depth():
    data=rows('build265_callsite_operand_results.csv')
    assert len(data)==8
    assert all(x['reachable']=='True' and x['depth_sufficient']=='True' for x in data)
def test_interpreter_does_not_claim_all_operands_are_concrete():
    data=rows('build265_callsite_operand_results.csv')
    assert sum(x['all_operands_known']=='True' for x in data)==7
    c873=next(x for x in data if x['class']=='c' and x['offset']=='873')
    assert c873['all_operands_known']=='False'
    assert 'UNKNOWN' in c873['operand_values']
def test_supported_opcode_coverage_is_explicit():
    data=rows('build265_unsupported_opcode_audit.csv')
    assert data==[]
def test_symbolic_coordinates_preserve_tile_scale_expression():
    data=rows('build265_callsite_operand_results.csv')
    g=next(x for x in data if x['class']=='g')
    assert 'CONST(24)' in g['operand_values']
    assert 'STATIC.a' in g['operand_values']
def test_operand_state_trace_has_instruction_level_records():
    data=rows('build265_renderer_operand_states.csv')
    assert len(data)>800
    assert any(x['class']=='g' and x['offset']=='80' for x in data)
