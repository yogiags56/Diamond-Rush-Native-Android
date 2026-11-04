import importlib.util, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("decode_verified",HERE.parent/"decode_verified_gen0_sprite.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class VerifiedGen0SpriteDecodeTest(unittest.TestCase):
    def test_original_payload_decodes_eight_frames(self):
        payload=HERE.parents[1]/"reference"/"sections"/"gen0_section_04.bin"
        frames,meta=mod.decode(payload.read_bytes())
        self.assertEqual(len(frames),8)
        self.assertEqual((frames[0].width,frames[0].height),(24,24))
        self.assertEqual(meta["pixel_bytes"],2304)
        self.assertEqual(meta["palette_format"],"RGB565")
    def test_frames_are_not_all_identical(self):
        payload=HERE.parents[1]/"reference"/"sections"/"gen0_section_04.bin"
        frames,_=mod.decode(payload.read_bytes())
        self.assertGreater(len({f.tobytes() for f in frames}),1)
    def test_rejects_unverified_payload_shape(self):
        with self.assertRaises(ValueError): mod.decode(b"short")
if __name__=="__main__": unittest.main()
