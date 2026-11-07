import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'research/build235_sprite_room_composite_binding_audit.py'
spec = importlib.util.spec_from_file_location('build235_binding_audit', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def rows(name):
    with (ROOT / 'research' / name).open(newline='') as handle:
        return list(csv.DictReader(handle))


def test_build235_binds_all_ten_static_slots_to_87_sprite_records():
    summary = rows('build235_resource_binding_summary.csv')
    assert len(summary) == 10
    assert sum(int(row['sprite_record_count']) for row in summary) == 87
    assert all(row['bundle'] and row['entry_index'] != '' for row in summary)


def test_all_composite_component_records_and_leaf_expansions_are_in_range():
    components = rows('build235_composite_component_bindings.csv')
    leaves = rows('build235_composite_group_leaf_expansion.csv')
    assert len(components) == 843
    assert len(leaves) == 843
    assert all(row['target_range_status'] == 'in_range' for row in components)
    assert all(row['sprite_range_status'] == 'in_range' for row in leaves)
    assert sum(row['target_type'] == 'composite_group' for row in components) == 1


def test_animation_frames_resolve_to_valid_composite_groups_or_explicit_sentinel():
    frames = rows('build235_animation_group_bindings.csv')
    assert len(frames) == 85
    assert sum(row['group_status'] == 'in_range' for row in frames) == 82
    assert sum(row['group_status'] == 'no_group_sentinel' for row in frames) == 3
    assert not any(row['group_status'] == 'out_of_range' for row in frames)


def test_animation_frame_expansion_contains_only_valid_sprite_records():
    draw_rows = rows('build235_animation_leaf_draw_bindings.csv')
    assert len(draw_rows) == 719
    assert all(row['sprite_range_status'] == 'in_range' for row in draw_rows)


def test_only_proven_i_d_render_consumers_are_reported_as_such():
    summary = rows('build235_resource_binding_summary.csv')
    render_slots = {int(row['global_f_slot']) for row in summary if row['i_D_render_bytecode_offsets']}
    assert render_slots == {9, 10}
    # Other static slots still have independent original consumer sites.
    assert all(int(row['all_original_consumer_site_count']) > 0 for row in summary)


def test_consumer_catalog_is_parsed_from_the_checked_in_evidence():
    consumers = module.load_render_consumers()
    assert consumers[9] == [6107, 7236]
    assert consumers[10] == [6348, 6357, 6369]
