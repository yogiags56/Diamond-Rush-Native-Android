from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyPerCellRenderTrace.kt"
RESOLVER = ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyRenderDispatchResolver.kt"


def test_trace_model_keeps_coordinates_and_raw_planes_separate():
    s = SRC.read_text()
    for field in ("row: Int", "column: Int", "mapX: Int", "mapY: Int",
                  "screenX: Int", "screenY: Int", "integerPlaneLowByte: Int",
                  "signedBytePlaneValue: Int", "packedIntegerPlaneValue: Int"):
        assert field in s


def test_trace_preserves_two_main_passes_and_overlay_order_as_distinct_fields():
    s = SRC.read_text()
    assert "firstPass = LegacyRenderDispatchResolver.selectFirstMainPass" in s
    assert "secondPass = LegacyRenderDispatchResolver.selectSecondMainPass" in s
    assert "secondaryOverlay = LegacyRenderDispatchResolver.resolveOverlayFrame" in s


def test_canonical_trace_has_stable_header_and_no_locale_formatting():
    s = SRC.read_text()
    assert 'const val HEADER = "row,column,mapX,mapY,screenX,screenY' in s
    assert 'joinToString(",")' in s
    assert "joinToString(\"\\n\", postfix = \"\\n\")" in s


def test_trace_does_not_invent_viewport_iteration_or_semantic_names():
    s = SRC.read_text()
    assert "traceCell(" in s
    assert "for (row" not in s and "for (column" not in s
    assert "tileName" not in s.lower()
    assert "objectName" not in s.lower()


def test_resolver_remains_authority_for_raw_dispatch_semantics():
    s = RESOLVER.read_text()
    assert "selectFirstMainPass" in s
    assert "selectSecondMainPass" in s
    assert "resolveOverlayFrame" in s
    assert "supplementalResources" in s
