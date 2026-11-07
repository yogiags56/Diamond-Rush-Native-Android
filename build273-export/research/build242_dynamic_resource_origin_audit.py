import csv, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / 'original.jar'
# i.j()V tableswitch targets and the resource-slot assignment branch reached by each record.
GEN_SLOT_BY_RECORD = {
    0: (33, 6214, 'record-enabled-by-c-bit'),
    1: (34, 6228, 'record-enabled-by-c-bit'),
    3: (7, 6414, 'record-enabled-by-c-bit'),
    4: (3, 6475, 'record-enabled-by-c-bit; only when aA!=2'),
    5: (58, 6407, 'record-enabled-by-c-bit'),
    6: (21, 6385, 'record-enabled-by-c-bit'),
    7: (20, 6489, 'record-enabled-by-c-bit; aA==2 adds image-state initialization'),
    8: (5, 6428, 'record-enabled-by-c-bit'),
    9: (12, 6555, 'record-enabled-by-c-bit'),
    11: (11, 6676, 'record-enabled-by-c-bit'),
    12: (10, 6688, 'record-enabled-by-c-bit'),
    13: (1, 6670, 'record-enabled-by-c-bit'),
    14: (6, 6522, 'record-enabled-by-c-bit'),
    16: (37, 6242, 'record-enabled-by-c-bit'),
    18: (37, 6242, 'record-enabled-by-c-bit'),
    19: (7, 6683, 'record-enabled-by-c-bit'),
    20: (13, 6470, 'record-enabled-by-c-bit'),
    21: (3, 6475, 'record-enabled-by-c-bit; only when aA!=2'),
    22: (8, 6463, 'record-enabled-by-c-bit'),
    23: (30, 6262, 'record-enabled-by-c-bit'),
    24: (57, 6434, 'record-enabled-by-c-bit; image cache 15 cleared and helper called'),
    25: (17, 6402, 'record-enabled-by-c-bit'),
    27: (19, 6390, 'record-enabled-by-c-bit'),
    28: (45, 6309, 'record-enabled-by-c-bit'),
    29: (26, 6331, 'record-enabled-by-c-bit'),
    30: (15, 6302, 'record-enabled-by-c-bit'),
    31: (29, 6297, 'record-enabled-by-c-bit'),
    32: (32, 6255, 'record-enabled-by-c-bit'),
    33: (22, 6290, 'record-enabled-by-c-bit'),
    34: (27, 6283, 'record-enabled-by-c-bit'),
    35: (28, 6276, 'record-enabled-by-c-bit'),
    36: (35, 6221, 'record-enabled-by-c-bit'),
    37: (29, 6269, 'record-enabled-by-c-bit'),
    38: (36, 6235, 'record-enabled-by-c-bit'),
    39: (6, 6421, 'record-enabled-by-c-bit'),
    40: (2, 6249, 'record-enabled-by-c-bit'),
    41: (38, 6200, 'record-enabled-by-c-bit'),
    42: (39, 6207, 'record-enabled-by-c-bit'),
}
CACHE_BY_RECORD = {
    2: ('24/25', 'aA/ah conditional image-cache copies'),
    10: ('4', 'constructs b[4] wrapper; no f[] assignment'),
    15: ('conditional f[4] and f[21]', 'bu bit 1 creates f[21]; bu bit 2 binds f[4]'),
    17: ('conditional f[4] and f[21]', 'same shared handler as record 15'),
    26: ('static d field', 'object assigned to static d, not f[]'),
}
CM_SLOT_BY_RECORD = {
    1: (56, 6964, 'record-enabled-by-bu-bit; aA==1-or-2 applies extra initialization'),
    2: (59, 6945, 'record-enabled-by-bu-bit'),
    3: (13, 7040, 'record-enabled-by-bu-bit; invokes r()'),
    6: (43, 6920, 'record-enabled-by-bu-bit'),
}

def inspect_bundle(z, name):
    b = z.read(name)
    count = b[0]
    header_end = 1 + count * 8
    lengths = [int.from_bytes(b[1 + 8*i + 4:1 + 8*i + 8], 'little') for i in range(count)]
    assert header_end <= len(b)
    assert sum(lengths) == len(b) - header_end, (name, sum(lengths), len(b)-header_end)
    return count, lengths, header_end

def payload_signature(z, name, index, lengths, header_end):
    payload_offset = header_end + sum(lengths[:index])
    payload = z.read(name)[payload_offset:payload_offset + lengths[index]]
    return payload[:4].hex()

