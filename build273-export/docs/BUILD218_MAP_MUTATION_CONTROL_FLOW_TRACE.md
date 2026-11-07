# Build 218 — Map Mutation Control-Flow Trace

## Scope

Build 218 converts the Build 217 map-plane inventory into an instruction-level branch-edge index and a candidate map-write-site catalogue. It does not claim that every `bastore`/`iastore` in a map-related method writes to a map plane. The JVM operand stack must be traced to prove each store target.

## 1. Audit coverage

- 66 methods in `i.class` contain references to at least one of the five map planes.
- 552 `bastore`/`iastore` instructions occur within those methods.
- 458 stores have a nearby reference to one of the five map-plane fields within the conservative 18-line inspection window. These are **candidate attributions**, not stack-verified facts.
- 94 stores do not have a nearby map-plane field reference. Inspection of `f()` shows examples that write to local arrays or unrelated fields, so these must not be counted as confirmed map mutations.
- 7,143 instruction-level control-flow edges were extracted from conditional branches, gotos, and switch tables in the 66 methods.
- All 7,143 extracted branch targets resolve to actual bytecode instruction offsets in their respective methods.

## 2. Candidate store distribution

| Field | Candidate stores | Methods |
|---|---:|---:|
| `a:[[B` | 129 | 30 |
| `b:[[B` | 68 | 14 |
| `c:[[B` | 79 | 20 |
| `a:[[I` | 63 | 19 |
| `b:[[I` | 119 | 20 |


These counts identify candidate store targets based on the nearest field reference in the local instruction window. They are useful for prioritizing operand-stack tracing, not a substitute for it.

## 3. Highest-activity methods

| Method | All array stores in method | Candidate plane stores | Unresolved stores | Branch instructions |
|---|---:|---:|---:|---:|
| `private void aj();` | 112 | 112 | 0 | 468 |
| `private void j();` | 81 | 70 | 11 | 302 |
| `private void f();` | 57 | 2 | 55 | 498 |
| `private void as();` | 54 | 54 | 0 | 153 |
| `private void W();` | 35 | 34 | 1 | 523 |
| `private void aa();` | 33 | 18 | 15 | 174 |
| `private void ao();` | 20 | 20 | 0 | 66 |
| `private void am();` | 18 | 18 | 0 | 34 |
| `private boolean a(int, int, boolean);` | 17 | 17 | 0 | 131 |
| `private void ab();` | 13 | 13 | 0 | 22 |
| `private void d(byte);` | 12 | 12 | 0 | 13 |
| `private void e(byte);` | 10 | 10 | 0 | 46 |
| `private static void l(int, int);` | 9 | 9 | 0 | 0 |
| `private void l(int);` | 7 | 7 | 0 | 20 |
| `private void ap();` | 6 | 6 | 0 | 23 |

`aj()` is the highest-activity method in this pass: it contains 112 array-store instructions, with candidate references to all five map planes. It is the first target for deeper stack and state tracing. This does not yet establish its exact gameplay responsibility.

`j()` contains 81 stores and is a mixed state-machine/room-loading method. It includes initialization and post-load processing, so its writes must be separated by state branch before they are interpreted as runtime gameplay mutations.

`f()` contains 57 stores, but only two are near map-plane references in this pass. Many other stores initialize local arrays or unrelated state. This is a concrete example of why method-level store counts cannot be treated as map-mutation counts.

## 4. Control-flow edge extraction

`research/build218_map_mutation_cfg_edges.csv` contains instruction-level edges for the 66 map-related methods:

- conditional branches: taken and fallthrough edges;
- unconditional jumps: taken edges;
- `tableswitch`/`lookupswitch`: case and default edges.

The file is an edge index, not yet a fully reconstructed semantic state graph. Exception-handler edges and JVM operand-stack dataflow are not included in this milestone.

## 5. Central setter result

The Build 217 setter `a(short, short, byte, int)` directly writes to `a:[[B` and `b:[[I`. A descriptor search across the available Build 214 class disassemblies did not identify a direct call site to this exact descriptor. Therefore it is retained as a proven write primitive, but this milestone does not assume it is the universal mutation path.

## 6. What is now established

- Map-related methods and their branch structure are indexed.
- Store sites have bytecode offsets and nearby field/call/branch context.
- Switch and branch targets are validated against decoded instruction offsets.
- Candidate field references are separated from unresolved stores.
- High-activity methods are prioritized for operand-stack tracing.

## 7. What remains unresolved

- Exact operand-stack provenance for each candidate store.
- Semantic meaning of each map-plane value and bit.
- Which method corresponds to digging, falling, collecting, movement, enemy updates, or collision.
- Whether the central setter is used indirectly through interfaces/reflection or outside the available class disassemblies.
- Exception control flow and inter-method state propagation.
- Full before/after examples of actual gameplay mutations.

## 8. Next milestone — Build 219

1. Perform operand-stack-aware attribution for every candidate store in `aj()`, `as()`, `W()`, and `aa()`.
2. Split `j()` by its `tableswitch` state branches, separating room initialization from later runtime work.
3. Trace callers and callees around the highest-confidence mutation blocks.
4. Capture representative coordinate/index calculations feeding map writes.
5. Relate write values to the two cell-dispatch passes from Build 216.
6. Build a conservative cell/object binding table with explicit unknown values.

## Validation boundaries

- Static bytecode instruction/branch extraction: performed.
- Branch target validation: 7,143/7,143 resolved.
- Python regression suite: see `BUILD218_TEST_RESULTS.txt`.
- Kotlin compilation, Android Gradle, device runtime, visual parity, and APK: not performed.
