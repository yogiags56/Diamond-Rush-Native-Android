from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'android/src/main/kotlin/com/diamondrush/legacy/LegacySpriteRasterExecution.kt'
CHECKS = ROOT / 'android/src/test/kotlin/com/diamondrush/legacy/Build238SpriteRasterExecutionChecks.kt'


def test_raster_surface_is_bounded_and_argb_sized():
    source = SOURCE.read_text()
    assert 'Math.multiplyExact(width, height)' in source
    assert 'pixelCount <= maxPixels' in source
    assert 'IntArray(pixelCount)' in source


def test_midp_transform_bits_match_build213_semantics():
    source = SOURCE.read_text()
    assert 'op.drawFlags and 0x03' in source
    assert '(transform and 0x01)' in source
    assert '(transform and 0x02)' in source
    checks = CHECKS.read_text()
    assert 'verifyMidpHorizontalVerticalAndCombinedTransforms' in checks


def test_clipping_preserves_negative_positions_and_half_open_edges():
    source = SOURCE.read_text()
    assert 'clip.rightExclusive' in source
    assert 'clip.bottomExclusive' in source
    assert 'maxOf(op.x, clipLeft)' in source
    assert 'Math.addExact(op.x, op.spriteWidth)' in source
    assert 'verifyClippingAndNegativeCoordinates' in CHECKS.read_text()


def test_alpha_blending_and_transparency_are_explicit():
    source = SOURCE.read_text()
    assert 'sourceOver(out[destinationIndex], source)' in source
    assert 'if (alpha == 0)' in source
    assert 'fun sourceOver(destination: Int, source: Int)' in source
    checks = CHECKS.read_text()
    assert 'verifyTransparentPixelsDoNotOverwriteDestination' in checks
    assert 'verifyPartialAlphaUsesSourceOver' in checks


def test_draw_order_and_operation_provenance_are_preserved():
    source = SOURCE.read_text()
    assert 'for (draw in draws)' in source
    assert 'val op = draw.operation' in source
    assert 'executedOperations' in source
    assert 'verifyUntransformedBlitAndPainterOrder' in CHECKS.read_text()


def test_invalid_payload_and_surface_size_are_rejected():
    checks = CHECKS.read_text()
    assert 'verifyViewportClipAndSurfaceSafety' in checks
    assert 'verifyInvalidPixelPayloadIsRejectedAtBindingBoundary' in checks
