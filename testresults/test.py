def recur_function(n):
    if n <= 0:
        return 0
    else:
        return recur_function(n-1) + 1

class MyClass:
    def __init__(self, x):
        self.x = x

my_object = MyClass(5)
print(recur_function(5))