"""Build245: enumerate exact renderer callsites and JVM descriptors from original bytecode.

This deliberately does not infer runtime f[] receiver values or composite-group
arguments when the producer-to-call stack chain is not established.
"""
import csv, re, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
JAR=ROOT/'original.jar'
# javap is required so this audit uses the shipped original classfile, not a handwritten map.
import subprocess
text=subprocess.check_output(['javap','-classpath',str(JAR),'-c','-p','i'],text=True)
start=text.index('  private void D();')
end=text.find('\n  private ',start+20)
method=text[start:end]
pattern=re.compile(r"\s*(\d+):\s+(\w+).*?//\s+(.*)$")
rows=[]
for line in method.splitlines():
    m=pattern.match(line)
    if not m: continue
    off,op,comment=m.group(1),m.group(2),m.group(3).strip()
    if not op.startswith('invoke'): continue
    if 'f.a:' not in comment and 'Graphics.' not in comment and 'Image.' not in comment and 'i:(II)Z' not in comment: continue
    if 'f.a:(Ljavax/microedition/lcdui/Graphics;' in comment and comment.endswith('IIIIIII)V'): family='SPRITE_DRAW_7_INT_ARGS'
    elif 'f.a:(Ljavax/microedition/lcdui/Graphics;' in comment and comment.endswith('IIIIII)V'): family='SPRITE_DRAW_6_INT_ARGS'
    elif 'f.a:(I)I' in comment or 'f.a:(II)I' in comment: family='SPRITE_METADATA_ACCESSOR'
    elif 'Graphics.' in comment: family='GRAPHICS_API'
    elif 'Image.' in comment: family='IMAGE_API'
    else: family='HELPER_OR_OTHER'
    rows.append({'method':'i.D()V','bytecode_offset':int(off),'opcode':op,'invocation':comment,'family':family,
                 'descriptor_int_argument_count':comment.count('I') if '(' in comment else '',
                 'receiver_f_array_slot':'UNRESOLVED_FROM_THIS_CALLSITE_AUDIT',
                 'composite_group_argument':'UNRESOLVED_FROM_THIS_CALLSITE_AUDIT',
                 'evidence_status':'EXACT_CALLSITE_DESCRIPTOR_ONLY'})
out=ROOT/'research/build245_render_callsite_provenance.csv'
with out.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Extract nearby original bytecode lines for manual/next-stage stack analysis.
lines=method.splitlines(); offsets={r['bytecode_offset'] for r in rows}
excerpt=[]
for i,line in enumerate(lines):
    m=re.match(r'\s*(\d+):',line)
    if m and int(m.group(1)) in offsets:
        excerpt.extend(lines[max(0,i-7):min(len(lines),i+2)]);excerpt.append('')
(ROOT/'research/build245_render_callsite_bytecode_excerpts.txt').write_text('\n'.join(excerpt))
print(f'callsite_rows={len(rows)} sprite7={sum(r["family"]=="SPRITE_DRAW_7_INT_ARGS" for r in rows)} sprite6={sum(r["family"]=="SPRITE_DRAW_6_INT_ARGS" for r in rows)}')
