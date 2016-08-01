import unittest

from pyqart.qr.data.raw import Raw


class TestRaw(unittest.TestCase):
    def test_raw(self):
        raw = Raw(b'Hello, world!', 8)
        self.assertEqual(
            raw.output.as_string,
            '0100' + '00001101' +
            '01001000' + '01100101' + '01101100' + '01101100' +
            '01101111' + '00101100' + '00100000' + '01110111' +
            '01101111' + '01110010' + '01101100' + '01100100' +
            '00100001',
        )
