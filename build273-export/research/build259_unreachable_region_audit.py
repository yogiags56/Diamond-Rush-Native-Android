from pathlib import Path
import csv, collections
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'research'
def read(n):
 with (R/n).open(newline='') as f:return list(csv.DictReader(f))
def write(n,rows):
 with (R/n).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 blocks=read('build255_renderer_basic_blocks.csv'); edges=read('build255_renderer_cfg_edges.csv'); ins=read('build255_renderer_instructions.csv'); calls=read('build255_callsite_basic_block_map.csv')
 reach={int(x['block_start']) for x in read('build258_block_reachability_audit.csv') if x['reachable_with_exception_edges']=='TRUE'}
 bmap={int(x['block_start']):x for x in blocks}; un=set(bmap)-reach
 adj=collections.defaultdict(set); cross=[]
 for e in edges:
  a,b=int(e['source_block']),int(e['target_block'])
  if a in un and b in un:adj[a].add(b);adj[b].add(a)
  if a in reach and b in un:cross.append((a,b,e['edge_type']))
 comps=[];seen=set()
 for n in sorted(un):
  if n in seen:continue
  q=[n];seen.add(n);c=[]
  while q:
   x=q.pop();c.append(x)
   for y in adj[x]:
    if y not in seen:seen.add(y);q.append(y)
  comps.append(sorted(c))
 comp_rows=[]
 for i,c in enumerate(comps,1):
  comp_rows.append({'component_id':i,'block_count':len(c),'first_block':c[0],'last_block':c[-1],'first_instruction':bmap[c[0]]['first_instruction'],'last_instruction':bmap[c[-1]]['last_instruction'],'contains_renderer_callsites':sum(int(x['block_start']) in c for x in calls),'classification':'UNREACHABLE_FROM_ENTRY_NORMAL_CFG'})
 write('build259_unreachable_components.csv',comp_rows)
 cross_rows=[{'source_block':a,'target_block':b,'edge_type':t} for a,b,t in cross]
 if not cross_rows:cross_rows=[{'source_block':'NONE','target_block':'NONE','edge_type':'NO_REACHABLE_TO_UNREACHABLE_EDGE'}]
 write('build259_cross_region_edges.csv',cross_rows)
 call_rows=[]
 for c in calls:
  b=int(c['block_start']);call_rows.append({'callsite_offset':c['callsite_offset'],'block_start':b,'reachability':'ENTRY_REACHABLE' if b in reach else 'UNREACHABLE_FROM_ENTRY','descriptor':c['descriptor']})
 write('build259_callsite_region_audit.csv',call_rows)
 inst_by_block=collections.defaultdict(list)
 for x in ins:
  o=int(x['offset'])
  for b in blocks:
   if int(b['block_start'])<=o<=int(b['block_end']):inst_by_block[int(b['block_start'])].append(x);break
 # Capture the boundary and first 80 instructions from the detached region.
 selected=[x for x in ins if 6120<=int(x['offset'])<=6330]
 write('build259_region_boundary_instructions.csv',[{'offset':x['offset'],'instruction':x['instruction']} for x in selected])
 summary=[{'metric':'unreachable_component_count','value':len(comps)},{'metric':'unreachable_block_count','value':len(un)},{'metric':'unreachable_instruction_count','value':sum(int(bmap[b]['instruction_count']) for b in un)},{'metric':'reachable_to_unreachable_cfg_edges','value':len(cross)},{'metric':'renderer_callsites_in_unreachable_region','value':sum(x['reachability']=='UNREACHABLE_FROM_ENTRY' for x in call_rows)},{'metric':'renderer_callsites_in_reachable_region','value':sum(x['reachability']=='ENTRY_REACHABLE' for x in call_rows)},{'metric':'detached_region_start','value':min(un)},{'metric':'detached_region_end_block_start','value':max(un)},{'metric':'boundary_return_offset','value':6170}]
 write('build259_summary.csv',summary)
 print('\n'.join(f"{x['metric']}: {x['value']}" for x in summary))
if __name__=='__main__':main()
