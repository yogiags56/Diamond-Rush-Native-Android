import unittest, zipfile, struct, os

MAGIC=bytes([0xdf,3,1,1])
def parse(data):
    if len(data)<8 or data[:4]!=MAGIC: raise ValueError("signature")
    p=6
    def count():
        nonlocal p
        if p+2>len(data): raise ValueError("count")
        v=struct.unpack_from("<h",data,p)[0];p+=2;return max(v,0)
    def take(n):
        nonlocal p
        if p+n>len(data): raise ValueError("bounds")
        x=data[p:p+n];p+=n;return x
    dims=take(count()*2); records=take(count()*4); ng=count()
    counts=[];starts=[]
    for _ in range(ng):
        e=take(4);counts.append(e[0]);starts.append(struct.unpack_from("<h",e,2)[0])
    gd=take(ng*2)
    return dims,records,counts,starts

def resolve(section,root,x,y,flags,max_depth=128):
    dims,recs,counts,starts=section
    out=[];active=set()
    def expand(g,ox,oy,depth,gpath,cpath,active_flags):
        if depth>max_depth: raise ValueError("depth")
        if g in active: raise ValueError("cycle")
        active.add(g)
        try:
            for ci in range(counts[g]):
                base=(starts[g]+ci)*4
                if base<0 or base+4>len(recs): raise ValueError("record")
                child=recs[base]; dx=recs[base+1] if recs[base+1]<128 else recs[base+1]-256
                dy=recs[base+2] if recs[base+2]<128 else recs[base+2]-256
                ctrl=recs[base+3]
                cx=ox-dx if active_flags&1 else ox+dx
                cy=oy-dy if active_flags&2 else oy+dy
                drawflags=active_flags^(ctrl&15)
                if ctrl&16:
                    if child>=len(counts): raise ValueError("target")
                    expand(child,cx,cy,depth+1,gpath+[g],cpath+[ci],drawflags)
                else:
                    db=child*2
                    if db+1>=len(dims): raise ValueError("dimension")
                    dx0=dims[db];dy0=dims[db+1]
                    fx=cx-dx0 if active_flags&1 else cx
                    fy=cy-dy0 if active_flags&2 else cy
                    out.append((child,fx,fy,active_flags,drawflags,tuple(gpath+[g]),tuple(cpath+[ci])))
        finally: active.remove(g)
    if root<0 or root>=len(counts): raise ValueError("root")
    expand(root,x,y,1,[],[],flags)
    return out

def all_sections():
    jar=os.path.join(os.path.dirname(__file__),"../original/DMR320x240-Celsius.jar")
    with zipfile.ZipFile(jar) as z:
        for name in z.namelist():
            if not name.endswith(".f"): continue
            d=z.read(name); n=d[0]; base=1+n*8
            for i in range(n):
                off,ln=struct.unpack_from("<II",d,1+i*8); payload=d[base+off:base+off+ln]
                if payload[:4]!=MAGIC: continue
                yield name,i,parse(payload)

class Build207ResolverTests(unittest.TestCase):
    def test_every_group_in_every_df03_payload_expands(self):
        total=0; leaves=0
        for name,index,s in all_sections():
            for group in range(len(s[2])):
                commands=resolve(s,group,100,80,0)
                total+=1; leaves+=len(commands)
        self.assertEqual(total,1129)
        self.assertGreater(leaves,0)
    def test_nested_payloads_expand(self):
        nested=0
        for name,index,s in all_sections():
            for g in range(len(s[2])):
                cmds=resolve(s,g,0,0,0)
                if any(len(c[5])>1 for c in cmds): nested+=1
        self.assertGreater(nested,0)
    def test_flagged_component_position_and_leaf_anchor(self):
        dims=bytes([4,6])
        recs=bytes([0,3,2,0])
        s=(dims,recs,[1],[0])
        self.assertEqual(resolve(s,0,10,20,0)[0][:5],(0,13,22,0,0))
        self.assertEqual(resolve(s,0,10,20,3)[0][:5],(0,3,12,3,3))
    def test_control_xor_kept_separate(self):
        s=(bytes([0,0]),bytes([0,0,0,5]),[1],[0])
        cmd=resolve(s,0,1,2,0x20)[0]
        self.assertEqual(cmd[3],0x20);self.assertEqual(cmd[4],0x25)
    def test_nested_cycle_guard(self):
        s=(bytes([0,0]),bytes([0,0,0,0x10]),[1],[0])
        with self.assertRaises(ValueError): resolve(s,0,0,0,0)
    def test_depth_guard(self):
        # 0 -> 1 -> 2, max depth 2
        s=(bytes([0,0]),bytes([1,0,0,0x10, 2,0,0,0x10, 0,0,0,0]),[1,1,1],[0,1,2])
        with self.assertRaises(ValueError): resolve(s,0,0,0,0,max_depth=2)
    def test_leaf_dimension_bounds_guard(self):
        s=(bytes([0]),bytes([1,0,0,0]),[1],[0])
        with self.assertRaises(ValueError): resolve(s,0,0,0,0)
    def test_empty_group_emits_no_commands(self):
        s=(bytes([0,0]),bytes(),[0],[0])
        self.assertEqual(resolve(s,0,0,0,0),[])
if __name__=="__main__": unittest.main()


def test_nested_group_receives_xor_adjusted_flags():
    # Root group 0 contains nested group 1 and applies transform flag bit 0.
    # Group 1's leaf then uses that incoming flag for its X anchor and draw flags.
    dims = bytes([4, 6])
    records = bytes([
        1, 3, 2, 0x11,  # group 0 -> group 1; low nibble 1
        0, 0, 0, 0      # group 1 -> sprite 0
    ])
    section = (dims, records, [1, 1], [0, 1])
    cmd = resolve(section, 0, 10, 20, 0)[0]
    assert cmd[1] == 9  # nested incoming flag 1 subtracts sprite width from x
    assert cmd[3] == 1
    assert cmd[4] == 1
