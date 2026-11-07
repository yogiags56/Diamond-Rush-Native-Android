from pathlib import Path
import csv,re,subprocess
ROOT=Path(__file__).resolve().parents[1]; JAR=ROOT/'original.jar'; OUT=ROOT/'research'
source=list(csv.DictReader((OUT/'build261_actual_renderer_invocations.csv').open()))
rows=[r for r in source if r['caller_class']!='i' and r['renderer_family']!='other']
ins_re=re.compile(r'^\s*(\d+):\s+([a-z][a-z0-9_]*)\b(.*)$')
window=[]; summary=[]
for r in rows:
    cls=r['caller_class']; decl=r['caller_method']; target=int(r['bytecode_offset'])
    txt=subprocess.check_output(['javap','-classpath',str(JAR),'-p','-c',cls],text=True)
    active=False; parsed=[]
    for line in txt.splitlines():
        if line.startswith('  ') and '(' in line and ')' in line and line.rstrip().endswith(';') and not line.strip().startswith(('Code:','LineNumberTable','LocalVariableTable','StackMapTable')):
            active=(line.strip()==decl)
            if active: continue
            elif parsed: break
        if not active: continue
        m=ins_re.match(line)
        if m:
            off,op,rest=m.groups(); parsed.append((int(off),op,rest.strip()))
    idx=next((i for i,x in enumerate(parsed) if x[0]==target),None)
    if idx is None: raise RuntimeError(f'offset not found {cls} {decl} {target}')
    desc=r['target_descriptor']; ints=desc.count('I'); slots=2+ints
    # Keep an instruction window only. It is not a proven operand stack or value provenance.
    start=max(0,idx-18)
    for j,(off,op,rest) in enumerate(parsed[start:idx+1],start):
        window.append({'caller_class':cls,'caller_method':decl,'callsite_offset':target,'instruction_index_in_window':j-start,'bytecode_offset':off,'opcode':op,'operand_or_comment':rest,'is_renderer_invoke':off==target})
    summary.append({'caller_class':cls,'caller_method':decl,'bytecode_offset':target,'invoke_opcode':r['invoke_opcode'],'renderer_family':r['renderer_family'],'descriptor':desc,'integer_arguments':ints,'receiver_plus_argument_slots':slots,'context_instruction_count':idx-start+1,'operand_values_decoded':False,'cfg_reachability_claimed':False})
for name,data in [('build262_cross_class_callsite_summary.csv',summary),('build262_cross_class_instruction_windows.csv',window)]:
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
print('cross-class renderer callsites:',len(summary))
print('context instructions:',len(window))
for r in summary: print(r['caller_class'],r['bytecode_offset'],r['renderer_family'],'slots=',r['receiver_plus_argument_slots'])
