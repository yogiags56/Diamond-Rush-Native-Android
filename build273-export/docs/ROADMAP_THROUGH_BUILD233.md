# Roadmap Through Build 233

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
| 234 | Reconstruct exact sprite payload decoder behavior for mapped entries | Next |
| 235 | Bind room cells to decoded sprite/composite records | Planned |
| 236 | Expand draw commands into concrete sprite operations | Planned |
| 237+ | Scene rasterization, HUD/menu/effects integration | Planned |
| Final | Android lifecycle/input/audio, device parity, APK | Not started |

## Build 233 findings

Ten direct static bundle-to-slot mappings are proven in `i.b(I)V`. The loader helper establishes an 8-byte resource-directory record and uses the supplied integer as a directory entry index.

Four dynamic assignment sites remain separate. The existing DF03 parser reports failures for all ten mapped payloads; Build 234 must resolve parser-layout gaps before claiming successful asset decoding.
