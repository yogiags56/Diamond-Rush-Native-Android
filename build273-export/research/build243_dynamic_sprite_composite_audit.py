from pathlib import Path
import csv, struct, hashlib

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "research" / "build242_payload_fixtures"
SPECS = {
    27: ("slot27.bin", "/gen3.f", 7, 31, 11, [7, 7, 3, 4, 5, 3, 2]),
    30: ("slot30.bin", "/gen2.f", 8, 12, 11, [2, 1, 2, 2, 2, 1, 1, 1]),
    56: ("slot56.bin", "/cm.f", 6, 8, 6, [1, 2, 2, 1, 1, 1]),
}

def parse(data):
    p = 6
    def s16():
        nonlocal p
        v = struct.unpack_from("<h", data, p)[0]; p += 2
        return v
    sprite_count = s16()
    dims = data[p:p + sprite_count * 2]; p += sprite_count * 2
    component_count = s16()
    components = data[p:p + component_count * 4]; p += component_count * 4
    group_count = s16()
    groups = []
    for _ in range(group_count):
        count = data[p]; start = struct.unpack_from("<h", data, p + 2)[0]
        p += 4; groups.append((count, start))
    p += group_count * 4
    five_count = s16(); p += five_count * 5
    byte_short_count = s16(); p += byte_short_count * 4
    palette_format = s16(); palette_count, colors = data[p], data[p + 1]; p += 2
    palettes = []
    for _ in range(palette_count):
        palette = []
        for _ in range(colors):
            palette.append(struct.unpack_from("<H", data, p)[0]); p += 2
        palettes.append(palette)
    pixel_format = s16()
    sprites = []
    for i in range(sprite_count):
        length = s16()
        payload = data[p:p + length]; p += length
        sprites.append((dims[i * 2], dims[i * 2 + 1], payload))
    assert p == len(data), (p, len(data))
    return components, groups, palettes, palette_format, pixel_format, sprites

def expand1555(v):
    a = 255 if v & 0x8000 else 0
    r = ((v >> 10) & 31) * 255 // 31
    g = ((v >> 5) & 31) * 255 // 31
    b = (v & 31) * 255 // 31
    return (a << 24) | (r << 16) | (g << 8) | b

rows, sprite_rows = [], []
for slot, (filename, resource, expected_groups, expected_components, expected_sprites, expected_counts) in SPECS.items():
    data = (FIXTURES / filename).read_bytes()
    components, groups, palettes, palette_format, pixel_format, sprites = parse(data)
    assert len(groups) == expected_groups and sum(c for c, _ in groups) == expected_components
    assert len(sprites) == expected_sprites and [c for c, _ in groups] == expected_counts
    assert palette_format == 21781 and pixel_format == 5632
    for gi, (count, start) in enumerate(groups):
        for ci in range(count):
            off = (start + ci) * 4
            sprite, x, y, flags = components[off:off + 4]
            nested = bool(flags & 0x10)
            assert (sprite < expected_groups if nested else sprite < expected_sprites)
            rows.append([slot, resource, gi, start, ci, start + ci, sprite, x if x < 128 else x-256,
                         y if y < 128 else y-256, flags, "nested-group" if nested else "leaf-sprite"])
    for si, (w, h, payload) in enumerate(sprites):
        n = w * h
        indices = []
        for byte in payload:
            indices.extend([byte >> 4, byte & 15])
        indices = indices[:n]
        assert len(indices) == n
        for pi, pal in enumerate(palettes):
            assert max(indices, default=0) < len(pal)
            argb = [expand1555(pal[i]) for i in indices]
            sprite_rows.append([slot, resource, si, w, h, pi, len(payload), n,
                                len(set(indices)), sum(1 for c in argb if c >> 24 == 0),
                                hashlib.sha256(bytes(payload)).hexdigest()])

with (ROOT / "research" / "build243_dynamic_composite_component_attribution.csv").open("w", newline="") as f:
    w = csv.writer(f); w.writerow(["global_slot","resource_path","group_index","group_first_record","component_index","absolute_component_record","sprite_or_nested_group_index","offset_x_signed","offset_y_signed","control_byte","record_kind"]); w.writerows(rows)
with (ROOT / "research" / "build243_dynamic_sprite_pixel_decode_audit.csv").open("w", newline="") as f:
    w = csv.writer(f); w.writerow(["global_slot","resource_path","sprite_index","width","height","palette_index","encoded_bytes","decoded_pixels","distinct_palette_indices","transparent_pixels","payload_sha256"]); w.writerows(sprite_rows)
print(f"COMPONENT_ROWS={len(rows)}")
print(f"SPRITE_PALETTE_ROWS={len(sprite_rows)}")
print("GROUPS=21 COMPONENTS=51 SPRITES=28 PALETTE_DECODE_INSTANCES=40")
print("ALL_SPRITE_INDICES_AND_COMPOSITE_REFERENCES_VALID")
