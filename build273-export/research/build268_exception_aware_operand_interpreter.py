"""Build268 exception-aware CFG operand-stack analysis for renderer callers.

This is an abstract interpreter, not a JVM verifier. Values are symbolic strings;
unsupported instructions produce UNKNOWN and are explicitly counted.
"""
from pathlib import Path
import subprocess,re,csv,collections,hashlib
ROOT=Path(__file__).resolve().parents[1]; JAR=ROOT/'original.jar'; OUT=ROOT/'research'
TARGETS={
'b': [('public final void a(javax.microedition.lcdui.Graphics)', {87,113,141})],
'c': [('public final void a(javax.microedition.lcdui.Graphics)', {280,304,382}),('private void a(javax.microedition.lcdui.Graphics, byte[], int)',{873})],
'g': [('public static void a(javax.microedition.lcdui.Graphics)',{80})],
}
INS=re.compile(r'^\s*(\d+):\s+([a-z][a-z0-9_]*)(?:\s+(.*))?$')
BR=re.compile(r'\b(?:if[a-z0-9_]*|goto_w?|jsr_w?)\s+(-?\d+)')

def parse_method(text, signature):
    lines=text.splitlines(); start=next(i for i,l in enumerate(lines) if l.strip()==signature+';')
    desc=None; ins=[]; sw=None; switch={}
    for line in lines[start+1:]:
        if re.match(r'^\s{2}(?:public|private|protected)\s+', line) and line.rstrip().endswith(';') and line.strip()!=signature+';': break
        if line.strip().startswith('descriptor:'): desc=line.split(':',1)[1].strip()
        m=INS.match(line)
        if m:
            off,op,rest=m.groups(); ins.append((int(off),op,rest or ''))
            if op in ('tableswitch','lookupswitch'): sw=int(off); switch[sw]=[]
            continue
        if sw is not None:
            if '}' in line:
                sw=None
                continue
            m=re.match(r'^\s*default:\s*(-?\d+)',line)
            if m: switch[sw].append(int(m.group(1))); continue
            m=re.match(r'^\s*-?\d+:\s*(-?\d+)\s*$',line)
            if m: switch[sw].append(int(m.group(1))); continue
            if line.strip() and not line.startswith(' '): sw=None
    return desc,ins,switch

def slots(desc):
    args=re.search(r'\((.*?)\)',desc).group(1); out=[]; i=0
    while i<len(args):
        c=args[i]
        if c in 'ZBCSI': out.append('I'); i+=1
        elif c in 'JD': out.extend(['J','2']); i+=1
        elif c=='L': j=args.index(';',i); out.append('R'); i=j+1
        elif c=='[':
            i+=1
            while args[i]=='[': i+=1
            if args[i]=='L': i=args.index(';',i)+1
            else: i+=1
            out.append('R')
        else: raise ValueError(desc)
    return out

PHI_VALUES={}
PHI_IDS={}
def merge(a,b):
    if a==b:return a
    if a=='UNKNOWN' or b=='UNKNOWN' or 'UNKNOWN' in str(a) or 'UNKNOWN' in str(b): return 'UNKNOWN'
    def parts(x):
        if x.startswith('PHI#'):
            return set(PHI_VALUES.get(x, (x,)))
        return {x}
    vals=tuple(sorted(parts(a)|parts(b)))
    if len(vals)==1:return vals[0]
    if vals not in PHI_IDS:
        ident=f'PHI#{len(PHI_IDS)+1:03d}'
        PHI_IDS[vals]=ident; PHI_VALUES[ident]=vals
    return PHI_IDS[vals]
def merge_state(a,b):
    if a is None:return b,True
    if len(a[0])!=len(b[0]): return (['STACK_CONFLICT']+['UNKNOWN']*max(len(a[0]),len(b[0])),{}),True
    st=[merge(x,y) for x,y in zip(a[0],b[0])]
    keys=set(a[1])|set(b[1]); loc={k:merge(a[1].get(k,'UNKNOWN'),b[1].get(k,'UNKNOWN')) for k in keys}
    ns=(st,loc); return ns,ns!=a

