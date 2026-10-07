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


def pow_rekursiv(x, b, n):
    """Berechnet x^b mod n rekursiv, indem der Exponent immer halbiert wird.

    >>> pow_rekursiv(3, 200, 50) == pow(3, 200, 50)
    True
    """
    if b == 0:
        return 1 % n
    half = pow_rekursiv(x, b // 2, n)
    result = half * half % n
    if b % 2 == 1:
        result = result * x % n
    return result


def measure(func, x, b, n):
    """Ruft func(x, b, n) auf und liefert (Ergebnis, Laufzeit in Sekunden).

    >>> measure(pow, 2, 10, 1000)[0]
    24
    """
    start = time.perf_counter()
    result = func(x, b, n)
    return result, time.perf_counter() - start


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    for bits in [64, 512, 2048, 4096]:
        x, b, n = (random.getrandbits(bits) for _ in range(3))
        print(f"{bits} Bit:")
        for func in [pow, pow_iterativ, pow_rekursiv]:
            result, seconds = measure(func, x, b, n)
            print(f"  {func.__name__:<13} {seconds * 1000:8.3f} ms  richtig: {result == pow(x, b, n)}")
