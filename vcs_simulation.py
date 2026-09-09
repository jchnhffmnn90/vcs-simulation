"""Simple Version Control System (VCS) simulation in Python."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Commit:
    """Represents a single commit in the repository."""

    id: int
    message: str


class Repository:
    """Simulates a basic version control repository."""

    def __init__(self) -> None:
        self.commits: list[Commit] = []
        self._next_id: int = 1

    def commit(self, message: str) -> Commit:
        """Create and append a new commit with an incremental ID starting from 1."""
        new_commit = Commit(id=self._next_id, message=message)
        self.commits.append(new_commit)
        self._next_id += 1
        return new_commit

    def find_index(self, commit_id: int) -> int | None:
        """Return the index of a commit with the given ID, or None if not found."""
        for idx, item in enumerate(self.commits):
            if item.id == commit_id:
                return idx
        return None

    def get_commit(self, commit_id: int) -> Commit | None:
        """Return the commit with the given ID, or None if not found."""
        index = self.find_index(commit_id)
        return self.commits[index] if index is not None else None

    def format_log(self) -> list[str]:
        """Generate formatted lines of the commit history (newest first)."""
        if not self.commits:
            return ["Keine Commits vorhanden."]

        lines = ["--- Commit Log (neuester zuerst) ---"]
        for item in reversed(self.commits):
            lines.append(f"Commit #{item.id}: {item.message}")
        return lines

    def log(self) -> None:
        """Print all commits in descending chronological order (newest first)."""
        for line in self.format_log():
            print(line)

    def revert(self, commit_id: int) -> bool:
        """Reset repository to specified commit by removing later commits."""
        target_index = self.find_index(commit_id)
        if target_index is None:
            print(f"Fehler: Commit mit ID {commit_id} existiert nicht.")
            return False

        removed_count = len(self.commits) - (target_index + 1)
        self.commits = self.commits[: target_index + 1]
        print(
            f"Erfolgreich auf Commit #{commit_id} zurückgesetzt "
            f"({removed_count} nachfolgende(r) Commit(s) entfernt)."
        )
        return True


def main() -> None:
    """Demonstrate the functionality of the Repository class."""
    repo = Repository()

    print("=== 1. Mehrere Commits erstellen ===")
    repo.commit("Initialer Commit: Projektstruktur angelegt")
    repo.commit("Feature: Benutzer-Authentifizierung hinzugefügt")
    repo.commit("Feature: Dashboard-Ansicht implementiert")
    repo.commit("Bugfix: Fehler beim Login behoben")

    print("\n=== 2. Commit-Historie anzeigen (log) ===")
    repo.log()

    print("\n=== 3. Ungültigen Revert testen ===")
    repo.revert(99)

    print("\n=== 4. Revert auf Commit #2 durchführen ===")
    repo.revert(2)

    print("\n=== 5. Commit-Historie nach dem Revert anzeigen (log) ===")
    repo.log()

    print("\n=== 6. Weiteren Commit nach dem Revert hinzufügen ===")
    repo.commit("Feature: Neues Design eingeführt")
    repo.log()


if __name__ == "__main__":
    main()
