from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'android/src/main/kotlin/com/diamondrush/legacy/LegacyPaletteBoundSpriteDraw.kt'
CHECKS = ROOT / 'android/src/test/kotlin/com/diamondrush/legacy/Build237PaletteAwareSpriteChecks.kt'


def test_palette_index_is_explicit_and_never_guessed():
    source = SOURCE.read_text()
    assert 'paletteIndex: Int' in source
    assert 'paletteIndex in parsed.palettes.indices' in source
    assert 'Unsupported palette format' in source


def test_decoded_pixels_keep_global_and_local_sprite_identity():
    source = SOURCE.read_text()
    assert 'globalArraySlot' in source
    assert 'spriteIndex' in source
    assert 'decodedSprites.associateBy { it.globalArraySlot to it.spriteIndex }' in source


def test_pixel_decode_uses_existing_bytecode_aligned_decoder():
    source = SOURCE.read_text()
    assert 'LegacySpriteDecoder.decodePalette' in source
    assert 'LegacySpriteDecoder.decodeIndices' in source
    assert 'colorIndex in palette.indices' in source


def test_draw_operation_geometry_and_flags_are_preserved():
    source = SOURCE.read_text()
    assert 'LegacyPaletteBoundSpriteDraw(\n                operation, paletteIndex' in source
    assert 'decoded.width == operation.spriteWidth' in source
    assert 'decoded.height == operation.spriteHeight' in source
    checks = CHECKS.read_text()
    assert 'verifyOperationBindingPreservesGeometryAndFlags' in checks
    assert 'verifyDimensionMismatchIsRejected' in checks


def test_unsupported_palette_and_missing_sprite_are_regression_cases():
    checks = CHECKS.read_text()
    assert 'verifyUnsupportedPaletteFormatIsRejectedWithoutGuessing' in checks
    assert 'verifyInvalidPaletteAndMissingPixelsAreRejected' in checks


def test_build234_kotlin_parser_preserves_interleaved_length_payload_order():
    source = (ROOT / 'android/src/main/kotlin/com/diamondrush/legacy/LegacySpriteResourceBundleParser.kt').read_text()
    assert 'interleaved stream' in source
    assert 'val length = c.s16("sprite $index encoded length")' in source
    assert 'val encoded = c.take(length, "sprite $index pixel payload")' in source
    checks = (ROOT / 'android/src/test/kotlin/com/diamondrush/legacy/Build234SpriteResourceParserChecks.kt').read_text()
    assert 'verifySpriteLengthAndPayloadRecordsAreInterleaved' in checks


def test_original_mapped_sprite_audit_is_reproducible():
    audit = (ROOT / 'research/build237_original_mapped_sprite_decode_audit.kt').read_text()
    assert 'LegacyBundleSpriteSlotCatalog.staticBindings' in audit
    assert 'LegacyPaletteAwareSpriteDecoder.decodeResource' in audit
    assert 'sha256_pixel_stream' in audit


def test_full_original_df03_decode_audit_covers_all_sprite_palette_pairs():
    rows = (ROOT / 'research/build237_full_df03_pixel_decode_audit.csv').read_text().splitlines()
    assert len(rows) == 113  # header + 112 palette rows
    assert 'bundle,entry,sprite_count,palette_index' in rows[0]
    assert sum(int(row.split(',')[2]) for row in rows[1:]) == 2604
