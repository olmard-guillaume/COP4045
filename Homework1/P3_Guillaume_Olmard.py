# Create a function that takes a string and a substring length
# and returns the first duplicated substring if one exists.
def find_dup_str(s, n):
    """
    Finds the first duplicated substring of length n
    in the given string and returns it.
    """

    # Return an empty string if the substring length
    # is invalid or larger than the string.
    if n <= 0 or n > len(s):
        return ""

    # Traverse every possible substring of length n.
    for i in range(len(s) - n + 1):

        # Create the current substring using string slicing.
        sub = s[i:i + n]

        # Compare the current substring with the remaining
        # substrings that come after it.
        for j in range(i + n, len(s) - n + 1):

            # If a duplicate is found, return it immediately.
            if sub == s[j:j + n]:
                return sub

    # Return an empty string if no duplicate exists.
    return ""


# Create a function that finds the longest duplicated
# substring in the given string.
def find_max_dup(s):
    """
    Finds and returns the longest duplicated substring
    in the given string.
    """

    # Check substring lengths from largest to smallest.
    for n in range(len(s), 0, -1):

        # Call find_dup_str to search for a duplicate
        # of the current length.
        dup = find_dup_str(s, n)

        # Return the first duplicate that is found.
        if dup != "":
            return dup

    # Return an empty string if no duplicated substring exists.
    return ""


# Read the string from the user.
s = input("Enter a string: ")

# Read the desired substring length.
n = int(input("Enter substring length: "))

# Call the function to find the duplicated substring.
result = find_dup_str(s, n)

# Display the duplicated substring.
print("Duplicated substring:", result)

# Call the function to find the longest duplicated substring.
max_dup = find_max_dup(s)

# Display the longest duplicated substring.
print("Longest duplicated substring:", max_dup)