"""Build271: expand room/resource/composite joins into auditable candidate draw plans.

This deliberately preserves ambiguity: Build244 dispatch/resource joins are
candidate-only, not proof that a particular resource/group is selected at runtime.
"""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_rows():
    candidates = read_csv(RESEARCH / "build244_w0_room0_dynamic_candidate_join.csv")
    components = read_csv(RESEARCH / "build243_dynamic_composite_component_attribution.csv")
    component_map = {}
    for comp in components:
        key = (int(comp["global_slot"]), int(comp["group_index"]))
        component_map.setdefault(key, []).append(comp)

    rows = []
    for candidate in candidates:
        slot = int(candidate["global_f_slot_candidate"])
        group = int(candidate["composite_group_candidate"])
        for comp in component_map.get((slot, group), []):
            dx = int(comp["offset_x_signed"])
            dy = int(comp["offset_y_signed"])
            anchor_x = int(candidate["screen_x"])
            anchor_y = int(candidate["screen_y"])
            rows.append({
                "room_row": candidate["row"],
                "room_column": candidate["column"],
                "selector_bj": candidate["map_selector_bj"],
                "anchor_screen_x": anchor_x,
                "anchor_screen_y": anchor_y,
                "global_f_slot_candidate": slot,
                "resource_path": candidate["resource_path"],
                "record_index": candidate["record_index"],
                "composite_group_candidate": group,
                "component_index": comp["component_index"],
                "component_record": comp["absolute_component_record"],
                "record_kind": comp["record_kind"],
                "sprite_or_nested_group_index": comp["sprite_or_nested_group_index"],
                "offset_x_signed": dx,
                "offset_y_signed": dy,
                "candidate_destination_x": anchor_x + dx,
                "candidate_destination_y": anchor_y + dy,
                "control_byte": comp["control_byte"],
                "selection_status": "CANDIDATE_ONLY_NO_RUNTIME_SELECTION_PROOF",
                "transform_status": "NOT_RESOLVED_FROM_THIS_JOIN",
            })
    return rows


def main():
    rows = build_rows()
    out = RESEARCH / "build271_w0_room0_candidate_draw_plan.csv"
    fields = list(rows[0]) if rows else []
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    cells = {(r["room_row"], r["room_column"]) for r in rows}
    groups = {(r["global_f_slot_candidate"], r["composite_group_candidate"]) for r in rows}
    print(f"CANDIDATE_DRAW_ROWS={len(rows)}")
    print(f"ROOM_CELLS_WITH_CANDIDATE_DRAW_ROWS={len(cells)}")
    print(f"RESOURCE_GROUP_PAIRS={len(groups)}")
    print(f"RECORD_KINDS={sorted({r['record_kind'] for r in rows})}")
    print("SELECTION_STATUS=CANDIDATE_ONLY_NO_RUNTIME_SELECTION_PROOF")
    print("TRANSFORM_STATUS=NOT_RESOLVED_FROM_THIS_JOIN")


if __name__ == "__main__":
    main()
