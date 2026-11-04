import importlib.util, json, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("audit_decoder_layout", HERE.parent/"audit_decoder_layout.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class DecoderCorpusAuditTest(unittest.TestCase):
    def test_real_corpus_has_expected_bounded_sections(self):
        rows=mod.audit(HERE.parents[1]/"reference"/"sections")
        ok=[r for r in rows if r["status"]=="bounded_image_metadata"]
        self.assertEqual(len(rows),121)
        self.assertEqual(len(ok),29)
        self.assertTrue(all(r["pixel_data_bytes_after_metadata"]>=0 for r in ok))
    def test_known_palette_and_sprite_groups(self):
        rows=mod.audit(HERE.parents[1]/"reference"/"sections")
        by={r["file"]:r for r in rows}
        self.assertEqual(by["gen0_section_04.bin"]["image_count"],8)
        self.assertEqual(by["gen0_section_04.bin"]["palette_format"],21781)
        self.assertEqual(by["gen0_section_04.bin"]["palette_colors"],16)
    def test_unrecognized_is_not_called_corrupt(self):
        rows=mod.audit(HERE.parents[1]/"reference"/"sections")
        unknown=[r for r in rows if r["status"]=="unclassified_for_this_decoder"]
        self.assertGreater(len(unknown),0)
        self.assertTrue(all("reason" in r for r in unknown))
if __name__=="__main__": unittest.main()
