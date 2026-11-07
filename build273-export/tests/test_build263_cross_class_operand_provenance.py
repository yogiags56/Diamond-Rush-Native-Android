import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):
    with (ROOT/'research'/name).open() as f:return list(csv.DictReader(f))
def test_all_eight_cross_class_sites_have_operand_records():
    rows=read('build263_operand_provenance_summary.csv')
    assert len(rows)==8
    assert sum(int(r['operand_slots']) for r in rows)==64
def test_operand_records_match_descriptor_stack_contracts():
    rows=read('build263_operand_provenance_summary.csv')
    for r in rows:
        assert int(r['operand_slots'])==({'component_7int':9,'composite_6int':8,'leaf_4int':6}[r['renderer_family']])
def test_provenance_is_symbolic_not_runtime_evaluation():
    rows=read('build263_cross_class_operand_provenance.csv')
    assert len(rows)==64
    assert all(r['runtime_value_known']=='False' for r in rows)
    assert all(r['evidence_status'] in {'PROVEN','DERIVED','UNKNOWN'} for r in rows)
def test_g_coordinate_formula_is_explicitly_derived():
    rows=read('build263_cross_class_operand_provenance.csv')
    selected=[r for r in rows if r['caller_class']=='g' and r['operand_role'] in {'int_2','int_3'}]
    assert [r['symbolic_expression'] for r in selected]==['local1 * 24','(local2 - 1) * 24 + static b']
