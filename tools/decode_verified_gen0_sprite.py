#!/usr/bin/env python3
"""Decode the verified gen0_section_04 image payload into PNG frames.

This is deliberately resource-specific. It validates the exact observed
metadata and payload geometry rather than guessing a universal .f schema.
"""
from pathlib import Path
import argparse, json, struct
from PIL import Image

def u16(data, pos, signed=False):
    if pos < 0 or pos + 2 > len(data): raise ValueError("truncated u16")
    return int.from_bytes(data[pos:pos+2], "little", signed=signed)

def decode(data):
    pos=6
    n0=u16(data,pos,True); pos+=2
    if n0 != 8: raise ValueError("expected eight image entries")
    dimensions=[(u16(data,pos+i*2),u16(data,pos+i*2+1)) for i in []] # dimensions are byte pairs below
    pos+=n0*2
    n1=u16(data,pos,True); pos+=2+n1*4
    n2=u16(data,pos,True); pos+=2+n2*8
    n3=u16(data,pos,True); pos+=2+n3*5
    n4=u16(data,pos,True); pos+=2+n4*4
    fmt=u16(data,pos,True); pos+=2
    groups=data[pos]; colors=data[pos+1]; pos+=2
    if fmt != 21781 or groups != 1 or colors != 16:
        raise ValueError("unexpected palette format/count")
    words=[u16(data,pos+i*2) for i in range(colors)]; pos+=colors*2
    mode=u16(data,pos,True); pos+=2
    if mode != 5632: raise ValueError("expected 4-bit indexed pixel mode")
    deltas=[u16(data,pos+i*2,True) for i in range(n0)]; pos+=n0*2
    if pos != 238: raise ValueError(f"metadata boundary mismatch: {pos}")
    # Verified image dimensions are 24x24, 288 bytes per 4-bit image.
    if len(data)-pos != 8*288:
        raise ValueError("pixel payload length does not match eight 24x24 4-bit frames")
    palette=[]
    for w in words:
        r5=(w>>11)&31; g6=(w>>5)&63; b5=w&31
        palette.append(((r5<<3)|(r5>>2), (g6<<2)|(g6>>4), (b5<<3)|(b5>>2)))
    frames=[]
    for frame in range(8):
        chunk=data[pos+frame*288:pos+(frame+1)*288]
        im=Image.new("RGBA",(24,24))
        for byte_index,b in enumerate(chunk):
            for half,idx in enumerate((b>>4,b&15)):
                pixel=byte_index*2+half
                rgb=palette[idx]
                im.putpixel((pixel%24,pixel//24),(*rgb,0 if idx==0 else 255))
        frames.append(im)
    return frames, {"image_count":8,"width":24,"height":24,"mode":"4-bit indexed",
                    "palette_format":"RGB565","palette_colors":16,
                    "metadata_end":pos,"pixel_bytes":len(data)-pos}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("payload",type=Path)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    frames,meta=decode(a.payload.read_bytes())
    a.out.mkdir(parents=True,exist_ok=True)
    for i,im in enumerate(frames): im.save(a.out/f"gen0_section_04_frame_{i:02d}.png")
    sheet=Image.new("RGBA",(8*96,120),(35,30,25,255))
    from PIL import ImageDraw
    draw=ImageDraw.Draw(sheet)
    for i,im in enumerate(frames):
        sheet.paste(im.resize((72,72),Image.Resampling.NEAREST),(i*96+12,5),im)
        draw.text((i*96+44,85),str(i),fill="white")
    sheet.save(a.out/"gen0_section_04_contact_sheet.png")
    (a.out/"decode_report.json").write_text(json.dumps(meta,indent=2)+"\n")
    print(json.dumps(meta,indent=2))
if __name__=="__main__": main()
