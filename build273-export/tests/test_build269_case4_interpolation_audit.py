import csv
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'research'))
import build269_case4_interpolation_audit as audit

def test_original_bytecode_producer_slice_matches_expected_opcodes():
    got=audit.extract()
    assert len(audit.EXPECTED)==94
    assert all(got[o][0]==op for o,op in audit.EXPECTED.items())

def test_renderer_callsite_consumes_the_two_interpolated_locals():
    got=audit.extract()
    assert got[867][0]=='iload_0'
    assert got[868][0]=='iload'
    assert got[873][0]=='invokevirtual'
    assert 'f.a:' in got[873][1]

def test_case4_formulas_are_explicitly_signed_short_and_not_runtime_constants():
    audit.main()
    rows=list(csv.DictReader((ROOT/'research/build269_case4_operand_formulas.csv').open()))
    assert len(rows)==2
    assert {r['source_local'] for r in rows}=={'local 0','local 4'}
    assert all('S16(' in r['expression'] for r in rows)
    assert all('runtime integer not known' in r['confidence'] for r in rows)

def test_interpolation_clamp_is_minimum_of_instance_field_and_v14():
    got=audit.extract()
    assert got[788][0]=='iload'
    assert got[790][0]=='iload'
    assert got[792][0]=='if_icmple'
    assert got[795][0]=='iload'
    assert got[797][0]=='istore'
