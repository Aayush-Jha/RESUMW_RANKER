import os
import tempfile
import unittest

from utils.pdf_reader import extract_text_from_file
from utils.ranker import rank_resumes


class RankerTests(unittest.TestCase):
    def test_rank_resumes_prefers_best_skill_match(self):
        job_desc = "Python Django SQL Machine Learning"
        resumes = [
            ("strong_candidate.pdf", "Python Django SQL pandas scikit-learn"),
            ("weak_candidate.pdf", "Java Spring Boot"),
        ]

        results = rank_resumes(job_desc, resumes)

        self.assertEqual(results[0]["name"], "strong_candidate.pdf")
        self.assertGreater(results[0]["match_percentage"], results[1]["match_percentage"])
        self.assertGreaterEqual(results[0]["match_percentage"], 70)

    def test_extract_text_from_text_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as handle:
            handle.write("Python Django SQL")
            temp_path = handle.name

        try:
            extracted = extract_text_from_file(temp_path)
            self.assertIn("Python", extracted)
        finally:
            os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
