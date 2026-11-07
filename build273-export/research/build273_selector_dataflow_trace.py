"""Build273: trace W0 room0 bJ selectors through case logic and a(int) resolver.

This is a bytecode-evidence ledger, not execution of the original game.  It
models only facts directly established by the retained javap instruction
sequences: bJ source, switch target, aJ assignment, a(int) result, and explicit
f[] callsites. Runtime predicates remain conditional/unknown.
"""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
SOURCE = RESEARCH / "build244_w0_room0_dynamic_candidate_join.csv"

# Exact case facts transcribed from i_build214_full.javap.txt, method
# private void a(int,int,int,int,boolean), bytecode offsets 609 onward.
# helper mapping is from public static int a(int), offsets 0..206.
CASES = {
    3: dict(target=1890, aj="12 when (cell_word >> 8) - 1 >= 0; otherwise unchanged(-1)",
            helper_slot="NONE", helper_status="RESOLVES_TO_MINUS_ONE", direct="NONE",
            direct_guard="", evidence="case 1890-1927; helper switch 0-23/default"),
    4: dict(target=1549, aj="20 when (cell_word >> 8) >= this.aC; otherwise unchanged(-1)",
            helper_slot="43", helper_status="CONDITIONAL_DYNAMIC_RENDER", direct="NONE",
            direct_guard="cell high-byte >= this.aC", evidence="case 1549-1629; helper case 20 -> 43"),
    5: dict(target=1632, aj="NO_ASSIGNMENT", helper_slot="NONE",
            helper_status="NO_NEW_DYNAMIC_RENDER_SELECTION", direct="NONE", direct_guard="",
            evidence="case 1632-1639 diagnostic-only branch"),
    6: dict(target=1064, aj="26", helper_slot="NONE",
            helper_status="RESOLVES_TO_MINUS_ONE", direct="NONE", direct_guard="",
            evidence="case 1064-1360; helper default for 26"),
    7: dict(target=1416, aj="4", helper_slot="56",
            helper_status="DYNAMIC_RENDER_SLOT_56", direct="56",
            direct_guard="left-neighbor low byte is neither 9 nor 8",
            evidence="case 1416-1546; direct f[56] at 1501; helper case 4 -> 56"),
    8: dict(target=1796, aj="23", helper_slot="45",
            helper_status="DYNAMIC_RENDER_SLOT_45", direct="NONE", direct_guard="",
            evidence="case 1796-1887; helper case 23 -> 45"),
}


def read_rows():
    with SOURCE.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build(rows):
    selectors = sorted({int(r["map_selector_bj"]) for r in rows})
    out = []
    for selector in selectors:
        if selector not in CASES:
            raise ValueError(f"No exact bytecode trace recorded for selector {selector}")
        c = CASES[selector]
        cells = sorted({(int(r["row"]), int(r["column"])) for r in rows
                        if int(r["map_selector_bj"]) == selector})
        out.append({
            "raw_bj_selector": selector,
            "room_cell_count": len(cells),
            "switch_offset": 783,
            "branch_target": c["target"],
            "aj_assignment_or_expression": c["aj"],
            "dynamic_helper_f_slot": c["helper_slot"],
            "dynamic_helper_status": c["helper_status"],
            "direct_f_slot_call": c["direct"],
            "direct_call_guard": c["direct_guard"],
            "bytecode_evidence": c["evidence"],
            "resource_bundle_identity": "UNRESOLVED",
            "runtime_predicate_values": "UNKNOWN",
            "status": "BYTECODE_DATAFLOW_TRACED_RUNTIME_VALUES_NOT_EXECUTED",
        })
    return out


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def main():
    source_rows = read_rows()
    traced = build(source_rows)
    write_csv(RESEARCH / "build273_selector_dataflow_trace.csv", traced)
    by_selector = {int(r["raw_bj_selector"]): r for r in traced}
    cell_rows = []
    for source in source_rows:
        selector = int(source["map_selector_bj"])
        trace = by_selector[selector]
        cell_rows.append({
            "room_row": source["row"], "room_column": source["column"],
            "screen_x": source["screen_x"], "screen_y": source["screen_y"],
            "raw_bj_selector": selector, "branch_target": trace["branch_target"],
            "aj_assignment_or_expression": trace["aj_assignment_or_expression"],
            "dynamic_helper_f_slot": trace["dynamic_helper_f_slot"],
            "dynamic_helper_status": trace["dynamic_helper_status"],
            "direct_f_slot_call": trace["direct_f_slot_call"],
            "direct_call_guard": trace["direct_call_guard"],
            "resource_bundle_identity": "UNRESOLVED",
            "runtime_predicate_values": "UNKNOWN",
        })
    # The source join repeats rows for candidate groups; keep one row per room cell.
    unique = {(r["room_row"], r["room_column"]): r for r in cell_rows}
    cell_rows = [unique[k] for k in sorted(unique, key=lambda x: (int(x[0]), int(x[1])))]
    write_csv(RESEARCH / "build273_w0_room0_cell_selector_resolution.csv", cell_rows)
    direct = sum(r["direct_f_slot_call"] != "NONE" for r in traced)
    dynamic = sum(r["dynamic_helper_status"].startswith("DYNAMIC_RENDER_SLOT") for r in traced)
    print(f"ROOM_CELLS_TRACED={len(cell_rows)}")
    print(f"RAW_BJ_SELECTORS_TRACED={len(traced)}")
    print(f"SELECTORS_WITH_EXPLICIT_DIRECT_F_CALL={direct}")
    print(f"SELECTORS_WITH_RESOLVED_DYNAMIC_F_SLOT={dynamic}")
    print("RESOURCE_BUNDLE_IDENTITY=UNRESOLVED")
    print("RUNTIME_PREDICATE_VALUES=UNKNOWN")

if __name__ == "__main__":
    main()
