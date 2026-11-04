# Build 12 — decoder layout probe

Added `tools/probe_decoder_layout.py`, a conservative reader for the portions
of `f.a(byte[], int)` that are directly visible in bytecode: initial tables,
palette format/group/color counts, palette entries, the following mode/alpha
word, and cumulative image-offset deltas.

The palette format switch values are the signed-short constants `-30584`,
`17476`, `21781`, and `25861`; their entries consume 4, 2, 2, and 2 bytes
respectively. The probe does not attempt to decode pixel streams or build a
Bitmap.

## Important finding

The known `gen0_section_00.bin` fixture passes the early table and palette
bounds, but its subsequent image-offset deltas accumulate beyond the 323-byte
payload. The probe correctly rejects it rather than treating this resource
section as a valid complete sprite-decoder input. This confirms that matching
the initial header prefix alone is not enough to classify a payload as a sprite
atlas. The correct resource/caller path and any required payload slicing still
need to be established before decoding pixels.

Run:

```sh
python tools/probe_decoder_layout.py reference/sections/gen0_section_00.bin --json
python -m unittest discover -s tools/tests -v
```

No sprite image or Android Bitmap is claimed by this build.
