#!/usr/bin/env python3
"""Build 235: bind static f[] slots to render consumers and local composite/animation references."""
import csv
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'research'))
import df03_full_parser_audit as parser

SLOTS = ROOT / 'research/build233_bundle_to_global_sprite_slots.csv'
CONSUMERS = ROOT / 'android/src/main/kotlin/com/diamondrush/legacy/LegacySpriteResourceConsumerCatalog.kt'
JAR = ROOT / 'original.jar'

# Parse the checked-in, bytecode-derived Build232 numeric consumer catalog.
# This avoids copying offsets into a second hand-maintained mapping.

def load_render_consumers():
    source = CONSUMERS.read_text()
    found = {}
    pattern = re.compile(r"LegacySpriteResourceConsumerEvidence\((\d+),\s*listOf\(([^)]*)\)\)")
    for match in pattern.finditer(source):
        slot = int(match.group(1))
        offsets = [int(value.strip()) for value in match.group(2).split(',') if value.strip()]
        found[slot] = offsets
    return found


def load_all_consumer_sites():
    found = {}
    with (ROOT / 'research/build232_sprite_resource_array_accesses.csv').open(newline='') as handle:
        for row in csv.DictReader(handle):
            if row.get('array_field') != 'a' or not row.get('array_index_constant'):
                continue
            try:
                slot = int(row['array_index_constant'])
            except ValueError:
                continue
            found.setdefault(slot, []).append(
                f"{row['method']}@{row['bytecode_offset']}:{row['access_kind']}")
    return found


def signed_byte(v):
    return v - 256 if v >= 128 else v


def decode_layout(payload):
    x = parser.parse(payload)
    components = []
    raw = x['four_byte_table']
    for offset in range(0, len(raw), 4):
        components.append({
            'sprite_index': raw[offset],
            'offset_x': signed_byte(raw[offset + 1]),
            'offset_y': signed_byte(raw[offset + 2]),
            'control': raw[offset + 3],
        })
    groups = [(first, start) for first, _skipped, start in x['metadata']]
    animation_sequences = [(first, start) for first, _skipped, start in x['three']]
    return x, components, groups, animation_sequences


def expand_group(group_index, components, groups, active=None):
    active = set() if active is None else active
    if group_index in active or group_index < 0 or group_index >= len(groups):
        return [], [('invalid_or_cycle', group_index)]
    active.add(group_index)
    count, start = groups[group_index]
    leaves, errors = [], []
    for local_component in range(count):
        record_index = start + local_component
        if record_index < 0 or record_index >= len(components):
            errors.append(('component_out_of_range', record_index))
            continue
        record = components[record_index]
        target = record['sprite_index']
        if record['control'] & 0x10:
            child_leaves, child_errors = expand_group(target, components, groups, active)
            leaves.extend(child_leaves)
            errors.extend(child_errors)
        else:
            leaves.append(target)
    active.remove(group_index)
    return leaves, errors


