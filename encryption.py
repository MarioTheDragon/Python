# Mario Wenzl 4CN

from wenzl.u04_RSA.generate_keys import generate_keys
from wenzl.u04_RSA.file_to_ints import file2ints
import os


def keygen(length, verbosity=False, outputfile="keys.txt"):
    """
    Generiert Keys in keys.txt
    :param length: Länge des Schlüssels in bit
    :param verbosity: Wenn True dann enstehen mehr Ausgaben in Logfiles
    :param outputfile: Das File, in das die Keys geschrieben werden
    """
    keys = generate_keys(length, verbosity)
    with open(outputfile, "w") as f:
        f.write(f"{keys[0]}\n{keys[1]}\n{keys[2]}")


def encrypt(path, destpath, verbosity=False):
    """
    Verschlüsselt path in das file destpath
    :param path: Pfad und Name des Files, das verschlüsselt werden soll
    :param destpath: Pfad und Name des Output-Files
    :param verbosity: Wenn True dann enstehen mehr Ausgaben in Logfiles
    """
    if verbosity: print("Reading Keys...")
    with open("keys.txt") as f:
        key = f.readline()
        f.readline()
        n = f.readline()
    with open(destpath, "wb") as f:
        if verbosity: print("Starting to encrypt file...")
        nl = (int(n).bit_length() - 1) // 8
        bytes = int.to_bytes(os.path.getsize(path), 8, "little")
        f.write(bytes)
        bytes = [pow(subtext, int(key), int(n)) for subtext in file2ints(path, nl)]
        for i in bytes: f.write(int.to_bytes(i, nl + 1, "little"))
    if verbosity: print("Done writing encrypted Data into destpath")


def decrypt(path, destpath, verbosity=False):
    """
    Entschlüsselt path in das file destpath
    :param path: Pfad und Name des Files, das entschlüsselt werden soll
    :param destpath: Pfad und Name des Output-Files
    :param verbosity: Wenn True dann enstehen mehr Ausgaben in Logfiles
    """
    if verbosity: print("Reading Keys...")
    with open("keys.txt") as f:
        f.readline()
        key = f.readline()
        n = f.readline()
    bytes = b''
    if verbosity: print("Decrypting file...")
    with open(path, "rb") as f:
        nl = (int(n).bit_length() - 1) // 8
        file_size = int.from_bytes(f.read(8), "little")
        line = f.read(nl + 1)
        while file_size > 0:
            line = pow(int.from_bytes(line, "little"), int(key), int(n))
            bytes += int.to_bytes(line, min(nl, file_size), "little")
            file_size -= nl
            line = f.read(nl + 1)
    if verbosity: print("Writing decrypted data into destpath")
    with open(destpath, "wb") as f:
        f.write(bytes)


if __name__ == '__main__':
    keygen(1024)
    encrypt("test.txt", "encrypted.txt")
    decrypt("encrypted.txt", "ergebnis.txt")
