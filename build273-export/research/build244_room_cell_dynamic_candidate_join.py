from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'research/build240_w0_room0_camera0_manifest.csv'
evidence=ROOT/'research/build241_main_dispatch_art_evidence.csv'
components=ROOT/'research/build243_dynamic_composite_component_attribution.csv'
slots=ROOT/'research/build242_build241_candidate_origin_join.csv'
out=ROOT/'research/build244_w0_room0_dynamic_candidate_join.csv'

def read(p):
    with p.open(newline='') as f:return list(csv.DictReader(f))
M=read(manifest); E=read(evidence); C=read(components); S=read(slots)
by_selector={int(r['selector']):r for r in E if r['pass']=='BJ'}
slot_info={int(r['global_f_slot']):r for r in S}
groups={}
for r in C: groups.setdefault(int(r['global_slot']),{}).setdefault(int(r['group_index']),[]).append(r)
rows=[]
for cell in M:
    if cell['bounds']!='IN': continue
    try: selector=int(cell['mapSecond'])
    except (ValueError,TypeError): continue
    ev=by_selector.get(selector)
    if not ev or not ev['candidate_resource_indices']: continue
    for slot_text in ev['candidate_resource_indices'].split(';'):
        slot=int(slot_text); si=slot_info.get(slot)
        if not si: continue
        for gi, leaves in sorted(groups.get(slot,{}).items()):
            rows.append({
              'row':cell['row'],'column':cell['column'],'screen_x':cell['screenX'],'screen_y':cell['logicalCanvasY'],
              'map_selector_bj':selector,'branch_target':ev['branch_target'],'global_f_slot_candidate':slot,
              'resource_path':si['bundle'],'record_index':si['record_index'],'payload_length':si['payload_length'],
              'composite_group_candidate':gi,'component_count':len(leaves),
              'sprite_indices':';'.join(x['sprite_or_nested_group_index'] for x in leaves),
              'dispatch_evidence':ev['confidence'],'resource_origin_evidence':si['status'],
              'join_status':'CANDIDATE_ONLY_NO_RUNTIME_SELECTION_PROOF'})
fields=list(rows[0]) if rows else ['row','column','screen_x','screen_y','map_selector_bj','branch_target','global_f_slot_candidate','resource_path','record_index','payload_length','composite_group_candidate','component_count','sprite_indices','dispatch_evidence','resource_origin_evidence','join_status']
with out.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
print(f'IN_BOUNDS_CELLS={sum(r["bounds"]=="IN" for r in M)}')
print(f'CELLS_WITH_DYNAMIC_CANDIDATES={len({(r["row"],r["column"]) for r in rows})}')
print(f'CELL_SLOT_GROUP_CANDIDATE_ROWS={len(rows)}')
print('STATUS=CANDIDATE_ONLY_NO_RUNTIME_SELECTION_PROOF')
