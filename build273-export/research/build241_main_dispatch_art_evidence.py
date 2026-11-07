import csv, zipfile
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
jar=ROOT/'original.jar'
cfg=ROOT/'research/build226_main_dispatch_cfg_attribution.csv'
room_counts=Counter()
with zipfile.ZipFile(jar) as z:
    for name in ('w0.bin','w1.bin','w2.bin'):
        b=z.read(name); count=b[1]; p=2
        for _ in range(count):
            w=int.from_bytes(b[p:p+2],'little'); h=int.from_bytes(b[p+2:p+4],'little'); p+=4
            n=w*h
            primary=b[p:p+n]; packed=b[p+2*n:p+3*n]
            for v in packed: room_counts[('BJ',v)] += 1
            for v in primary: room_counts[('BI',v-256 if v>=128 else v)] += 1
            p += 3*n
rows=[]
with cfg.open(newline='') as f:
    for r in csv.DictReader(f):
        pas='BJ' if r['pass']=='MAIN_PASS_SELECTOR_bJ' else 'BI'
        sel=int(r['raw_case_value'])
        accesses=[int(x) for x in r['direct_f_array_access_offsets'].split(';') if x]
        candidates=[int(x) for x in r['candidate_direct_resource_indices'].split(';') if x]
        rows.append({'pass':pas,'selector':sel,'branch_target':int(r['branch_target_offset']),
          'reachable_instructions':int(r['reachable_instructions_before_shared_tail']),
          'direct_array_access_offsets':';'.join(map(str,accesses)),
          'candidate_resource_indices':';'.join(map(str,candidates)),
          'reachable_render_calls':int(r['reachable_f_render_calls']),
          'original_room_occurrences':room_counts[(pas,sel)],
          'confidence':'CFG_REACHABLE_CANDIDATES_ONLY' if candidates else 'NO_REACHABLE_ART_EVIDENCE',
          'execution_status':'NOT_AN_EXCLUSIVE_BINDING'})
# Preserve signed-byte bypass / skip as explicit domain rows; not table-switch cases.
for sel,label in [(-1,'SKIP_SENTINEL'),(80,'SIGNED_BYTE_BYPASS_BOUNDARY'),(127,'SIGNED_BYTE_BYPASS_UPPER_EDGE')]:
    rows.append({'pass':'BI','selector':sel,'branch_target':'5976' if sel==-1 else '5676',
      'reachable_instructions':'','direct_array_access_offsets':'','candidate_resource_indices':'',
      'reachable_render_calls':'','original_room_occurrences':room_counts[('BI',sel)],
      'confidence':label,'execution_status':'CONTROL_FLOW_ONLY'})
out=ROOT/'research/build241_main_dispatch_art_evidence.csv'
with out.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f'rows={len(rows)} room_selector_occurrences={sum(room_counts.values())} bJ_cases={sum(1 for r in rows if r["pass"]=="BJ")} bI_cases={sum(1 for r in rows if r["pass"]=="BI")}')
print('room bJ values',sum(v for (p,_),v in room_counts.items() if p=='BJ'),'room bI values',sum(v for (p,_),v in room_counts.items() if p=='BI'))
print('candidate-bearing cases',sum(bool(r['candidate_resource_indices']) for r in rows))
