# Mario Wenzl 4CN

"""
>>> keys = generate_keys(1024)
>>> list = [secrets.randbits(1024) for x in range(1,50)]
>>> ergebnis = True
>>> for x in list:
...     c = pow(x,keys[0],keys[2])
...     y = pow(c,keys[1],keys[2])
...     ergebnis = ergebnis and x == y
>>> ergebnis
True
"""
from wenzl.u04_RSA.miller_rabin import generate_prime
import secrets


def extended_gcd(a, b):
    """
    Errechnet das Modinverse Element und den GGT
    :param a: Eine Zahl
    :param b: Eine weitere Zahl
    :return: Modinverses Element und GGT
    """
    (old_r, r) = (a, b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)

    while r != 0:
        quotient = old_r // r
        (old_r, r) = (r, old_r - quotient * r)
        (old_s, s) = (s, old_s - quotient * s)
        (old_t, t) = (t, old_t - quotient * t,)
    return [old_r, old_s, old_t]


def generate_keys(number_of_bits, verbosity=False):
    """
    Generiert ein Keypair
    :param number_of_bits: Schlüssellänge in bits
    :param verbosity: Wenn True dann enstehen mehr Ausgaben in Logfiles
    :return: Die Schlüssel (e und n) und d%phi
    """
    prime1 = generate_prime(number_of_bits >> 1)
    prime2 = generate_prime(number_of_bits - prime1.bit_length() + 1)
    while prime2.bit_length() <= number_of_bits - prime1.bit_length():
        prime2 = generate_prime(number_of_bits - prime1.bit_length() + 1)
    if verbosity: print("Calculating n")
    n = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)
    if verbosity:
        print("Generating Key 1")
    e = secrets.randbits(number_of_bits)
    while extended_gcd(phi, e)[0] != 1:
        e = secrets.randbits(number_of_bits)
    if verbosity: print("Generating Key 2")
    d = extended_gcd(e, phi)[1]
    return [e, d % phi, n]


if __name__ == '__main__':
    for x in range(1, 20):
        keys = generate_keys(1024)
        list = [secrets.randbits(1024) for x in range(1, 10)]
        for x in list:
            c = pow(x, keys[0], keys[2])
            y = pow(c, keys[1], keys[2])
            print(x == y)
