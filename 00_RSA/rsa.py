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


def save_key(key, filename):
    """Speichert einen Key als Textdatei (eine Zahl pro Zeile).

    >>> import os, tempfile
    >>> path = os.path.join(tempfile.mkdtemp(), "test.key")
    >>> save_key((3, 33, 4), path)
    >>> open(path).read()
    '3\\n33\\n4\\n'
    """
    with open(filename, "w") as f:
        for value in key:
            f.write(f"{value}\n")


def load_key(filename):
    """Liest einen Key, der mit save_key gespeichert wurde.

    >>> import os, tempfile
    >>> path = os.path.join(tempfile.mkdtemp(), "test.key")
    >>> save_key((3, 33, 4), path)
    >>> load_key(path)
    (3, 33, 4)
    """
    with open(filename) as f:
        return tuple(int(line) for line in f)


def encrypt_file(infile, outfile, public_key):
    """Verschlüsselt infile; in outfile steht zuerst die Länge, dann eine Zahl pro Zeile.

    >>> import os, tempfile
    >>> folder = tempfile.mkdtemp()
    >>> src, enc = os.path.join(folder, "a.txt"), os.path.join(folder, "a.enc")
    >>> _ = open(src, "wb").write(b"Hallo")
    >>> encrypt_file(src, enc, (5, 323, 8))
    >>> open(enc).read().split()
    ['5', '21', '241', '109', '109', '42']
    """
    block_bytes = public_key[2] // 8
    with open(infile, "rb") as f_in, open(outfile, "w") as f_out:
        data = f_in.read()
        f_in.seek(0)
        f_out.write(f"{len(data)}\n")
        for number in crypt(file2ints(f_in, block_bytes), public_key):
            f_out.write(f"{number}\n")


def decrypt_file(infile, outfile, private_key):
    """Entschlüsselt eine mit encrypt_file erzeugte Datei und schreibt die Original-Bytes.

    >>> import os, tempfile
    >>> folder = tempfile.mkdtemp()
    >>> src, enc, dec = (os.path.join(folder, name) for name in ("a.txt", "a.enc", "a.dec"))
    >>> _ = open(src, "wb").write(b"Hallo RSA!")
    >>> private, public = generate_keys(32)
    >>> encrypt_file(src, enc, public)
    >>> decrypt_file(enc, dec, private)
    >>> open(dec, "rb").read()
    b'Hallo RSA!'
    """
    block_bytes = private_key[2] // 8
    with open(infile) as f:
        length = int(f.readline())
        numbers = [int(line) for line in f]
    with open(outfile, "wb") as f:
        f.write(ints2bytes(crypt(numbers, private_key), block_bytes, length))


def main(argv=None):
    """Wertet die Kommandozeilen-Parameter aus und startet keygen, encrypt oder decrypt."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-k", "--keygen", help="generate new keys with the given length", type=int)
    group.add_argument("-e", "--encrypt", help="encrypt file")
    group.add_argument("-d", "--decrypt", help="decrypt file")
    args = parser.parse_args(argv)

    if args.keygen:
        private, public = generate_keys(args.keygen)
        save_key(private, PRIVATE_KEY_FILE)
        save_key(public, PUBLIC_KEY_FILE)
        if args.verbosity:
            print(f"Keys mit {args.keygen} Bit gespeichert in {PRIVATE_KEY_FILE} und {PUBLIC_KEY_FILE}")
    elif args.encrypt:
        encrypt_file(args.encrypt, args.encrypt + ".enc", load_key(PUBLIC_KEY_FILE))
        if args.verbosity:
            print(f"{args.encrypt} verschlüsselt -> {args.encrypt}.enc")
    elif args.decrypt:
        outfile = args.decrypt.removesuffix(".enc") + ".dec"
        decrypt_file(args.decrypt, outfile, load_key(PRIVATE_KEY_FILE))
        if args.verbosity:
            print(f"{args.decrypt} entschlüsselt -> {outfile}")


if __name__ == "__main__":
    main()
