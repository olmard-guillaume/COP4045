"""
Problem 4


"""

import csv
import os


def load_movie_list(filename: str) -> dict:
    """
    Reads a movie CSV file and stores the movies in a dictionary.


    """

    try:

        # Create an empty dictionary.
        movie_dictionary = {}

        # Open the CSV file.
        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file_object:

            # Create a CSV dictionary reader.
            reader = csv.DictReader(file_object)

            # Read each movie.
            for row in reader:

                # Get the movie title.
                title = row["Title"]

                # Get the movie year.
                year = row["Year"]

                # Store the row using title and year as the key.
                movie_dictionary[(title, year)] = row

        return movie_dictionary

    except Exception as error:

        # Display a user-friendly error message.
        print("Error loading movie file:", error)

        # Re-raise the exception.
        raise


def load_casts(filename: str) -> list:
    """
    Reads the IMDB casts CSV file.

    The casts file does not have a header.

    Parameters:
        filename - name of the casts CSV file

    Returns:
        A list containing the rows from the casts file.
    """

    try:

        # Create an empty list.
        casts_list = []

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file_object:

            # Create a CSV reader.
            reader = csv.reader(file_object)

            # Read every movie.
            for row in reader:

                casts_list.append(row)

        return casts_list

    except Exception as error:

        # Display a user-friendly error message.
        print("Error loading casts file:", error)

        # Re-raise the exception.
        raise


def create_collaboration_dictionary(
    rated_movies: dict,
    casts_list: list
) -> dict:
    """
    Creates a dictionary containing director/actor
    collaboration counts for top rated movies.


    """

    try:

        # Create an empty dictionary.
        collaboration_dictionary = {}

        # Examine every movie in the casts file.
        for movie in casts_list:

            # Make sure the row contains enough information.
            if len(movie) < 8:
                continue

            # Get the movie information.
            title = movie[0]
            year = movie[1]
            director = movie[2]


            if (title, year) not in rated_movies:
                continue

            # Actors are stored in positions 3 through 7.
            for actor in movie[3:8]:

                # Create a key for the director/actor pair.
                collaboration_key = (director, actor)

                # Add one to the collaboration count.
                if collaboration_key in collaboration_dictionary:

                    collaboration_dictionary[
                        collaboration_key
                    ] = collaboration_dictionary[
                        collaboration_key
                    ] + 1

                else:

                    collaboration_dictionary[
                        collaboration_key
                    ] = 1

        return collaboration_dictionary

    except Exception as error:

        # Display a user-friendly error message.
        print("Error creating collaboration dictionary:", error)

        # Re-raise the exception.
        raise


def create_grossing_actor_dictionary(
    grossing_movies: dict,
    casts_list: list
) -> dict:
    """
    Creates a dictionary containing the total USA box office
    for each actor in the top grossing movies.

    Parameters:
        grossing_movies - dictionary containing top grossing movies
        casts_list - list containing director and cast information

    Returns:
        A dictionary where each key is an actor and each value
        is their total box office from the movies.
    """

    try:

        # Create an empty dictionary.
        actor_dictionary = {}

        # Examine every movie in the casts file.
        for movie in casts_list:

            # Make sure the row contains enough information.
            if len(movie) < 8:
                continue

            # Get the movie title.
            title = movie[0]

            # Get the movie year.
            year = movie[1]

            # Check whether this movie is in the top grossing list.
            if (title, year) not in grossing_movies:
                continue

            # Get the movie information.
            movie_information = grossing_movies[
                (title, year)
            ]

            # Get the USA box office amount.
            box_office_string = movie_information[
                "USA Box Office"
            ]

            # Remove commas and convert to a number.
            box_office = float(
                box_office_string.replace(",", "")
                .replace("$", "")
            )

            # Process all five actors.
            for actor in movie[3:8]:

                # Add the movie's box office to the actor's total.
                if actor in actor_dictionary:

                    actor_dictionary[actor] = (
                        actor_dictionary[actor]
                        + box_office
                    )

                else:

                    actor_dictionary[actor] = box_office

        return actor_dictionary

    except Exception as error:

        # Display a user-friendly error message.
        print("Error creating actor dictionary:", error)

        # Re-raise the exception.
        raise


