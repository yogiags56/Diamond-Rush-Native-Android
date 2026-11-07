from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "research" / "build214_bytecode" / "i_build214_full.javap.txt").read_text(errors="replace")

def method(start, end=None):
    a = TEXT.index(start)
    if end is not None:
        b = TEXT.index(end, a)
    else:
        match = __import__("re").search(r"\\n  (?:public|private|protected) ", TEXT[a + len(start):])
        b = a + len(start) + match.start() if match else len(TEXT)
    return TEXT[a:b]

def test_room_loader_uses_resource_stream():
    j = method("private void j();", "private void a(boolean);")
    assert "getResourceAsStream" in j
    assert "InputStream.read" in j

def test_room_dimensions_are_unsigned_little_endian_16bit():
    a = method("public static int a(byte[], int);", "public static int b(byte[], int);")
    assert a.count("sipush        255") == 2
    assert "bipush        8" in a and "ishl" in a and "ior" in a

def test_room_record_dimensions_are_read_from_offsets_zero_and_two():
    j = method("private void j();", "private void a(boolean);")
    assert "invokestatic  #934                // Method a:([BI)I" in j
    assert "iconst_2" in j
    assert "Field e:I" in j and "Field f:I" in j

def test_primary_byte_plane_allocated_and_filled_from_first_payload():
    j = method("private void j();", "private void a(boolean);")
    assert "multianewarray #128,  2           // class \"[[B\"" in j
    assert "Field a:[[B" in j
    assert "bastore" in j

def test_two_integer_planes_allocated_and_loaded_from_byte_payloads():
    j = method("private void j();", "private void a(boolean);")
    assert "multianewarray #129,  2           // class \"[[I\"" in j
    assert "Field b:[[I" in j and "Field a:[[I" in j
    assert "iastore" in j

def test_nonselected_room_record_skip_uses_three_bytes_per_cell():
    j = method("private void j();", "private void a(boolean);")
    assert "Field e:I" in j and "Field f:I" in j
    assert "iconst_3" in j and "InputStream.skip" in j

def test_central_map_setter_updates_primary_byte_and_packed_int_plane():
    setter = method("public static void a(short, short, byte, int);")
    assert "Field a:[[B" in setter and "bastore" in setter
    assert "Field b:[[I" in setter and "iastore" in setter

def test_map_planes_are_distinct_from_runtime_byte_overlays():
    j = method("private void j();", "private void a(boolean);")
    assert "Field c:[[B" in j and "Field b:[[B" in j
    assert "Field a:[[B" in j and "Field a:[[I" in j
