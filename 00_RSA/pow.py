"""
Datei:        pow.py
Autor:        2144
Datum:        2026-10-07
Beschreibung: A.2 - eigene schnelle Exponentiation x^b mod n (iterativ und rekursiv)
              und Vergleich mit dem eingebauten pow().
"""
import random
import sys
import time


def pow_iterativ(x, b, n):
    """Berechnet x^b mod n über die Binärdarstellung von b (vom letzten Bit beginnend).

    >>> pow_iterativ(3, 200, 50) == pow(3, 200, 50)
    True
    """
    result = 1 % n
    x = x % n
    while b > 0:
        if b % 2 == 1:
            result = result * x % n
        x = x * x % n
        b //= 2
    return result
