def gcd(a, b):
    """
    Finds the greatest common divisor of two integers using the Euclidean algorithm.
    
    Args:
        a (int): The first integer.
        b (int): The second integer.
    
    Returns:
        int: The greatest common divisor of a and b.
    """
    while b != 0:
        a, b = b, a % b
    return a
