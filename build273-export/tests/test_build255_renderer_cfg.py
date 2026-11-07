from pathlib import Path
import csv
R=Path(__file__).resolve().parents[1]/"research"
def rows(n): return list(csv.DictReader((R/n).open()))
def test_cfg_uses_actual_renderer_method():
 b=rows("build255_renderer_basic_blocks.csv"); e=rows("build255_renderer_cfg_edges.csv")
 assert len(b)==322 and len(e)>0
 assert {x["method"] for x in b}=={"i.D()V"}
def test_block_boundaries_are_real_instruction_offsets():
 ins={int(x["offset"]):x["instruction"] for x in rows("build255_renderer_instructions.csv")}
 for b in rows("build255_renderer_basic_blocks.csv"):
  assert int(b["block_start"]) in ins and int(b["block_end"]) in ins
  assert b["first_instruction"]==ins[int(b["block_start"])]
  assert b["last_instruction"]==ins[int(b["block_end"])]
def test_all_renderer_callsites_map_to_real_invokes():
 x=rows("build255_callsite_basic_block_map.csv")
 assert len(x)==25
 assert all(r["mapping"]=="EXACT" for r in x)
 assert all(r["instruction_is_renderer_invoke"]=="TRUE" for r in x)
def test_switch_edges_are_present():
 assert sum(r["edge_type"]=="switch" for r in rows("build255_renderer_cfg_edges.csv"))>0
