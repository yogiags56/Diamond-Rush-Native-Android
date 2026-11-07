# Roadmap Through Build 234

| Build | Milestone | Status |
|---|---|---|
| 223 | Native room map model | Complete |
| 224–225 | Logical canvas, camera, viewport traversal | Complete |
| 226–227 | Main render dispatch and typed resolver | Complete |
| 228–229 | Deterministic per-cell and room scene trace | Complete |
| 230 | Main-pass draw-command planner | Complete |
| 231 | Original room archive integration (41 records) | Complete |
| 232 | Numeric sprite-resource consumer attribution | Complete |
| 233 | Static bundle directory entry -> global `f[]` slot attribution | Complete |
| 234 | Exact DF03 resource parser reconstruction | Complete |
| 235 | Bind decoded sprite records to room/composite references | Next |
| 236 | Expand draw commands into concrete sprite operations | Planned |
| 237+ | Scene rasterization, HUD/menu/effects integration | Planned |
| Final | Android lifecycle/input/audio, device parity, APK | Not started |

## Build 234 correction and result

The previous parser used `count * 2` for a table whose original bytecode allocates `count << 2`. Correcting that interpretation fixed the payload cursor alignment. Both four-byte tables now use four bytes per record.

The corrected audit parses all 94 DF03 entries in the original JAR, indexes 1,372 sprites, accounts for 139,268 encoded pixel bytes, and reports no trailing bytes or parser failures.

The ten Build233 static global-slot mappings now resolve to 87 sprite records. Build235 will connect those records to room/composite consumers, preserving opaque fields until their use is demonstrated.
