""" Problem 2  demonstrates list and dictionary comprehensions. """


def main() -> None:
    """
    Tests all list and dictionary comprehensions for Problem 2.
    """ 
    # Part A
    # Find all distinct a, b, c, d from 1 through 10 where
    # a^2 + b^2 = c^2 + d^2.


    abcd_list = [
        (a_int, b_int, c_int, d_int)
        for a_int in range(1, 11)
        for b_int in range(1, 11)
        for c_int in range(1, 11)
        for d_int in range(1, 11)
        if len({a_int, b_int, c_int, d_int}) == 4
        and a_int ** 2 + b_int ** 2 == c_int ** 2 + d_int ** 2
    ]

    print("Part A:")
    print(abcd_list)
    print()


    # Create tuples containing the lowercase string and its
    # length, but only for strings shorter than 5 characters.

    strings_list = [
        "One",
        "SEVEN",
        "three",
        "two",
        "Ten"
    ]

    lowercase_list = [
        (string_str.lower(), len(string_str))
        for string_str in strings_list
        if len(string_str) < 5
    ]

    print("Part B:")
    print(lowercase_list)
    print()


    # Part C
    # Convert full names from:
    # Firstname Middlename Lastname
    #
    # into:
    # Firstname M. Lastname

    names_list = [
        "Christopher Ashton Kutcher",
        "Elizabeth Stamatina Fey"
    ]

    shortened_names_list = [
        (
            name_str.split()[0]
            + " "
            + name_str.split()[1][0]
            + ". "
            + name_str.split()[2]
        )
        for name_str in names_list
    ]

    print("Part C:")
    print(shortened_names_list)
    print()


    # Part D
    # Find pairs of words that are anagrams.
    # The comparison is case insensitive.

    lst1 = [
        "Spam",
        "Trams",
        "Elbows",
        "Tops",
        "Astral"
    ]

    lst2 = [
        "Bowels",
        "Sample",
        "Altars",
        "Stop",
        "Course",
        "Smart"
    ]

    anagram_list = [
        (word1_str, word2_str)
        for word1_str in lst1
        for word2_str in lst2
        if sorted(word1_str.lower()) == sorted(word2_str.lower())
    ]

    print("Part D:")
    print(anagram_list)
    print()

    # Part E
    # Create a dictionary that maps each string to its length.


    s = [
        "one",
        "two",
        "three"
    ]

    length_dictionary = {
        string_str: len(string_str)
        for string_str in s
    }

    print("Part E:")
    print(length_dictionary)
    print()


    # Part F
    # Create a dictionary where:
    # key   = index of a vowel
    # value = vowel character
    # The vowel check is case insensitive.

    text = "Hello world"

    vowel_dictionary = {
        index_int: character_str
        for index_int, character_str in enumerate(text)
        if character_str.lower() in "aeiou"
    }

    print("Part F:")
    print(vowel_dictionary)
    print()


# Run the main function.
main()