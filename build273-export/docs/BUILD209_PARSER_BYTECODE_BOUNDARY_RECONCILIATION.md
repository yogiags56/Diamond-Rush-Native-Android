# Build 209 — Original Parser Bytecode Boundary Reconciliation

## Executive result

Build 209 revisits the full-resource parser using the original `f.a(byte[], int)` JVM bytecode, rather than extrapolating from the partial Build 206 composite parser. This exposed a significant issue in the previous resource-table interpretation.

**The Build 206–207 real-resource composite inventory is now provisional and must not be treated as a verified mapping of the original JAR.** Its parser treated the second count as four-byte component records and the third count as composite groups. The original bytecode shows a different sequence and widths. The generic component/group model in Builds 204–207 remains useful as an isolated data model, but its previous mapping to the 94 original DF03 payloads must be rebuilt.

## Bytecode-grounded structure

The parser receives an offset argument of zero at the audited wrapper call sites. The method advances that cursor by six bytes and then reads the following structures:

1. Signed-short sprite count; when positive, two bytes per sprite.
2. Signed-short secondary-table count; when positive, two bytes per entry.
3. Signed-short table-3 count; when positive:
   - one four-byte descriptor per entry, read as byte, skipped byte, signed short;
   - then a separate raw table of four bytes per entry.
4. Signed-short count followed by five bytes per entry.
5. Signed-short count followed by four bytes per entry, read as byte, skipped byte, signed short.
6. If sprite count is not positive, the original method returns here.
7. Palette format, palette count, color count, and palette entries for the four recognized palette formats.
8. Pixel format.
9. One interleaved record per sprite: signed-short payload length, immediately followed by that sprite's payload bytes.

The final point is a confirmed correction to Build 208: sprite lengths are **not** a standalone length table followed by a concatenated payload block. The original method scans each length and skips that sprite's payload before continuing to the next length.

Negative signed-short table counts are treated as absent by the original method's `count > 0` branches; they do not automatically consume bytes or throw. The parser also has a fixed 16-slot palette array. Unknown palette formats take the switch default branch and consume no palette bytes.

## Resource audit

The original JAR still contains 94 entries with the `DF03 01 01` signature.

Using the bytecode-aligned structural trace against all 94 entries:
- 19 entries completed the trace.
- 75 entries encountered a bounds, count, or palette-array exception.
- The 19 completed entries exposed 53 sprite payload records.
- Their observed pixel formats were 49 records of `0x1600`, three records of `0xAC00` (not yet supported by the known decoder), and one record of `0x0400`.

A separate static call-site audit identified 16 direct, literal-index calls to the sprite-bundle loader in the available Build 201 call-site map:
- 3 entries completed the structural trace (`ms.f` entries 2, 3, and 4).
- 13 entries encountered parser exceptions.
- The three completed entries use pixel format `0xAC00`, which is not yet implemented by the known decoder.

This does **not** prove the original game cannot load or display those resources. The original parser catches exceptions internally, and some call paths may be conditional or may use dynamic indices not covered by the literal-index audit. It does prove that the current reconstructed full parser is not yet a validated general-purpose decoder.

## Source changes

- Added `LegacySpriteBytecodeTrace.kt`, a conservative Kotlin representation of the observed table boundaries.
- Kept all tables opaque and positional; no unverified semantic labels are assigned.
- Added `df03_full_parser_audit.py` to regenerate the 94-entry structural inventory.
- Added `build209_callsite_parse_audit.csv` to retain direct call-site evidence and per-entry outcomes.
- Retained Build 204–208 source and tests for continuity, while documenting that the Build 206–207 real-resource graph interpretation is under re-audit.

## Validation

- Python regression and Build 209 tests: **41/41 passed**.
- Kotlin source compilation: **passed** using `kotlinc`.
- Static original-JAR structural audit: 19/94 trace-complete, 75/94 exceptions.
- Static direct call-site audit: 3/16 trace-complete, 13/16 exceptions.
- No Android Gradle build, Android runtime, sprite rasterization, visual parity, or playable APK is claimed.

## Important correction to project state

The old Build 206 counts (1,129 groups and 10,149 component records) and Build 207 full expansion totals were generated from a table alignment that does not match the full parser bytecode. Those totals are preserved as historical outputs, but they are **not currently accepted as verified original-resource facts**. They must be regenerated only after Build 210 resolves the consumers of the positional tables and validates the table mapping against real parser call paths.

## Next build — Build 210

1. Audit every consumer of the `f` fields in the original bytecode, using full field descriptors to disambiguate obfuscated names.
2. Establish which positional tables correspond to sprite dimensions, component records, composite group descriptors, frame/animation metadata, and auxiliary data.
3. Trace `f.a(IIII)` and the renderer's reads from those fields.
4. Rebuild the composite graph inventory from the corrected table boundaries.
5. Revalidate nested group references before allowing Build 207's resolver to consume original-resource data.
6. Only after this is stable, resume sprite rasterization and 320×240 scene assembly.
