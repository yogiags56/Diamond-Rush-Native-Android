#!/usr/bin/env python3
import sys, zipfile, struct, csv, hashlib, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_build210_fields import parse

ROOT=Path(__file__).resolve().parents[1]
JAR=ROOT/"original.jar"
OUT=ROOT/"previews"
OUT.mkdir(exist_ok=True)

def palette_argb(raw,fmt):
    out=[]
    if fmt==21781:
        for (v,) in struct.iter_unpack("<H",raw):
            a=255 if v&0x8000 else 0
            out.append((((v&0x7c00)<<9)>>16, (v&0x03e0)>>2, (v&0x001f)<<3, a))
    elif fmt==17476:
        for (v,) in struct.iter_unpack("<H",raw):
            out.append((((v>>8)&15)*17,((v>>4)&15)*17,(v&15)*17,((v>>12)&15)*17))
    elif fmt==-30584:
        for (v,) in struct.iter_unpack("<I",raw):
            out.append(((v>>16)&255,(v>>8)&255,v&255,(v>>24)&255))
    elif fmt==25861:
        for (v,) in struct.iter_unpack("<H",raw):
            out.append((0,0,0,0) if v==0xf81f else (((v&0xf800)>>8),((v&0x07e0)>>3),((v&0x001f)<<3),255))
    else: raise ValueError(f"unsupported palette format {fmt}")
    return out

def decode(payload,w,h,fmt):
    count=w*h;out=[];p=0
    def nxt():
        nonlocal p
        if p>=len(payload):raise ValueError("truncated")
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
                if run<1 or len(out)+run>count:raise ValueError("invalid RLE")
                v=nxt();out.extend([v]*run)
            else:out.append(t)
    elif fmt==1024:
        while len(out)<count:
            b=nxt()
            for sh in (6,4,2,0):
                if len(out)<count:out.append((b>>sh)&3)
    else:raise ValueError(f"unsupported pixel format {fmt}")
    if p!=len(payload):raise ValueError("trailing payload bytes")
    return out

def transform_image(im,flags):
    t=flags&3
    if t==0:return im
    if t==1:return im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    if t==2:return im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if t==3:return im.transpose(Image.Transpose.ROTATE_180)
    raise ValueError(t)

def resolve(x,root):
    dims,recs,counts,starts=x["f"],x["h"],x["g"],x["bstarts"]
    out=[];active=set()
    def expand(g,ox,oy,flags,gpath,cpath):
        if g in active:raise ValueError("cycle")
        active.add(g)
        for ci in range(counts[g]):
            base=(starts[g]+ci)*4
            si,dx,dy,ctrl=recs[base:base+4]
            dx=dx if dx<128 else dx-256
            dy=dy if dy<128 else dy-256
            cx=ox-dx if flags&1 else ox+dx
            cy=oy-dy if flags&2 else oy+dy
            nextflags=flags^(ctrl&15)
            if ctrl&16:
                expand(si,cx,cy,nextflags,gpath+[g],cpath+[ci])
            else:
                w,h=dims[si*2:si*2+2]
                px=cx-w if flags&1 else cx
                py=cy-h if flags&2 else cy
                out.append((si,px,py,flags,nextflags,gpath+[g],cpath+[ci]))
        active.remove(g)
    expand(root,0,0,0,[],[])
    return out

