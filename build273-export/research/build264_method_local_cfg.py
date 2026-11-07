"""Build264: conservative method-local CFG and renderer-callsite reachability audit.

Uses javap's decoded instruction offsets from the original JAR. It does not
interpret operand values or claim JVM verification; it only establishes normal
control-flow reachability within each caller method.
"""
from pathlib import Path
import subprocess,re,csv,collections
ROOT=Path(__file__).resolve().parents[1]; JAR=ROOT/'original.jar'; OUT=ROOT/'research'
TARGETS={
'b':{'public final void a(javax.microedition.lcdui.Graphics)':{87,113,141}},
'c':{'public final void a(javax.microedition.lcdui.Graphics)':{280,304,382},'private void a(javax.microedition.lcdui.Graphics, byte[], int)':{873}},
'g':{'public static void a(javax.microedition.lcdui.Graphics)':{80}}
}
INS=re.compile(r'^\s*(\d+):\s+([a-z][a-z0-9_]*)(?:\s+(.*))?$')
METHOD_RE=re.compile(r'^\s{2}(.+);$')
BRANCH=re.compile(r'\b(?:if[a-z0-9_]*|goto_w?|jsr_w?)\s+(-?\d+)')
rows=[]; blockrows=[]; edgerows=[]
for cls, method_targets in TARGETS.items():
    txt=subprocess.check_output(['javap','-classpath',str(JAR),'-p','-c',cls],text=True)
    methods={}; method_switch_targets={}; current=None; in_code=False; switch_offset=None
    for line in txt.splitlines():
        if line.strip().endswith(' {};') and '(' not in line:
            current=None; in_code=False; switch_offset=None; continue
        if line.startswith('  ') and '(' in line and ')' in line and line.rstrip().endswith(';') and not line.lstrip().startswith(('Code:','LineNumberTable','LocalVariableTable','StackMapTable')):
            current=line.strip()[:-1]; methods[current]=[]; method_switch_targets[current]=[]; in_code=False; switch_offset=None; continue
        if current is None: continue
        if line.strip()=='Code:': in_code=True; continue
        if not in_code: continue
        m=INS.match(line)
        if m:
            off,op,rest=m.groups(); methods[current].append({'off':int(off),'op':op,'rest':rest or ''})
            if op in ('tableswitch','lookupswitch'): switch_offset=int(off)
            continue
        if switch_offset is not None:
            sm=re.match(r'^\s*(?:-?\d+:\s*)?default:\s*(-?\d+)',line)
            if sm: method_switch_targets[current].append((switch_offset,int(sm.group(1)),'switch_default'))
            else:
                sm=re.match(r'^\s*(-?\d+):\s*(-?\d+)\s*$',line)
                if sm: method_switch_targets[current].append((switch_offset,int(sm.group(2)),'switch_case'))
                elif line.strip() and not line.startswith(' '): switch_offset=None
        # javap next declaration ends prior method implicitly
    # Restrict to methods that contain requested target offsets.
    for meth,ins in methods.items():
        wanted=sorted(set(method_targets.get(meth,set())).intersection(i['off'] for i in ins))
        if not wanted: continue
        byoff={i['off']:i for i in ins}; offs=sorted(byoff); nxt={o:(offs[k+1] if k+1<len(offs) else None) for k,o in enumerate(offs)}
        succ={o:[] for o in offs}
        switch_map=collections.defaultdict(list)
        for src,dst,kind in method_switch_targets[meth]: switch_map[src].append((dst,kind))
        for o,i in byoff.items():
            op=i['op']; rest=i['rest']; targets=[]
            if op in ('tableswitch','lookupswitch'): targets=[d for d,k in switch_map[o]]
            else:
                bm=BRANCH.search(op+' '+rest)
                if bm: targets=[int(bm.group(1))]
            for d in targets:
                if d in byoff and d not in succ[o]: succ[o].append(d); edgerows.append({'class':cls,'method':meth,'source_offset':o,'target_offset':d,'edge_kind':'branch_or_switch'})
            terminal=op in ('return','ireturn','lreturn','freturn','dreturn','areturn','athrow','ret')
            unconditional=op in ('goto','goto_w','jsr','jsr_w','tableswitch','lookupswitch')
            if not terminal and not unconditional and nxt[o] is not None and nxt[o] not in succ[o]:
                succ[o].append(nxt[o]); edgerows.append({'class':cls,'method':meth,'source_offset':o,'target_offset':nxt[o],'edge_kind':'fallthrough'})
        # JVM method entry always begins at first decoded instruction.
        entry=offs[0]; seen={entry}; q=[entry]
        while q:
            u=q.pop(0)
            for v in succ[u]:
                if v not in seen: seen.add(v); q.append(v)
        # Basic blocks from leaders (entry, branch targets, post-branch instructions).
        leaders={entry}
        for o,i in byoff.items():
            leaders.update(succ[o][:])
            if (len(succ[o])!=1 or (succ[o] and succ[o][0] != nxt[o])) and nxt[o] is not None: leaders.add(nxt[o])
        leaders=sorted(leaders); leader_set=set(leaders)
        for ix,start in enumerate(leaders):
            end=leaders[ix+1]-1 if ix+1<len(leaders) else offs[-1]
            members=[o for o in offs if start<=o<=end]
            if members:
                blockrows.append({'class':cls,'method':meth,'block_start':start,'block_end':end,'instruction_count':len(members),'reachable':start in seen})
        for o in wanted:
            rows.append({'class':cls,'method':meth,'callsite_offset':o,'opcode':byoff[o]['op'],'instruction_count':len(ins),'reachable_instruction_count':sum(x in seen for x in offs),'reachable':o in seen,'predecessor_count':sum(o in s for s in succ.values()),'cfg_edge_count':sum(map(len,succ.values()))})
for name,data in [('build264_callsite_reachability.csv',rows),('build264_method_basic_blocks.csv',blockrows),('build264_method_cfg_edges.csv',edgerows)]:
    p=OUT/name
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]) if data else ['empty']); w.writeheader(); w.writerows(data)
print('callsite rows',len(rows),'reachable',sum(r['reachable'] for r in rows))
for r in rows: print(r['class'],r['callsite_offset'],r['reachable'],r['instruction_count'],r['cfg_edge_count'])
print('blocks',len(blockrows),'edges',len(edgerows))
