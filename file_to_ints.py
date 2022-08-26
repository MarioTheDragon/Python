# Mario Wenzl 4CN

def file2ints(path, length):
    """
    Erstellt aus einem File ein Generator Object mit Zahlen der Größe length in bit
    :param path: Pfad und Name des Files
    :param length: Länge der Zahlen, welche RSA später verschlüsselt in bit
    :return: Generator Object mit den Zahlen
    """
    with open(path, 'rb') as f:
        byte = f.read(length)
        yield int.from_bytes(byte, 'little')
        while byte != b'':
            byte = f.read(length)
            yield int.from_bytes(byte, 'little')

if __name__ == '__main__':
    print(list(file2ints("test.txt", 2)))