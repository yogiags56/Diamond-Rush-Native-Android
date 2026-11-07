# Diamond Rush Native Android Port — Roadmap through Build 255

- Builds 198–239: resource decoding, sprite/composite raster foundations, animation and viewport reconstruction.
- Builds 240–244: room structure, resource candidate census, dynamic resource attribution.
- Builds 245–247: renderer callsite inventory and callee overload semantics.
- Builds 248–252: caller producer provenance, descriptor stack contracts, conservative producer-slice replay.
- Builds 253–254: CFG join audit and method identity reconciliation; prior CFG aliases were not the renderer method.
- Build 255: extracted exact `i.D()V` from `original.jar`; rebuilt 3,925 instructions, 325 basic blocks, 566 CFG edges; parsed 10 switch instructions; mapped all 25 renderer callsites.

## Next: Build 256 — CFG Worklist Abstract Interpretation
Implement a conservative instruction-level worklist over the verified `i.D()V` CFG. Merge operand stacks and locals with explicit TOP/UNKNOWN states, include all switch edges, preserve unresolved branch paths, and validate callsite stack shapes against Build251 descriptors. Do not promote any draw arguments unless all incoming paths agree on value and provenance.
