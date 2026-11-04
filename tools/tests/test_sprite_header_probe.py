import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "audit_sprite_headers.py"
spec = importlib.util.spec_from_file_location("audit_sprite_headers", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SpriteHeaderProbeTests(unittest.TestCase):
    def test_known_gen0_prefix(self):
        data = (SCRIPT.parents[1] / "reference" / "sections" / "gen0_section_00.bin").resolve().read_bytes()
        result = module.probe(data)
        self.assertEqual(result["status"], "prefix_valid")
        self.assertEqual(result["table0_count"], 5)
        self.assertEqual(result["table1_count_signed"], 5)

    def test_short_payload(self):
        self.assertEqual(module.probe(b"1234567")["status"], "too_short")

    def test_table_zero_bounds(self):
        data = b"\0" * 6 + bytes([255, 127])
        self.assertEqual(module.probe(data)["status"], "table0_out_of_bounds")


if __name__ == "__main__":
    unittest.main()
