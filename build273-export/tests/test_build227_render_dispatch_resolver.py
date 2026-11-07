from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "android/src/main/kotlin/com/diamondrush/legacy"
CATALOG = (PKG / "LegacyRenderDispatchCatalog.kt").read_text()
RESOLVER = (PKG / "LegacyRenderDispatchResolver.kt").read_text()

def test_build226_generated_kotlin_newline_corruption_is_repaired():
    assert r"\\n" not in CATALOG
    assert "LegacyRawDispatchCase(3, 1890)," in CATALOG
    assert "LegacyRawDispatchCase(49, 2452)," in CATALOG

def test_main_dispatch_selectors_are_separate():
    assert "selectFirstMainPass" in RESOLVER
    assert "selectSecondMainPass" in RESOLVER
    assert "integerPlaneLowByte" in RESOLVER
    assert "signedBytePlaneValue" in RESOLVER

def test_signed_byte_precheck_is_preserved():
    assert "signedSelector == -1" in RESOLVER
    assert "(signedSelector - 80).toByte().toInt()" in RESOLVER
    assert "SIGNED_BYTE_BYPASS_TO_SHARED_TAIL" in RESOLVER

def test_secondary_overlay_filter_and_frame_rules_are_typed():
    assert "raw < 38 || raw >= 80" in RESOLVER
    assert "animationClock shr 2" in RESOLVER
    assert "animationClock shr 1" in RESOLVER
    assert "packedHigh and 0xff" in RESOLVER
    assert "((packedHigh - 1) * 7) / 16" in RESOLVER
    assert "(raw - 80).toByte().toInt()" in RESOLVER
    assert "DIRECT_DRAW_ARGUMENT" in RESOLVER
    assert "directDrawArgument" in RESOLVER

def test_resolver_connects_animation_and_composite_layers():
    assert "LegacySpriteAnimationTable" in RESOLVER
    assert "LegacySpriteAnimationFramePlacement" in RESOLVER
    assert "CompositeSpriteObjectResolver(section)" in RESOLVER
    assert "LegacyResolvedCompositeOverlay" in RESOLVER

def test_supplemental_metadata_conditions_are_not_merged():
    assert "supplementalResourceIndices" in RESOLVER
    assert "packedIntegerPlaneValue" in RESOLVER
    assert "signedBytePlaneValue" in RESOLVER
