"""
Unit tests for the prompt builder module.
"""
import unittest
from src.prompt_builder import build_prompt

class TestPromptBuilder(unittest.TestCase):
    def test_build_prompt(self):
        context = ["This is context 1.", "This is context 2."]
        question = "What is the answer?"
        prompt = build_prompt(context, question)
        expected_prompt = "This is context 1.\nThis is context 2.\n\nQuestion: What is the answer?\nAnswer:"
        self.assertEqual(prompt, expected_prompt)

if __name__ == "__main__":
    unittest.main()