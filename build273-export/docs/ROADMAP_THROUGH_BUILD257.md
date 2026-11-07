# Diamond Rush Native Android Port — Roadmap through Build 257

- Builds 198–239: resource decoding, sprite/composite raster foundations, animation and viewport reconstruction.
- Builds 240–244: room structure and resource candidate census.
- Builds 245–247: renderer callsite inventory and callee overload semantics.
- Builds 248–252: caller producer provenance and conservative slice replay.
- Builds 253–256: exact renderer method recovery, corrected CFG, CFG integrity.
- Build 257: initial conservative worklist state propagation over 322 blocks. 247 reachable, 20 stack-shape conflicts, 13/25 reachable callsite snapshots with sufficient raw depth. No argument tuples promoted.

## Next: Build 258 — Exception Edges and Verifier-Style State Merge
Extract exception tables from classfile Code attributes, include handler edges, and re-evaluate callsite reachability. Strengthen stack/local merge typing and category-2 handling. Preserve unresolved states; do not infer argument order from stack depth alone.
