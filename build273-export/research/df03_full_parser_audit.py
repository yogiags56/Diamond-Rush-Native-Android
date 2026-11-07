#!/usr/bin/env python3
"""Bytecode-aligned inventory of complete DF03 01 01 resources."""
import csv, struct, sys, zipfile
MAGIC=b'\xdf\x03\x01\x01'
def s16(b,p): return struct.unpack_from('<h',b,p)[0]
def u16(b,p): return struct.unpack_from('<H',b,p)[0]
def parse(b):
    if b[:4]!=MAGIC: raise ValueError('signature')
    p=6
    def count(label):
        nonlocal p
        n=s16(b,p); p+=2
        return max(0, n)  # Original bytecode enters the table branch only when count > 0.
    def take(n):
        nonlocal p
        if n<0 or p+n>len(b): raise ValueError(f'truncated at {p}, need {n}, size {len(b)}')
        x=b[p:p+n]; p+=n; return x
    # Direct transcription of f.a(byte[], int), offsets 21..480.
    sprite_count=count('sprite')
    sprite_dimensions=take(sprite_count*2)
    # f.a([B,I)V: field h is allocated as count << 2 (four bytes per record).
    table2_count=count('four-byte table')
    four_byte_table=take(table2_count*4)
    # The next count controls three structures:
    # g[B] + b[S] (four bytes consumed per row), then a[B] allocated as count << 2.
    table3_count=count('byte-short table')
    metadata=[]
    for _ in range(table3_count):
        first=take(1)[0]
        skipped=take(1)[0]  # bytecode advances over this byte without storing it
        short=s16(b,p); p+=2
        metadata.append((first,skipped,short))
    paired_byte_table=take(table3_count*4)
    five_count=count('five-byte table')
    five_records=take(five_count*5)
    three_count=count('byte/short table')
    three_records=[]
    for _ in range(three_count):
        first=take(1)[0]; skipped=take(1)[0]
        short=s16(b,p); p+=2
        three_records.append((first,skipped,short))
    if sprite_count == 0:
        return dict(sprite_count=sprite_count,dims=sprite_dimensions,four_byte_table=four_byte_table,
                    metadata=metadata,paired_byte_table=paired_byte_table,five=five_records,three=three_records,
                    palfmt=0,palettes=[],pixfmt=0,lengths=[],offsets=[],payloads=[],
                    trailing=b[p:],consumed=p)
    palette_format=s16(b,p); p+=2
    palette_count=take(1)[0]; color_count=take(1)[0]
    if palette_count>16: raise ValueError(f'palette count {palette_count} exceeds 16')
    if palette_format in (-30584,17476,21781,25861):
        entry=4 if palette_format==-30584 else 2
        palettes=[take(color_count*entry) for _ in range(palette_count)]
    else:
        # The original lookupswitch default branch consumes no palette bytes.
        palettes=[]
    pixel_format=s16(b,p); p+=2
    # Bytecode scans and copies an interleaved [signed-short length][payload] stream.
    lengths=[]; offsets=[]; payloads=[]; total=0
    for i in range(sprite_count):
        n=s16(b,p); p+=2
        if n<0: raise ValueError(f'negative sprite length {n} at sprite {i}')
        offsets.append(total); lengths.append(n); payloads.append(take(n)); total+=n
    return dict(sprite_count=sprite_count,dims=sprite_dimensions,four_byte_table=four_byte_table,
                metadata=metadata,paired_byte_table=paired_byte_table,five=five_records,three=three_records,
                palfmt=palette_format,palettes=palettes,pixfmt=pixel_format,lengths=lengths,
                offsets=offsets,payloads=payloads,trailing=b[p:],consumed=p)


def read_bundle_entries(bundle):
    if not bundle:
        raise ValueError('empty resource bundle')
    count=bundle[0]
    directory_end=1+count*8
    if directory_end>len(bundle):
        raise ValueError('truncated resource directory')
    entries=[]
    for index in range(count):
        off,ln=struct.unpack_from('<II',bundle,1+index*8)
        start=directory_end+off
        end=start+ln
        if end<start or end>len(bundle):
            raise ValueError(f'bundle entry {index} outside resource bundle')
        entries.append((index,off,ln,bundle[start:end]))
    return entries

def main(jar,out):
    rows=[]; failures=[]; formats={}; total_sprites=0; total_payload_bytes=0
    with zipfile.ZipFile(jar) as z:
      for name in z.namelist():
       if not name.endswith('.f'): continue
       cont=z.read(name)
       for i,off,ln,payload in read_bundle_entries(cont):
        if payload[:4]!=MAGIC: continue
        try:
         x=parse(payload); formats[x['pixfmt']]=formats.get(x['pixfmt'],0)+len(x['payloads'])
         total_sprites+=len(x['payloads']); total_payload_bytes+=sum(x['lengths'])
         rows.append([name,i,len(payload),x['sprite_count'],len(x['four_byte_table'])//4,
                      len(x['metadata']),len(x['paired_byte_table'])//4,len(x['five'])//5,
                      len(x['three']),x['palfmt'],len(x['palettes']),
                      len(x['palettes'][0]) if x['palettes'] else 0,x['pixfmt'],
                      sum(x['lengths']),len(x['trailing']),'ok'])
        except Exception as e: failures.append((name,i,str(e)))
    with open(out,'w',newline='') as f:
      w=csv.writer(f); w.writerow(['bundle','entry','bytes','sprite_count','four_byte_table_count',
       'metadata_row_count','paired_four_byte_table_count','five_byte_table_count','byte_short_row_count',
       'palette_format','palettes','colors_per_palette','pixel_format','pixel_bytes','trailing_bytes','status']); w.writerows(rows)
    with open(out.replace('.csv','_failures.csv'),'w',newline='') as f:
      w=csv.writer(f); w.writerow(['bundle','entry','error']); w.writerows(failures)
    print(f'parsed={len(rows)} failed={len(failures)} total_sprites={total_sprites} pixel_bytes={total_payload_bytes} pixel_formats={formats}')
    for e in failures[:20]: print('FAIL',*e)
if __name__=='__main__': main(sys.argv[1],sys.argv[2])
