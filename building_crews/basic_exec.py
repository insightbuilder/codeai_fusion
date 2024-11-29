exec_locals = {}
code = "print('hello world')\na = 6\nc=5\nprint(a)"
exec(code, {}, exec_locals)
print(exec_locals)


def fibonacci(n):
    if n <= 0:
        return "Input should be a positive integer."
    elif n == 1:
        return 0
    elif n == 2:
        print("Entering 2")
        return 1
    else:
        # print("Entering else")
        a, b = 0, 1
        for _ in range(2, n):
            # print("iter")
            a, b = b, a + b
        return b


print(fibonacci(20))


def fibo_fact(n):
    if n <= 0:
        return "Input should be a positive integer."
    if n == 0:
        return 0
    elif n == 2 or n == 1:
        return 1
    else:
        return fibo_fact(n - 1) + fibo_fact(n - 2)


print(fibo_fact(20))

exec_locals = {}
code = "a = sum([20, 28])\nprint(a)"
exec(code, {}, exec_locals)
print(exec_locals)
