import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(p): return list(csv.DictReader((ROOT/p).open()))
def test_all_1372_sprites_decode():
 r=rows('research/build211_sprite_decode_inventory.csv'); assert len(r)==1372
 assert all(x['decode_status']=='PASS' and int(x['decoded_pixels'])==int(x['width'])*int(x['height']) for x in r)
def test_kotlin_python_hash_parity():
 a=rows('research/build211_sprite_decode_inventory.csv'); b=rows('research/build211_kotlin_decode_inventory.csv')
 assert len(a)==len(b)==1372
 ka=lambda x:(x['bundle'],x['entry'],x['sprite'])
 aa={ka(x):x for x in a}; bb={ka(x):x for x in b}; assert aa.keys()==bb.keys()
 assert all(aa[k]['sha256_indices']==bb[k]['sha256_indices'] for k in aa)
def test_supported_formats_match_original_inventory():
 r=rows('research/build211_sprite_decode_inventory.csv')
 assert {x['pixel_format'] for x in r}=={'0x1600','0x27F1','0x0400'}
def test_palette_indices_within_palette():
 r=rows('research/build211_sprite_decode_inventory.csv')
 assert all(int(x['max_palette_index'])<int(x['colors_per_palette']) for x in r)
