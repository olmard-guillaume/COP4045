
# This is where we import math and plot modules
import math 
import matplotlib.pyplot as plt 

# Start of while loop where you input a as a_str string and convert it to a_float
while True: 

    a_str = input("enter coefficent a (press enter to quit) : " )

    if a_str == "":
        break

    a_float = float(a_str)
# input coefficients b,c converted into floats
    b_float = float(input("coefficent b : ")) 
    c_float = float(input("coefficent c : ")) 
# computes the discriminate of the quadratic formula 
    formula_float = b_float ** 2 - 4 * a_float * c_float 

# first iteration of if discriminate with is less than 0 print no real solutions
    if formula_float < 0 :  
        print(" no real solutions ")
# second iteration that has elif statement equals to 0
# in the end setting x2_float to x1_float printing one solution if it has one solution 
    elif formula_float == 0 : 
        x1_float = (-b_float + math.sqrt(formula_float)) / (2 * a_float) 
        x2_float = x1_float
        print(" one solution : " , x1_float)

# Third iteration then checks if formula_float is grater than 0 
# setting x1_float and x2_float to the quadratic formula  
#finishing with printing the two solutions x1_float and x2_float
    elif formula_float > 0 : 
        x1_float = (-b_float + math.sqrt(formula_float)) / (2 * a_float) 
        x2_float = (-b_float - math.sqrt(formula_float)) / (2 * a_float) 
        print(" two solutions : " , x1_float , x2_float)   

# these are xs and ys storing plot values

    xs = []
    ys = []

# This sets x0 and x1 to a min and max setting graph domain
    if formula_float >= 0:
        x0 = min(x1_float, x2_float) - 2
        x1 = max(x1_float, x2_float) + 2
    else:
        # Graphed centered off vertex if no real roots
        xopt = -b_float / (2 * a_float)
        x0 = xopt - 5
        x1 = xopt + 5
# sets x to x0 and n = 150 with dx subtracting x1 minus 0 divided by n
    x = x0
    n = 150
    dx = (x1 - x0) / n 

# this is a while loop that appends (x,y)
    while x <= x1 :
        xs.append(x)

        y = a_float * x ** 2 + b_float * x + c_float

        ys.append(y)
        x += dx
# this plots the graph and opens it with plt.shw while clearing last graph 
    plt.clf
    plt.plot(xs, ys, "rx-")
    plt.grid(True)
    plt.show()