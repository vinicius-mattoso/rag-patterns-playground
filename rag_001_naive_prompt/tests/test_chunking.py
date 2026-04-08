"""
Unit tests for the chunking module.
"""
import unittest
from src.chunking import chunk_text

class TestChunking(unittest.TestCase):
    def test_chunk_text(self):
        text = "abcdefghijklmnopqrstuvwxyz"
        chunks = chunk_text(text, chunk_size=5, overlap=2)
        self.assertEqual(chunks, ["abcde", "cdefg", "efghi", "ghijk", "ijklm", "klmno", "mnopq", "opqrs", "qrstu", "stuvw", "uvwxy", "xyz"])

if __name__ == "__main__":
    unittest.main()