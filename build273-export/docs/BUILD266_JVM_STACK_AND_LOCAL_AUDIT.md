# Build266 — JVM stack-shape contracts and local provenance audit

## Scope

Build266 extends the Build265 evidence package in two narrow areas:

1. The callsite CSV now includes the local-variable snapshot at each renderer invocation, so unresolved values can be tied to specific local slots rather than only appearing as anonymous stack `UNKNOWN` values.
2. A standalone JVM computational-stack contract module models legal category-1/category-2 forms for `pop`, `pop2`, `dup`, `dup_x1`, `dup_x2`, `dup2`, `dup2_x1`, `dup2_x2`, and `swap`. Invalid category combinations and underflow raise explicit errors.

This is a tested semantic helper, not a full JVM verifier and not yet integrated as a replacement execution engine for the Build265 worklist.

## Key result: c.a(Graphics, byte[], int), offset 873

The invoke stack still contains two unresolved integer operands. The new local snapshot identifies their corresponding local slots:

- local 0: `UNKNOWN`
- local 4: `UNKNOWN`
- local 2: symbolic `i2s(CALL[i.a](...))`
- local 5: symbolic `i2s(CALL[i.a](...))`

The bytecode around the callsite shows local 0 is assigned at offset 817 and local 4 at offset 836; the interpreter's merged incoming state still cannot preserve a unique symbolic expression for those slots. The values are therefore deliberately not guessed. The local snapshot is a provenance checkpoint, not proof of concrete runtime values.

## Stack contracts

The new helper represents each computational value with width 1 or 2 JVM slots. It covers the legal category forms of the listed stack-manipulation instructions and rejects invalid forms explicitly. Fifteen focused tests cover valid category combinations, invalid category combinations, and underflow.

## Validation

- Build265 interpreter rerun: 8/8 callsites reachable; 8/8 descriptor stack depths sufficient; 7/8 all operands symbolically expressed.
- Full project pytest: recorded separately in `BUILD266_TEST_RESULTS.txt`.
- No Kotlin compile, Android Gradle build, device runtime, room rasterization, visual parity, or APK packaging is claimed.

## Limitations

- Category-2 helper is not yet wired into the legacy string-based abstract interpreter.
- Exception-table parsing and exceptional control-flow edges remain pending.
- The two unresolved locals at c offset 873 still require path-sensitive producer/merge analysis.
- Interprocedural method effects and concrete runtime field/array contents remain unknown.
