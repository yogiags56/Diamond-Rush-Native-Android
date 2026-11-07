import struct
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'research'))
from audit_build210_fields import parse

def s(v): return struct.pack('<h', v)
def fixture():
    b=bytearray(b'\xdf\x03\x01\x01\x01\x01')
    b += s(2) + bytes([2,3,4,5])                    # f:[B, two dimensions per sprite
    b += s(2) + bytes([7,8,9,10,11,12,13,14])    # h:[B, four bytes per component
    b += s(1) + bytes([2,0]) + s(1) + bytes([0,0,24,24]) # g, b, a:[B]
    b += s(1) + bytes([4,0,0,0,15])               # c:[B], five-byte record
    b += s(1) + bytes([6,0]) + s(0)                # b:[B], a:[S]
    b += s(0x5515) + bytes([1,2]) + s(0x1600)      # palette format/counts + palette below? 
    # Correct order is palette bytes before pixel format; insert two ARGB1555 colors.
    # Rebuild tail with two colors then pixel format.
    del b[-2:]
    b += bytes([0x00,0x7c,0x1f,0x00]) + s(0x1600)
    b += s(2) + bytes([0x12,0x34]) + s(1) + bytes([0x56])
    return bytes(b)

def test_exact_field_widths_and_interleaved_payloads():
    x=parse(fixture())
    assert len(x['f']) == 4
    assert len(x['h']) == 8
    assert len(x['g']) == 1 and x['g'] == [2]
    assert len(x['agroups']) == 4
    assert len(x['crec']) == 5
    assert x['btable'] == [6] and x['ashort'] == [0]
    assert x['lengths'] == [2,1]
    assert x['payloads'] == [b'\x12\x34', b'\x56']
    assert x['pixfmt'] == 0x1600

def test_all_original_df03_payloads_parse():
    import zipfile, struct
    jar=Path(__file__).resolve().parents[1] / 'original' / 'DMR320x240-Celsius.jar'
    with zipfile.ZipFile(jar) as z:
        found=0; sprites=0
        for name in z.namelist():
            if not name.endswith('.f'): continue
            cont=z.read(name); n=cont[0]; base=1+n*8
            for i in range(n):
                off,ln=struct.unpack_from('<II',cont,1+i*8)
                payload=cont[base+off:base+off+ln]
                if payload[:4] == b'\xdf\x03\x01\x01':
                    x=parse(payload); found+=1; sprites+=len(x['payloads'])
        assert found == 94
        assert sprites == 1372

def test_reconstructed_composite_graph_has_valid_ranges_and_acyclic_nesting():
    import zipfile, struct
    jar=Path(__file__).resolve().parents[1] / 'original' / 'DMR320x240-Celsius.jar'
    nested_edges=0
    with zipfile.ZipFile(jar) as z:
        for name in z.namelist():
            if not name.endswith('.f'): continue
            cont=z.read(name); n=cont[0]; base=1+n*8
            for i in range(n):
                off,ln=struct.unpack_from('<II',cont,1+i*8)
                payload=cont[base+off:base+off+ln]
                if payload[:4] != b'\xdf\x03\x01\x01': continue
                x=parse(payload); groups=len(x['g']); components=len(x['h'])//4
                graph=[[] for _ in range(groups)]
                for group,count in enumerate(x['g']):
                    start=x['bstarts'][group]
                    assert start >= 0 and start+count <= components
                    for j in range(count):
                        record=x['h'][(start+j)*4:(start+j+1)*4]
                        if record[3] & 0x10:
                            nested_edges += 1
                            assert record[0] < groups
                            graph[group].append(record[0])
                state=[0]*groups
                def visit(v):
                    state[v]=1
                    for w in graph[v]:
                        assert state[w] != 1
                        if state[w] == 0: visit(w)
                    state[v]=2
                for v in range(groups):
                    if state[v] == 0: visit(v)
    assert nested_edges == 11
