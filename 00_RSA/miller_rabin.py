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


SMALL_PRIMES = first_primes(100)


def split_n(n):
    """Zerlegt n - 1 in 2^s * d mit ungeradem d und liefert (s, d).

    >>> split_n(221)
    (2, 55)
    """
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    return s, d


def is_witness(a, n, s, d):
    """Liefert True, wenn a beweist, dass n keine Primzahl ist.

    >>> is_witness(137, 221, 2, 55), is_witness(174, 221, 2, 55)
    (True, False)
    """
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for _ in range(s - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return False
    return True


def is_prim_millerrabin(n, anzahl=20):
    """Miller-Rabin-Test für ungerade n > 3: True bedeutet "sehr wahrscheinlich eine Primzahl".

    >>> is_prim_millerrabin(557), is_prim_millerrabin(561)
    (True, False)
    """
    s, d = split_n(n)
    for _ in range(anzahl):
        a = rnd.randint(2, n - 2)
        if is_witness(a, n, s, d):
            return False
    return True