def display_top_collaborations(
    rated_filename: str,
    casts_filename: str,
    limit: int | None = 10
) -> None:
    """
    Displays director/actor collaboration rankings.

    Only movies appearing in the top rated movie list are used.

    Parameters:
        rated_filename - name of the top rated CSV file
        casts_filename - name of the casts CSV file
        limit - maximum number of rankings to display.
                None displays all rankings.
    """

    try:

        # Load the top rated movies.
        rated_movies = load_movie_list(
            rated_filename
        )

        # Load the cast information.
        casts_list = load_casts(
            casts_filename
        )

        # Create the collaboration dictionary.
        collaboration_dictionary = (
            create_collaboration_dictionary(
                rated_movies,
                casts_list
            )
        )

        # Sort the collaborations by number of movies
        # from highest to lowest.
        ranking_list = sorted(
            collaboration_dictionary.items(),
            key=lambda item: item[1],
            reverse=True
        )

        print("Top Director/Actor Collaborations")
        print("----------------------------------")

        # Keep track of the ranking number.
        rank_int = 1

        # Display the requested number of entries.
        for collaboration, number_of_movies in ranking_list:

            # Stop if the requested limit has been reached.
            if limit is not None and rank_int > limit:
                break

            # Separate the director and actor.
            director = collaboration[0]
            actor = collaboration[1]

            print(
                str(rank_int)
                + ". "
                + director
                + " - "
                + actor
                + " - "
                + str(number_of_movies)
                + " movies"
            )

            rank_int = rank_int + 1

        print()

    except Exception as error:

        # Display a user-friendly error message.
        print("Error displaying collaborations:", error)

        # Re-raise the exception.
        raise


def display_top_actors(
    grossing_filename: str,
    casts_filename: str,
    limit: int | None = 10
) -> None:
    """
    Displays actors ranked by the total USA box office
    of movies in the top grossing movie list.

    Parameters:
        grossing_filename - name of the top grossing CSV file
        casts_filename - name of the casts CSV file
        limit - maximum number of rankings to display.
                None displays all rankings.
    """

    try:

        # Load the top grossing movies.
        grossing_movies = load_movie_list(
            grossing_filename
        )

        # Load the cast information.
        casts_list = load_casts(
            casts_filename
        )

        # Create the actor box office dictionary.
        actor_dictionary = (
            create_grossing_actor_dictionary(
                grossing_movies,
                casts_list
            )
        )

        ranking_list = sorted(
            actor_dictionary.items(),
            key=lambda item: item[1],
            reverse=True
        )

        print("Top Actors by Total Box Office")
        print("------------------------------")

        # Keep track of the ranking number.
        rank_int = 1

        # Display the requested number of entries.
        for actor, total_box_office in ranking_list:

            # Stop if the requested limit has been reached.
            if limit is not None and rank_int > limit:
                break

            print(
                str(rank_int)
                + ". "
                + actor
                + " - $"
                + format(total_box_office, ",.2f")
            )

            rank_int = rank_int + 1

        print()

    except Exception as error:

        print("Error displaying actors:", error)

        raise


def main() -> None:
    """
    Test the movie ranking functions.
    """

    program_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    rated_filename = os.path.join(
        program_folder,
        "imdb-top-rated.csv"
    )

    grossing_filename = os.path.join(
        program_folder,
        "imdb-top-grossing.csv"
    )

    casts_filename = os.path.join(
        program_folder,
        "imdb-top-casts.csv"
    )

    print("Name: Guillaume Olmard")
    print("IMDB Movie Rankings")
    print("====================")
    print()

    # Part A
    print("Part A")
    display_top_collaborations(
        rated_filename,
        casts_filename,
        10
    )

    # Part B
    print("Part B")
    display_top_actors(
        grossing_filename,
        casts_filename,
        10
    )


main()