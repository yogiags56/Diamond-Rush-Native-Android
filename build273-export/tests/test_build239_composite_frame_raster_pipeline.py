from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / 'android/src/main/kotlin/com/diamondrush/legacy/LegacyCompositeFrameRasterPipeline.kt'
CHECKS = ROOT / 'android/src/test/kotlin/com/diamondrush/legacy/Build239CompositeFrameRasterPipelineChecks.kt'


def test_pipeline_joins_concrete_expansion_palette_binding_and_rasterization():
    source = PIPELINE.read_text()
    assert 'LegacyConcreteSpriteDrawOperationResolver.expand' in source
    assert 'LegacyPaletteAwareSpriteDecoder.bindOperations' in source
    assert 'LegacySpriteRasterExecution.rasterize' in source


def test_pipeline_requires_explicit_resource_and_animation_selection():
    source = PIPELINE.read_text()
    assert 'resolved.selection.resourceIndex == resource.globalArraySlot' in source
    assert 'LegacyOverlaySelectionKind.ANIMATION_SEQUENCE_FRAME' in source
    assert 'Direct-draw argument path cannot enter composite-frame raster pipeline' in source


def test_pipeline_preserves_no_group_sentinel_as_empty_draw_list():
    source = PIPELINE.read_text()
    assert 'placement.frame.compositeGroupIndex == null' in source
    assert 'No-group animation frame unexpectedly contains composite leaves' in source
    assert 'emptyList()' in source


def test_kotlin_checks_cover_full_frame_binding_and_rejection_boundaries():
    source = CHECKS.read_text()
    assert 'verifyResolvedFrameRunsThroughBindingAndRasterizer' in source
    assert 'verifyEmptyNoGroupFrameProducesBlankSurface' in source
    assert 'verifyResourceMismatchAndDirectDrawAreRejected' in source
