import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_build266_callsite_rows_include_local_variable_snapshot():
    rows=list(csv.DictReader((ROOT/'research/build265_callsite_operand_results.csv').open()))
    assert all('local_values' in r for r in rows)
def test_c873_local_0_and_4_remain_unknown_without_guessing():
    rows=list(csv.DictReader((ROOT/'research/build265_callsite_operand_results.csv').open()))
    row=next(r for r in rows if r['class']=='c' and r['offset']=='873')
    locals_={int(x.split('=',1)[0]):x.split('=',1)[1] for x in row['local_values'].split(' | ')}
    assert locals_[0]=='UNKNOWN' and locals_[4]=='UNKNOWN'
def test_c873_other_key_locals_have_symbolic_producers():
    rows=list(csv.DictReader((ROOT/'research/build265_callsite_operand_results.csv').open()))
    row=next(r for r in rows if r['class']=='c' and r['offset']=='873')
    locals_={int(x.split('=',1)[0]):x.split('=',1)[1] for x in row['local_values'].split(' | ')}
    assert locals_[2].startswith('i2s(CALL[i.a]')
    assert locals_[5].startswith('i2s(CALL[i.a]')
def test_renderer_stack_arguments_remain_unmodified_by_local_audit():
    rows=list(csv.DictReader((ROOT/'research/build265_callsite_operand_results.csv').open()))
    row=next(r for r in rows if r['class']=='c' and r['offset']=='873')
    assert row['reachable']=='True' and row['depth_sufficient']=='True'
    assert row['all_operands_known']=='False'
def test_only_eight_target_callsite_records_are_retained():
    rows=list(csv.DictReader((ROOT/'research/build265_callsite_operand_results.csv').open()))
    assert len(rows)==8
