#Olmard Guillaume 

# Problem 4: Non-interactive text editor

"""
Problem 4: Non-interactive text editor.

This program implements functions to read, find, replace, and append
text in UTF-8 files. It also includes unit tests for ed_find() and
ed_replace(), and a main() function demonstrating all four functions.
"""


def testif(condition: bool, message: str) -> None:
    """
    Check whether a test condition is true.

    Preconditions:
        condition must be a Boolean value.
        message must be a string.

    Postconditions:
        Prints a message if the condition is false.
        Does not change the condition or message.
    """
    if not condition:
        print("TEST FAILED:", message)


def ed_read(filename: str, from_: int = 0, to: int = -1) -> str:
    """
    Read a portion of a UTF-8 text file.

    Preconditions:
        filename is the name or path of an existing readable file.
        from_ is a nonnegative file position.
        to is -1 or a nonnegative file position.

    Postconditions:
        Returns the text in the half-open interval [from_, to).
        If to == -1, reads from from_ through the end of the file.
        Raises IndexError if from_ exceeds the file length or if
        to exceeds the file length, or if to < from_.
        File I/O errors are passed to the caller.
        The file is not modified.
    """
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    file_length = len(content)

    if from_ < 0:
        raise IndexError("The starting position cannot be negative.")

    if to < -1:
        raise IndexError("The ending position must be -1 or nonnegative.")

    if from_ > file_length:
        raise IndexError("The starting position exceeds the file length.")

    if to != -1:
        if to > file_length:
            raise IndexError("The ending position exceeds the file length.")

        if to < from_:
            raise IndexError("The ending position cannot precede the start.")

        return content[from_:to]

    return content[from_:]


def ed_find(filename: str, search_str: str) -> list[int]:
    """
    Find all positions of a string in a file.

    Preconditions:
        filename is the name or path of an existing readable file.
        search_str is a string.

    Postconditions:
        Returns a list of starting positions where search_str occurs.
        Positions are zero-based.
        An empty search string returns every position from zero
        through the length of the file.
        Returns an empty list if a nonempty search string is absent.
        File I/O errors are passed to the caller.
        The file is not modified.
    """
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    positions: list[int] = []
    position = 0

    if search_str == "":
        return list(range(len(content) + 1))

    while True:
        position = content.find(search_str, position)

        if position == -1:
            break

        positions.append(position)
        position += 1

        # Avoid an infinite loop when searching for an empty string.
        if search_str == "" and position > len(content):
            break

    return positions


def ed_replace(
    filename: str,
    search_str: str,
    replace_with: str,
    occurrence: int = -1,
) -> int:
    """
    Replace occurrences of a string in a file.

    Preconditions:
        filename is the name or path of an existing readable and writable
        file.
        search_str and replace_with are strings.
        occurrence is -1 or a nonnegative integer.

    Postconditions:
        If occurrence == -1, replaces every non-overlapping occurrence.
        If occurrence >= 0, replaces only the occurrence at that
        zero-based match index.
        Returns the number of replacements made.
        If the requested occurrence does not exist, returns zero.
        An empty search string raises ValueError.
        File I/O errors are passed to the caller.
        The file is not changed if validation fails before writing.
    """
    if not isinstance(occurrence, int) or isinstance(occurrence, bool):
        raise TypeError("occurrence must be an integer.")

    if occurrence < -1:
        raise ValueError("occurrence must be -1 or nonnegative.")

    if search_str == "":
        raise ValueError("search_str cannot be empty.")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    positions = ed_find_in_text(content, search_str)

    if occurrence == -1:
        replacement_count = len(positions)

        if replacement_count == 0:
            return 0

        new_content = content.replace(search_str, replace_with)

    elif occurrence >= len(positions):
        return 0

    else:
        target_position = positions[occurrence]

        new_content = (
            content[:target_position]
            + replace_with
            + content[target_position + len(search_str):]
        )
        replacement_count = 1

    with open(filename, "w", encoding="utf-8") as file:
        file.write(new_content)

    return replacement_count


def ed_find_in_text(content: str, search_str: str) -> list[int]:
    """
    Find non-overlapping occurrences in an in-memory string.

    Preconditions:
        content and search_str are strings.
        search_str is not empty.

    Postconditions:
        Returns the zero-based starting positions of each
        non-overlapping occurrence. Does not modify either string.
    """
    positions: list[int] = []
    position = 0

    if search_str == "":
        return list(range(len(content) + 1))

    while True:
        position = content.find(search_str, position)

        if position == -1:
            break

        positions.append(position)
        position += 1

        # Avoid an infinite loop when searching for an empty string.
        if search_str == "" and position > len(content):
            break

    return positions


