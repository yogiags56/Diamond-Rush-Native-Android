from pathlib import Path
import csv, struct, collections
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'research'
JAR=ROOT/'original.jar'

def parse_class_method(data, wanted_name='D', wanted_desc='()V'):
    p=8
    def u1():
        nonlocal p; x=data[p]; p+=1; return x
    def u2():
        nonlocal p; x=struct.unpack_from('>H',data,p)[0]; p+=2; return x
    def u4():
        nonlocal p; x=struct.unpack_from('>I',data,p)[0]; p+=4; return x
    count=u2(); cp=[None]*count; i=1
    while i<count:
        tag=u1()
        if tag==1:
            n=u2(); cp[i]=data[p:p+n].decode('utf-8','replace'); p+=n
        elif tag in (3,4): p+=4
        elif tag in (5,6): p+=8; i+=1
        elif tag in (7,8,16,19,20): cp[i]=u2()
        elif tag in (9,10,11,12,17,18): p+=4
        elif tag==15: p+=3
        else: raise ValueError(f'unknown constant-pool tag {tag} at {p}')
        i+=1
    access=u2(); this_class=u2(); super_class=u2()
    for _ in range(u2()): u2()
    for _ in range(u2()):
        u2(); u2(); u2()
        for _ in range(u2()): u2(); p+=u4()
    target=None
    for _ in range(u2()):
        flags=u2(); name=cp[u2()]; desc=cp[u2()]
        attrs=u2()
        for _ in range(attrs):
            attr_name=cp[u2()]; length=u4(); end=p+length
            if name==wanted_name and desc==wanted_desc and attr_name=='Code':
                max_stack=u2(); max_locals=u2(); code_len=u4(); code_start=p
                p+=code_len; n_exc=u2(); entries=[]
                for _ in range(n_exc):
                    start=u2(); stop=u2(); handler=u2(); catch=u2()
                    entries.append((start,stop,handler,cp[catch] if catch else 'ANY'))
                target={'max_stack':max_stack,'max_locals':max_locals,'code_length':code_len,'exception_table':entries}
            p=end
    if target is None: raise LookupError(f'method {wanted_name}{wanted_desc} Code attribute not found')
    return target

def readcsv(name):
    with (R/name).open(newline='') as f:return list(csv.DictReader(f))

def main():
    import zipfile
    with zipfile.ZipFile(JAR) as z: raw=z.read('i.class')
    m=parse_class_method(raw)
    ex=m['exception_table']
    with (R/'build258_exception_table.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['start_pc','end_pc_exclusive','handler_pc','catch_type'])
        w.writerows(ex)
    blocks=readcsv('build255_renderer_basic_blocks.csv')
    edges=readcsv('build255_renderer_cfg_edges.csv')
    calls=readcsv('build255_callsite_basic_block_map.csv')
    starts={int(b['block_start']) for b in blocks}
    byrange=[(int(b['block_start']),int(b['block_end'])) for b in blocks]
    exception_edges=[]
    for start,end,handler,catch in ex:
        if handler not in starts: raise AssertionError(f'handler {handler} not a block start')
        for bs,be in byrange:
            if bs < end and be >= start:
                exception_edges.append((bs,handler,start,end,catch))
    with (R/'build258_exception_cfg_edges.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['source_block','handler_block','protected_start_pc','protected_end_pc_exclusive','catch_type']);w.writerows(exception_edges)
    succ=collections.defaultdict(set)
    for e in edges:succ[int(e['source_block'])].add(int(e['target_block']))
    for a,b,_,_,_ in exception_edges:succ[a].add(b)
    entry=min(starts); seen={entry}; q=collections.deque([entry])
    while q:
        s=q.popleft()
        for t in succ[s]:
            if t not in seen:seen.add(t);q.append(t)
    unreachable=sorted(starts-seen)
    incoming=collections.defaultdict(list)
    for a,ts in succ.items():
        for t in ts:incoming[t].append(a)
    rows=[]
    for b in blocks:
        s=int(b['block_start']); rows.append({'block_start':s,'block_end':b['block_end'],'reachable_with_exception_edges':str(s in seen).upper(),'incoming_cfg_sources':';'.join(map(str,sorted(incoming[s]))),'component_root_candidate':str(s in unreachable and not any(x in unreachable for x in incoming[s])).upper()})
    with (R/'build258_block_reachability_audit.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    call_reach=[]
    for c in calls:
        s=int(c['block_start']);call_reach.append({'callsite_offset':c['callsite_offset'],'block_start':s,'reachable_with_exception_edges':str(s in seen).upper()})
    with (R/'build258_callsite_reachability_delta.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=call_reach[0]);w.writeheader();w.writerows(call_reach)
    summary=[('class_file','i.class'),('method','i.D()V'),('code_length_bytes',m['code_length']),('max_stack',m['max_stack']),('max_locals',m['max_locals']),('exception_table_entries',len(ex)),('exception_cfg_edges',len(exception_edges)),('normal_cfg_blocks',len(starts)),('blocks_reachable_after_exception_edge_audit',len(seen)),('unreachable_blocks_after_exception_edge_audit',len(unreachable)),('renderer_callsites_total',len(calls)),('renderer_callsites_reachable_after_exception_edge_audit',sum(x['reachable_with_exception_edges']=='TRUE' for x in call_reach)),('exception_edges_added',len(exception_edges))]
    with (R/'build258_summary.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['metric','value']);w.writerows(summary)
    print('\n'.join(f'{k}: {v}' for k,v in summary))
    print('unreachable block starts:',unreachable)
if __name__=='__main__':main()
