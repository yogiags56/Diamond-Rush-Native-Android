import sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from probe_decoder_layout import probe, FormatError

class DecoderLayoutProbeTests(unittest.TestCase):
    def test_known_fixture_fails_safely_at_impossible_offsets(self):
        data = (ROOT / 'reference/sections/gen0_section_00.bin').read_bytes()
        with self.assertRaisesRegex(FormatError, 'cumulative size'):
            probe(data)

    def test_rejects_truncated_fixed_prefix(self):
        with self.assertRaises(FormatError): probe(b'123')

    def test_rejects_negative_first_count(self):
        data = bytearray(16); data[6:8] = b'\xff\xff'
        with self.assertRaisesRegex(FormatError, 'negative image table count'):
            probe(bytes(data))

if __name__ == '__main__': unittest.main()
