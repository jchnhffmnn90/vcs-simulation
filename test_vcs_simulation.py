"""Unit tests for VCS simulation using unittest."""

import io
import unittest
from unittest.mock import patch

from vcs_simulation import Repository


class TestRepository(unittest.TestCase):
    def test_commit_creates_incremental_ids(self) -> None:
        repo = Repository()
        c1 = repo.commit("First")
        c2 = repo.commit("Second")

        self.assertEqual(c1.id, 1)
        self.assertEqual(c1.message, "First")
        self.assertEqual(c2.id, 2)
        self.assertEqual(c2.message, "Second")
        self.assertEqual(len(repo.commits), 2)

    def test_revert_valid_commit(self) -> None:
        repo = Repository()
        repo.commit("First")
        repo.commit("Second")
        repo.commit("Third")

        with patch("sys.stdout", new=io.StringIO()):
            success = repo.revert(2)
        self.assertTrue(success)
        self.assertEqual(len(repo.commits), 2)
        self.assertEqual([c.id for c in repo.commits], [1, 2])

    def test_revert_invalid_commit(self) -> None:
        repo = Repository()
        repo.commit("First")

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            success = repo.revert(42)
            self.assertFalse(success)
            self.assertEqual(len(repo.commits), 1)
            self.assertIn("Fehler: Commit mit ID 42 existiert nicht.", fake_out.getvalue())

    def test_log_output_order(self) -> None:
        repo = Repository()
        repo.commit("First")
        repo.commit("Second")

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            repo.log()
            output = fake_out.getvalue()
            pos_second = output.find("Commit #2: Second")
            pos_first = output.find("Commit #1: First")
            self.assertNotEqual(pos_second, -1)
            self.assertNotEqual(pos_first, -1)
            self.assertLess(pos_second, pos_first)


if __name__ == "__main__":
    unittest.main()
