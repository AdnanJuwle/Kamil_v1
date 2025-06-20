def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def divide(a, b):
    return a / b

print("Welcome to the calculator!")
choice = input("Enter your choice (1-3): ")
if choice == '1':
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    print("Result of addition:", add(a, b))
elif choice == '2':
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    print("Result of subtraction:", subtract(a, b))
else:
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    print("Result of division:", divide(a, b))