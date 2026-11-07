from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
JAVAP = ROOT / "research" / "build214_bytecode" / "i_build214_full.javap.txt"
TEXT = JAVAP.read_text(errors="replace")

def method_slice(start_marker, end_marker):
    start = TEXT.index(start_marker)
    end = TEXT.index(end_marker, start)
    return TEXT[start:end]

def switch_cases(method_text):
    lines = method_text.splitlines()
    found = []
    for i, line in enumerate(lines):
        m = re.search(r"(\d+): (tableswitch|lookupswitch)\s+\{", line)
        if not m:
            continue
        cases = []
        for row in lines[i+1:]:
            if "}" in row:
                break
            cm = re.match(r"\s*(-?\d+):\s*(-?\d+)\s*$", row)
            if cm:
                cases.append((int(cm.group(1)), int(cm.group(2))))
        found.append((int(m.group(1)), cases))
    return found

def test_two_distinct_visible_cell_dispatches_exist():
    d = method_slice("private void D();", "private void E();")
    switches = switch_cases(d)
    assert any(len(c) == 35 and c[0][0] == 3 and c[-1][0] == 37 for _, c in switches)
    assert any(len(c) == 50 and c[0][0] == 0 and c[-1][0] == 49 for _, c in switches)

def test_first_pass_uses_bj_dispatch_field():
    d = method_slice("private void D();", "private void E();")
    assert "Field bJ:I" in d
    assert "tableswitch   { // 3 to 37" in d

def test_second_pass_uses_bi_dispatch_field():
    d = method_slice("private void D();", "private void E();")
    assert "Field bI:I" in d
    assert "tableswitch   { // 0 to 49" in d

def test_first_pass_case_34_directly_references_f27():
    d = method_slice("private void D();", "private void E();")
    assert "34: 940" in d
    branch = d[d.index("940: getstatic"):d.index("967: aload_3")]
    assert "bipush        27" in branch
    assert "Field a:[Lf;" in branch

def test_first_pass_14_and_33_share_selector_path():
    d = method_slice("private void D();", "private void E();")
    assert "14: 967" in d and "33: 967" in d
    block = d[d.index("967: aload_3"):d.index("1064: aload_3")]
    assert "Field a:[[I" in block
    assert "bipush        8" in block and "bipush        22" in block

def test_second_pass_has_special_cases_31_32_36():
    d = method_slice("private void D();", "private void E();")
    assert "31: 6755" in d
    assert "32: 6820" in d
    assert "36: 6704" in d

def test_second_pass_uses_generic_f42_path():
    d = method_slice("private void D();", "private void E();")
    assert "bipush        80" in d
    assert "bipush        42" in d
    assert "Field a:[Lf;" in d

def test_second_pass_consumes_packed_high_metadata_and_byte54():
    d = method_slice("private void D();", "private void E();")
    assert "ldc           #5                  // int -268435456" in d
    assert "bipush        28" in d
    assert "bipush        54" in d
    assert "bipush        13" in d
    assert "bipush        7" in d
