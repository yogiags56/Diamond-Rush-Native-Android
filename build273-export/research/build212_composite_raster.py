#!/usr/bin/env python3
import sys, zipfile, struct, csv, hashlib, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_build210_fields import parse

ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / "original.jar"
OUT = ROOT / "previews"
OUT.mkdir(exist_ok=True)

def palette_argb(raw, fmt):
    out=[]
    if fmt == 21781:
        for (v,) in struct.iter_unpack("<H", raw):
            a=255 if v&0x8000 else 0
            r=((v & 0x7c00) << 9) >> 16
            g=((v & 0x03e0) << 6) >> 8
            b=((v & 0x001f) << 3)
            out.append((r,g,b,a))
    elif fmt == 17476:
        for (v,) in struct.iter_unpack("<H", raw):
            out.append((((v>>8)&15)*17,((v>>4)&15)*17,(v&15)*17,((v>>12)&15)*17))
    elif fmt == -30584:
        for (v,) in struct.iter_unpack("<I", raw):
            out.append(((v>>16)&255,(v>>8)&255,v&255,(v>>24)&255))
    elif fmt == 25861:
        for (v,) in struct.iter_unpack("<H", raw):
            if v == 0xf81f: out.append((0,0,0,0))
            else: out.append((((v>>11)&31)*255//31,((v>>5)&63)*255//63,(v&31)*255//31,255))
    else: raise ValueError(f"palette format {fmt:#x}")
    return out

def decode(payload,w,h,fmt):
    count=w*h; out=[]; p=0
    def nxt():
        nonlocal p
        if p>=len(payload): raise ValueError("truncated")
        b=payload[p];p+=1;return b
    if fmt==5632:
        while len(out)<count:
            b=nxt();out.append(b>>4)
            if len(out)<count:out.append(b&15)
    elif fmt==10225:
        while len(out)<count:
            t=nxt()
            if t>=128:
                run=t-128
                if run<1 or len(out)+run>count: raise ValueError("bad RLE")
                v=nxt();out.extend([v]*run)
            else:out.append(t)
    elif fmt==1024:
        while len(out)<count:
            b=nxt()
            for sh in (6,4,2,0):
                if len(out)<count:out.append((b>>sh)&3)
    else:raise ValueError(f"format {fmt:#x}")
    if p!=len(payload):raise ValueError(f"trailing {len(payload)-p}")
    return out

def resolve(x, root):
    out=[]; active=set()
    def expand(g, ox, oy, flags, gp, cp):
        if g in active: raise ValueError("cycle")
        active.add(g)
        for ci in range(x["g"][g]):
            base=(x["bstarts"][g]+ci)*4
            si,dx,dy,ctrl=x["h"][base:base+4]
            dx=dx if dx<128 else dx-256
            dy=dy if dy<128 else dy-256
            cx=ox-dx if flags&1 else ox+dx
            cy=oy-dy if flags&2 else oy+dy
            drawflags=flags^(ctrl&15)
            if ctrl&16: expand(si,cx,cy,flags,gp+[g],cp+[ci])
            else:
                w,h=x["f"][si*2:si*2+2]
                px=cx-w if flags&1 else cx
                py=cy-h if flags&2 else cy
                out.append((si,px,py,drawflags,gp+[g],cp+[ci]))
        active.remove(g)
    expand(root,0,0,0,[],[])
    return out

def blend(dst, src):
    sr,sg,sb,sa=src
    if sa==0:return dst
    if sa==255:return src
    dr,dg,db,da=dst
    oa=sa+(da*(255-sa)+127)//255
    if oa==0:return (0,0,0,0)
    def ch(s,d): return min(255,(s*sa+(d*da*(255-sa)+127)//255+oa//2)//oa)
    return (ch(sr,dr),ch(sg,dg),ch(sb,db),oa)

rows=[];selected=[]
with zipfile.ZipFile(JAR) as z:
    for bundle in z.namelist():
        if not bundle.endswith(".f"):continue
        cont=z.read(bundle); n=cont[0]; base=1+n*8
        for entry in range(n):
            off,ln=struct.unpack_from("<II",cont,1+entry*8)
            b=cont[base+off:base+off+ln]
            if b[:4]!=b"\xdf\x03\x01\x01":continue
            x=parse(b)
            if not x["g"]:continue
            pals=palette_argb(x["pals"][0],x["pf"]) if x["pals"] else []
            sprites=[]
            for i,payload in enumerate(x["payloads"]):
                w,h=x["f"][2*i:2*i+2]
                inds=decode(payload,w,h,x["pixfmt"])
                if max(inds,default=0)>=len(pals):raise ValueError("palette overflow")
                im=Image.new("RGBA",(w,h))
                im.putdata([pals[q] for q in inds])
                sprites.append(im)
            for group in range(len(x["g"])):
                cmds=resolve(x,group)
                if len(cmds)<3 or any(c[3]!=0 for c in cmds):continue
                minx=min(c[1] for c in cmds); miny=min(c[2] for c in cmds)
                maxx=max(c[1]+sprites[c[0]].width for c in cmds)
                maxy=max(c[2]+sprites[c[0]].height for c in cmds)
                w=maxx-minx;h=maxy-miny
                if w<=0 or h<=0 or w>4096 or h>4096:continue
                canvas=Image.new("RGBA",(w,h),(0,0,0,0))
                for si,px,py,flags,gp,cp in cmds:
                    canvas.alpha_composite(sprites[si],(px-minx,py-miny))
                stem=f"{bundle.replace('.','_')}_e{entry}_g{group}"
                path=OUT/f"composite_{stem}.png"
                canvas.save(path)
                rows.append([bundle,entry,group,len(cmds),len(set(c[0] for c in cmds)),w,h,minx,miny,
                             sum(1 for p in canvas.getdata() if p[3]>0),str(path.relative_to(ROOT))])
                selected.append((bundle,entry,group,canvas.copy(),len(cmds)))
with (ROOT/"research/build212_composite_raster_inventory.csv").open("w",newline="") as f:
    wr=csv.writer(f);wr.writerow(["bundle","entry","group","leaf_commands","unique_sprites","width","height","origin_x","origin_y","nontransparent_pixels","preview"]);wr.writerows(rows)
# Make one labelled contact sheet with useful representative outputs.
chosen=[]
for wanted in [("ms.f",1,0),("ui.f",1,0),("ui.f",2,21),("0.f",1,1),("o.f",0,37)]:
    hit=next((q for q in selected if q[:3]==wanted),None)
    if hit:chosen.append(hit)
if chosen:
    cw,ch=320,220
    sheet=Image.new("RGB",(cw*2,ch*math.ceil(len(chosen)/2)),(34,37,42))
    draw=ImageDraw.Draw(sheet);font=ImageFont.load_default()
    for i,(bundle,entry,group,im,ncmd) in enumerate(chosen):
        x=(i%2)*cw;y=(i//2)*ch
        draw.text((x+6,y+5),f"{bundle} entry {entry} group {group} | {ncmd} leaves | {im.width}x{im.height}",font=font,fill=(255,255,255))
        im.thumbnail((cw-16,ch-32),Image.Resampling.NEAREST)
        sheet.paste(im,(x+(cw-im.width)//2,y+24+(ch-30-im.height)//2),im)
    sheet.save(OUT/"build212_composite_contact_sheet.png")
print(f"resources parsed; composites={len(rows)}; selected={len(chosen)}")
for r in rows:
    if (r[0],r[1],r[2]) in [("ms.f",1,0),("ui.f",1,0),("ui.f",2,20),("0.f",1,1),("o.f",0,98)]:
        print("REPRESENTATIVE",r)
