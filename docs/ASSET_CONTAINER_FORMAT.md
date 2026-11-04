# Original `.f` resource container — verified extraction rules

Reverse-engineering is based on the original `i` class bytecode and its helper
`a(String, int)`, plus sprite decoder class `f`.

## Container layout

Each resource is a section container:

1. One unsigned byte: number of sections (`N`).
2. `N` index records, each 8 bytes:
   - 4-byte unsigned little-endian payload offset.
   - 4-byte unsigned little-endian payload length.
3. Concatenated payload area. Each record's offset is relative to the start of
   this payload area (immediately after the index table).

The original loader reads the one-byte count, reads `N * 8` bytes of index,
looks up the selected record, skips its offset in the stream, and reads exactly
its length. It then passes that extracted payload (offset 0) to `f.a(byte[], 0)`.
The decoded group is selected by `f.a(group, 0, -1, -1)` or by the corresponding
helper overload.

Passing the complete `.f` file directly to the sprite decoder is incorrect:
the decoder expects one indexed payload, not the outer container.

## Extraction tool

`tools/extract_f_sections.py` reproduces the container slicing operation and
writes the exact section payloads plus a JSON manifest. It does not decode the
internal sprite format or export PNGs.

## Inventory from the supplied JAR

The extractor validated every section boundary in all 24 `.f` resources and
extracted 121 payload sections. No section extended beyond its resource file.

| Resource | Sections |
|---|---:|
| `0.f`, `1.f`, `2.f` | 4 each |
| `b0.f` | 2 |
| `b1.f` | 1 |
| `cm.f` | 8 |
| `cr.f`, `demo.f`, `demoui.f` | 1 each |
| `gen0.f`, `gen1.f`, `gen2.f`, `gen3.f` | 10 each |
| `gen4.f` | 3 |
| `mm0.f` | 3 |
| `mm1.f` | 1 |
| `mmv.f` | 6 |
| `ms.f` | 5 |
| `o.f` | 2 |
| `snd.f` | 21 |
| `spl.f` | 3 |
| `tips.f` | 5 |
| `tipst.f` | 1 |
| `ui.f` | 5 |

## Next decoder milestone

The next task is to validate the internal payload parser and map resource
section indices to their actual roles (gameplay sprites, UI, effects, sound,
level assets). Section extraction is verified; image decoding and the resource
role map are not yet complete.

## Integrity audit (Build 04)

`tools/audit_asset_sections.py` independently reopens the original JAR, parses
all `.f` containers, checks that section payload ranges do not overlap, checks
the extracted manifest against the original index records, and compares every
extracted payload byte-for-byte with its source. Run it with:

```sh
python tools/audit_asset_sections.py reference/DMR320x240-Celsius-original.jar reference/sections
```

The current source package passes: 121 payloads across 24 resources, totaling
250,742 payload bytes. This verifies container extraction only; it does not
claim that the internal sprite/image payloads have been decoded.
