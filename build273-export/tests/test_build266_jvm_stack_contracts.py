import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research"))
from build266_jvm_stack_contracts import (
    Value, StackShapeError, pop, pop2, dup, dup_x1, dup_x2, dup2,
    dup2_x1, dup2_x2, swap,
)
A=Value('A'); B=Value('B'); C=Value('C'); D=Value('D'); L=Value('L',2); D2=Value('D2',2)
def test_category_two_pop2(): assert pop2([L]) == []
def test_pop2_two_category_one(): assert pop2([A,B]) == []
def test_pop_rejects_category_two():
    with pytest.raises(StackShapeError): pop([L])
def test_dup_category_one(): assert dup([A]) == [A,A]
def test_dup_rejects_category_two():
    with pytest.raises(StackShapeError): dup([L])
def test_dup_x1_form(): assert dup_x1([A,B]) == [B,A,B]
def test_dup_x2_category_two_form(): assert dup_x2([L,A]) == [A,L,A]
def test_dup2_category_two_form(): assert dup2([L]) == [L,L]
def test_dup2_two_category_one_form(): assert dup2([A,B]) == [A,B,A,B]
def test_dup2_x1_category_two_form(): assert dup2_x1([A,L]) == [L,A,L]
def test_dup2_x2_category_two_over_category_two(): assert dup2_x2([L,D2]) == [D2,L,D2]
def test_dup2_x2_two_category_one_over_two_category_one(): assert dup2_x2([C,D,A,B]) == [A,B,C,D,A,B]
def test_swap_category_one(): assert swap([A,B]) == [B,A]
def test_swap_rejects_category_two():
    with pytest.raises(StackShapeError): swap([L,A])
def test_stack_underflow_is_explicit():
    with pytest.raises(StackShapeError): dup([])
