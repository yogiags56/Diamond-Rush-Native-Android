import struct
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"research"))
from audit_build210_fields import parse

MAGIC=b"\xdf\x03\x01\x01"

def all_resources():
    import zipfile
    with zipfile.ZipFile(ROOT/"original.jar") as z:
        for name in z.namelist():
            if not name.endswith(".f"): continue
            cont=z.read(name)
            if not cont: continue
            n=cont[0];base=1+n*8
            for entry in range(n):
                off,ln=struct.unpack_from("<II",cont,1+entry*8)
                blob=cont[base+off:base+off+ln]
                if blob[:4]==MAGIC:
                    yield name,entry,parse(blob)

def frames(x):
    out=[]
    for si,(count,start) in enumerate(zip(x["btable"],x["ashort"])):
        for fi in range(count):
            p=(start+fi)*5
            r=x["crec"][p:p+5]
            group=r[0]
            duration=r[1]
            dx=r[2] if r[2]<128 else r[2]-256
            dy=r[3] if r[3]<128 else r[3]-256
            control=r[4]
            out.append((si,fi,group,duration,dx,dy,control))
    return out

def place(frame,base_x,base_y,incoming_flags,inherited_x=0,inherited_y=0):
    _,_,group,duration,dx,dy,control=frame
    if incoming_flags&0x20:
        ox=dx if incoming_flags&1 else -dx
        oy=dy if incoming_flags&2 else -dy
    else:
        ox,oy=inherited_x,inherited_y
    return {"group":None if group==255 else group,"x":base_x-ox,"y":base_y-oy,
            "offset_x":ox,"offset_y":oy,"duration":duration,
            "draw_flags":incoming_flags^(control&0x0f)}

def test_all_five_byte_records_are_partitioned_by_sequence_counts():
    total_records=sequences=0
    for _,_,x in all_resources():
        nrec=len(x["crec"])//5
        assert len(x["btable"])==len(x["ashort"])
        assert sum(x["btable"])==nrec
        for count,start in zip(x["btable"],x["ashort"]):
            assert start>=0 and start+count<=nrec
        total_records+=nrec;sequences+=len(x["btable"])
    assert total_records==1238
    assert sequences==188

def test_all_animation_group_references_are_valid_or_explicit_ff_sentinel():
    valid=sentinels=0
    for _,_,x in all_resources():
        for frame in frames(x):
            group=frame[2]
            if group==255:sentinels+=1
            else:
                assert group<len(x["g"])
                valid+=1
    assert valid==1235 and sentinels==3

def test_duration_values_are_unsigned_and_positive_in_original_resources():
    values=[f[3] for _,_,x in all_resources() for f in frames(x)]
    assert len(values)==1238 and min(values)==1 and max(values)==90 and 0 not in values

def test_record_offsets_are_signed_bytes_and_control_flags_are_low_nibble_only():
    flags=set();offsets=[]
    for _,_,x in all_resources():
        for f in frames(x):
            offsets.extend((f[4],f[5]));flags.add(f[6])
    assert min(offsets)==-100 and max(offsets)==120
    assert flags=={0,1}

def test_flag_0x20_enables_signed_frame_offsets_and_sign_bits():
    f=(0,0,12,3,-4,7,1)
    p=place(f,100,80,0x20)
    assert (p["x"],p["y"],p["offset_x"],p["offset_y"])==(96,87,4,-7)
    p=place(f,100,80,0x23)
    assert (p["x"],p["y"],p["offset_x"],p["offset_y"])==(104,73,-4,7)

def test_without_flag_0x20_inherited_offsets_are_preserved():
    f=(0,0,12,3,-4,7,1)
    p=place(f,100,80,0,inherited_x=5,inherited_y=-6)
    assert (p["x"],p["y"])==(95,86)
    assert p["draw_flags"]==1

def test_record_control_low_nibble_is_xored_into_incoming_flags():
    f=(0,0,12,3,-4,7,1)
    assert place(f,0,0,0)["draw_flags"]==1
    assert place(f,0,0,1)["draw_flags"]==0
    assert place(f,0,0,0x20)["draw_flags"]==0x21

def test_mmv_ff_records_are_retained_as_no_group_frames():
    matches=[]
    for name,entry,x in all_resources():
        if name=="mmv.f" and entry in (1,2,3):
            matches.append([f[2] for f in frames(x)])
    assert matches==[[0,255],[0,255],[0,255]]

def test_kotlin_animation_table_source_preserves_raw_and_decoded_fields():
    src=(ROOT/"android/src/main/kotlin/com/diamondrush/legacy/LegacySpriteAnimationTable.kt").read_text()
    for token in ["rawCompositeGroupIndex","durationUnits","offsetX","offsetY",
                  "controlFlags","NO_GROUP","incomingFlags and 0x20",
                  "incomingFlags xor (frame.controlFlags and 0x0f)"]:
        assert token in src


def test_original_renderers_confirm_logical_canvas_and_gameplay_bars():
    c=(ROOT/"research/build213_bytecode/c_build214_full.javap.txt").read_text()
    i=(ROOT/"research/build213_bytecode/i_build214_full.javap.txt").read_text()
    assert "sipush        320" in c and "bipush        31" in c and "sipush        209" in c
    assert "sipush        320" in i and "sipush        240" in i
    assert "Graphics.setClip:(IIII)V" in i

def test_dynamic_palette_state_is_used_as_palette_index_in_resource_initialization():
    i=(ROOT/"research/build213_bytecode/i_build214_full.javap.txt").read_text()
    assert "Field aA:I" in i
    assert "Method f.a:(IIII)V" in i
    # The original resource initializer loads aA as the first palette argument,
    # then stores the same value into the f object's active palette field.
    assert "getfield      #402                // Field aA:I" in i
    assert "putfield      #304                // Field f.a:I" in i
