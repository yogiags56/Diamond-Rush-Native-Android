import csv
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def rows(name):
    with (ROOT/'research'/name).open() as f:
        return list(csv.DictReader(f))


def test_switch_parser_reaches_offset_873_from_case_4():
    spec=importlib.util.spec_from_file_location('build268',ROOT/'research/build268_exception_aware_operand_interpreter.py')
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    import subprocess
    text=subprocess.check_output(['javap','-classpath',str(ROOT/'original.jar'),'-p','-c','-s','c'],text=True)
    sig='private void a(javax.microedition.lcdui.Graphics, byte[], int)'
    _,ins,switches=m.parse_method(text,sig)
    switch_offset=next(o for o,op,_ in ins if op=='lookupswitch')
    assert 729 in switches[switch_offset]
    assert 873 in {o for o,_,_ in ins}


def test_all_eight_renderer_callsites_are_reachable_and_descriptor_sized():
    data=rows('build268_callsite_operand_results.csv')
    assert len(data)==8
    assert all(r['reachable']=='True' for r in data)
    assert all(r['depth_sufficient']=='True' for r in data)
    assert all(int(r['stack_depth_before'])==int(r['required_slots']) for r in data)


def test_two_previously_unknown_operands_are_phi_provenance_not_unknown():
    data=rows('build268_callsite_operand_results.csv')
    r=next(x for x in data if x['class']=='c' and x['offset']=='873')
    args=r['operand_values'].split(' | ')
    assert len(args)==8
    assert args[3].startswith('PHI#')
    assert args[4].startswith('PHI#')
    assert 'UNKNOWN' not in args[3] and 'UNKNOWN' not in args[4]
    phi={x['phi_id']:x['alternatives'] for x in rows('build268_phi_provenance.csv')}
    assert args[3] in phi and args[4] in phi


def test_exception_handler_entry_has_single_exception_reference():
    data=rows('build268_renderer_operand_states.csv')
    handlers={939,964,1132,1157}
    found={int(r['offset']):r for r in data if r['class']=='c' and r['method'].startswith('private') and int(r['offset']) in handlers}
    assert set(found)==handlers
    assert all(r['stack']=='EXCEPTION(java/lang/Exception)' and r['stack_depth']=='1' for r in found.values())


def test_exception_transfers_remain_separate_and_conservative():
    data=rows('build268_exception_state_transfers.csv')
    assert len(data)==69  # only reachable protected instructions propagated by the worklist
    assert {int(r['handler']) for r in data}=={939,964,1132,1157}
    assert all(r['catch_type']=='java/lang/Exception' for r in data)
