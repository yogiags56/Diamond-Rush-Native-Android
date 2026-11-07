#!/usr/bin/env python3
"""Field-aligned audit of original f.a(byte[],int), based on Build 201 javap."""
import csv, struct, sys, zipfile
MAGIC=b'\xdf\x03\x01\x01'
PALETTES={-30584:4,17476:2,21781:2,25861:2}
def s16(b,p): return struct.unpack_from('<h',b,p)[0]
def parse(b):
    if b[:4]!=MAGIC: raise ValueError('signature')
    p=6
    def count():
        nonlocal p
        n=s16(b,p); p+=2
        return max(0,n)
    def take(n):
        nonlocal p
        if n<0 or p+n>len(b): raise ValueError(f'truncated at {p}, need {n}, size {len(b)}')
        x=b[p:p+n]; p+=n; return x
    ns=count(); f=take(ns*2)
    nh=count(); h=take(nh*4)
    ng=count(); g=[]; bstarts=[]
    for _ in range(ng):
        g.append(take(1)[0]); take(1); bstarts.append(s16(b,p)); p+=2
    agroups=take(ng*4)
    nc=count(); crec=take(nc*5)
    nb=count(); btable=[]; ashort=[]
    for _ in range(nb):
        btable.append(take(1)[0]); take(1); ashort.append(s16(b,p)); p+=2
    if ns==0:
        return locals() | {'p':p,'pixfmt':0,'payloads':[],'lengths':[],'pixels':b''}
    pf=s16(b,p); p+=2
    npal=take(1)[0]; ncolor=take(1)[0]
    if npal>16: raise ValueError(f'palette count {npal} exceeds fixed 16-slot array')
    pals=[]
    for _ in range(npal):
        if pf in PALETTES: pals.append(take(ncolor*PALETTES[pf]))
        else: pals.append(bytes(ncolor*4)) # original int[] allocated; default switch leaves zeros
    pixfmt=s16(b,p); p+=2
    lengths=[]; offsets=[]; payloads=[]; total=0
    for i in range(ns):
        n=s16(b,p); p+=2
        if n<0: raise ValueError(f'negative sprite payload length {n} at sprite {i}')
        offsets.append(total); lengths.append(n); payloads.append(None)
        p+=n
        if p>len(b): raise ValueError(f'truncated sprite {i} payload at {p-n}, length {n}, size {len(b)}')
        total+=n
    # The original method's first pass computes cumulative offsets by skipping each
    # [length][payload] record; its second pass copies payloads from those positions.
    q=p-total-2*ns
    pixel_chunks=[]
    for n in lengths:
        q+=2; pixel_chunks.append(b[q:q+n]); q+=n
    pixels=b''.join(pixel_chunks)
    payloads=pixel_chunks
    return locals() | {'p':p,'payloads':payloads,'pixels':pixels}
def main(jar,out):
    rows=[]; fails=[]; pixformats={}; total_sprites=0; total_bytes=0
    with zipfile.ZipFile(jar) as z:
      for name in z.namelist():
       if not name.endswith('.f'): continue
       cont=z.read(name); n=cont[0]; base=1+n*8
       for i in range(n):
        off,ln=struct.unpack_from('<II',cont,1+i*8); b=cont[base+off:base+off+ln]
        if b[:4]!=MAGIC: continue
        try:
         x=parse(b); total_sprites+=len(x['payloads']); total_bytes+=len(x['pixels'])
         pixformats[x['pixfmt']]=pixformats.get(x['pixfmt'],0)+len(x['payloads'])
         rows.append([name,i,len(b),len(x['f'])//2,len(x['h'])//4,len(x['g']),len(x['agroups'])//4,
           len(x['crec'])//5,len(x['btable']),len(x['ashort']),x['pf'],x['npal'],x['ncolor'],x['pixfmt'],
           len(x['payloads']),len(x['pixels']),len(b)-x['p'],'ok'])
        except Exception as e: fails.append([name,i,len(b),str(e)])
    with open(out,'w',newline='') as f:
      w=csv.writer(f); w.writerow(['bundle','entry','bytes','sprite_count_f','component_count_h','group_count_g','group_aux_a_bytes','five_record_count_c','byte_table_count_b','short_table_count_a','palette_format','palette_count','colors_per_palette','pixel_format','payload_count','pixel_bytes','trailing_bytes','status']); w.writerows(rows)
    with open(out.replace('.csv','_failures.csv'),'w',newline='') as f:
      w=csv.writer(f); w.writerow(['bundle','entry','bytes','error']); w.writerows(fails)
    print(f'parsed={len(rows)} failed={len(fails)} sprites={total_sprites} pixel_bytes={total_bytes} formats={pixformats}')
    for x in fails[:12]: print('FAIL',*x)
if __name__=='__main__': main(sys.argv[1],sys.argv[2])
