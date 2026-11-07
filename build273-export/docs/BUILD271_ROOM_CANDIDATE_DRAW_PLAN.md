# Build271 — W0 Room0 Candidate Draw Plan

## Objective

Expand the Build244 room-cell/resource/group candidate join and Build243
composite-component inventory into a row-level candidate draw plan. This is a
reproducible structural join, not a runtime trace.

## Result

- 4,110 candidate component rows
- 90 room cells with candidate rows
- 21 distinct resource/group pairs
- All 51 known composite components are leaf-sprite records, repeated across
  candidate room-cell/group combinations
- Candidate destination coordinates are calculated as room-cell screen anchor
  plus signed composite component offsets

## Important interpretation limits

1. Build244 labels its resource/group associations as candidate-only. It does
   not prove exclusive runtime selection for a room cell.
2. The output preserves every candidate instead of selecting one resource or
   group by guesswork.
3. The coordinates are candidate component destinations relative to the
   existing room screen anchor. They are not yet proven final Graphics draw
   coordinates after all renderer flags, transforms, clipping, camera offsets,
   and draw-order rules.
4. The source composite inventory contains leaf-sprite components only for
   these 21 groups; no nested-group records were present in this joined data.
5. No full room rasterization, Kotlin compilation, Android Gradle build,
   device runtime, visual parity, or playable APK is claimed.

## Reproduction

```bash
python research/build271_room_candidate_draw_plan.py
pytest -q
```

Output: `research/build271_w0_room0_candidate_draw_plan.csv`.
