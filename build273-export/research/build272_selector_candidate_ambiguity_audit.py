"""Build272: quantify W0 room0 selector-to-resource ambiguity without guessing.

The source join contains CFG-reachable candidate sets, not runtime selection.
This audit groups the existing evidence by raw bJ selector and room cell and
makes ambiguity explicit. It deliberately does not choose a resource/group.
"""
from __future__ import annotations
import csv
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
SOURCE = RESEARCH / "build244_w0_room0_dynamic_candidate_join.csv"


def read_rows():
    with SOURCE.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def audit(rows):
    by_selector = defaultdict(list)
    by_cell = defaultdict(list)
    for r in rows:
        by_selector[int(r["map_selector_bj"])].append(r)
        by_cell[(int(r["row"]), int(r["column"]))].append(r)

    selector_rows = []
    for selector, items in sorted(by_selector.items()):
        resources = sorted({(int(x["global_f_slot_candidate"]), x["resource_path"], int(x["record_index"])) for x in items})
        groups = sorted({(int(x["global_f_slot_candidate"]), int(x["composite_group_candidate"])) for x in items})
        targets = sorted({int(x["branch_target"]) for x in items})
        selector_rows.append({
            "raw_bj_selector": selector,
            "branch_targets": ";".join(map(str, targets)),
            "candidate_row_count": len(items),
            "candidate_resource_count": len(resources),
            "candidate_resources": ";".join(f"f[{slot}]={path}#record{record}" for slot, path, record in resources),
            "candidate_resource_group_pair_count": len(groups),
            "candidate_resource_group_pairs": ";".join(f"f[{slot}]/group{group}" for slot, group in groups),
            "selection_status": "AMBIGUOUS_CANDIDATE_SET_NOT_RUNTIME_SELECTION",
        })

    cell_rows = []
    for (row, col), items in sorted(by_cell.items()):
        selectors = sorted({int(x["map_selector_bj"]) for x in items})
        resources = sorted({(int(x["global_f_slot_candidate"]), x["resource_path"], int(x["record_index"])) for x in items})
        groups = sorted({(int(x["global_f_slot_candidate"]), int(x["composite_group_candidate"])) for x in items})
        cell_rows.append({
            "room_row": row, "room_column": col,
            "selector_values": ";".join(map(str, selectors)),
            "candidate_row_count": len(items),
            "candidate_resource_count": len(resources),
            "candidate_resource_slots": ";".join(str(x[0]) for x in resources),
            "candidate_resource_group_pair_count": len(groups),
            "selection_status": "AMBIGUOUS_CANDIDATE_SET_NOT_RUNTIME_SELECTION",
        })

    return selector_rows, cell_rows


def write_csv(path, rows):
    if not rows:
        raise RuntimeError(f"No rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def main():
    rows = read_rows()
    selector_rows, cell_rows = audit(rows)
    write_csv(RESEARCH / "build272_selector_candidate_summary.csv", selector_rows)
    write_csv(RESEARCH / "build272_cell_candidate_ambiguity.csv", cell_rows)
    print(f"SOURCE_CANDIDATE_ROWS={len(rows)}")
    print(f"RAW_BJ_SELECTORS={len(selector_rows)}")
    print(f"ROOM_CELLS={len(cell_rows)}")
    print(f"SELECTOR_RESOURCE_BINDINGS_PROVEN=0")
    print(f"CELLS_WITH_MULTIPLE_CANDIDATE_RESOURCES={sum(int(x['candidate_resource_count']) > 1 for x in cell_rows)}")
    print("RUNTIME_SELECTION=UNRESOLVED")


if __name__ == "__main__":
    main()
