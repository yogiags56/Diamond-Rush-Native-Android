# Build 253 — CFG Predecessor State Merge Audit

## Purpose
Join Build220 CFG edges and Build221 instruction-entry abstract states to the 25 renderer callsites identified in Build248.

## Results
- Renderer callsites inspected: 25
- Callsite targets with all predecessor stack depths consistent: 0
- Targets with missing predecessor abstract states: 0
- Targets with conflicting predecessor stack depths: 0
- All 25 remain unpromoted; argument values and composite groups remain UNKNOWN.

## Interpretation boundary
This is a conservative predecessor-state audit, not a complete JVM worklist interpreter. It does not propagate newly computed states through the CFG and does not establish invocation argument values. Build221's abstract interpreter has known unmodeled opcodes and no exception edges. Depth consistency is a structural check, not proof of stack-value equivalence.

## Next
Build254 should implement iterative worklist propagation over basic blocks with explicit abstract values, stack-shape merge, local-variable merge, and conservative UNKNOWN propagation. It must model opcodes encountered on paths into renderer callsites and reject inconsistent JVM stack shapes.
