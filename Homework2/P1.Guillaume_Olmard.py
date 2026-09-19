"""
This program numbers the lines of a Python file and parses
the functions contained in a Python source file.
"""

# Import the modules used to parse Python source code.
import ast
import io
import tokenize


def line_number(input_file: str, output_file: str) -> None:
    """
    Reads a text file and writes each line to another file
    with the line number added to the beginning of the line.

    Parameters:
        input_file - name of the file to read
        output_file - name of the file to write
    """

    try:

        # Open the input file for reading.
        with open(input_file, "r") as input_file_object:

            # Open the output file for writing.
            with open(output_file, "w") as output_file_object:

                # Start the line number at 1.
                line_int = 1

                # Read every line in the input file.
                for line in input_file_object:

                    # Write the line number and the original line.
                    output_file_object.write(
                        str(line_int) + ". " + line
                    )

                    # Increase the line number.
                    line_int = line_int + 1

    except Exception as error:

        # Display a user-friendly error message.
        print("Error numbering the file:", error)

        # Re-raise the original exception.
        raise


def remove_comments(source: str) -> str:
    """
    Removes comments from Python source code while keeping
    strings and docstrings unchanged.

    Parameters:
        source - Python source code as a string

    Returns:
        The source code with comments removed.
    """

    try:

        # Split the source into lines.
        source_lines = source.splitlines(keepends=True)

        # Find all tokens in the Python source.
        tokens = tokenize.generate_tokens(
            io.StringIO(source).readline
        )

        # Remove each actual comment from its line.
        for token in tokens:

            if token.type == tokenize.COMMENT:

                # Get the line and column where the comment starts.
                line_number_int = token.start[0] - 1
                column_int = token.start[1]

                # Remove the comment while keeping the indentation
                # and code before the comment.
                source_lines[line_number_int] = (
                    source_lines[line_number_int][:column_int]
                    + "\n"
                )

        # Put all of the lines back together.
        return "".join(source_lines)

    except (tokenize.TokenError, IndentationError):

        # Return the original source if tokenizing fails.
        return source


def parse_functions(py_file: str) -> tuple:
    """
    Reads and parses a Python source file and returns a tuple
    containing information about each function in the file.

    Each function tuple contains:
        element 0 - line number of the function definition
        element 1 - function name
        element 2 - formal argument list
        element 3 - function signature and body

    The returned functions are ordered alphabetically by name.

    Parameters:
        py_file - name of the Python source file

    Returns:
        A tuple of tuples containing information about the functions.
    """

    try:

        # Open the Python file and read all of its contents.
        with open(py_file, "r") as file_object:
            source = file_object.read()

        # Parse the original Python source code.
        tree = ast.parse(source)

        # Remove comments while preserving the original formatting.
        source_without_comments = remove_comments(source)

        # Split the cleaned source into individual lines.
        source_lines = source_without_comments.splitlines(
            keepends=True
        )

        # Create an empty list to store function information.
        function_list = []

        # Find every function definition in the Python file.
        for node in ast.walk(tree):

            # Check for regular and asynchronous functions.
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                # Get the formal argument list as a string.
                argument_list = ast.unparse(node.args)

                # Get the starting and ending lines of the function.
                start_line = node.lineno
                end_line = node.end_lineno

                # Create a list to store the function lines.
                function_lines = []

                # Get every line that belongs to the function.
                for line_number_int in range(
                    start_line - 1, end_line
                ):

                    # Get the current line.
                    current_line = source_lines[line_number_int]

                    # Remove the newline from the end.
                    current_line = current_line.rstrip("\n")

                    # Keep the line if it is not empty.
                    if current_line.strip() != "":
                        function_lines.append(current_line)

                # Create the complete function code string.
                function_code = ""

                # Add every cleaned line to the function code.
                for function_line in function_lines:
                    function_code = (
                        function_code
                        + function_line
                        + "\n"
                    )

                # Create a tuple containing the function information.
                function_tuple = (
                    node.lineno,
                    node.name,
                    argument_list,
                    function_code
                )

                # Add the function tuple to the list.
                function_list.append(function_tuple)

        # Sort the functions alphabetically by function name.
        function_list.sort(
            key=lambda function: function[1]
        )

        # Convert the list into a tuple of tuples.
        return tuple(function_list)

    except Exception as error:

        # Display a user-friendly error message.
        print("Error parsing the Python file:", error)

        # Re-raise the original exception.
        raise


def main() -> None:
    """
    Tests the line_number and parse_functions functions
    using this Python source file.
    """

    # Get the name of the Python file currently being executed.
    source_file = __file__

    # Create a separate output file so the source program
    # is not overwritten.
    numbered_file = "P1.Guillaume_Olmard_numbered.txt"

    # Test the line_number function.
    line_number(source_file, numbered_file)

    # Display the name of the created file.
    print("Numbered file created:", numbered_file)

    # Test parse_functions using this Python source file.
    parsed_functions = parse_functions(source_file)

    # Display the tuple returned by parse_functions.
    print("Parsed functions:")
    print(parsed_functions)


main()