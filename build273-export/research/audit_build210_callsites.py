#!/usr/bin/env python3
import csv, io, struct, sys, zipfile
from pathlib import Path
from audit_build210_fields import parse
root=Path(__file__).resolve().parents[1]
jar_path=Path(sys.argv[1]) if len(sys.argv)>1 else root/'original'/'DMR320x240-Celsius.jar'
prior_path=Path(sys.argv[2]) if len(sys.argv)>2 else root/'previous_build207.zip'
out_path=Path(sys.argv[3]) if len(sys.argv)>3 else root/'research'/'build210_callsite_parse_audit.csv'
with zipfile.ZipFile(prior_path) as prior:
 b201=zipfile.ZipFile(io.BytesIO(prior.read('previous_build201.zip')))
 callsites=list(csv.DictReader(io.StringIO(b201.read('research/resource_loader_callsites.csv').decode())))
jar=zipfile.ZipFile(jar_path); rows=[]
for row in callsites:
 if row['loader']!='spriteBundle' or not row['index_expression'].isdigit(): continue
 bundle,index=row['bundle'],int(row['index_expression'])
 try:
  container=jar.read(bundle); count=container[0]; base=1+count*8
  off,ln=struct.unpack_from('<II',container,1+index*8); payload=container[base+off:base+off+ln]
  if payload[:4]!=b'\xdf\x03\x01\x01': status,detail='not_df03',payload[:4].hex()
  else:
   x=parse(payload); status='parsed'; detail=f"sprites={len(x['payloads'])};groups={len(x['g'])};components={len(x['h'])//4};pixel={x['pixfmt']}"
 except Exception as exc: status,detail='exception',str(exc)
 rows.append([row['class'],row['method'],bundle,index,row['call_instruction'],status,detail])
with out_path.open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['class','method','bundle','entry','bytecode_callsite','status','detail']);w.writerows(rows)
print(f'call_sites={len(rows)} parsed={sum(r[5]=="parsed" for r in rows)} failures={sum(r[5]=="exception" for r in rows)}')
