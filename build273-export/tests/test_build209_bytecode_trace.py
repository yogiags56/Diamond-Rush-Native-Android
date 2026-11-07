import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit', ROOT/'research'/'df03_full_parser_audit.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def make_payload():
    b = bytearray(b'\xdf\x03\x01\x01\x01\x01')
    def s(v): b.extend(int(v).to_bytes(2, 'little', signed=True))
    # sprite count + two dimension bytes per sprite
    s(2); b.extend(bytes([24, 24, 16, 16]))
    # four-byte table count + four bytes per entry (count << 2 in original bytecode)
    s(1); b.extend(bytes([0x34, 0x12, 0x56, 0x78]))
    # table-3 count + four-byte descriptors + four-byte records
    s(1); b.extend(bytes([2, 0xAA, 0x10, 0x00])); b.extend(bytes([1, 2, 3, 4]))
    # five-byte table
    s(1); b.extend(bytes([1, 2, 3, 4, 5]))
    # table-5 count + four-byte descriptors
    s(1); b.extend(bytes([3, 0xBB, 0x20, 0x00]))
    # ARGB8888, one palette, two colors
    s(-30584); b.extend(bytes([1, 2])); b.extend(bytes(range(8)))
    # pixel format; interleaved length+payload records
    s(0x1600); s(3); b.extend(b'abc'); s(2); b.extend(b'de')
    return bytes(b)


def test_exact_table_boundaries_and_interleaved_sprite_payloads():
    x = audit.parse(make_payload())
    assert len(x['dims']) == 4
    assert len(x['four_byte_table']) == 4
    assert len(x['metadata']) == 1
    assert len(x['paired_byte_table']) == 4
    assert len(x['five']) == 5
    assert len(x['three']) == 1
    assert x['palfmt'] == -30584
    assert x['pixfmt'] == 0x1600
    assert x['lengths'] == [3, 2]
    assert x['offsets'] == [0, 3]
    assert x['payloads'] == [b'abc', b'de']
    assert x['trailing'] == b''


def test_unknown_palette_format_consumes_no_palette_payload():
    b = bytearray(make_payload())
    # This test uses a second tiny payload where the switch default leaves cursor unchanged.
    b = bytearray(b'\xdf\x03\x01\x01\x01\x01')
    def s(v): b.extend(int(v).to_bytes(2, 'little', signed=True))
    s(1); b.extend(b'\x18\x18')
    s(0)
    s(0)
    s(0)
    s(0)
    s(0x1234); b.extend(bytes([1, 1]))
    s(0x1600); s(1); b.extend(b'Z')
    x = audit.parse(bytes(b))
    assert x['palfmt'] == 0x1234
    assert x['palettes'] == []
    assert x['pixfmt'] == 0x1600
    assert x['payloads'] == [b'Z']


def test_rejects_negative_or_truncated_lengths():
    b = bytearray(make_payload())
    # Corrupt final payload length to -1.
    b[-5:-3] = (-1).to_bytes(2, 'little', signed=True)
    try:
        audit.parse(bytes(b))
    except ValueError:
        pass
    else:
        raise AssertionError('negative payload length must be rejected')


if __name__ == '__main__':
    import pytest
    raise SystemExit(pytest.main([__file__, '-q']))


def test_nonpositive_table_counts_consume_no_table_bytes():
    b = bytearray(b"\xdf\x03\x01\x01\x01\x01")
    def s(v): b.extend(int(v).to_bytes(2, "little", signed=True))
    s(1); b.extend(b"\x18\x18")
    s(-1)  # four-byte table count: branch skipped
    s(0)   # table 3 count: branch skipped
    s(-2)  # five-byte table count: branch skipped
    s(0)   # table 5 count: branch skipped
    s(0x1234); b.extend(bytes([1, 1]))
    s(0x1600); s(1); b.extend(b"Q")
    x = audit.parse(bytes(b))
    assert x["four_byte_table"] == b""
    assert x["metadata"] == []
    assert x["five"] == b""
    assert x["three"] == []
    assert x["payloads"] == [b"Q"]
