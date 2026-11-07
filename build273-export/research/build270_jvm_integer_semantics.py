"""Build270: executable JVM int and signed-short semantics for Build269 formulas.

This module models only the arithmetic operations observed in the audited
bytecode slice. It is not a general JVM implementation.
"""
from dataclasses import dataclass

INT_MIN = -(1 << 31)
INT_MAX = (1 << 31) - 1

class ArithmeticException(ZeroDivisionError):
    """JVM-style integer division by zero."""


def i32(value: int) -> int:
    """Narrow an integer to a signed JVM 32-bit int."""
    value &= 0xFFFFFFFF
    return value - 0x100000000 if value & 0x80000000 else value


def s16(value: int) -> int:
    """JVM i2s semantics: retain low 16 bits and sign extend."""
    value &= 0xFFFF
    return value - 0x10000 if value & 0x8000 else value


def idiv(numerator: int, denominator: int) -> int:
    """JVM idiv: truncate toward zero, with JVM overflow corner case."""
    numerator = i32(numerator)
    denominator = i32(denominator)
    if denominator == 0:
        raise ArithmeticException("/ by zero")
    if numerator == INT_MIN and denominator == -1:
        return INT_MIN
    quotient = abs(numerator) // abs(denominator)
    if (numerator < 0) ^ (denominator < 0):
        quotient = -quotient
    return i32(quotient)


def jvm_add(a: int, b: int) -> int:
    return i32(i32(a) + i32(b))


def jvm_sub(a: int, b: int) -> int:
    return i32(i32(a) - i32(b))


def jvm_mul(a: int, b: int) -> int:
    return i32(i32(a) * i32(b))


@dataclass(frozen=True)
class InterpolationInputs:
    v2: int
    v4: int
    v6: int
    v6b: int
    v14: int
    instance_b: int


def _weighted(a: int, b: int, weight: int, limit: int) -> int:
    """Evaluate (a*weight + b*(limit-weight))/limit as JVM int ops, then i2s."""
    left = jvm_mul(a, weight)
    right = jvm_mul(b, jvm_sub(limit, weight))
    numerator = jvm_add(left, right)
    return s16(idiv(numerator, limit))


def evaluate_case4(inputs: InterpolationInputs) -> tuple[int, int]:
    """Return (local0, local4) using bytecode-observed case-4 operations."""
    v2, v4, v6, v6b, v14 = map(s16, (inputs.v2, inputs.v4, inputs.v6, inputs.v6b, inputs.v14))
    instance_b = i32(inputs.instance_b)
    weight = min(instance_b, v14)
    x = _weighted(v6, v2, weight, v14)
    y = _weighted(v6b, v4, weight, v14)
    return x, y
