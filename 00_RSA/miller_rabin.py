"""
Datei:        miller_rabin.py
Autor:        2144
Datum:        2026-10-07
Beschreibung: A.1.2/A.1.3 - Primzahltest nach Miller-Rabin und Erzeugen großer Primzahlen.
"""
import random

rnd = random.SystemRandom()


def first_primes(count):
    """Liefert die ersten count Primzahlen (durch einfaches Probedividieren).

    >>> first_primes(5)
    [2, 3, 5, 7, 11]
    """
    primes = []
    n = 2
    while len(primes) < count:
        if all(n % p != 0 for p in primes):
            primes.append(n)
        n += 1
    return primes
