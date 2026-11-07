#!/usr/bin/env python3
"""Rebuild the nested composite graph from the field-aligned Build 210 parser."""
import csv, struct, sys, zipfile
from pathlib import Path
from audit_build210_fields import parse
root=Path(__file__).resolve().parents[1]
jar_path=Path(sys.argv[1]) if len(sys.argv)>1 else root/'original'/'DMR320x240-Celsius.jar'
out_path=Path(sys.argv[2]) if len(sys.argv)>2 else root/'research'/'build210_composite_graph_validation.csv'
rows=[]; total_groups=total_components=total_edges=0; invalid=bad_ranges=cycles=0
with zipfile.ZipFile(jar_path) as jar:
 for name in jar.namelist():
  if not name.endswith('.f'): continue
  cont=jar.read(name); count=cont[0]; base=1+count*8
  for index in range(count):
   off,ln=struct.unpack_from('<II',cont,1+index*8); payload=cont[base+off:base+off+ln]
   if payload[:4]!=b'\xdf\x03\x01\x01': continue
   x=parse(payload); ng=len(x['g']); nc=len(x['h'])//4
   total_groups+=ng; total_components+=nc
   adjacency=[[] for _ in range(ng)]; entry_edges=entry_invalid=entry_bad=entry_cycles=0
   for group,component_count in enumerate(x['g']):
    start=x['bstarts'][group]
    if start<0 or start+component_count>nc:
     entry_bad+=1; bad_ranges+=1
    for local in range(component_count):
     at=(start+local)*4
     if at<0 or at+4>len(x['h']): continue
     rec=x['h'][at:at+4]
     if rec[3]&0x10:
      target=rec[0]; entry_edges+=1; total_edges+=1
      if target>=ng: entry_invalid+=1; invalid+=1
      else: adjacency[group].append(target)
   state=[0]*ng; stack=[]
   def visit(v):
    global cycles
    state[v]=1; stack.append(v)
    for w in adjacency[v]:
     if state[w]==0: visit(w)
     elif state[w]==1:
      entry_cycles_local[0]+=1
    stack.pop();state[v]=2
   entry_cycles_local=[0]
   for v in range(ng):
    if state[v]==0: visit(v)
   entry_cycles=entry_cycles_local[0]; cycles+=entry_cycles
   rows.append([name,index,len(payload),x['sprite_count'] if 'sprite_count' in x else len(x['f'])//2,ng,nc,entry_edges,entry_invalid,entry_bad,entry_cycles])
with open(out_path,'w',newline='') as f:
 w=csv.writer(f);w.writerow(['bundle','entry','payload_bytes','sprite_count','group_count','component_record_count','nested_edges','invalid_nested_targets','bad_group_ranges','cycles']);w.writerows(rows)
print(f'resources={len(rows)} groups={total_groups} components={total_components} nested_edges={total_edges} invalid_targets={invalid} bad_ranges={bad_ranges} cycles={cycles}')