def blend(dst,src):
    sr,sg,sb,sa=src
    if sa==0:return dst
    if sa==255:return src
    dr,dg,db,da=dst
    oa=sa+(da*(255-sa)+127)//255
    if oa==0:return (0,0,0,0)
    def ch(s,d):return min(255,(s*sa+(d*da*(255-sa)+127)//255+oa//2)//oa)
    return (ch(sr,dr),ch(sg,dg),ch(sb,db),oa)

rows=[];multi=[];flag_hist=[0,0,0,0];root_count=0;cmd_count=0
with zipfile.ZipFile(JAR) as z:
    for bundle in z.namelist():
        if not bundle.endswith(".f"):continue
        cont=z.read(bundle);n=cont[0];base=1+n*8
        for entry in range(n):
            off,ln=struct.unpack_from("<II",cont,1+entry*8)
            blob=cont[base+off:base+off+ln]
            if blob[:4]!=b"\xdf\x03\x01\x01":continue
            x=parse(blob)
            if not x["g"]:continue
            pals=[palette_argb(raw,x["pf"]) for raw in x["pals"]]
            if len(pals)>1:multi.append([bundle,entry,len(pals),x["ncolor"],len(x["g"])])
            sprites_by_palette=[]
            for pi,pal in enumerate(pals):
                sprites=[]
                for si,payload in enumerate(x["payloads"]):
                    w,h=x["f"][si*2:si*2+2]
                    indices=decode(payload,w,h,x["pixfmt"])
                    if max(indices,default=0)>=len(pal):raise ValueError("palette index overflow")
                    im=Image.new("RGBA",(w,h));im.putdata([pal[q] for q in indices])
                    sprites.append(im)
                sprites_by_palette.append(sprites)
            for group in range(len(x["g"])):
                cmds=resolve(x,group);root_count+=1;cmd_count+=len(cmds)
                if not cmds:continue
                for c in cmds:flag_hist[c[4]&3]+=1
                # Raster all roots using palette row zero. Alternate palette rows are exported separately below.
                sprites=sprites_by_palette[0]
                minx=min(c[1] for c in cmds);miny=min(c[2] for c in cmds)
                maxx=max(c[1]+sprites[c[0]].width for c in cmds)
                maxy=max(c[2]+sprites[c[0]].height for c in cmds)
                w=maxx-minx;h=maxy-miny
                if w<1 or h<1 or w>4096 or h>4096:continue
                canvas=Image.new("RGBA",(w,h),(0,0,0,0))
                for si,px,py,inc,draw,gp,cp in cmds:
                    im=transform_image(sprites[si],draw)
                    canvas.alpha_composite(im,(px-minx,py-miny))
                stem=f"{bundle.replace('.','_')}_e{entry}_g{group}"
                dest=OUT/f"composite_{stem}.png";canvas.save(dest)
                rows.append([bundle,entry,group,len(cmds),w,h,minx,miny,
                             sum(1 for q in canvas.getdata() if q[3]), 
                             sum(1 for c in cmds if c[4]&3),str(dest.relative_to(ROOT))])
                # Multi-palette representative previews: one composite per palette row for first 3 multi-palette resources.
                if len(pals)>1 and group==0 and len(multi)<=3:
                    for pi in range(1,len(pals)):
                        cv=Image.new("RGBA",(w,h),(0,0,0,0))
                        for si,px,py,inc,draw,gp,cp in cmds:
                            cv.alpha_composite(transform_image(sprites_by_palette[pi][si],draw),(px-minx,py-miny))
                        cv.save(OUT/f"palette_{pi}_{stem}.png")

with (ROOT/"research/build213_composite_inventory.csv").open("w",newline="") as f:
    wr=csv.writer(f);wr.writerow(["bundle","entry","group","leaf_commands","width","height","origin_x","origin_y","nontransparent_pixels","transformed_leaves","preview"]);wr.writerows(rows)
with (ROOT/"research/build213_multi_palette_resources.csv").open("w",newline="") as f:
    wr=csv.writer(f);wr.writerow(["bundle","entry","palette_count","colors_per_palette","group_count"]);wr.writerows(multi)
with (ROOT/"research/build213_transform_histogram.csv").open("w",newline="") as f:
    wr=csv.writer(f);wr.writerow(["midp_transform","meaning","leaf_command_count"]);wr.writerows([
        [0,"TRANS_NONE",flag_hist[0]],[1,"TRANS_MIRROR_ROT180",flag_hist[1]],
        [2,"TRANS_MIRROR",flag_hist[2]],[3,"TRANS_ROT180",flag_hist[3]]])
print(f"roots={root_count}; rasterized={len(rows)}; leaf_commands={cmd_count}; transform_hist={flag_hist}; multi_palette_resources={len(multi)}")
for r in rows:
    if (r[0],r[1],r[2]) in [("ms.f",1,0),("ui.f",1,0),("ui.f",2,21),("0.f",1,1),("o.f",0,37)]:
        print("REP",r)
