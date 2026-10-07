"""
Datei:        fermat.py
Autor:        2144
Datum:        2026-10-07
Beschreibung: A.1.1 - berechnet a^(p-1) mod p für alle a in Z_p (kleiner Satz von Fermat)
              und zeigt, was bei Primzahlen und Nicht-Primzahlen herauskommt.
"""
from collections import Counter


def fermat_test(p):
    """Berechnet a^(p-1) mod p für alle a = 1 ... p-1 und zählt, wie oft jedes Ergebnis vorkommt.

    >>> fermat_test(5)
    Counter({1: 4})
    """
    return Counter(pow(a, p - 1, p) for a in range(1, p))
