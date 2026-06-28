import os
import tempfile
import unittest

import pandas as pd

from utils.dataset_loader import load_training_data


class DatasetLoaderTests(unittest.TestCase):
    def test_load_training_data_reads_csv_with_required_columns(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as handle:
            handle.write("resume_text,job_description,label\nPython Django SQL,Python Django SQL,1\nJava Spring Boot,Python Django SQL,0\n")
            temp_path = handle.name

        try:
            df = load_training_data(temp_path)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertTrue({"resume_text", "job_description", "label"}.issubset(df.columns))
            self.assertEqual(len(df), 2)
        finally:
            os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
