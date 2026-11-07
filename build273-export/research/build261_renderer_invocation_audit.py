from pathlib import Path
import subprocess,re,csv,collections
ROOT=Path(__file__).resolve().parents[1]; JAR=ROOT/'original.jar'; OUT=ROOT/'research'
CLASSES=['b','c','f','g','i']
PAT=re.compile(r'^\s*(\d+):\s+(invokevirtual|invokespecial|invokestatic|invokeinterface)\s+#(\d+).*// (?:Method|InterfaceMethod) f\.a:(\([^ ]*\).*)$')
METHOD=re.compile(r'^\s{2}(.+);$')
rows=[]
for cls in CLASSES:
    txt=subprocess.check_output(['javap','-classpath',str(JAR),'-p','-c',cls],text=True)
    current='(class initializer / unknown)'
    for line in txt.splitlines():
        if line.startswith('  ') and line.rstrip().endswith(';') and not line.strip().startswith(('Code:','LineNumberTable','LocalVariableTable','StackMapTable')):
            # Method declarations are indented two spaces and have no bytecode offset prefix.
            s=line.strip()
            if not re.match(r'^\d+:',s) and '(' in s and ')' in s:
                current=s
        m=PAT.match(line)
        if m:
            off,op,cp,desc=m.groups()
            rows.append({'caller_class':cls,'caller_method':current,'bytecode_offset':int(off),'invoke_opcode':op,'constant_pool_index':int(cp),'target_class':'f','target_method':'a','target_descriptor':desc,'renderer_family': 'leaf_4int' if desc=='(Ljavax/microedition/lcdui/Graphics;IIII)V' else 'composite_6int' if desc=='(Ljavax/microedition/lcdui/Graphics;IIIIII)V' else 'component_7int' if desc=='(Ljavax/microedition/lcdui/Graphics;IIIIIII)V' else 'other'})
path=OUT/'build261_actual_renderer_invocations.csv'
with path.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for (c,m,d,fam),n in sorted(collections.Counter((r['caller_class'],r['caller_method'],r['target_descriptor'],r['renderer_family']) for r in rows).items()):
 summary.append({'caller_class':c,'caller_method':m,'target_descriptor':d,'renderer_family':fam,'invoke_count':n})
with (OUT/'build261_actual_renderer_invocation_summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
print('actual renderer invokes:',len(rows))
print('by class:',dict(collections.Counter(r['caller_class'] for r in rows)))
print('by descriptor:',dict(collections.Counter(r['target_descriptor'] for r in rows)))
print('distinct caller methods:',len(set((r['caller_class'],r['caller_method']) for r in rows)))
print('output:',path)
