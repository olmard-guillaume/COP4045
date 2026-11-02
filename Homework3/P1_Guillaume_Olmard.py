
# Olmard Guillaume

# Problem 1 NVector

"""
Class NVector represents a vector in N-dimensional space.
It supports addition, multiplication, indexing, and comparison.
"""


class NVector:
    """
    Represents a vector of real numbers stored in a list.
    """

    def __init__(self, *Vector_elements: object) -> None:
        """
        Create a vector from a sequence or individual numbers.
        A new list is created so the original list is not shared.
        """
        if len(Vector_elements) == 1:
            self.vector_elements = list(Vector_elements[0])
        else:
            self.vector_elements = list(Vector_elements)

    def __len__(self) -> int:
        """Return the number of elements."""
        return len(self.vector_elements)

    def __getitem__(self, index: int) -> float:
        """Return an element using its index."""
        return self.vector_elements[index]

    def __setitem__(self, index: int, value: float) -> None:
        """Change an element using its index."""
        self.vector_elements[index] = value

    def __str__(self) -> str:
        """Return the vector as a string."""
        return str(self.vector_elements)

    def __eq__(self, other: object) -> bool:
        """Check whether two vectors have equal elements."""
        if not isinstance(other, NVector):
            return False
        return self.vector_elements == other.vector_elements

    def __ne__(self, other: object) -> bool:
        """Check whether two vectors are different."""
        return not self == other

    def __add__(self, other: object) -> "NVector":
        """Add another vector or a number to every element."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have the same length.")

            result = []
            for i in range(len(self)):
                result.append(self[i] + other[i])

            return NVector(result)

        if isinstance(other, (int, float)):
            result = []
            for element in self.vector_elements:
                result.append(element + other)
            return NVector(result)

        return NotImplemented

    def __radd__(self, other: object) -> "NVector":
        """Support addition when the vector is on the right."""
        return self.__add__(other)

    def __mul__(self, other: object) -> float:
        """Return the dot product or the sum of elements times a number."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have the same length.")

            total = 0
            for i in range(len(self)):
                total += self[i] * other[i]
            return total

        if isinstance(other, (int, float)):
            total = 0
            for element in self.vector_elements:
                total += element * other
            return total

        return NotImplemented

    def __rmul__(self, other: object) -> float:
        """Support multiplication when the vector is on the right."""
        return self.__mul__(other)

    @classmethod
    def zeros(cls, n: int) -> "NVector":
        """Create a vector containing n zeros."""
        if not isinstance(n, int):
            raise TypeError("The number of zeros must be an integer.")

        if n < 0:
            raise ValueError("The number of zeros cannot be negative.")

        return cls([0] * n)


def testif(
    b: bool,
    testname: str,
    msgOK: str = "",
    msgFailed: str = ""
) -> bool:
    """Print whether a test passed and return its result."""
    if b:
        print("Success: " + testname + "; " + msgOK)
    else:
        print("Failed: " + testname + "; " + msgFailed)

    return b


def main() -> None:
    """Test the NVector class."""
    print("Testing NVector")

    # Part a: Create vectors using different argument formats.
    vector_a = NVector([3, 0, 1, -1])
    vector_b = NVector((3, 0, 1, -1))
    vector_c = NVector(3, 0, 1, -1)

    testif(
        vector_a == vector_b == vector_c,
        "Part a",
        "All three constructors work.",
        "The constructors do not match."
    )

    # Additional test: Make sure the original list is not shared.
    original_list = [3, 0, 1, -1]
    vector_copy = NVector(original_list)
    original_list[0] = 100

    testif(
        vector_copy[0] == 3,
        "Constructor copy",
        "The original list is not shared.",
        "The original list was shared."
    )

    # Part b: Test length.
    testif(
        len(vector_a) == 4,
        "Part b",
        "The vector has four elements.",
        "The vector length is incorrect."
    )

    # Part c: Test indexing, including negative indexing.
    testif(
        vector_a[0] == 3 and vector_a[-1] == -1,
        "Part c",
        "Indexing works.",
        "Indexing failed."
    )

    # Additional test: Invalid index should raise IndexError.
    try:
        vector_a[10]
        invalid_index_test = False
    except IndexError:
        invalid_index_test = True

    testif(
        invalid_index_test,
        "Invalid index",
        "IndexError was raised correctly.",
        "IndexError was not raised."
    )

    # Part d: Test changing an element.
    vector_d = NVector([3, 0, 1, -1])
    vector_d[1] = 5

    testif(
        vector_d[1] == 5 and vector_d[-1] == -1,
        "Part d",
        "Element assignment works.",
        "Element assignment failed."
    )

    # Part e: Test string representation.
    testif(
        str(vector_a) == "[3, 0, 1, -1]",
        "Part e",
        "String representation works.",
        "String representation failed."
    )

    # Part f: Test equality and inequality.
    testif(
        vector_a == vector_b and vector_a != NVector([1, 2]),
        "Part f",
        "Equality and inequality work.",
        "Comparison failed."
    )

    # Part g: Test vector addition and scalar addition.
    vector_sum = vector_a + vector_b
    vector_plus_number = vector_a + 2
    number_plus_vector = 2 + vector_a

    testif(
        vector_sum == NVector([6, 0, 2, -2])
        and vector_plus_number == NVector([5, 2, 3, 1])
        and number_plus_vector == NVector([5, 2, 3, 1]),
        "Part g",
        "Addition works.",
        "Addition failed."
    )

    # Additional test: Adding vectors of different lengths.
    try:
        vector_a + NVector([1, 2])
        different_length_test = False
    except ValueError:
        different_length_test = True

    testif(
        different_length_test,
        "Different length addition",
        "ValueError was raised correctly.",
        "ValueError was not raised."
    )

    # Part h: Test dot product and scalar multiplication.
    dot_product = vector_a * vector_b
    scalar_product = vector_a * 2
    reflected_product = 2 * vector_a

    testif(
        dot_product == 11
        and scalar_product == 6
        and reflected_product == 6,
        "Part h",
        "Multiplication works.",
        "Multiplication failed."
    )

    # Part i: Test zeros.
    zero_vector = NVector.zeros(4)

    testif(
        zero_vector == NVector([0, 0, 0, 0]),
        "Part i",
        "The zeros method works.",
        "The zeros method failed."
    )

    # Additional test: Test zeros with dimension zero.
    testif(
        NVector.zeros(0) == NVector([]),
        "Zeros boundary test",
        "A zero-dimensional vector works.",
        "The zero-dimensional vector failed."
    )

    # Display FAU student ID for the required screenshot.
    student_id = "23884392"
    print("\nFAU Student ID:", student_id)

    print("\nTesting completed.")


if __name__ == "__main__":
    main()
