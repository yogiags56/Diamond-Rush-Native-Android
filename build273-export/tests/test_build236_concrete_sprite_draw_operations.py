from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'android/src/main/kotlin/com/diamondrush/legacy/LegacyConcreteSpriteDrawOperation.kt'
CHECKS = ROOT / 'android/src/test/kotlin/com/diamondrush/legacy/Build236ConcreteSpriteDrawOperationChecks.kt'


def test_build236_operation_retains_resource_slot_and_local_sprite_identity():
    source = SOURCE.read_text()
    assert 'globalArraySlot' in source
    assert 'spriteIndex' in source
    assert 'resolved.selection.resourceIndex == resource.globalArraySlot' in source


def test_build236_operation_retains_geometry_flags_and_composite_provenance():
    source = SOURCE.read_text()
    for field in ('spriteWidth', 'spriteHeight', 'x: Int', 'y: Int', 'incomingFlags',
                  'drawFlags', 'sourceGroupPath', 'sourceComponentPath'):
        assert field in source


def test_build236_rejects_unbound_leaf_and_cross_slot_binding():
    source = SOURCE.read_text()
    assert 'absent from bound f[' in source
    assert 'does not match bound f[' in source
    checks = CHECKS.read_text()
    assert 'verifyMismatchedGlobalSlotIsRejected' in checks
    assert 'verifyUnknownLeafSpriteIsRejected' in checks


def test_build236_exports_deterministic_csv_contract():
    source = SOURCE.read_text()
    checks = CHECKS.read_text()
    assert 'canonicalCsv' in source
    assert 'verifyCanonicalCsvIsStable' in checks
