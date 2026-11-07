import importlib.util
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'research/build252_symbolic_producer_slice.py'
spec=importlib.util.spec_from_file_location('b252',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def test_all_25_callsite_slices_are_emitted():
 rows=list(__import__('csv').DictReader((P.parent/'build252_symbolic_producer_slice.csv').open()))
 assert len(rows)==25
 assert all(r['status']=='PARTIAL_LINEAR_SLICE_NOT_FULL_INVOCATION_PROOF' for r in rows)
def test_symbolic_integer_arithmetic_is_preserved():
 ins=[(0,'bipush','24',''),(2,'iload','7',''),(4,'imul',None,''),(5,'iconst_3',None,''),(6,'iadd',None,'')]
 stack,_,_,_,under,_=m.replay(ins)
 assert under==0 and stack[-1].startswith('IADD(IMUL(')
def test_branch_is_a_barrier_not_guessed_through():
 ins=[(0,'iconst_1',None,''),(1,'ifeq','9',''),(4,'iconst_2',None,'')]
 stack,_,_,bar,_,_=m.replay(ins)
 assert bar and stack==['CONST(2)']