def write_csv(path, header, rows):
    with path.open('w', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    slot_rows = list(csv.DictReader(SLOTS.open(newline='')))
    consumer_map = load_render_consumers()
    all_consumer_sites = load_all_consumer_sites()

    summary, component_rows, animation_rows, draw_rows, group_leaf_rows = [], [], [], [], []
    with zipfile.ZipFile(JAR) as archive:
        for binding in slot_rows:
            slot = int(binding['global_f_slot'])
            bundle = binding['bundle_path'].lstrip('/')
            entry_index = int(binding['bundle_entry_index'])
            entries = parser.read_bundle_entries(archive.read(bundle))
            payload = entries[entry_index][3]
            x, components, groups, sequences = decode_layout(payload)
            sprite_count = x['sprite_count']
            direct_leaf_edges = nested_edges = component_errors = 0
            for group_index, (count, start) in enumerate(groups):
                for local_index in range(count):
                    record_index = start + local_index
                    if record_index < 0 or record_index >= len(components):
                        component_rows.append([slot, bundle, entry_index, group_index, local_index,
                                               record_index, '', '', '', '', 'invalid_component_record', 'invalid'])
                        component_errors += 1
                        continue
                    record = components[record_index]
                    nested = bool(record['control'] & 0x10)
                    if nested:
                        nested_edges += 1
                        target_type = 'composite_group'
                    else:
                        direct_leaf_edges += 1
                        target_type = 'sprite_record'
                    component_rows.append([
                        slot, bundle, entry_index, group_index, local_index, record_index,
                        record['sprite_index'], record['offset_x'], record['offset_y'],
                        record['control'], target_type,
                        'in_range' if (record['sprite_index'] < len(groups) if nested else record['sprite_index'] < sprite_count) else 'out_of_range'
                    ])

            for root_group in range(len(groups)):
                leaves, expansion_errors = expand_group(root_group, components, groups)
                for ordinal, sprite_index in enumerate(leaves):
                    group_leaf_rows.append([
                        slot, bundle, entry_index, root_group, ordinal, sprite_index,
                        'in_range' if sprite_index < sprite_count else 'out_of_range',
                        len(expansion_errors)
                    ])

            animation_frame_refs = 0
            animation_record_count = len(x['five']) // 5
            for sequence_index, (frame_count, first_record) in enumerate(sequences):
                for frame_index in range(frame_count):
                    record_index = first_record + frame_index
                    if record_index < 0 or record_index >= animation_record_count:
                        animation_rows.append([slot, bundle, entry_index, sequence_index, frame_index,
                                               record_index, '', '', '', '', 'invalid_record'])
                        continue
                    p = record_index * 5
                    raw_group, duration, ox, oy, flags = x['five'][p:p+5]
                    group = None if raw_group == 255 else raw_group
                    status = 'no_group_sentinel' if group is None else ('in_range' if group < len(groups) else 'out_of_range')
                    animation_rows.append([slot, bundle, entry_index, sequence_index, frame_index,
                                           record_index, raw_group, duration, signed_byte(ox),
                                           signed_byte(oy), flags, status])
                    if group is not None and group < len(groups):
                        animation_frame_refs += 1
                        leaves, errors = expand_group(group, components, groups)
                        for ordinal, sprite_index in enumerate(leaves):
                            draw_rows.append([slot, bundle, entry_index, sequence_index, frame_index,
                                              record_index, group, ordinal, sprite_index,
                                              'in_range' if sprite_index < sprite_count else 'out_of_range'])

            # Use the exact Build232 resource-index inventory for consumer presence;
            # no offset is fabricated when a row has no per-index offsets.
            consumer_evidence = consumer_map.get(slot, [])
            consumer_status = 'indexed_by_build232' if consumer_evidence else 'no_direct_i_D_render_consumer'
            summary.append([
                slot, bundle, entry_index, ';'.join(map(str, consumer_evidence)), len(consumer_evidence),
                ';'.join(all_consumer_sites.get(slot, [])), len(all_consumer_sites.get(slot, [])), consumer_status,
                sprite_count, len(groups), len(components), len(sequences), animation_record_count,
                direct_leaf_edges, nested_edges, component_errors, animation_frame_refs,
            ])

    write_csv(ROOT / 'research/build235_resource_binding_summary.csv',
        ['global_f_slot','bundle','entry_index','i_D_render_bytecode_offsets','i_D_consumer_offset_count',
         'all_original_consumer_sites','all_original_consumer_site_count','consumer_evidence_status',
         'sprite_record_count','composite_group_count','component_record_count','animation_sequence_count',
         'animation_record_count','direct_leaf_component_edges','nested_composite_edges',
         'invalid_component_records','valid_animation_frame_group_refs'], summary)
    write_csv(ROOT / 'research/build235_composite_component_bindings.csv',
        ['global_f_slot','bundle','entry_index','group_index','component_index','component_record_index',
         'target_index','offset_x_signed','offset_y_signed','control_byte','target_type','target_range_status'], component_rows)
    write_csv(ROOT / 'research/build235_animation_group_bindings.csv',
        ['global_f_slot','bundle','entry_index','sequence_index','frame_index','animation_record_index',
         'raw_group_index','duration_units','offset_x_signed','offset_y_signed','control_flags','group_status'], animation_rows)
    write_csv(ROOT / 'research/build235_composite_group_leaf_expansion.csv',
        ['global_f_slot','bundle','entry_index','root_group_index','leaf_ordinal','sprite_record_index',
         'sprite_range_status','expansion_error_count'], group_leaf_rows)
    write_csv(ROOT / 'research/build235_animation_leaf_draw_bindings.csv',
        ['global_f_slot','bundle','entry_index','sequence_index','frame_index','animation_record_index',
         'composite_group_index','leaf_ordinal','sprite_record_index','sprite_range_status'], draw_rows)

    print(f'slots={len(summary)} sprite_records={sum(int(r[8]) for r in summary)} '
          f'component_edges={len(component_rows)} animation_frame_rows={len(animation_rows)} '
          f'animation_leaf_rows={len(draw_rows)} group_leaf_rows={len(group_leaf_rows)}')
    print('component_errors=', sum(int(r[15]) for r in summary))
    print('animation_group_refs=', sum(int(r[16]) for r in summary))
    print('out_of_range_component_targets=', sum(r[-1] == 'out_of_range' for r in component_rows))
    print('out_of_range_animation_groups=', sum(r[-1] == 'out_of_range' for r in animation_rows))

if __name__ == '__main__':
    main()
