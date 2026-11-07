# Build 217 — Room Data Plane Loading and Mutation Trace

## Scope

Build 217 traces the selected room record in `i.j()` and the public static cell setter `i.a(short, short, byte, int)`. It establishes the binary shape and the minimal proven write contract for the core map planes. It does not yet decode every cell value into gameplay semantics.

## 1. Room record selection and dimensions

The room loader obtains an `InputStream` from a resource path selected through the game's resource-name table. It reads a four-byte room header, then calls `i.a(byte[], int)` at offsets 0 and 2 to obtain the two dimensions.

That helper combines two unsigned bytes in little-endian order:

`value = (b[offset] & 0xFF) | ((b[offset + 1] & 0xFF) << 8)`

The dimensions are stored in instance fields `e` and `f`. The bytecode uses them as the first and second dimensions of the map arrays. We preserve the original field names because their semantic names have not been proven.

## 2. Serialized per-cell data

For the selected room, the loader allocates and fills these planes:

| Field | JVM type | Load behavior established |
|---|---|---|
| `a:[[B` | `byte[][]` | Filled from the first width×height byte payload |
| `b:[[I` | `int[][]` | Filled from the second width×height byte payload |
| `a:[[I` | `int[][]` | Filled from the third width×height byte payload |

The two integer planes are populated using `baload` followed by `iastore`. This means the source byte is sign-extended when stored as an integer. Do not silently normalize those values to unsigned 0–255 before a complete consumer audit.

For non-selected room records, the loader skips `width × height × 3` bytes after reading the four-byte dimension header. This is direct evidence that the serialized per-cell payload contains three byte planes.

## 3. Runtime byte overlays

The loader also allocates `b:[[B` and `c:[[B` as separate byte-array planes. During the selected-room post-processing branch, the code initializes cells in these planes to zero. These are distinct from the three serialized source planes above.

The current evidence supports treating `b:[[B` and `c:[[B` as runtime working/overlay planes, but their exact gameplay names and all consumers remain unresolved.

## 4. Central cell setter

The method `public static void a(short, short, byte, int)` is a compact write primitive:

- first short indexes the first dimension;
- second short indexes the cell within that row;
- byte argument is written to `a:[[B`;
- integer argument is written to `b:[[I`.

This establishes that the primary byte plane and one integer plane are updated together by this API. It does **not** establish that all map mutations use this setter; the bytecode contains many additional direct writes in gameplay methods.

## 5. Additional mutation-site inventory

`research/build217_map_plane_method_inventory.csv` records methods that reference one or more of the five map planes, alongside byte/int store counts. It is a method-level index for the next tracing pass, not a complete statement-level data-flow graph.

Direct mutation is visible in gameplay/update methods such as `f()`, `M()`, `W()`, `aa()`, `ab()`, `aj()`, and `as()`. Several of these contain multiple `bastore`/`iastore` operations. Their exact event meanings need call-site and state analysis before they can be assigned to movement, digging, falling, collection, enemies, or effects.

## 6. What is now safe to implement

A native map model can preserve:
- the two room dimensions without changing their original byte order;
- the primary signed byte plane;
- both signed integer planes, retaining all original values;
- two independent runtime byte overlays;
- atomic updates of the `a:[[B` and `b:[[I` pair when the central setter is used.

Do not collapse the planes into one `tileId`, discard sign information, or infer semantic names from numeric values alone.

## 7. Roadmap position

The project is in **Stage 3: Gameplay Engine Reconstruction**. The resource decoding and sprite renderer foundations are substantially audited; room loading and cell dispatch are now partially understood. A complete game simulation, native scene runtime, input/state parity, and Android integration are still outstanding.

## 8. Next milestone — Build 218

1. Build a control-flow-aware map write graph for direct stores in gameplay methods.
2. Trace which operations call the central setter and which bypass it.
3. Track representative cell changes across movement and object-state methods.
4. Decode the post-load room scan beginning at the selected room's post-processing branch.
5. Relate packed integer plane values to consumers without dropping unknown bits.
6. Add small deterministic before/after fixtures for proven mutations.

## Validation boundaries

- Static bytecode inspection: performed.
- Python regression suite: see `BUILD217_TEST_RESULTS.txt`.
- Kotlin compilation: not performed.
- Android Gradle build: not performed.
- Emulator/device runtime, gameplay parity, and APK: not performed.
