# Mario Wenzl 4CN

import random
import secrets


def is_prim_millerrabin(number, anzahl=20):
    """
    Überprüft gemäß Miller Rabin ob eine Zahl eine Primzahl ist
    :param number: Zu überprüfende Zahl
    :param anzahl: Anzahl an Durchläufen (Höhere Anzahl bedeutet genaueres Ergebnis)
    :return: True/False - ist die Zahl eine Primzahl
    """
    divider = number
    r = 0
    divider -= 1
    while divider & 1 == 0:
        divider = divider >> 1
        r += 1
    d = int(divider)

    for i in range(anzahl):
        a = random.randint(2, number - 2)
        x = pow(a, d, number)
        if x == 1 or x == number - 1: continue
        for j in range(r - 1):
            x = pow(x, 2, number)
            if x == number - 1:
                break
        else:
            return False
    return True


def generate_prime(bits):
    """
    Generiert eine Primzahl mit bits länge
    :param bits: Länge der zu generierenden Primzahl in bits
    :return: Primzahl der Länge bits
    """
    while True:
        potPrime = secrets.randbits(bits)
        if potPrime <= 3: potPrime += 4
        potPrime += not (potPrime & 1)
        if is_prim_millerrabin(potPrime, 20):
            return potPrime


def generate_prime_greater_than_2pow512():
    """
    Errechnet die erste Primzahl größer als 2^512
    :return: Erste Primzahl größer als 2^512
    """
    potPrime = pow(2, 512) + 1
    while True:
        if is_prim_millerrabin(potPrime, 20):
            return potPrime
        potPrime += 2


# print(is_prim_millerrabin(191926127353949))
# print(generate_prime_greater_than_2pow512())