def transfer(op,rest,stack,locals_,offset):
    s=list(stack); l=dict(locals_); supported=True
    def pop(n=1):
        if len(s)<n: return ['UNKNOWN']*n
        vals=s[-n:]; del s[-n:]; return vals
    def push(v): s.append(v)
    # constants and local loads/stores
    if op.startswith(('iconst_','bipush','sipush')): push('CONST('+ (op[7:] if op.startswith('iconst_') else rest.split()[0])+')')
    elif op=='aconst_null': push('NULL')
    elif op=='ldc' or op=='ldc_w' or op=='ldc2_w': push('CONST('+rest.split('//')[0].strip()+')')
    elif op=='new': push('NEW('+rest.split('//')[-1].strip()+')')
    elif op.startswith('lconst_') or op.startswith('dconst_'): push('UNKNOWN2'); push('2')
    elif op.startswith(('iload','aload','lload','fload','dload')):
        idx=int(op.split('_')[1]) if '_' in op and op.split('_')[1].isdigit() else int(rest.split()[0])
        push(l.get(idx,f'LOCAL{idx}'))
    elif op.startswith(('istore','astore','lstore','fstore','dstore')):
        idx=int(op.split('_')[1]) if '_' in op and op.split('_')[1].isdigit() else int(rest.split()[0]); l[idx]=pop()[0]
    elif op=='iinc':
        p=re.findall(r'-?\d+',rest); idx=int(p[0]); amt=int(p[1]); l[idx]=f'({l.get(idx,f"LOCAL{idx}")}+{amt})'
    elif op in ('getfield','getstatic'):
        fld=re.search(r'Field (.*?):(.*)$',rest)
        ownername=fld.group(1) if fld else 'FIELD'; typ=fld.group(2) if fld else '?'
        if op=='getfield': recv=pop()[0]; expr=f'{recv}.{ownername}'
        else: expr=f'STATIC.{ownername}'
        push(expr)
    elif op in ('putfield','putstatic'): pop(2 if op=='putfield' else 1)
    elif op in ('iaload','baload','caload','saload','aaload','laload','faload','daload'):
        arr,idx=pop(2); push(f'{arr}[{idx}]')
    elif op in ('iastore','bastore','castore','sastore','aastore','lastore','fastore','dastore'): pop(3)
    elif op=='arraylength': push(f'len({pop()[0]})')
    elif op in ('iadd','isub','imul','idiv','irem','iand','ior','ixor','ishl','ishr','iushr','ladd','lsub','land','lor','lxor'):
        b,a=pop(2); sym={'iadd':'+','isub':'-','imul':'*','idiv':'/','irem':'%','iand':'&','ior':'|','ixor':'^','ishl':'<<','ishr':'>>','iushr':'>>>'}.get(op,op); push(f'({a}{sym}{b})')
    elif op in ('ineg','i2b','i2c','i2s','i2l','i2f','i2d','i2s','l2i','f2i','d2i','checkcast','instanceof','newarray','anewarray'):
        v=pop()[0] if op not in ('newarray','anewarray') else pop()[0]
        push(f'{op}({v})')
    elif op in ('dup','dup_x1','dup_x2','swap'):
        if op=='dup' and s: s.append(s[-1])
        elif op=='swap' and len(s)>=2:s[-1],s[-2]=s[-2],s[-1]
        elif op=='dup_x1' and len(s)>=2: v1=s.pop();v2=s.pop();s.extend([v1,v2,v1])
        elif op=='dup_x2' and len(s)>=3: v1=s.pop();v2=s.pop();v3=s.pop();s.extend([v1,v3,v2,v1])
        else: supported=False
    elif op.startswith('invoke'):
        m=re.search(r'Method (.*?):(\(.*)',rest)
        if not m: supported=False
        else:
            target,md=m.groups(); args=slots(md); ret=md.split(')',1)[1]
            vals=pop(len(args)+(0 if op=='invokestatic' else 1));
            if target.startswith('f.a:') and offset in (87,113,141,280,304,382,873,80):
                pass
            if ret!='V': push(f'CALL[{target}]('+','.join(vals)+')')
    elif op.startswith('if_icmp') or op in ('if_acmpeq','if_acmpne'): pop(2)
    elif op.startswith('if') or op in ('tableswitch','lookupswitch'): pop(1)
    elif op in ('goto','goto_w','nop','return','ireturn','areturn','athrow','pop'): 
        if op in ('ireturn','areturn','athrow','pop'):pop()
    elif op in ('pop2',):pop(2)
    elif op in ('lcmp','fcmpl','fcmpg','dcmpl','dcmpg'):pop(2);push('CMP')
    else: supported=False
    if not supported:
        # Preserve stack shape conservatively where possible; values become unknown.
        s=['UNKNOWN']*len(s)
    return s,l,supported

