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


def print_result(p):
    """Gibt das Ergebnis von fermat_test(p) im Format des Angabeblatts aus.

    >>> print_result(9)
       9 ->   25 % -> res[1]=2, len(res)=4 - [(1, 2), (4, 2), (0, 2), (7, 2)]
    """
    res = fermat_test(p)
    percent = int(res[1] * 100 / (p - 1))
    print(f"{p:>4} -> {percent:>4} % -> res[1]={res[1]}, len(res)={len(res)} - {res.most_common(7)}")


if __name__ == "__main__":
    for p in [2, 3, 5, 7, 11, 997, 9, 15, 21, *range(551, 571), 6601, 8911]:
        print_result(p)
