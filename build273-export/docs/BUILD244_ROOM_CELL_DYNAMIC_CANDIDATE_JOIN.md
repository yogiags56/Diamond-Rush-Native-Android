# Build 244 — Room Cell to Dynamic Composite Candidate Join

## Goal

Join the original `w0.bin` room 0 camera-0 cell manifest (Build240) to the CFG-derived `bJ` dispatch candidate resource slots (Build241), confirmed dynamic resource origins (Build242), and parsed composite groups/components (Build243).

## Result

`research/build244_w0_room0_dynamic_candidate_join.csv` contains 1,530 candidate rows:
- 135 in-bounds cells in the room manifest;
- 90 cells have one or more dynamic-resource candidates;
- each row combines cell coordinates, raw `bJ` selector, CFG branch target, candidate `f[]` slot, resource path/record/payload length, composite group index, component count, and referenced sprite indices.

The CSV marks every row `CANDIDATE_ONLY_NO_RUNTIME_SELECTION_PROOF`. This is an evidence join, not proof that a specific slot/group is selected at runtime for a cell. CFG reachability is not exclusive selection. It is therefore not passed to the rasterizer as a draw operation.

## Reproduction

```bash
python research/build244_room_cell_dynamic_candidate_join.py
python -m pytest -q
```

## Validation

- Python regression suite: 225 passed, 4 existing Pillow deprecation warnings.
- All Kotlin production and test sources compile together.
- Kotlin regression runner through Build244 passes, including Build242 resource fixtures and Build243 composite index checks.

## Next step

Build245 should trace the actual runtime argument values at the render callsites for the supported `bJ` branches, especially how `f[]` slot and composite group are selected. Only after that trace should cell-to-group candidate rows be promoted to concrete draw operations. Keep the direct `f[42]` six-integer path isolated until its semantics are proven.

## Limitations

No room rasterization, Android Gradle build, device runtime, screenshot parity, or APK packaging is claimed.
