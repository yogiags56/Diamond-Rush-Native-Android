from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"android/src/main/kotlin/com/diamondrush/legacy"
def read(n): return (K/n).read_text()
def test_room_model_preserves_all_five_planes():
    s=read("LegacyRoomMapPlanes.kt")
    for token in ["primaryByte","serializedIntPlane","secondaryIntPlane","runtimeByteOverlayB","runtimeByteOverlayC"]:
        assert token in s
def test_integer_plane_values_are_not_unsigned_normalized():
    s=read("LegacyRoomPayloadDecoder.kt")
    assert "secondPlaneBytes[it].toInt()" in s
    assert "thirdPlaneBytes[it].toInt()" in s
    assert "& 0xFF" not in s[s.index("val secondInts"):s.index("val planes")]
def test_dimensions_are_unsigned_little_endian_16bit():
    s=read("LegacyRoomPayloadDecoder.kt")
    assert "readUnsignedLittleEndian16" in s
    assert "val high = bytes[offset + 1].toInt() and 0xFF" in s
    assert "return low or (high shl 8)" in s
def test_room_skip_uses_three_serialized_planes():
    s=read("LegacyRoomPayloadDecoder.kt")
    assert "cells.toLong() * SERIALIZED_PLANES" in s
    assert "SERIALIZED_PLANES = 3" in s
def test_setter_only_changes_proven_pair():
    s=read("LegacyRoomMapPlanes.kt")
    body=s.split("fun setPrimaryAndSerializedInt",1)[1].split("}",1)[0]
    assert "primary[i] = byteValue" in body
    assert "serializedInt[i] = intValue" in body
    assert "secondaryInt" not in body and "overlay" not in body
def test_bounds_and_overflow_are_checked():
    s=read("LegacyRoomMapPlanes.kt")
    assert "product <= Int.MAX_VALUE" in s
    assert "first in 0 until firstDimension" in s
    assert "second in 0 until secondDimension" in s
