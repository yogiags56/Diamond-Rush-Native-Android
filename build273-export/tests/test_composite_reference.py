import unittest

def parse_record(data, base):
    if base < 0 or base > len(data)-4:
        raise ValueError("bounds")
    return (data[base] & 255,
            data[base+1] if data[base+1] < 128 else data[base+1]-256,
            data[base+2] if data[base+2] < 128 else data[base+2]-256,
            data[base+3] & 255)

def record_base(short_table, group, component):
    if group < 0 or group >= len(short_table) or component < 0:
        raise ValueError("index")
    slot = short_table[group] + component
    if slot < 0:
        raise ValueError("slot")
    return slot*4

def adjusted_flags(flags, control):
    return flags ^ (control & 0x0f)

def position(x,y,flags,dx,dy):
    return (x-dx if flags & 1 else x+dx,
            y-dy if flags & 2 else y+dy)

class CompositeRecordTests(unittest.TestCase):
    def test_unsigned_sprite_index(self):
        self.assertEqual(parse_record(bytes([255,0,0,0]),0)[0],255)
    def test_signed_offsets_positive(self):
        self.assertEqual(parse_record(bytes([1,12,7,0]),0)[1:3],(12,7))
    def test_signed_offsets_negative(self):
        self.assertEqual(parse_record(bytes([1,0xf4,0xfe,0]),0)[1:3],(-12,-2))
    def test_nested_flag_bit_0x10(self):
        self.assertTrue(parse_record(bytes([1,0,0,0x10]),0)[3] & 0x10)
    def test_transform_low_nibble_only(self):
        self.assertEqual(adjusted_flags(0x30,0xA5),0x35)
    def test_record_stride_and_component_offset(self):
        self.assertEqual(record_base([3,9],1,2),44)
    def test_flag_dependent_position(self):
        self.assertEqual(position(100,50,0,7,-3),(107,47))
        self.assertEqual(position(100,50,3,7,-3),(93,53))
    def test_reject_truncated(self):
        with self.assertRaises(ValueError): parse_record(bytes([1,2,3]),0)
    def test_reject_bad_group(self):
        with self.assertRaises(ValueError): record_base([0],1,0)
    def test_reject_negative_slot(self):
        with self.assertRaises(ValueError): record_base([-2],0,0)

if __name__ == "__main__":
    unittest.main()
