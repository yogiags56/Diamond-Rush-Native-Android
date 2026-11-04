import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from parse_sprite_header import parse,FormatError
class HeaderParserTests(unittest.TestCase):
 def test_real_gen0_payloads_parse_or_fail_cleanly(self):
  files=sorted((ROOT/'reference'/'sections').glob('gen0_section_*.bin'))
  self.assertEqual(len(files),10)
  for p in files: self.assertLessEqual(parse(p.read_bytes()).metadata_end,p.stat().st_size)
 def test_known_gen0_prefix(self):
  h=parse((ROOT/'reference'/'sections'/'gen0_section_00.bin').read_bytes())
  self.assertEqual((h.table0_entries,h.table1_records,h.table2_records,h.metadata_end),(5,5,1,48))
 def test_negative_count_rejected(self):
  d=bytearray(10); d[6]=0xff; d[7]=0xff
  with self.assertRaises(FormatError): parse(bytes(d))
 def test_table_overrun_rejected(self):
  d=bytearray(8); d[6]=2
  with self.assertRaises(FormatError): parse(bytes(d))
 def test_truncated_fixed_header(self):
  with self.assertRaises(FormatError): parse(b'123')
if __name__=='__main__': unittest.main()
