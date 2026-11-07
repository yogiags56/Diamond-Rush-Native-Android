# Build272 — W0 Room0 Selector/Candidate Ambiguity Audit

## Purpose

Build271 expanded the existing W0 room0 candidate join into component-level
candidate rows. Build272 audits the selector-to-candidate relationship without
turning CFG-reachable candidate unions into runtime resource selections.

## Results

- Source candidate rows: 1,530
- Raw `bJ` selector values: 6 (3, 4, 5, 6, 7, 8)
- Room cells represented: 90
- Cells with more than one candidate resource: 90
- Proven exclusive selector-to-resource bindings: 0
- Runtime resource selection: unresolved

The candidate resource families present in the source join are:

- `f[27]` → `/gen3.f`, record 34
- `f[30]` → `/gen2.f`, record 23
- `f[56]` → `/cm.f`, record 1

These are candidate associations, not proof that a specific slot is selected
for a given cell. Each selector summary preserves the branch target and all
candidate resource/group pairs. Each cell summary preserves its candidate set.

## Interpretation

This audit confirms that the current candidate join is still ambiguous at every
represented cell. It does not justify choosing the first resource, the most
frequent resource, or a group by ordering. The next reverse-engineering step
must trace the actual `bJ` case's field/array reads and predicates to the exact
`f[]` slot and composite group at runtime.

## Validation boundary

The generator is a deterministic Python audit over existing evidence. It does
not execute the original game, prove runtime selection, resolve renderer
transforms, rasterize a complete room, compile an Android application, or
produce a playable APK.
