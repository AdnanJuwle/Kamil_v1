def calculate():
    print("Calculator")
    num1 = float(input("Enter first number: "))
    operator = input("Enter operator (+,-,*,/): ")
    num2 = float(input("Enter second number: "))

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        result = num1 / num2
    else:
        print("Invalid operator. Please use (+, -, *, /)")
        return

    print(f"Result: {result}")

calculate()