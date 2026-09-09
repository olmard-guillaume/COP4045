# created a f string that let users input n then we converted it to a integer 

n_str = input("Enter n: ")
n = int(n_str)

# creat a find pythagorean function that included a list for tuples which is a immutable object 
def find_Pythagorean(n):

    pythagorean_tuple_list = []

# a for loop which sets a , b , c to 1 and and add 1 
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
# pythagorean formula
                Pythagorean_theorem = (a**2 + b**2) == (c**2)
# if statments that states if the theorem is true append the tuple list and returns it at the end 
                if Pythagorean_theorem:
                    pythagorean_tuple_list.append((a, b, c))

    return pythagorean_tuple_list

# setting pythagorean therom list to the function find pythagorean
Pyhagorean_theorem_list = find_Pythagorean(n)

# print statement
print("Pythagorean triples:")
# for loop that states for every triple in the list print the triple
for triple in Pyhagorean_theorem_list:
    print(triple)