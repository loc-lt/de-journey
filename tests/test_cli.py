from __future__ import annotations

import unittest

from tiki_crawler.cli import should_auto_restart


class CliRunnerTests(unittest.TestCase):
    def test_should_auto_restart_returns_false_when_disabled(self) -> None:
        self.assertFalse(should_auto_restart(auto_restart=False, restart_count=0, max_restarts=0))

    def test_should_auto_restart_allows_unlimited_restarts_when_max_is_zero(self) -> None:
        self.assertTrue(should_auto_restart(auto_restart=True, restart_count=99, max_restarts=0))

    def test_should_auto_restart_stops_after_configured_limit(self) -> None:
        self.assertTrue(should_auto_restart(auto_restart=True, restart_count=0, max_restarts=1))
        self.assertFalse(should_auto_restart(auto_restart=True, restart_count=1, max_restarts=1))


if __name__ == "__main__":
    unittest.main()
