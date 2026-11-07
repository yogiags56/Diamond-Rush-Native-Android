"""Build267: parse Code exception tables directly from original classfiles.

This is a classfile metadata audit, not a complete JVM verifier. It reports
only exception edges explicitly encoded in each method's Code attribute.
"""
from pathlib import Path
import zipfile, struct, csv, hashlib, json
ROOT=Path(__file__).resolve().parents[1]
JAR=ROOT/'original.jar'; OUT=ROOT/'research'
TARGETS={
 'b': {('a','(Ljavax/microedition/lcdui/Graphics;)V')},
 'c': {('a','(Ljavax/microedition/lcdui/Graphics;)V'),('a','(Ljavax/microedition/lcdui/Graphics;[BI)V')},
 'g': {('a','(Ljavax/microedition/lcdui/Graphics;)V')},
}
class Reader:
 def __init__(self,b): self.b=b; self.p=0
 def u1(self): v=self.b[self.p]; self.p+=1; return v
 def u2(self): v=struct.unpack_from('>H',self.b,self.p)[0]; self.p+=2; return v
 def u4(self): v=struct.unpack_from('>I',self.b,self.p)[0]; self.p+=4; return v
 def take(self,n): v=self.b[self.p:self.p+n]; self.p+=n; return v

def parse_class(data):
 r=Reader(data); magic=r.u4()
 if magic!=0xCAFEBABE: raise ValueError('bad class magic')
 minor,major=r.u2(),r.u2(); count=r.u2(); cp=[None]*count; i=1
 while i<count:
  tag=r.u1()
  if tag==1:
   n=r.u2(); cp[i]=('Utf8',r.take(n).decode('utf-8','replace'))
  elif tag in (3,4): cp[i]=(tag,r.take(4))
  elif tag in (5,6): cp[i]=(tag,r.take(8)); i+=1
  elif tag in (7,8,16,19,20): cp[i]=(tag,r.u2())
  elif tag in (9,10,11,12,17,18): cp[i]=(tag,r.u2(),r.u2())
  elif tag==15: cp[i]=(tag,r.u1(),r.u2())
  else: raise ValueError(f'unknown constant pool tag {tag}')
  i+=1
 def utf(idx):
  x=cp[idx]
  return x[1] if x and x[0]=='Utf8' else ''
 r.u2(); r.u2(); r.u2() # access, this, super
 for _ in range(r.u2()): r.u2()
 def skip_attrs():
  for _ in range(r.u2()):
   r.u2(); n=r.u4(); r.take(n)
 for _ in range(r.u2()):
  r.u2(); r.u2(); r.u2(); skip_attrs()
 methods=[]
 for _ in range(r.u2()):
  access=r.u2(); name=utf(r.u2()); desc=utf(r.u2()); attrs=[]
  for _ in range(r.u2()):
   aname=utf(r.u2()); length=r.u4(); payload=r.take(length)
   if aname=='Code':
    cr=Reader(payload); max_stack=cr.u2(); max_locals=cr.u2(); code_len=cr.u4(); code=cr.take(code_len)
    ex=[]
    for _ in range(cr.u2()):
     start,end,handler,catch=cr.u2(),cr.u2(),cr.u2(),cr.u2()
     catch_name=''
     if catch:
      cpi=cp[catch]
      catch_name=utf(cpi[1]) if cpi and cpi[0]==7 else ''
     ex.append({'start_pc':start,'end_pc':end,'handler_pc':handler,'catch_type_index':catch,'catch_type':catch_name or ('<any>' if catch==0 else '?')})
    attrs.append({'max_stack':max_stack,'max_locals':max_locals,'code_length':code_len,'exception_table':ex})
  methods.append({'access':access,'name':name,'descriptor':desc,'code':attrs[0] if attrs else None})
 return {'major':major,'minor':minor,'methods':methods}

def main():
 rows=[]
 with zipfile.ZipFile(JAR) as z:
  for cls,targets in TARGETS.items():
   c=parse_class(z.read(cls+'.class'))
   for m in c['methods']:
    if (m['name'],m['descriptor']) not in targets: continue
    code=m['code']
    if not code: raise RuntimeError(f'missing Code: {cls}.{m["name"]}{m["descriptor"]}')
    for e in code['exception_table']:
     rows.append({'class':cls,'method':m['name'],'descriptor':m['descriptor'],**e})
    if not code['exception_table']:
     rows.append({'class':cls,'method':m['name'],'descriptor':m['descriptor'],'start_pc':'','end_pc':'','handler_pc':'','catch_type_index':'','catch_type':'<none>'})
 with (OUT/'build267_exception_table.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['class','method','descriptor','start_pc','end_pc','handler_pc','catch_type_index','catch_type']);w.writeheader();w.writerows(rows)
 # Expand protected ranges to conservative instruction-level exception edges.
 # Instruction-level edges avoid relying on Build264's normal-flow CFG, which
 # did not designate all handler offsets as leaders.
 import subprocess, re
 signatures={
  ('b','(Ljavax/microedition/lcdui/Graphics;)V'):'public final void a(javax.microedition.lcdui.Graphics)',
  ('c','(Ljavax/microedition/lcdui/Graphics;[BI)V'):'private void a(javax.microedition.lcdui.Graphics, byte[], int)',
  ('c','(Ljavax/microedition/lcdui/Graphics;)V'):'public final void a(javax.microedition.lcdui.Graphics)',
  ('g','(Ljavax/microedition/lcdui/Graphics;)V'):'public static void a(javax.microedition.lcdui.Graphics)',
 }
 offsets_by_method={}
 for (cls,desc),sig in signatures.items():
  txt=subprocess.check_output(['javap','-classpath',str(JAR),'-p','-c','-s',cls],text=True)
  lines=txt.splitlines(); start=next(i for i,l in enumerate(lines) if l.strip()==sig+';')
  found=[]
  for line in lines[start+1:]:
   m=re.match(r'^\s*(\d+):\s+',line)
   if m: found.append(int(m.group(1)))
   elif found and line.strip().startswith('descriptor:'): continue
   elif found and line.strip() and not line.startswith(' '): break
  offsets_by_method[(cls,desc)]=found
 edges=[]
 for row in rows:
  if row['catch_type']=='<none>': continue
  cls=row['class']; desc=row['descriptor']; lo=int(row['start_pc']); hi=int(row['end_pc']); handler=int(row['handler_pc'])
  protected=[o for o in offsets_by_method[(cls,desc)] if lo<=o<hi]
  for off in protected:
   edges.append({'class':cls,'method':signatures[(cls,desc)],'source_instruction':off,'target_handler':handler,'protected_start':lo,'protected_end_exclusive':hi,'catch_type':row['catch_type'],'edge_kind':'exception_conservative'})
 with (OUT/'build267_exception_cfg_edges.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['class','method','source_instruction','target_handler','protected_start','protected_end_exclusive','catch_type','edge_kind']);w.writeheader();w.writerows(edges)
 summary={'target_methods':sum(len(v) for v in TARGETS.values()),'exception_table_entries':sum(1 for x in rows if x['catch_type']!='<none>'),'methods_without_handlers':sum(1 for x in rows if x['catch_type']=='<none>'),'exception_cfg_edges_emitted':len(edges),'handler_offsets':sorted({int(x['handler_pc']) for x in rows if x['catch_type']!='<none>'}),'note':'Instruction-level conservative exception edges are emitted from every instruction offset within each protected Code range. These are potential edges, not proof that every instruction throws.'}
 (OUT/'build267_exception_audit_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
