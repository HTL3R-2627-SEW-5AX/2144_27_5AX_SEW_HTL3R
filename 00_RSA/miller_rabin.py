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


def is_prime(n):
    """Prüft n zuerst mit den ersten 100 Primzahlen und danach mit Miller-Rabin.

    >>> [x for x in range(30) if is_prime(x)]
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n == p:
            return True
        if n % p == 0:
            return False
    return is_prim_millerrabin(n)


def generate_prime(bits):
    """Erzeugt eine zufällige Primzahl mit genau bits Bits (höchstes und niedrigstes Bit gesetzt).

    >>> p = generate_prime(64)
    >>> p.bit_length(), is_prime(p)
    (64, True)
    """
    while True:
        n = rnd.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(n):
            return n


def next_prime(n):
    """Liefert die erste Primzahl, die größer als n ist.

    >>> next_prime(13)
    17
    """
    n += 1
    while not is_prime(n):
        n += 1
    return n


def to_binary_lines(n, width=12):
    """Stellt n binär dar, mit width Zeichen pro Zeile.

    >>> print(to_binary_lines(42, 3))
    101
    010
    """
    b = bin(n)[2:]
    return "\n".join(b[i:i + width] for i in range(0, len(b), width))


if __name__ == "__main__":
    print("Erste Primzahl > 2^512:", next_prime(2 ** 512))

    magic = 24566544301293569
    print(f"\nIst {magic} prim? {is_prime(magic)}")
    print(to_binary_lines(magic))

    magic2 = next_prime(magic)
    print(f"\nNächste Primzahl: {magic2}")
    print(to_binary_lines(magic2))
