# TODO:
# Create a function called calculate that takes three arguments:
# - A number
# - An operator ("+", "-", "*", or "/")
# - Another number
# The function should return the result of the calculation
def calculate(x):
    return 10 + x
def aaa(x):
    return 10 + x
def bbb(x):
    return 10 * x
def ccc(x):
    return 10 / x
#function code here

# Test the function with different operations
print(calculate(10))  # should return 20
print(aaa(-10))
print(bbb(10))
print(ccc(10))

# example 2.0

def calculate(num1, operator, num2):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "*":
        return num1 * num2
    elif operator == "/":
        return num1 / num2
    else:
        return "Invalid operator"

print(calculate(10, "+", 10))  # should return 20
print(calculate(10, "-", 10))  # should return 0
print(calculate(10, "*", 10))  # should return 100
print(calculate(10, "/", 10))  # should return 1.0