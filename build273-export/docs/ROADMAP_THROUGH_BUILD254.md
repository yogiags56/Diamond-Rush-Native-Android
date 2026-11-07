# Diamond Rush Native Android Port — Roadmap through Build 254

- Builds 198–239: resource decoding, sprite/composite raster foundations, animation and viewport reconstruction.
- Builds 240–244: room structure, resource candidate census, dynamic resource attribution.
- Builds 245–247: renderer callsite inventory and callee overload semantics.
- Builds 248–252: caller producer provenance, descriptor stack contracts, conservative symbolic producer-slice replay.
- Build 253: predecessor-state audit; direct join was not valid.
- Build 254: identified root cause — renderer callsites are labeled `i.D()V`, while existing CFG labels are `aj`, `as`, `W`, and `aa`. No exact method identity mapping exists.

## Next milestone
Build 255 must regenerate the CFG directly from the exact `i.D()V` method body in the original class file, or establish a verifiable class-file mapping from obfuscated method identifiers to analysis aliases. Only then can basic-block state propagation proceed safely.
