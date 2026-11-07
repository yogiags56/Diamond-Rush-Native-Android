from pathlib import Path
import zipfile, struct, csv, collections
ROOT=Path(__file__).resolve().parents[1]; JAR=ROOT/'original.jar'; R=ROOT/'research'

def parse(data, class_name):
 p=8
 def u1():
  nonlocal p; x=data[p]; p+=1; return x
 def u2():
  nonlocal p; x=struct.unpack_from('>H',data,p)[0]; p+=2; return x
 def u4():
  nonlocal p; x=struct.unpack_from('>I',data,p)[0]; p+=4; return x
 n=u2(); cp=[None]*n; i=1
 while i<n:
  tag=u1()
  if tag==1:
   l=u2(); cp[i]=data[p:p+l].decode('utf8','replace'); p+=l
  elif tag in (3,4): p+=4
  elif tag in (5,6): p+=8; i+=1
  elif tag in (7,8,16,19,20): cp[i]=(tag,u2())
  elif tag in (9,10,11,12,17,18): cp[i]=(tag,u2(),u2())
  elif tag==15: p+=3
  else: raise ValueError(tag)
  i+=1
 def utf(i):
  x=cp[i]; return x if isinstance(x,str) else ''
 def cls(i):
  x=cp[i]; return utf(x[1]) if x and x[0]==7 else ''
 refs=[]
 for idx,x in enumerate(cp):
  if x and x[0] in (10,11):
   owner=cls(x[1]); nt=cp[x[2]]; refs.append((idx,owner,utf(nt[1]),utf(nt[2])))
 access=u2(); this=u2(); sup=u2()
 for _ in range(u2()):u2()
 for _ in range(u2()):
  u2();u2();u2()
  for _ in range(u2()):u2();p+=u4()
 methods=[]
 for _ in range(u2()):
  flags=u2(); name=utf(u2()); desc=utf(u2()); attrs=u2(); clen=0; exc=0
  for _ in range(attrs):
   an=utf(u2()); ln=u4(); end=p+ln
   if an=='Code':
    u2();u2();clen=u4();p+=clen;exc=u2();p+=8*exc
   p=end
  methods.append((name,desc,clen,exc))
 return methods,refs

def main():
 all_methods=[]; all_refs=[]
 with zipfile.ZipFile(JAR) as z:
  for path in sorted(x for x in z.namelist() if x.endswith('.class')):
   cn=path[:-6]
   ms,rs=parse(z.read(path),cn)
   for n,d,l,e in ms:all_methods.append({'class':cn,'method':n,'descriptor':d,'code_length':l,'exception_handlers':e})
   for idx,o,n,d in rs:all_refs.append({'caller_class':cn,'cp_index':idx,'target_class':o,'target_method':n,'target_descriptor':d})
 with (R/'build260_jar_method_inventory.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(all_methods[0]));w.writeheader();w.writerows(all_methods)
 with (R/'build260_cross_class_method_references.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(all_refs[0]));w.writeheader();w.writerows(all_refs)
 target=[x for x in all_refs if x['target_class']=='i']
 target_f=[x for x in all_refs if x['target_class']=='f' and x['target_method']=='a']
 rows=[]
 for label,items in [('references_to_i',target),('sprite_renderer_f_a_references',target_f)]:
  by=collections.Counter((x['caller_class'],x['target_method'],x['target_descriptor']) for x in items)
  for (caller,m,d),count in sorted(by.items()):rows.append({'category':label,'caller_class':caller,'target_method':m,'target_descriptor':d,'constant_pool_reference_count':count})
 with (R/'build260_renderer_cross_reference_summary.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print('class_files:',len(set(x['class'] for x in all_methods)))
 print('methods:',len(all_methods),'methods_with_code:',sum(x['code_length']>0 for x in all_methods))
 print('method_reference_entries:',len(all_refs))
 print('references_to_i:',len(target),'sprite_renderer_f_a_references:',len(target_f))
 print('caller classes with i refs:',sorted(set(x['caller_class'] for x in target)))
 print('caller classes with f.a refs:',sorted(set(x['caller_class'] for x in target_f)))
if __name__=='__main__':main()
