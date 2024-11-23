#!/bin/python


def addme(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    print("Lets add two numbers")
    num1 = int(input("Enter a number: "))
    num2 = int(input("Enter a number: "))
    added = addme(num1, num2)
    print("The Added value is", added)
