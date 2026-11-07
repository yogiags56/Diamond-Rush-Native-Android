import importlib.util, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('b260',ROOT/'research/build260_cross_method_reference_audit.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
def test_all_jar_classes_and_methods_parse():
 with zipfile.ZipFile(ROOT/'original.jar') as z:
  classes=[n for n in z.namelist() if n.endswith('.class')]
  assert len(classes)==12
  total=0
  for n in classes:
   methods,refs=b.parse(z.read(n),n[:-6]); assert methods
   total+=len(methods)
  assert total==322
def test_renderer_method_metadata():
 with zipfile.ZipFile(ROOT/'original.jar') as z: methods,_=b.parse(z.read('i.class'),'i')
 d=[x for x in methods if x[0]=='D' and x[1]=='()V']
 assert d==[('D','()V',8029,0)]
def test_sprite_renderer_overloads_referenced_across_classes():
 with zipfile.ZipFile(ROOT/'original.jar') as z:
  refs=[]
  for n in z.namelist():
   if n.endswith('.class'):
    _,r=b.parse(z.read(n),n[:-6]); refs.extend((n[:-6],o,m,d) for _,o,m,d in r)
 assert any(c=='b' and o=='f' and m=='a' and 'Graphics;' in d for c,o,m,d in refs)
 assert any(c=='i' and o=='f' and m=='a' and 'Graphics;' in d for c,o,m,d in refs)
