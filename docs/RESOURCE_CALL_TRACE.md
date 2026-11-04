# Resource loader call trace — Build 09

This trace was taken from `javap -c -p i` on the supplied original JAR, then checked against the extracted `.f` container inventory.

## Exact loader contract

The original public helper `i.a(String, int)` performs these operations:

1. Opens the named classpath resource with `getResourceAsStream`.
2. Reads its first byte `N` and allocates `N * 8` bytes for the section index.
3. Reads the index table.
4. Computes the selected record address as `sectionIndex * 8`.
5. Reads a 32-bit little-endian offset and a 32-bit little-endian length from that record (through helper `i.b(byte[], int)`).
6. Skips the offset from the beginning of the payload area, then reads `length` bytes.

The sprite-loading overload `i.a(String, int, int, int)` then constructs `f`, calls `f.a(payload, 0)`, and materializes each requested group using `f.a(group, 0, -1, -1)`.

This confirms the key boundary: `f` receives one selected section payload, not the complete `.f` container. The extraction tool's section files represent those payloads.

## Concrete call sites observed in `i.b(int)`

The bytecode contains the following resource/section selections. The first column is the resource string, the second is the section index passed to `i.a(String,int)`, and the third notes the use visible at the call site.

| Resource | Section index | Observed use |
|---|---:|---|
| `/mmv.f` | 0 | Loaded into sprite decoder; group 0 materialized |
| `/mmv.f` | 5 | Loaded into sprite decoder; group 0 materialized |
| `/mmv.f` | 4 | Loaded into sprite decoder; group 0 materialized |
| `/mmv.f` | 1 | Loaded into sprite decoder; group 0 materialized |
| `/mmv.f` | 2 | Loaded into sprite decoder; group 0 materialized |
| `/mmv.f` | 3 | Loaded into sprite decoder; group 0 materialized |
| `/ui.f` | 3 | Loaded into sprite decoder; group 0 materialized |
| `/0.f` | 3 | Dynamically constructed resource name; group 0 materialized |
| `/cm.f` | 2 | Loaded; groups 0 and 1 materialized |
| `/ms.f` | 0 | Loaded into sprite decoder; group 0 materialized |
| `/cm.f` | 7 | Loaded into sprite decoder; group 0 materialized |

A separate call loads `/cr.f`, section 0, as a raw byte array rather than through the sprite decoder. This is direct evidence that not every `.f` resource is necessarily a sprite payload.

## Important limitations

- These are concrete calls from one method/state dispatcher, not a complete inventory of every resource call in the game.
- The section index alone does not identify semantic content (character, menu, tiles, effects). That requires tracing the consumer and sprite indices.
- The trace establishes the payload handoff and group materialization call. It does not prove the current Python header parser has correctly mapped every later field.
- No replacement Android Bitmap decoder has been validated yet.

## Verification

The original JAR was disassembled locally. The existing extracted section corpus contains `/mmv.f` sections 0–5, `/ui.f` section 3, `/0.f` section 3, `/cm.f` sections 2 and 7, `/ms.f` section 0, and `/cr.f` section 0. The complete existing Python regression suite passes (12 tests).