def ed_append(filename: str, string: str) -> int:
    """
    Append text to the end of a file.

    Preconditions:
        filename is a valid file name or path.
        string is the text to append.

    Postconditions:
        Appends string to the file using UTF-8 encoding.
        Creates the file if it does not exist.
        Returns the number of characters written.
        File I/O errors are passed to the caller.
    """
    with open(filename, "a", encoding="utf-8") as file:
        return file.write(string)


def test_ed_find() -> None:
    """
    Unit tests for ed_find().

    Preconditions:
        The program can create and access a temporary test file.

    Postconditions:
        Tests found, missing, and repeated strings.
        Prints a failure message if a test fails.
        Removes the test file after testing.
    """
    filename = "test_ed_find.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("abcabc123abc")

    testif(ed_find(filename, "abc") == [0, 3, 9],
           "ed_find should find every occurrence.")

    testif(ed_find(filename, "123") == [6],
           "ed_find should find a single occurrence.")

    testif(ed_find(filename, "xyz") == [],
           "ed_find should return an empty list when not found.")

    testif(ed_find(filename, "cab") == [2],
           "ed_find should find a substring inside the text.")

    import os
    os.remove(filename)

    print("ed_find tests completed.")


def test_ed_replace() -> None:
    """
    Unit tests for ed_replace().

    Preconditions:
        The program can create and access a temporary test file.

    Postconditions:
        Tests replacing all occurrences, replacing one occurrence,
        and requesting an occurrence that does not exist.
        Prints a failure message if a test fails.
        Removes the test file after testing.
    """
    filename = "test_ed_replace.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("abc123abc123")

    replaced = ed_replace(filename, "abc", "XYZ")
    testif(replaced == 2,
           "ed_replace should replace all occurrences.")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    testif(content == "XYZ123XYZ123",
           "ed_replace should produce the expected content.")

    with open(filename, "w", encoding="utf-8") as file:
        file.write("abc123abc123")

    replaced = ed_replace(filename, "abc", "XYZ", 1)
    testif(replaced == 1,
           "ed_replace should replace only the requested occurrence.")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    testif(content == "abc123XYZ123",
           "ed_replace should replace the second occurrence only.")

    replaced = ed_replace(filename, "abc", "XYZ", 5)
    testif(replaced == 0,
           "ed_replace should return zero for a missing occurrence.")

    import os
    os.remove(filename)

    print("ed_replace tests completed.")


def main() -> None:
    """
    Demonstrate all four text-editing functions and run the unit tests.

    Preconditions:
        The program can create and modify files in its working folder.

    Postconditions:
        Demonstrates append, read, find, and replace operations.
        Runs the ed_find() and ed_replace() unit tests.
    """
    filename = "file1.txt"

    # Start with a clean demonstration file.
    with open(filename, "w", encoding="utf-8") as file:
        file.write("")

    print("DEMONSTRATING THE TEXT EDITOR")
    print("-----------------------------")

    # Demonstrate appending text.
    written = ed_append(filename, "0123456789")
    print("Characters appended:", written)

    ed_append(filename, "0123456789")

    # Demonstrate reading a range and reading to the end.
    print("Read positions 3 through 8:", ed_read(filename, 3, 9))
    print("Read from position 3 to the end:", ed_read(filename, 3))

    # Demonstrate finding a string.
    print("Positions of '345':", ed_find(filename, "345"))
    print("Positions of '356':", ed_find(filename, "356"))

    # Demonstrate replacing one occurrence.
    replacements = ed_replace(filename, "345", "ABCDE", 1)
    print("Number of replacements:", replacements)
    print("File after replacing one occurrence:", ed_read(filename))

    # Demonstrate replacing all occurrences.
    with open(filename, "w", encoding="utf-8") as file:
        file.write("01234567890123456789")

    replacements = ed_replace(filename, "345", "ABCDE")
    print("Number of replacements:", replacements)
    print("File after replacing all occurrences:", ed_read(filename))

    # Display the student ID for the required terminal screenshot.
    # Replace the placeholder with your own FAU student ID.
    student_id = "23884392"
    print("\nFAU Student ID:", student_id)

    # Run the unit tests.
    print("\nRUNNING UNIT TESTS")
    print("------------------")
    test_ed_find()
    test_ed_replace()

    print("\nProgram completed.")


if __name__ == "__main__":
    main()
