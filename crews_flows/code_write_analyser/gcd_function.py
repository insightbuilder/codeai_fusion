def gcd(a, b):
    """
    Find the Greatest Common Divisor of two integers.
    
    Args:
        a (int): The first integer.
        b (int): The second integer.
    
    Returns:
        int: The Greatest Common Divisor of a and b.
    """
    while b != 0:
        a, b = b, a % b
    return a
