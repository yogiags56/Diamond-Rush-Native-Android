import importlib.util
from pathlib import Path
import csv

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build267',ROOT/'research/build267_classfile_exception_audit.py')
b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)

def test_original_classfile_parser_finds_four_c_exception_handlers():
    import zipfile
    with zipfile.ZipFile(ROOT/'original.jar') as z:
        parsed=b.parse_class(z.read('c.class'))
    m=next(x for x in parsed['methods'] if x['name']=='a' and x['descriptor']=='(Ljavax/microedition/lcdui/Graphics;[BI)V')
    assert m['code']['code_length'] > 1157
    assert [(x['start_pc'],x['end_pc'],x['handler_pc'],x['catch_type']) for x in m['code']['exception_table']] == [
        (912,936,939,'java/lang/Exception'),
        (945,961,964,'java/lang/Exception'),
        (1105,1129,1132,'java/lang/Exception'),
        (1138,1154,1157,'java/lang/Exception'),
    ]

def test_other_three_selected_methods_have_no_exception_handlers():
    import zipfile
    with zipfile.ZipFile(ROOT/'original.jar') as z:
        expected={
          ('b','(Ljavax/microedition/lcdui/Graphics;)V'),
          ('c','(Ljavax/microedition/lcdui/Graphics;)V'),
          ('g','(Ljavax/microedition/lcdui/Graphics;)V'),
        }
        actual=set()
        for cls in ('b','c','g'):
            p=b.parse_class(z.read(cls+'.class'))
            for m in p['methods']:
                if m['name']=='a' and m['descriptor']=='(Ljavax/microedition/lcdui/Graphics;)V':
                    if not m['code']['exception_table']: actual.add((cls,m['descriptor']))
        assert actual==expected

def test_exception_edges_are_inside_original_protected_ranges():
    b.main()
    with (ROOT/'research/build267_exception_cfg_edges.csv').open() as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==116
    assert all(int(x['protected_start']) <= int(x['source_instruction']) < int(x['protected_end_exclusive']) for x in rows)
    assert {int(x['target_handler']) for x in rows} == {939,964,1132,1157}
