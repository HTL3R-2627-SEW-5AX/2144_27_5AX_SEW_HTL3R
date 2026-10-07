"""
Datei:        rsa.py
Autor:        2144
Datum:        2026-10-07
Beschreibung: A.3-A.5 - RSA-Schlüssel erzeugen, Dateien ver- und entschlüsseln (Textbook-RSA).
              Aufruf: rsa.py [-h] [-v] (-k KEYGEN | -e ENCRYPT | -d DECRYPT)
"""
import argparse
import math

from miller_rabin import generate_prime, rnd

PRIVATE_KEY_FILE = "private.key"
PUBLIC_KEY_FILE = "public.key"


def generate_keys(bits):
    """Erzeugt ein Schlüsselpaar (private, public) für Blöcke mit bits Bits; ein Key ist (d bzw. e, n, bits).

    >>> private, public = generate_keys(64)
    >>> numbers = [0, 1, 2, 42, 12345, 2 ** 63, 2 ** 64 - 1]
    >>> list(crypt(crypt(numbers, public), private)) == numbers
    True
    """
    p = generate_prime(bits // 2 + 1)
    q = generate_prime(bits // 2 + 1)
    while q == p:
        q = generate_prime(bits // 2 + 1)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = rnd.randrange(3, phi)
    while math.gcd(e, phi) != 1:
        e = rnd.randrange(3, phi)
    d = pow(e, -1, phi)

    return (d, n, bits), (e, n, bits)


def crypt(numbers, key):
    """Ver- bzw. entschlüsselt jede Zahl mit dem Key (je nachdem, ob public oder private Key).

    >>> list(crypt([2, 3], (7, 33, 4)))
    [29, 9]
    """
    exponent, n, bits = key
    for x in numbers:
        yield pow(x, exponent, n)


def file2ints(file, block_bytes):
    """Liest eine binäre Datei blockweise und liefert jeden Block als int (letzter Block mit 0 aufgefüllt).

    >>> import io
    >>> list(file2ints(io.BytesIO(b"abc"), 2))
    [24930, 25344]
    """
    while True:
        block = file.read(block_bytes)
        if not block:
            break
        yield int.from_bytes(block.ljust(block_bytes, b"\0"), "big")


def ints2bytes(numbers, block_bytes, length):
    """Wandelt die Zahlen wieder in Bytes um und schneidet auf die ursprüngliche Länge ab.

    >>> ints2bytes([24930, 25344], 2, 3)
    b'abc'
    """
    data = b"".join(x.to_bytes(block_bytes, "big") for x in numbers)
    return data[:length]
