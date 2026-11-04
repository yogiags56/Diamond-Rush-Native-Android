import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / 'audit_asset_sections.py'
spec = importlib.util.spec_from_file_location('audit_asset_sections', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def container(payloads):
    count = len(payloads)
    table_size = 1 + count * 8
    offset = 0
    table = bytearray([count])
    body = bytearray()
    for payload in payloads:
        table += offset.to_bytes(4, 'little')
        table += len(payload).to_bytes(4, 'little')
        body += payload
        offset += len(payload)
    return bytes(table + body)


class ContainerAuditTests(unittest.TestCase):
    def test_reads_multiple_sections(self):
        parsed = module.parse_container(container([b'abc', b'defg']), 'test.f')
        self.assertEqual([(x[0], x[1], x[2], x[3]) for x in parsed],
                         [(0, 0, 3, b'abc'), (1, 3, 4, b'defg')])

    def test_rejects_truncated_index(self):
        with self.assertRaisesRegex(ValueError, 'truncated index'):
            module.parse_container(b'\x02' + b'\x00' * 7, 'bad.f')

    def test_rejects_payload_outside_file(self):
        data = b'\x01' + (0).to_bytes(4, 'little') + (20).to_bytes(4, 'little') + b'x'
        with self.assertRaisesRegex(ValueError, 'past EOF'):
            module.parse_container(data, 'bad.f')

    def test_rejects_empty_payload(self):
        data = b'\x01' + (0).to_bytes(4, 'little') + (0).to_bytes(4, 'little')
        with self.assertRaisesRegex(ValueError, 'empty payload'):
            module.parse_container(data, 'bad.f')


if __name__ == '__main__':
    unittest.main()
