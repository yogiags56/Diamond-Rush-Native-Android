import csv, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read_csv(name):
    with (ROOT/'research'/name).open(newline='') as f:
        return list(csv.DictReader(f))

def test_build242_traces_all_dynamic_stream_records_and_bundle_lengths():
    rows=read_csv('build242_dynamic_resource_origin_audit.csv')
    assert len(rows)==63
    assert sum(r['loader']=='A_A_STREAM' for r in rows)==12
    assert sum(r['loader']=='GEN_STREAM' for r in rows)==43
    assert sum(r['loader']=='CM_STREAM' for r in rows)==8
    assert all(r['payload_signature']=='df030101' for r in rows)
    with zipfile.ZipFile(ROOT/'original.jar') as z:
        for name in ['0.f','1.f','2.f','gen0.f','gen1.f','gen2.f','gen3.f','gen4.f','cm.f']:
            b=z.read(name); count=b[0]
            lengths=[int.from_bytes(b[1+8*i+4:1+8*i+8],'little') for i in range(count)]
            assert sum(lengths)==len(b)-(1+count*8)

def test_build242_resolves_build241_candidate_slots_to_exact_bundle_records():
    rows=read_csv('build242_build241_candidate_origin_join.csv')
    by_slot={int(r['global_f_slot']):r for r in rows}
    assert set(by_slot)=={27,30,56}
    assert (by_slot[27]['bundle'],int(by_slot[27]['record_index']),int(by_slot[27]['payload_length']))==('/gen3.f',34,754)
    assert (by_slot[30]['bundle'],int(by_slot[30]['record_index']),int(by_slot[30]['payload_length']))==('/gen2.f',23,1846)
    assert (by_slot[56]['bundle'],int(by_slot[56]['record_index']),int(by_slot[56]['payload_length']))==('/cm.f',1,1258)
    assert all(r['status']=='RESOURCE_ORIGIN_CONFIRMED_NOT_RENDER_SELECTION' for r in rows)
    fixture_dir=ROOT/'android/src/test/resources/build242'
    with zipfile.ZipFile(ROOT/'original.jar') as z:
        for slot,bundle,index,fixture in [(27,'gen3.f',4,'slot27.bin'),(30,'gen2.f',3,'slot30.bin'),(56,'cm.f',1,'slot56.bin')]:
            b=z.read(bundle); count=b[0]; pos=1+count*8+sum(int.from_bytes(b[1+8*i+4:1+8*i+8],'little') for i in range(index))
            length=int.from_bytes(b[1+8*index+4:1+8*index+8],'little')
            assert (fixture_dir/fixture).read_bytes()==b[pos:pos+length]
