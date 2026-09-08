import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "gcm_utils", Path(__file__).resolve().parents[1] / "authentification-1/gcm/utils.py"
)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)


class ByteConversionTests(unittest.TestCase):
    def test_bit_order_preserves_leading_zeroes(self):
        self.assertEqual(utils.bytes_to_bits(b"\x01\x80"), [0] * 7 + [1, 1] + [0] * 7)

    def test_all_byte_values_round_trip(self):
        value = bytes(range(256))
        self.assertEqual(utils.bits_to_bytes(utils.bytes_to_bits(value)), value)

    def test_empty_payload_round_trips(self):
        self.assertEqual(utils.bits_to_bytes(utils.bytes_to_bits(b"")), b"")

    def test_xor_uses_each_byte(self):
        self.assertEqual(utils.xor(b"\x00\xff\x55", b"\xff\x0f\xaa"), b"\xff\xf0\xff")

    def test_xor_rejects_different_lengths(self):
        with self.assertRaises(AssertionError):
            utils.xor(b"one", b"four")
