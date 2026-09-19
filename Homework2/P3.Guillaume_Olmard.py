"""
Problem 3

This program implements a simplified social network using
dictionaries, lists, and tuples.
"""

import csv


def add_user(sn: dict, username: str, fullname: str) -> bool:
    """
    Adds a new user to the social network.

    The new user initially has no friends.

    Parameters:
        sn - social network dictionary
        username - username of the new user
        fullname - full name of the new user

    Returns:
        True if the user was added successfully.
        False if the username already exists.
    """

    try:

        # Check if the username already exists.
        if username in sn:
            return False

        # Add the new user with an empty friend list.
        sn[username] = (fullname, [])

        return True

    except Exception as error:

        # Display a user-friendly error message.
        print("Error adding user:", error)

        # Re-raise the exception.
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """
    Adds a mutual friendship between two users.

    Parameters:
        sn - social network dictionary
        user1 - first username
        user2 - second username

    Returns:
        True if the friendship was added successfully.
        False if either user does not exist.
    """

    try:

        # Check that both users exist.
        if user1 not in sn or user2 not in sn:
            return False

        # Get the friend lists for both users.
        user1_friends = sn[user1][1]
        user2_friends = sn[user2][1]

        # Add user2 to user1's friend list if necessary.
        if user2 not in user1_friends:
            user1_friends.append(user2)

        # Add user1 to user2's friend list if necessary.
        if user1 not in user2_friends:
            user2_friends.append(user1)

        return True

    except Exception as error:

        # Display a user-friendly error message.
        print("Error adding friend:", error)

        # Re-raise the exception.
        raise


def get_friends(
    sn: dict,
    user1: str,
    distance: int
) -> list:
    """
    Finds all friends within the specified link distance.

    Friends at distance 1 are the user's immediate friends.
    Friends at distance 2 include the immediate friends and
    their friends, and so on.

    Parameters:
        sn - social network dictionary
        user1 - username to search from
        distance - maximum link distance

    Returns:
        A list containing usernames found within the distance.
        Returns an empty list if the user does not exist or
        there are no friends to return.
    """

    try:

        # Return an empty list if the user does not exist.
        if user1 not in sn:
            return []

        # Return an empty list if the distance is not positive.
        if distance <= 0:
            return []

        # This list stores the users we still need to visit.
        search_list = []

        # Add the starting user's friends to the search list.
        for friend in sn[user1][1]:
            search_list.append((friend, 1))

        # This set keeps track of users already visited.
        visited = set()

        # The starting user has already been visited.
        visited.add(user1)

        # This list stores the final result.
        friends_list = []

        # Continue searching while there are users to examine.
        while len(search_list) > 0:

            # Remove the first item from the search list.
            current_user, current_distance = search_list.pop(0)

            # Skip users that have already been visited.
            if current_user in visited:
                continue

            # Mark the current user as visited.
            visited.add(current_user)

            # Add the current user to the result.
            friends_list.append(current_user)

            # Only search farther if we have not reached
            # the requested distance.
            if current_distance < distance:

                # Add the current user's friends to the search.
                for friend in sn[current_user][1]:

                    if friend not in visited:
                        search_list.append(
                            (friend, current_distance + 1)
                        )

        return friends_list

    except Exception as error:

        # Display a user-friendly error message.
        print("Error finding friends:", error)

        # Re-raise the exception.
        raise


def save_network(filename: str, sn: dict) -> None:
    """
    Saves a social network dictionary to a CSV file.

    Each row contains the username, full name, and friends.

    Parameters:
        filename - name of the CSV file
        sn - social network dictionary
    """

    try:

        # Open the CSV file for writing.
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file_object:

            # Create a CSV writer.
            writer = csv.writer(file_object)

            # Write a header row.
            writer.writerow(
                ["username", "fullname", "friends"]
            )

            # Write each user to the CSV file.
            for username, user_data in sn.items():

                # Get the full name.
                fullname = user_data[0]

                # Get the friend list.
                friends = user_data[1]

                # Store the friends as a comma-separated string.
                friends_string = ",".join(friends)

                # Write the user's information.
                writer.writerow(
                    [username, fullname, friends_string]
                )

    except Exception as error:

        # Display a user-friendly error message.
        print("Error saving network:", error)

        # Re-raise the exception.
        raise


