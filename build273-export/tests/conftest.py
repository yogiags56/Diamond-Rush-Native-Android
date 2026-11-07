"""Skip research tests whose proprietary/local-only inputs are not in source export."""
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]

# These tests deliberately require the user's local original game archive or
# derived visual/payload fixtures. The public source export omits those inputs.
REQUIRES_ORIGINAL_JAR = {
    "test_build206_payloads.py",
    "test_build207_resolver.py",
    "test_build210_field_layout.py",
    "test_build231_world_room_archive.py",
    "test_build247_sprite_draw_callee_semantics.py",
    "test_build269_case4_interpolation_audit.py",
    "test_build214_animation_table.py",
    "test_build234_df03_resource_parser.py",
    "test_build240_room_render_assembly.py",
    "test_build241_main_dispatch_art_evidence.py",
    "test_build242_dynamic_resource_origin.py",
    "test_build258_exception_cfg_audit.py",
    "test_build260_cross_method_reference_audit.py",
    "test_build267_classfile_exception_audit.py",
    "test_build268_exception_aware_operand_interpreter.py",
}
REQUIRES_PAYLOAD_FIXTURES = {
    "test_build243_dynamic_composite_attribution.py",
}
REQUIRES_PREVIEWS = {
    "test_build212_composite_raster.py",
    "test_build213_draw_flags_palette.py",
}


def pytest_collection_modifyitems(config, items):
    has_jar = (ROOT / "original.jar").is_file() or (ROOT / "original" / "DMR320x240-Celsius.jar").is_file()
    has_previews = (ROOT / "previews").is_dir()
    for item in items:
        name = Path(str(item.fspath)).name
        if name in REQUIRES_ORIGINAL_JAR and not has_jar:
            item.add_marker(pytest.mark.skip(reason="requires local original game JAR; not redistributed"))
        elif name in REQUIRES_PAYLOAD_FIXTURES and not (ROOT / "research" / "build242_payload_fixtures" / "slot27.bin").is_file():
            item.add_marker(pytest.mark.skip(reason="requires local binary payload fixtures; not redistributed"))
        elif name in REQUIRES_PREVIEWS and not has_previews:
            item.add_marker(pytest.mark.skip(reason="requires local derived sprite previews; not redistributed"))
