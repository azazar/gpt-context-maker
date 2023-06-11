import unittest
import os
from pathlib import Path
from modules import file_reader, comment_filter, token_counter, code_summarizer, context_reducer, prompt_generator

class TestProject(unittest.TestCase):

    def setUp(self):
        self.test_dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/test_project"
        self.project_path = Path(self.test_dir_path)

    def test_file_reader(self):
        files = file_reader.read_all_code_files(self.test_dir_path)
        expected_files = 14
        self.assertEqual(len(files), expected_files)

        for file in files:
            self.assertTrue(file.exists())  # each file should exist

    def test_comment_filter(self):
        for file in file_reader.read_all_code_files(self.project_path):
            with open(file, "r") as f:
                file_content = f.read()
            content = comment_filter.remove_comments(file, file_content)
            self.assertNotIn("# This is a sample python file", content)
            self.assertNotIn("// This is a sample comment", content)  # C++ style comments should be removed
            self.assertNotIn("/* This is a sample comment */", content)  # C style comments should be removed

    def test_token_counter(self):
        for file in file_reader.read_all_code_files(self.project_path):
            with open(file, "r") as f:
                file_content = f.read()
            original_tokens = token_counter.count_tokens(file_content)
            print(f"Original tokens: {original_tokens}")
            content = comment_filter.remove_comments(file, file_content)
            tokens = token_counter.count_tokens(content)
            print(f"Tokens after comment removal: {tokens}")
            if "# This is a sample python file" in file_content or "// This is a sample comment" in file_content or "/* This is a sample comment */" in file_content:  # Add a check here
                self.assertGreater(original_tokens, tokens)

    def test_context_reducer(self):
        summaries = [{"file_content": file.read_text(), "variables": [], "functions": [], "classes": [], "extra_code": []} for file in file_reader.read_all_code_files(self.project_path)]
        reduced_context = context_reducer.reduce_context(summaries)
        self.assertTrue(len(reduced_context) > 0)

        # Test if the reduced context has fewer tokens than the original context
        original_tokens = sum(token_counter.count_tokens(summary["file_content"]) for summary in summaries)
        reduced_tokens = sum(token_counter.count_tokens(summary["file_content"]) for summary in reduced_context)
        self.assertLessEqual(reduced_tokens, original_tokens)

    def test_prompt_generator(self):
        summaries = [{"filename": str(file), "file_content": file.read_text(), "variables": [], "functions": [], "classes": [], "extra_code": []} for file in file_reader.read_all_code_files(self.project_path)]
        for summary in summaries:
            prompt = prompt_generator.generate_prompt(summary)
            self.assertTrue(len(prompt) > 0)

            # Test if the filename is included in the prompt
            self.assertIn(summary["filename"], prompt)

if __name__ == "__main__":
    unittest.main()
