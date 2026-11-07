"""Build246: classify receiver and argument producer evidence at sprite draw callsites.

Uses javap output from the original JAR. Only syntactically explicit producer
chains are promoted; local-variable receivers and expressions remain unresolved.
"""
import csv,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
jar=ROOT/'original.jar'
text=subprocess.check_output(['javap','-classpath',str(jar),'-c','-p','i'],text=True)
a=text.index('  private void D();'); b=text.find('\n  private ',a+20); method=text[a:b]
ins=[]
for line in method.splitlines():
 m=re.match(r'\s*(\d+):\s+(\w+)(?:\s+(.*?))?(?:\s+//\s+(.*))?$',line)
 if m: ins.append((int(m.group(1)),m.group(2),m.group(3) or '',m.group(4) or '',line.strip()))
rows=[]
for i,(off,op,arg,comment,line) in enumerate(ins):
 if op not in ('invokevirtual','invokespecial','invokestatic','invokeinterface') or 'Method f.a:(Ljavax/microedition/lcdui/Graphics;' not in comment: continue
 desc=comment.split('Method ',1)[-1]
 count=7 if desc.endswith('IIIIIII)V') else 6 if desc.endswith('IIIIII)V') else 0
 if not count: continue
 # Receiver producer: look back a bounded instruction slice for direct array load.
 prior=ins[max(0,i-24):i]
 direct=None
 for j in range(len(prior)-2):
  x=prior[j:j+3]
  if x[0][1]=='getstatic' and 'a:[Lf;' in x[0][3] and x[1][1] in ('bipush','sipush','iconst_0','iconst_1','iconst_2','iconst_3','iconst_4','iconst_5') and x[2][1]=='aaload':
   val=x[1][2]
   try: slot=int(val)
   except: slot={'iconst_0':0,'iconst_1':1,'iconst_2':2,'iconst_3':3,'iconst_4':4,'iconst_5':5}.get(x[1][1])
   if slot is not None: direct=slot
 # Most recent direct array access before call is receiver if no later reference load; record only when exact.
 receiver='UNRESOLVED'
 evidence='NO_EXACT_RECEIVER_PRODUCER'
 if direct is not None:
  receiver=f'f[{direct}]'; evidence='EXPLICIT_GETSTATIC_ARRAY_CONSTANT_AALOAD_IN_LOCAL_SLICE'
 # Capture concise last 18 bytecode instructions as producer slice.
 slice_lines=[x[4] for x in ins[max(0,i-18):i]]
 # Composite group: only label immediate integer expression when receiver explicit and obvious sequence
 # For this audit, preserve raw operand slice rather than interpret arguments.
 rows.append({'method':'i.D()V','bytecode_offset':off,'descriptor':desc,'integer_argument_count':count,
              'receiver_slot':receiver,'receiver_evidence':evidence,
              'argument_producer_slice':' | '.join(slice_lines),
              'composite_group':'UNRESOLVED_RAW_ARGUMENTS_RETAINED',
              'status':'RECEIVER_EXPLICIT' if direct is not None else 'PARTIAL_PROVENANCE'})
out=ROOT/'research/build246_render_argument_provenance.csv'
with out.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={}
for r in rows: summary[r['receiver_slot']]=summary.get(r['receiver_slot'],0)+1
(ROOT/'research/build246_render_argument_provenance_summary.txt').write_text(
 f"sprite_draw_callsites={len(rows)}\n"+''.join(f"{k}={v}\n" for k,v in sorted(summary.items()))+
 "\nComposite group arguments remain unresolved; raw producer slices retained.\n")
print((ROOT/'research/build246_render_argument_provenance_summary.txt').read_text())
