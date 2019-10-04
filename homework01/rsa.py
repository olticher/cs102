import math

def is_prime(n):
    """
    Tests to see if a number is prime.

    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0: 
            return False
    return n > 1

def gcd(a, b):
    """
    Euclid's algorithm for determining the greatest common divisor.

    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    if a == 0:
        return b
    else:
        return gcd(b %a, a)