rows=[]; blockrows=[]; unsupported=[]; conflicts=[]; handler_rows=[]
for cls, methods in TARGETS.items():
    txt=subprocess.check_output(['javap','-classpath',str(JAR),'-p','-c','-s',cls],text=True)
    for signature, callsites in methods:
        desc,ins,switches=parse_method(txt,signature)
        if not ins: raise RuntimeError((cls,signature,'no instructions'))
        by={o:(op,r) for o,op,r in ins}; offs=sorted(by); nxt={o:(offs[i+1] if i+1<len(offs) else None) for i,o in enumerate(offs)}
        succ={o:[] for o in offs}
        for o,(op,rest) in by.items():
            dest=[]
            if op in ('tableswitch','lookupswitch'):dest=switches.get(o,[])
            else:
                m=BR.search(op+' '+rest)
                if m:dest=[int(m.group(1))]
            for d in dest:
                if d in by and d not in succ[o]:succ[o].append(d)
            term=op in ('return','ireturn','lreturn','freturn','dreturn','areturn','athrow','ret')
            uncond=op in ('goto','goto_w','tableswitch','lookupswitch')
            if not term and not uncond and nxt[o] is not None and nxt[o] not in succ[o]:succ[o].append(nxt[o])
        # Exact Code exception table parsed from the original classfile by Build267.
        # Handler edges are conservative: every instruction in a protected range may throw.
        handler_specs=[]
        ex_path=OUT/'build267_exception_table.csv'
        if ex_path.exists():
            with ex_path.open() as ef:
                for er in csv.DictReader(ef):
                    if er['class']==cls and er['descriptor']==desc and er['catch_type'] not in ('<none>',''):
                        handler_specs.append((int(er['start_pc']),int(er['end_pc']),int(er['handler_pc']),er['catch_type']))
        # initial locals: receiver if non-static, then descriptor args
        local={}; idx=0
        if not signature.startswith('public static') and not signature.startswith('private static'):
            local[idx]='THIS';idx+=1
        for typ in slots(desc): local[idx]=f'PARAM{idx}';idx+=2 if typ=='J' else 1
        states={offs[0]:([],local)}; q=collections.deque([offs[0]]); visits=collections.Counter(); pre_states={}; unsupported_ops=collections.Counter()
        while q:
            o=q.popleft(); visits[o]+=1
            if visits[o]>30: continue
            op,rest=by[o]; st,loc=states[o]
            if o in callsites: pre_states[o]=(list(st),dict(loc))
            ns,nl,ok=transfer(op,rest,st,loc,o)
            if not ok: unsupported_ops[op]+=1
            for d in succ[o]:
                merged,changed=merge_state(states.get(d), (ns,nl))
                if d not in states or changed: states[d]=merged;q.append(d)
            # Exception transfer preserves locals and replaces operand stack with one exception ref.
            for lo,hi,handler,catch in handler_specs:
                if lo <= o < hi:
                    ex_state=(['EXCEPTION('+catch+')'],dict(loc))
                    merged,changed=merge_state(states.get(handler),ex_state)
                    if handler not in states or changed: states[handler]=merged;q.append(handler)
                    handler_rows.append({'class':cls,'method':signature,'source_instruction':o,'handler':handler,'catch_type':catch,'local_count':len(loc)})
        for o in callsites:
            op,rest=by[o]; snap=pre_states.get(o)
            m=re.search(r'Method (.*?):(\(.*)',rest); target,md=m.groups() if m else ('UNKNOWN','()V')
            need=len(slots(md))+(0 if op=='invokestatic' else 1)
            stack=snap[0] if snap else []
            args=stack[-need:] if len(stack)>=need else []
            rows.append({'class':cls,'method':signature,'offset':o,'invoke':target,'descriptor':md,'reachable':snap is not None,'stack_depth_before':len(stack),'required_slots':need,'depth_sufficient':len(stack)>=need,'operand_values':' | '.join(args) if args else 'UNKNOWN','local_values':' | '.join(f'{k}={v}' for k,v in sorted((snap[1] if snap else {}).items())),'all_operands_known':bool(args) and all(x!='UNKNOWN' and 'UNKNOWN' not in x for x in args),'unsupported_opcode_count':sum(unsupported_ops.values())})
        for o in offs:
            if o in states:
                blockrows.append({'class':cls,'method':signature,'offset':o,'opcode':by[o][0],'stack_depth':len(states[o][0]),'stack':' | '.join(states[o][0]),'local_count':len(states[o][1])})
        for op,n in unsupported_ops.items(): unsupported.append({'class':cls,'method':signature,'opcode':op,'count':n})
        for o in offs:
            if o in states and states[o][0] and states[o][0][0]=='STACK_CONFLICT': conflicts.append({'class':cls,'method':signature,'offset':o,'reason':'stack-depth merge conflict'})

def write(name,data,fields):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
write('build268_renderer_operand_states.csv',blockrows,['class','method','offset','opcode','stack_depth','stack','local_count'])
write('build268_callsite_operand_results.csv',rows,['class','method','offset','invoke','descriptor','reachable','stack_depth_before','required_slots','depth_sufficient','operand_values','local_values','all_operands_known','unsupported_opcode_count'])
write('build268_unsupported_opcode_audit.csv',unsupported,['class','method','opcode','count'])
write('build268_stack_merge_conflicts.csv',conflicts,['class','method','offset','reason'])
write('build268_exception_state_transfers.csv',handler_rows,['class','method','source_instruction','handler','catch_type','local_count'])
phi_rows=[{'phi_id':k,'alternatives':' || '.join(v)} for k,v in sorted(PHI_VALUES.items())]
write('build268_phi_provenance.csv',phi_rows,['phi_id','alternatives'])
print('callsites',len(rows),'reachable',sum(r['reachable'] for r in rows),'depth_sufficient',sum(r['depth_sufficient'] for r in rows),'fully_known',sum(r['all_operands_known'] for r in rows))
print('states',len(blockrows),'unsupported opcode rows',len(unsupported),'merge conflicts',len(conflicts))
for r in rows: print(r['class'],r['offset'],'depth',r['stack_depth_before'],'need',r['required_slots'],'sufficient',r['depth_sufficient'],'args',r['operand_values'])