def load_network(filename: str) -> dict:
    """
    Loads a social network from a CSV file.

    Parameters:
        filename - name of the CSV file

    Returns:
        A dictionary containing the social network.
    """

    try:

        # Create an empty social network.
        sn = {}

        # Open the CSV file for reading.
        with open(
            filename,
            "r",
            newline="",
            encoding="utf-8"
        ) as file_object:

            # Create a CSV reader.
            reader = csv.reader(file_object)

            # Skip the header row.
            next(reader)

            # Read every user from the file.
            for row in reader:

                # Get the username.
                username = row[0]

                # Get the full name.
                fullname = row[1]

                # Get the friend string.
                friends_string = row[2]

                # Convert the friend string back into a list.
                if friends_string == "":
                    friends = []
                else:
                    friends = friends_string.split(",")

                # Add the user to the network.
                sn[username] = (fullname, friends)

        return sn

    except Exception as error:

        # Display a user-friendly error message.
        print("Error loading network:", error)

        # Re-raise the exception.
        raise


def main() -> None:
    """
    Tests all social network functions.
    """

    # ---------------------------------------------------------
    # Create an initial social network.
    # ---------------------------------------------------------

    sn = {
        "alice": (
            "Alice Smith",
            ["maria"]
        ),
        "maria": (
            "Maria Cortez",
            ["alice", "joe", "david"]
        ),
        "joe": (
            "Joseph Adams",
            ["maria", "eve"]
        ),
        "eve": (
            "Evelyn Cooper",
            ["joe"]
        ),
        "david": (
            "David Benson",
            ["maria"]
        )
    }

    print("Initial social network:")
    print(sn)
    print()


    # ---------------------------------------------------------
    # Test part A: add_user
    # ---------------------------------------------------------

    print("Part A:")

    result = add_user(
        sn,
        "sarah",
        "Sarah Johnson"
    )

    print("Adding Sarah:", result)
    print(sn)
    print()


    # Try adding a user that already exists.
    result = add_user(
        sn,
        "alice",
        "Alice Smith"
    )

    print("Adding Alice again:", result)
    print()


    # ---------------------------------------------------------
    # Test part B: add_friend
    # ---------------------------------------------------------

    print("Part B:")

    result = add_friend(
        sn,
        "sarah",
        "alice"
    )

    print("Adding Sarah and Alice as friends:", result)
    print(sn)
    print()


    # Try adding a friendship with a user that does not exist.
    result = add_friend(
        sn,
        "sarah",
        "unknown"
    )

    print("Adding Sarah and unknown user:", result)
    print()


    # ---------------------------------------------------------
    # Test part C: get_friends
    # ---------------------------------------------------------

    print("Part C:")

    friends_distance_1 = get_friends(
        sn,
        "alice",
        1
    )

    print("Alice distance 1:")
    print(friends_distance_1)
    print()

    friends_distance_2 = get_friends(
        sn,
        "alice",
        2
    )

    print("Alice distance 2:")
    print(friends_distance_2)
    print()

    friends_distance_3 = get_friends(
        sn,
        "alice",
        3
    )

    print("Alice distance 3:")
    print(friends_distance_3)
    print()


    # ---------------------------------------------------------
    # Test an invalid username.
    # ---------------------------------------------------------

    friends_invalid = get_friends(
        sn,
        "unknown",
        2
    )

    print("Unknown user:")
    print(friends_invalid)
    print()


    # ---------------------------------------------------------
    # Test part D: save_network
    # ---------------------------------------------------------

    print("Part D:")

    filename = "social_network.csv"

    save_network(
        filename,
        sn
    )

    print("Network saved to:", filename)
    print()


    # ---------------------------------------------------------
    # Test part E: load_network
    # ---------------------------------------------------------

    print("Part E:")

    loaded_network = load_network(
        filename
    )

    print("Network loaded from file:")
    print(loaded_network)
    print()


# Run the main function.
main()