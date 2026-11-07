from pathlib import Path
import csv
R=Path(__file__).resolve().parents[1]/"research"
def rows(n): return list(csv.DictReader((R/n).open()))
def test_bytecode_instruction_offsets_are_unique():
 x=rows("build255_renderer_instructions.csv");o=[int(r["offset"]) for r in x]
 assert len(o)==3811 and len(o)==len(set(o))
def test_basic_blocks_partition_instruction_stream():
 ins=rows("build255_renderer_instructions.csv"); blocks=rows("build255_renderer_basic_blocks.csv")
 owner=[]
 for b in blocks:
  members=[r for r in ins if int(b["block_start"])<=int(r["offset"])<=int(b["block_end"])]
  assert len(members)==int(b["instruction_count"])
  assert members[0]["instruction"]==b["first_instruction"]
  assert members[-1]["instruction"]==b["last_instruction"]
  owner.extend(int(x["offset"]) for x in members)
 assert sorted(owner)==sorted(int(r["offset"]) for r in ins)
def test_all_renderer_callsites_mapped():
 x=rows("build255_callsite_basic_block_map.csv")
 assert len(x)==25 and all(r["mapping"]=="EXACT" and r["instruction_is_renderer_invoke"]=="TRUE" for r in x)
def test_cfg_edges_reference_real_blocks():
 starts={int(x["block_start"]) for x in rows("build255_renderer_basic_blocks.csv")}
 assert all(int(x["source_block"]) in starts and int(x["target_block"]) in starts for x in rows("build255_renderer_cfg_edges.csv"))
def test_switch_edges_exist():
 assert any(x["edge_type"]=="switch" for x in rows("build255_renderer_cfg_edges.csv"))