rows=[]
with zipfile.ZipFile(JAR) as z:
    # State-10 loader opens "/" + aA + ".f" and reads records 0..3.
    for variant in range(3):
        name=f'{variant}.f'
        count,lengths,header_end=inspect_bundle(z,name)
        for rec,length in enumerate(lengths):
            mapping={0:(60,5672,'d bit 0 must be set'),1:(16,5693,'d bit 1 must be set'),2:(42,5716,'record-enabled by state path'),3:('',5732,'image cache b[8], no f[] slot')}
            slot,branch,condition=mapping[rec]
            rows.append(dict(loader='A_A_STREAM',bundle=f'/{name}',global_record_index=rec,
                local_record_index=rec,header_entry_offset=1+8*rec,length_field_offset=1+8*rec+4,
                payload_length=length,payload_signature=payload_signature(z,name,rec,lengths,header_end),global_f_slot=slot,secondary_destination='image cache 8' if rec==3 else '',
                branch_offset=branch,condition=condition,source_status='BYTECODE_CONFIRMED'))
    for bundle_no in range(5):
        name=f'gen{bundle_no}.f'
        count,lengths,header_end=inspect_bundle(z,name)
        for rec,length in enumerate(lengths):
            slot,branch,condition = GEN_SLOT_BY_RECORD.get(rec, ('', '', '')) if bundle_no < 4 else ('','','')
            absolute_record = bundle_no*10+rec
            # Mapping is keyed by the global record index in the i.j()V loop.
            mapped = GEN_SLOT_BY_RECORD.get(absolute_record)
            slot,branch,condition = mapped if mapped else ('','','')
            cache,cache_note = CACHE_BY_RECORD.get(absolute_record, ('',''))
            rows.append(dict(loader='GEN_STREAM',bundle=f'/{name}',global_record_index=absolute_record,
                local_record_index=rec,header_entry_offset=1+8*rec,length_field_offset=1+8*rec+4,
                payload_length=length,payload_signature=payload_signature(z,name,rec,lengths,header_end),global_f_slot=slot,secondary_destination=cache,
                branch_offset=branch,condition=condition or cache_note,
                source_status='BYTECODE_CONFIRMED' if slot!='' or cache!='' else 'RECORD_PARSED_NO_SLOT_BINDING_IN_SWITCH'))
    count,lengths,header_end=inspect_bundle(z,'cm.f')
    for rec,length in enumerate(lengths):
        slot,branch,condition=CM_SLOT_BY_RECORD.get(rec,('','',''))
        secondary={0:'image cache 11',4:'image cache 5',5:'image cache 18',6:'image cache 20 cleared'} .get(rec,'')
        rows.append(dict(loader='CM_STREAM',bundle='/cm.f',global_record_index=rec,local_record_index=rec,
            header_entry_offset=1+8*rec,length_field_offset=1+8*rec+4,payload_length=length,payload_signature=payload_signature(z,'cm.f',rec,lengths,header_end),
            global_f_slot=slot,secondary_destination=secondary,branch_offset=branch,condition=condition,
            source_status='BYTECODE_CONFIRMED' if slot!='' or secondary!='' else 'RECORD_PARSED_NO_SLOT_BINDING_IN_SWITCH'))

out=ROOT/'research/build242_dynamic_resource_origin_audit.csv'
with out.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
# Focused join with the three candidate slots raised by Build241 selector bJ=6.
focus=[]
for slot in (27,30,56):
    r=next(x for x in rows if str(x['global_f_slot'])==str(slot))
    focus.append(dict(global_f_slot=slot,bundle=r['bundle'],record_index=r['global_record_index'],
        local_record_index=r['local_record_index'],length_field_offset=r['length_field_offset'],
        payload_length=r['payload_length'],payload_signature=r['payload_signature'],branch_offset=r['branch_offset'],
        condition=r['condition'],status='RESOURCE_ORIGIN_CONFIRMED_NOT_RENDER_SELECTION'))
with (ROOT/'research/build242_build241_candidate_origin_join.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(focus[0])); w.writeheader(); w.writerows(focus)
print('records',len(rows),'aA records',sum(r['loader']=='A_A_STREAM' for r in rows),'gen records',sum(r['loader']=='GEN_STREAM' for r in rows),'cm records',sum(r['loader']=='CM_STREAM' for r in rows))
print('resource origin joins')
for r in focus: print(r)
assert all(r['payload_signature']=='df030101' for r in rows)
print('all 63 payloads have DF03 signature; all bundle payload length sums verified')
