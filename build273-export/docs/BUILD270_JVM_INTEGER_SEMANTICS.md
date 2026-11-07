# Build270 — JVM integer semantics for case-4 interpolation

## Scope

Build270 adds an executable, deliberately narrow model of the arithmetic
semantics observed in the original bytecode slice for `c.a(Graphics, byte[], int)`.
It is not a full JVM interpreter or verifier.

## Implemented semantics

- signed 32-bit wraparound for `iadd`, `isub`, and `imul`;
- `idiv` truncation toward zero;
- JVM `INT_MIN / -1` behavior;
- division-by-zero exception behavior (`ArithmeticException`);
- `i2s` signed 16-bit narrowing;
- the audited `min(this.b, v14)` interpolation weight;
- evaluation of the two formulas feeding locals 0 and 4 at renderer callsite 873.

The input values representing byte-array reads are narrowed to signed 16-bit at
the same points established by Build269's `i2s` instructions. Arithmetic between
those conversions uses JVM 32-bit integer behavior.

## Formula model

`x = S16(idiv(i32(i32(v6*m) + i32(v2*i32(v14-m))), v14))`

`y = S16(idiv(i32(i32(v6b*m) + i32(v4*i32(v14-m))), v14))`

where `m = min(this.b, v14)` and each `v*` is first narrowed with `i2s`.

## Validation

The focused tests cover signed-short boundaries, 32-bit overflow, negative
integer division, the JVM division overflow corner case, divide-by-zero,
interpolation arithmetic, clamp behavior, and input narrowing.

Concrete game values remain runtime-dependent. This module validates semantics;
it does not infer byte-array contents or claim that the entire method has been
verified against a JVM implementation.

## Android status

No Android Gradle application, Activity, APK, device runtime, full-room rendering,
or visual parity is claimed by Build270.
