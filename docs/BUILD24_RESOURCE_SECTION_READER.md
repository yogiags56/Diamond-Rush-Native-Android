# Build 24 — Original resource section reader

Build 24 adds a native Java reader for the original Diamond Rush `.f` indexed resource containers.

## What changed

- Packaged all 24 original `.f` containers from `DMR320x240-Celsius-original.jar` under `app/src/main/assets/original/` without rewriting their bytes.
- Added `engine/ResourceSectionReader.java`, a platform-neutral parser for the one-byte section count and eight-byte little-endian `(offset, length)` entries.
- `readSection(container, index)` returns a defensive copy of exactly the selected payload. It rejects empty/truncated tables, invalid indexes, empty payloads, and payload ranges outside the container.
- Added `tools/tests/ResourceSectionReaderTest.java` with synthetic boundary cases and a sweep over every packaged original container.

## Verification

- 8 reader behavior checks passed.
- All 121 indexed sections across the original resource containers were read successfully.
- The separate extraction audit still confirms all 121 previously extracted reference payloads are byte-identical to the original JAR: 24 resources, 250,742 payload bytes.

## Important boundary

This is the resource-container reader, not yet the sprite decoder. It establishes a correct native equivalent of the original `i.a(String, int)` section extraction boundary. Palette decoding, sprite metadata interpretation, frame composition, and animation wiring remain separate steps. The preview remains a placeholder scene until those are integrated.
