import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'research'))
import build270_jvm_integer_semantics as jvm


def test_signed_short_narrowing_boundaries():
    assert jvm.s16(0x7fff) == 32767
    assert jvm.s16(0x8000) == -32768
    assert jvm.s16(0xffff) == -1
    assert jvm.s16(0x18001) == -32767


def test_jvm_int_overflow_wraps_at_32_bits():
    assert jvm.i32(0x7fffffff + 1) == -2147483648
    assert jvm.jvm_mul(0x40000000, 4) == 0
    assert jvm.jvm_add(2147483647, 1) == -2147483648


def test_idiv_truncates_toward_zero_not_python_floor():
    assert jvm.idiv(-7, 3) == -2
    assert jvm.idiv(7, -3) == -2
    assert jvm.idiv(-7, -3) == 2


def test_idiv_jvm_overflow_corner_case():
    assert jvm.idiv(jvm.INT_MIN, -1) == jvm.INT_MIN


def test_idiv_zero_raises_jvm_arithmetic_exception():
    with pytest.raises(jvm.ArithmeticException, match='/ by zero'):
        jvm.idiv(12, 0)


def test_case4_interpolation_matches_weighted_formula():
    values=jvm.InterpolationInputs(v2=10,v4=30,v6=50,v6b=70,v14=100,instance_b=25)
    # x=(50*25 + 10*75)/100 = 20; y=(70*25 + 30*75)/100 = 40
    assert jvm.evaluate_case4(values) == (20,40)


def test_case4_interpolation_clamps_weight_to_v14():
    values=jvm.InterpolationInputs(v2=10,v4=30,v6=50,v6b=70,v14=100,instance_b=150)
    assert jvm.evaluate_case4(values) == (50,70)


def test_case4_zero_v14_preserves_exception_behavior():
    values=jvm.InterpolationInputs(v2=1,v4=2,v6=3,v6b=4,v14=0,instance_b=5)
    with pytest.raises(jvm.ArithmeticException):
        jvm.evaluate_case4(values)


def test_case4_operands_are_signed_short_before_interpolation():
    values=jvm.InterpolationInputs(v2=65546,v4=65566,v6=65586,v6b=65606,v14=65636,instance_b=25)
    assert jvm.evaluate_case4(values) == (20,40)
