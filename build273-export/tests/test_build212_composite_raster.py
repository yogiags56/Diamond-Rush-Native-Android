import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_build212_archive_is_preserved_as_historical_milestone():
    archive = ROOT / "previous_build212.zip"
    assert archive.is_file()
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        assert any("build212_composite_raster_inventory.csv" in n for n in names)
        assert any("CompositeSpriteRasterizer.kt" in n for n in names)
        assert sum(1 for n in names if n.endswith(".png") and "composite_" in n) >= 300
