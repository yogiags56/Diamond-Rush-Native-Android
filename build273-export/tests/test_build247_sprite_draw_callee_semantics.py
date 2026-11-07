import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_build247_callee_semantics_audit_passes():
    result = subprocess.run(
        ['python', str(ROOT / 'research/build247_sprite_draw_callee_semantics.py')],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    assert 'PASS: 7-int delegates to 6-int recursive composite routine' in result.stdout
    assert 'PASS: 6-int dispatches leaf sprite to 4-int routine' in result.stdout
    assert 'PASS: 4-int draws image region' in result.stdout

def test_build247_semantics_are_explicitly_limited_to_callee():
    report = (ROOT / 'research/build247_sprite_draw_callee_semantics.txt').read_text()
    assert 'Caller-side values at individual i.D()V callsites remain a separate provenance task.' in report
