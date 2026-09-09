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

    def test_log_empty_repository(self) -> None:
        repo = Repository()
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            repo.log()
            self.assertEqual(fake_out.getvalue().strip(), "Keine Commits vorhanden.")

    def test_format_log_empty_and_populated(self) -> None:
        repo = Repository()
        self.assertEqual(repo.format_log(), ["Keine Commits vorhanden."])

        repo.commit("First")
        repo.commit("Second")
        expected = [
            "--- Commit Log (neuester zuerst) ---",
            "Commit #2: Second",
            "Commit #1: First",
        ]
        self.assertEqual(repo.format_log(), expected)

    def test_find_index_and_get_commit(self) -> None:
        repo = Repository()
        c1 = repo.commit("First")
        c2 = repo.commit("Second")

        self.assertEqual(repo.find_index(1), 0)
        self.assertEqual(repo.find_index(2), 1)
        self.assertIsNone(repo.find_index(99))

        self.assertEqual(repo.get_commit(1), c1)
        self.assertEqual(repo.get_commit(2), c2)
        self.assertIsNone(repo.get_commit(99))

    def test_revert_to_head_commit(self) -> None:
        repo = Repository()
        repo.commit("First")
        repo.commit("Second")

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            success = repo.revert(2)
            self.assertTrue(success)
            self.assertEqual(len(repo.commits), 2)
            self.assertIn("0 nachfolgende(r) Commit(s) entfernt", fake_out.getvalue())

    def test_revert_empty_repository(self) -> None:
        repo = Repository()
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            success = repo.revert(1)
            self.assertFalse(success)
            self.assertIn("Fehler: Commit mit ID 1 existiert nicht.", fake_out.getvalue())


if __name__ == "__main__":
    unittest.main()
