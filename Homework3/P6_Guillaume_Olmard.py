#Olmard Guillaume


# Problem 6: storage entries represented as files and nested folders.

from __future__ import annotations

import unittest


class Entry:
    """Base class for an entry in a folder hierarchy."""

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        """Initialize an entry with a name and optional parent."""
        self.name = name
        self._parent = parent

    def parent(self) -> Entry | None:
        """Return the entry's parent, or None for a root entry."""
        return self._parent

    def size(self) -> int:
        """Return the storage size; subclasses provide the implementation."""
        raise NotImplementedError

    def absolute_path(self) -> list[Entry]:
        """Return the path from this entry up through the root entry."""
        path = [self]
        current_parent = self.parent()

        if current_parent is not None:
            path.extend(current_parent.absolute_path())

        return path


class File(Entry):
    """A file entry with a byte size."""

    def __init__(self, name: str, parent: Entry | None, bytes_used: int) -> None:
        """Initialize a file and require a nonnegative byte count."""
        super().__init__(name, parent)

        if bytes_used < 0:
            raise ValueError("bytes_used cannot be negative")

        self.bytes_used = bytes_used

    def size(self) -> int:
        """Return the number of bytes used by the file."""
        return self.bytes_used


class Folder(Entry):
    """A folder entry containing zero or more child entries."""

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        """Initialize an empty folder."""
        super().__init__(name, parent)
        self._children: list[Entry] = []

    def add(self, entry: Entry) -> None:
        """Add an entry and set this folder as its parent."""
        entry._parent = self
        self._children.append(entry)

    def children(self) -> tuple[Entry, ...]:
        """Return the folder's children as a tuple."""
        return tuple(self._children)

    def size(self) -> int:
        """Return the total size of files in the folder tree."""
        total = 0

        for entry in self._children:
            total += entry.size()

        return total


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    """Return files at or above minimum_size in the entry hierarchy."""
    if isinstance(entry, File):
        if entry.size() >= minimum_size:
            return [entry]
        return []

    if isinstance(entry, Folder):
        large_files: list[File] = []
        for child in entry.children():
            large_files.extend(find_large_files(child, minimum_size))
        return large_files

    return []


def names(entries: list[Entry]) -> list[str]:
    """Convert entries to names for readable demonstrations and tests."""
    return [entry.name for entry in entries]


def build_example_hierarchy() -> tuple[Folder, File]:
    """Build a hierarchy at least three folder levels deep."""
    root = Folder("root")
    documents = Folder("documents")
    projects = Folder("projects")
    python = Folder("python")

    report = File("report.txt", documents, 900)
    small_file = File("notes.txt", documents, 100)
    program = File("main.py", python, 600)
    readme = File("README.md", projects, 1500)

    documents.add(report)
    documents.add(small_file)
    projects.add(readme)
    python.add(program)
    projects.add(python)
    root.add(documents)
    root.add(projects)

    return root, program


class Problem6Tests(unittest.TestCase):
    """Unit tests for large-file search and absolute paths."""

    def setUp(self) -> None:
        """Create a small hierarchy before each test."""
        self.root = Folder("root")
        self.folder = Folder("folder")
        self.small_file = File("small.txt", self.folder, 50)
        self.large_file = File("large.txt", self.folder, 200)
        self.folder.add(self.small_file)
        self.folder.add(self.large_file)
        self.root.add(self.folder)

    def test_find_large_files_in_folder(self) -> None:
        """A folder search should return nested files meeting the threshold."""
        self.assertEqual(
            find_large_files(self.root, 100),
            [self.large_file],
        )

    def test_find_large_files_in_file(self) -> None:
        """Searching a file should include only that file when it qualifies."""
        self.assertEqual(find_large_files(self.large_file, 200), [self.large_file])
        self.assertEqual(find_large_files(self.small_file, 100), [])

    def test_absolute_path(self) -> None:
        """A file path should run from the file up to the root folder."""
        self.assertEqual(
            names(self.large_file.absolute_path()),
            ["large.txt", "folder", "root"],
        )

    def test_absolute_path_for_root(self) -> None:
        """The root path should contain only the root entry."""
        self.assertEqual(names(self.root.absolute_path()), ["root"])


if __name__ == "__main__":
    unittest.main(exit=False)

    root, nested_file = build_example_hierarchy()

    print("FAU student ID: 23884392")
    print("Outer folder size:", root.size())
    print("Large files at 500 bytes:", names(find_large_files(root, 500)))
    print("Large files at 1000 bytes:", names(find_large_files(root, 1000)))
    print("Nested file absolute path:", names(nested_file.absolute_path()))
