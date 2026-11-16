from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tiki_crawler.input_loader import load_and_validate_product_ids


class InputLoaderTests(unittest.TestCase):
    def test_load_and_validate_product_ids_deduplicates_and_skips_invalid_rows(self) -> None:
        csv_content = "id\n123\n456\n123\nabc\n\n789\n"

        with tempfile.TemporaryDirectory() as tmp_dir:
            input_file = Path(tmp_dir) / "products.csv"
            input_file.write_text(csv_content, encoding="utf-8")

            ids, report = load_and_validate_product_ids(input_file)

        self.assertEqual(ids, [123, 456, 789])
        self.assertEqual(report.total_rows, 5)
        self.assertEqual(report.valid_rows, 4)
        self.assertEqual(report.invalid_rows, 1)
        self.assertEqual(report.duplicate_rows, 1)
        self.assertEqual(report.unique_product_ids, 3)


if __name__ == "__main__":
    unittest.main()
