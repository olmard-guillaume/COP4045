# Import the plotting library used to create the graph
import matplotlib.pyplot as plt

# Import the math library so the user can enter functions
import math


def plot_function(fun_str: str, domain: tuple[float, float], ns: int) -> None:
    """
    Creates a table and graph of a mathematical function.

    Parameters:
        fun_str - string containing the function entered by the user
        domain - tuple containing the minimum and maximum x values
        ns - number of sample points to calculate
    """

    # Get the minimum and maximum x values from the tuple
    xmin_float = domain[0]
    xmax_float = domain[1]

    # Create empty lists to store x and y values
    xs_list = []
    ys_list = []

    # Calculate the spacing between each x value
    dx_float = (xmax_float - xmin_float) / (ns - 1)

    # Start x at the minimum value
    x_float = xmin_float

    # Continue until the desired number of sample points is reached
    while len(xs_list) < ns:

        # Store the current x value
        xs_list.append(x_float)

        # Make x available for eval()
        x = x_float

        # Evaluate the user entered function
        y_float = eval(fun_str)

        # Store the y value
        ys_list.append(y_float)

        # Move to the next x value
        x_float = x_float + dx_float

    # Print the headings for the x and y table
    print("{:<10} {:<10}".format("x", "y"))
    print("----------------------")

    # Variable used to traverse the lists
    i_int = 0

    # Print every x and y value stored in the lists
    while i_int < len(xs_list):

        print("{:<10.3f} {:<10.3f}".format(xs_list[i_int], ys_list[i_int]))

        i_int = i_int + 1

    # Plot the function using the calculated sample points
    plt.plot(xs_list, ys_list, "rx-")

    # Label the graph axes
    plt.xlabel("x")
    plt.ylabel("y")

    # Display the function entered by the user as the graph title
    plt.title(fun_str)

    # Display grid lines to make the graph easier to read
    plt.grid(True)

    # Display the completed graph
    plt.show()


# Read the mathematical function from the user
fun_str = input("Enter function with variable x: ")

xmin_float = float(input("Enter xmin: "))
xmax_float = float(input("Enter xmax: "))
ns_int = int(input("Enter number of samples: "))

domain_tuple = (xmin_float, xmax_float)

# Call the function to calculate and display the table and graph
plot_function(fun_str, domain_tuple, ns_int)