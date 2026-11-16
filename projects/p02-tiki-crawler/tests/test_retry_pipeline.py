from __future__ import annotations

import unittest

from tiki_crawler.retry_pipeline import classify_failed_attempts


class RetryPipelineTests(unittest.TestCase):
    def test_classify_failed_attempts_splits_confirmed_404_and_unstable(self) -> None:
        history = {
            101: [
                {"round": 1, "status_code": 404, "error": "http_404", "elapsed_s": 0.1},
                {"round": 2, "status_code": 404, "error": "http_404", "elapsed_s": 0.2},
            ],
            202: [
                {"round": 1, "status_code": 403, "error": "http_403", "elapsed_s": 0.1},
                {"round": 2, "status_code": 404, "error": "http_404", "elapsed_s": 0.2},
            ],
        }

        confirmed_404, unstable, error_breakdown = classify_failed_attempts(history)

        self.assertEqual(len(confirmed_404), 1)
        self.assertEqual(confirmed_404[0]["product_id"], 101)
        self.assertEqual(len(unstable), 1)
        self.assertEqual(unstable[0]["product_id"], 202)
        self.assertEqual(error_breakdown["http_404"], 2)


if __name__ == "__main__":
    unittest.main()
