from pathlib import Path
import subprocess,re,csv,collections
ROOT=Path(__file__).resolve().parents[1]; JAR=ROOT/'original.jar'; OUT=ROOT/'research'
INV=OUT/'build261_actual_renderer_invocations.csv'
rows=list(csv.DictReader(INV.open()))
targets=[r for r in rows if r['renderer_family']!='other']
methods=sorted(set((r['caller_class'],r['caller_method']) for r in targets))
ins_re=re.compile(r'^\s*(\d+):\s+([a-z][a-z0-9_]*)\b(.*)$')
branch_re=re.compile(r'\b(?:goto_w|goto|if[a-z_]+)\s+(-?\d+)')
switch_case_re=re.compile(r'^\s*(?:-?\d+|default):\s+(-?\d+)\s*$')
all_instr=[]; block_rows=[]; edge_rows=[]; call_rows=[]
for cls,decl in methods:
    txt=subprocess.check_output(['javap','-classpath',str(JAR),'-p','-c',cls],text=True)
    lines=txt.splitlines(); active=False; current=None; parsed=[]
    for line in lines:
        if line.startswith('  ') and '(' in line and ')' in line and line.rstrip().endswith(';') and not line.strip().startswith(('Code:','LineNumberTable','LocalVariableTable','StackMapTable')):
            active=(line.strip()==decl)
            if active: current=decl
            elif parsed: break
            continue
        if not active: continue
        m=ins_re.match(line)
        if m:
            off,op,rest=m.groups(); parsed.append({'offset':int(off),'op':op,'rest':rest.strip(),'raw':line.strip(),'targets':[]})
        elif parsed and (parsed[-1]['op'] in ('tableswitch','lookupswitch')):
            sm=switch_case_re.match(line)
            if sm: parsed[-1]['targets'].append(int(sm.group(1)))
    if not parsed: continue
    offsets=[x['offset'] for x in parsed]; idx={o:i for i,o in enumerate(offsets)}
    leaders={offsets[0]}
    for i,x in enumerate(parsed):
        m=branch_re.search(x['raw'])
        if m:
            t=int(m.group(1)); x['targets'].append(t)
        if x['targets']: leaders.update(t for t in x['targets'] if t in idx)
        if x['op'] in ('goto','goto_w','tableswitch','lookupswitch') or x['op'].startswith('if') or x['op'] in ('ireturn','lreturn','freturn','dreturn','areturn','return','athrow'):
            if i+1<len(parsed): leaders.add(offsets[i+1])
    leaders=sorted(leaders); blocks=[]
    for bi,start in enumerate(leaders):
        end=leaders[bi+1]-1 if bi+1<len(leaders) else offsets[-1]
        members=[x for x in parsed if start<=x['offset']<=end]
        if members: blocks.append((start,end,members))
    bmap={x[0]:i for i,x in enumerate(blocks)}
    succ=collections.defaultdict(set)
    for i,(st,en,mem) in enumerate(blocks):
        last=mem[-1]; op=last['op']; ts=[t for t in last['targets'] if t in bmap]
        succ[i].update(bmap[t] for t in ts)
        fall=(i+1<len(blocks))
        terminal=op in ('goto','goto_w','tableswitch','lookupswitch','ireturn','lreturn','freturn','dreturn','areturn','return','athrow')
        if fall and not terminal: succ[i].add(i+1)
        for j in sorted(succ[i]): edge_rows.append({'caller_class':cls,'caller_method':decl,'from_block':st,'to_block':blocks[j][0],'edge_kind':'branch' if blocks[j][0] in ts else 'fallthrough'})
    seen={0}; q=[0]
    while q:
        u=q.pop(0)
        for v in succ[u]:
            if v not in seen: seen.add(v); q.append(v)
    for i,(st,en,mem) in enumerate(blocks):
        block_rows.append({'caller_class':cls,'caller_method':decl,'block_start':st,'block_end':en,'instruction_count':len(mem),'reachable_from_entry':i in seen,'successor_count':len(succ[i])})
    for r in targets:
        if r['caller_class']==cls and r['caller_method']==decl:
            off=int(r['bytecode_offset']); b=next((x for x in blocks if x[0]<=off<=x[1]),None)
            call_rows.append({**r,'block_start':b[0] if b else '', 'block_end':b[1] if b else '', 'cfg_reachable':bool(b and bmap[b[0]] in seen),'method_instruction_count':len(parsed),'method_block_count':len(blocks),'reachable_block_count':len(seen)})
for name,data in [('build262_caller_basic_blocks.csv',block_rows),('build262_caller_cfg_edges.csv',edge_rows),('build262_callsite_cfg_status.csv',call_rows)]:
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]) if data else ['empty']);w.writeheader();w.writerows(data)
print('caller methods:',len(methods),'blocks:',len(block_rows),'edges:',len(edge_rows))
print('renderer callsites:',len(call_rows),'CFG reachable:',sum(x['cfg_reachable'] for x in call_rows))
for r in call_rows: print(r['caller_class'],r['caller_method'],r['bytecode_offset'],r['renderer_family'],'reachable=',r['cfg_reachable'],'block=',r['block_start'])
