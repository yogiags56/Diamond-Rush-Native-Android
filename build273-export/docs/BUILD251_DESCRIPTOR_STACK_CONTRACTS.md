# Build 251 — Descriptor Stack Contracts

Build251 parses JVM method descriptors and verifies the operand-slot count consumed by each of the 25 known renderer callsites. It correctly counts category-2 `long` and `double` values as two JVM slots, while references and integer-family values consume one.

Results: all 25 Build250 invocation descriptors satisfy their expected receiver-plus-argument slot contracts. The six-integer overload consumes 8 slots including receiver; the seven-integer overload consumes 9.

This milestone deliberately does not claim to interpret the actual runtime operand stack. Descriptor arity constrains a call but cannot recover values or prove composite-group selection. All callsite composite groups remain UNKNOWN.

Run `python research/build251_descriptor_stack_contracts.py` and `python -m pytest -q`.
