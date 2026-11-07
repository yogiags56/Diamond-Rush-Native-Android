"""Build266 JVM computational-stack shape helpers.

Values are (symbol, width) pairs, where width is 1 or 2 JVM slots.
This module models legal stack forms for pop/dup/swap instructions; it is
not a complete verifier or bytecode interpreter.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Value:
    symbol: str
    width: int = 1
    def __post_init__(self):
        if self.width not in (1, 2):
            raise ValueError('JVM computational value width must be 1 or 2')

class StackShapeError(ValueError):
    pass

def _take(stack, n):
    if len(stack) < n:
        raise StackShapeError('operand stack underflow')
    return list(stack[:-n]), list(stack[-n:])

def pop(stack):
    rest, (v,) = _take(stack, 1)
    if v.width != 1:
        raise StackShapeError('pop requires category-1 value')
    return rest

def pop2(stack):
    rest, vals = _take(stack, 1)
    if vals[-1].width == 2:
        return rest
    rest, second = _take(rest, 1)
    if second[-1].width != 1:
        raise StackShapeError('pop2 requires one category-2 or two category-1 values')
    return rest

def dup(stack):
    rest, (v,) = _take(stack, 1)
    if v.width != 1: raise StackShapeError('dup requires category-1 value')
    return rest + [v, v]

def dup_x1(stack):
    rest, (v2, v1) = _take(stack, 2)
    if v1.width != 1 or v2.width != 1: raise StackShapeError('dup_x1 requires two category-1 values')
    return rest + [v1, v2, v1]

def dup_x2(stack):
    rest, (v1,) = _take(stack, 1)
    if v1.width != 1: raise StackShapeError('dup_x2 top must be category-1')
    rest, (v2,) = _take(rest, 1)
    if v2.width == 2: return rest + [v1, v2, v1]
    rest, (v3,) = _take(rest, 1)
    if v3.width != 1: raise StackShapeError('invalid dup_x2 form')
    return rest + [v1, v3, v2, v1]

def dup2(stack):
    rest, (v1,) = _take(stack, 1)
    if v1.width == 2: return rest + [v1, v1]
    rest, (v2,) = _take(rest, 1)
    if v2.width != 1: raise StackShapeError('invalid dup2 form')
    return rest + [v2, v1, v2, v1]

def dup2_x1(stack):
    rest, (v1,) = _take(stack, 1)
    if v1.width == 2:
        rest, (v2,) = _take(rest, 1)
        if v2.width != 1: raise StackShapeError('invalid dup2_x1 form')
        return rest + [v1, v2, v1]
    rest, (v2,) = _take(rest, 1)
    rest, (v3,) = _take(rest, 1)
    if v1.width != 1 or v2.width != 1 or v3.width != 1: raise StackShapeError('invalid dup2_x1 form')
    return rest + [v3, v2, v1, v3, v2, v1]

def dup2_x2(stack):
    rest, (v1,) = _take(stack, 1)
    if v1.width == 2:
        rest, (v2,) = _take(rest, 1)
        if v2.width == 2: return rest + [v1, v2, v1]
        rest, (v3,) = _take(rest, 1)
        if v2.width != 1 or v3.width != 1: raise StackShapeError('invalid dup2_x2 form')
        return rest + [v1, v3, v2, v1]
    rest, (v2,) = _take(rest, 1)
    if v1.width != 1 or v2.width != 1: raise StackShapeError('invalid dup2_x2 form')
    rest, (v3,) = _take(rest, 1)
    if v3.width == 2: return rest + [v2, v1, v3, v2, v1]
    rest, (v4,) = _take(rest, 1)
    if v3.width != 1 or v4.width != 1: raise StackShapeError('invalid dup2_x2 form')
    return rest + [v2, v1, v4, v3, v2, v1]

def swap(stack):
    rest, (v2, v1) = _take(stack, 2)
    if v1.width != 1 or v2.width != 1: raise StackShapeError('swap requires two category-1 values')
    return rest + [v1, v2]
