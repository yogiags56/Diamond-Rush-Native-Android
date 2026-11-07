# Diamond Rush Native Android Port — Roadmap through Build 256

- Builds 198–239: resource decoding, sprite/composite raster foundations, animation and viewport reconstruction.
- Builds 240–244: room structure and resource candidate census.
- Builds 245–247: renderer callsite inventory and callee overload semantics.
- Builds 248–252: caller producer provenance and conservative slice replay.
- Builds 253–254: CFG join audit and method identity reconciliation.
- Build 255: found exact `i.D()V`, but initial parser included numeric switch labels as fake instructions.
- Build 256: corrected instruction extraction; 3,811 real instructions, 322 blocks, 564 edges, 10 switches, all 25 callsites mapped. Added CFG integrity validation.

## Next: Build 257 — Worklist Abstract Interpreter
Build a fail-closed JVM abstract interpreter over the corrected CFG. Start with a small verified opcode subset, preserve unknown values, merge stacks/locals conservatively, and validate every transfer against descriptors. Exception edges and unsupported instructions must remain explicit barriers until modeled.
