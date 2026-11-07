import importlib.util
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'research/build251_descriptor_stack_contracts.py'
s=importlib.util.spec_from_file_location('b251',P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def test_seven_int_overload_stack_contract():
    consumed,produced,args,ret=m.stack_contract('(Ljavax/microedition/lcdui/Graphics;IIIIIII)V')
    assert (consumed,produced,len(args),ret)==(9,0,8,'V')
def test_six_int_overload_stack_contract():
    consumed,produced,args,ret=m.stack_contract('(Ljavax/microedition/lcdui/Graphics;IIIIII)V')
    assert (consumed,produced,len(args),ret)==(8,0,7,'V')
def test_category_two_slot_counting():
    assert m.stack_contract('(JD)V')[0]==5
