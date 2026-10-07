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


def main():
    """Liest den Modul von der Kommandozeile und gibt die gefundenen Faktoren aus."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
    parser.add_argument("-m", "--max", help="maximum number of tries", type=int, default=1_000_000)
    parser.add_argument("modul", help="RSA modulus N = p * q", type=int)
    args = parser.parse_args()

    result = fermat_factor(args.modul, args.max)
    if result is None:
        print(f"Keine Faktoren in {args.max} Versuchen gefunden.")
        return
    p, q, tries = result
    if args.verbosity:
        print(f"Es braucht {tries} Versuche, um die Faktoren von {args.modul} zu finden:")
        print(f" p = {p}")
        print(f" q = {q}")
    else:
        print((p, q))


if __name__ == "__main__":
    main()
