"""
Datei:        rsa_attack.py
Autor:        2144
Datum:        2026-10-07
Beschreibung: A.6 - Fermat-Angriff: zerlegt einen RSA-Modul N = p * q, wenn p und q nahe beieinander liegen.
              Aufruf: rsa_attack.py [-h] [-v] [-m MAX] modul
"""
import argparse
import math


def fermat_factor(n, max_tries=1_000_000):
    """Sucht a, b mit n = a^2 - b^2 und liefert (p, q, versuche) oder None, wenn nichts gefunden wurde.

    >>> fermat_factor(1000001000000090000037000001961)
    (1000000000000037, 1000001000000053, 125)
    """
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    for tries in range(1, max_tries + 1):
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            return a - b, a + b, tries
        a += 1
    return None
