#Olmard Guillaume 

# Problem 5: Recursive Tree Drawing



import turtle


def draw_leaf_straight(recursion_level: int, the_petiole: float,
                       branchno: int = 8) -> None:
    """Draw a vertical stem with side branches and smaller twigs."""

    def branch(level: int, length: float) -> None:
        if level <= 0 or length < 4:
            return

        turtle.width(max(1, level * 0.4))
        turtle.forward(length)

        saved_position = turtle.position()
        saved_heading = turtle.heading()

        turtle.left(35)
        branch(level - 1, length * 0.58)

        turtle.penup()
        turtle.goto(saved_position)
        turtle.setheading(saved_heading)
        turtle.pendown()

        turtle.right(35)
        turtle.right(35)
        branch(level - 1, length * 0.58)

        turtle.penup()
        turtle.goto(saved_position)
        turtle.setheading(saved_heading)
        turtle.pendown()

        turtle.backward(length)

    if recursion_level <= 0 or branchno <= 0:
        return

    start_y = -210

    turtle.penup()
    turtle.goto(0, start_y)
    turtle.setheading(90)
    turtle.pendown()
    turtle.width(2)
    turtle.forward(the_petiole)

    number_of_pairs = min(branchno, 5)
    spacing = the_petiole / (number_of_pairs + 1)

    for i in range(1, number_of_pairs + 1):
        branch_y = start_y + spacing * i
        side_length = the_petiole * (
            0.20 + 0.22 * (1 - i / (number_of_pairs + 1))
        )

        turtle.penup()
        turtle.goto(0, branch_y)
        turtle.setheading(145)
        turtle.pendown()
        branch(recursion_level, side_length)

        turtle.penup()
        turtle.goto(0, branch_y)
        turtle.setheading(35)
        turtle.pendown()
        branch(recursion_level, side_length)


def strB(n: int, base: int = 10) -> str:
    """Convert a non-negative integer to a string in the given base."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if not 2 <= base <= 26:
        raise ValueError("base must be between 2 and 26")

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if n < base:
        return digits[n]

    return strB(n // base, base) + digits[n % base]


def Cnk_m(n: int, k: int) -> int:
    """Calculate n choose k recursively using memoization."""
    memo: dict[tuple[int, int], int] = {}

    def calculate(current_n: int, current_k: int) -> int:
        if current_k < 0 or current_k > current_n:
            return 0
        if current_k == 0 or current_k == current_n:
            return 1
        if (current_n, current_k) in memo:
            return memo[(current_n, current_k)]
        result = calculate(current_n - 1, current_k - 1) + calculate(current_n - 1, current_k)
        memo[(current_n, current_k)] = result
        return result

    return calculate(n, k)


def make_pairs(seq1: list, seq2: list) -> list:
    """Return matching pairs from two sequences, stopping at the shorter one."""
    def build_pairs(index: int, pairs: list) -> list:
        if index >= len(seq1) or index >= len(seq2):
            return pairs
        pairs.append((seq1[index], seq2[index]))
        return build_pairs(index + 1, pairs)
    return build_pairs(0, [])


def testif(condition: bool, message: str) -> None:
    """Print an error message when condition is false."""
    if not condition:
        print("TEST FAILED:", message)


def test_strB() -> None:
    """Run four unit tests for strB."""
    testif(strB(0) == "0", "strB should convert zero")
    testif(strB(123, 16) == "7B", "strB should convert to hexadecimal")
    testif(strB(8191, 16) == "1FFF", "strB should use uppercase digits")
    testif(strB(123456789, 26) == "AA44A1", "strB should convert to base 26")


def test_Cnk_m() -> None:
    """Run four unit tests for Cnk_m."""
    testif(Cnk_m(5, 2) == 10, "C(5,2) should equal 10")
    testif(Cnk_m(10, 3) == 120, "C(10,3) should equal 120")
    testif(Cnk_m(20, 10) == 184756, "C(20,10) should equal 184756")
    testif(Cnk_m(6, 0) == 1, "C(n,0) should equal 1")


def test_make_pairs() -> None:
    """Run five unit tests for make_pairs."""
    testif(make_pairs([1, 2, 3], [4, 5, 6]) == [(1, 4), (2, 5), (3, 6)], "equal lengths")
    testif(make_pairs([1, 2, 3], [4, 5]) == [(1, 4), (2, 5)], "first longer")
    testif(make_pairs([1, 2, 3], [4, 5, 6, 7]) == [(1, 4), (2, 5), (3, 6)], "second longer")
    testif(make_pairs([], [4, 5, 6]) == [], "empty first sequence")
    testif(make_pairs([1, 2, 3], []) == [], "empty second sequence")


# Test the assignment functions.
test_strB()
test_Cnk_m()
test_make_pairs()

print("Base conversion:")
print(strB(255, 16))
print(strB(100, 2))
print(strB(1234, 10))
print(strB(123456789, 26))

print("\nBinomial coefficients:")
print(Cnk_m(5, 2))
print(Cnk_m(10, 3))
print(Cnk_m(20, 10))
print(Cnk_m(6, 0))

print("\nMaking pairs:")
print(make_pairs([1, 2, 3], [4, 5, 6]))
print(make_pairs([1, 2, 3], [4, 5]))
print(make_pairs([], [4, 5, 6]))

# Set up the Turtle window after the functions and tests.
turtle.clearscreen()
turtle.setup(width=850, height=650)
turtle.speed(0)
turtle.delay(0)
turtle.hideturtle()

print("\nFAU Student ID: 23884392")
draw_leaf_straight(6, 120)


turtle.done()
