import unittest
import os
from pathlib import Path
from modules import file_reader, comment_filter, token_counter, code_summarizer, context_reducer, prompt_generator

class TestProject(unittest.TestCase):

    def setUp(self):
        self.test_dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/test_project"
        self.project_path = Path("test_project")

    def test_file_reader(self):
        files = file_reader.read_all_code_files(self.test_dir_path)
        print("Directory path:", self.test_dir_path)  # Debug print
        print("Files:", files)  # Debug print
        # Update the expected number of files based on your actual test setup
        expected_files = 6
        self.assertEqual(len(files), expected_files)

    def test_comment_filter(self):
        for file in file_reader.read_all_code_files(self.project_path):
            content = comment_filter.remove_comments(file)
            # Test that no Python-style comments remain in the content
            self.assertNotIn("# This is a sample python file", content)

    def test_token_counter(self):
        for file in file_reader.read_all_code_files(self.project_path):
            content = comment_filter.remove_comments(file)
            tokens = token_counter.count_tokens(content)
            # Test that the token count is not zero
            self.assertNotEqual(tokens, 0)

    def test_context_reducer(self):
        summaries = [{"file_content": file.read_text(), "variables": [], "functions": [], "classes": [], "extra_code": []} for file in file_reader.read_all_code_files(self.project_path)]
        reduced_context = context_reducer.reduce_context(summaries)
        # Test that the reduced context is not empty
        self.assertTrue(len(reduced_context) > 0)

    def test_prompt_generator(self):
        summaries = [{"filename": str(file), "file_content": file.read_text(), "variables": [], "functions": [], "classes": [], "extra_code": []} for file in file_reader.read_all_code_files(self.project_path)]
        for summary in summaries:
            prompt = prompt_generator.generate_prompt(summary)
            # Test that the prompt is not empty
            self.assertTrue(len(prompt) > 0)

if __name__ == "__main__":
    unittest.main()
