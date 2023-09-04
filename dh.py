#import os
import random
from math import gcd as bltin_gcd
#PRIME = b"\xff\xff\xff\xff\xff\xff\xff\xff\xc9\x0f\xda\xa2\x21\x68\xc2\x34\xc4\xc6\x62\x8b\x80\xdc\x1c\xd1\x29\x02\x4e\x08\x8a\x67\xcc\x74\x02\x0b\xbe\xa6\x3b\x13\x9b\x22\x51\x4a\x08\x79\x8e\x34\x04\xdd\xef\x95\x19\xb3\xcd\x3a\x43\x1b\x30\x2b\x0a\x6d\xf2\x5f\x14\x37\x4f\xe1\x35\x6d\x6d\x51\xc2\x45\xe4\x85\xb5\x76\x62\x5e\x7e\xc6\xf4\x4c\x42\xe9\xa6\x37\xed\x6b\x0b\xff\x5c\xb6\xf4\x06\xb7\xed\xee\x38\x6b\xfb\x5a\x89\x9f\xa5\xae\x9f\x24\x11\x7c\x4b\x1f\xe6\x49\x28\x66\x51\xec\xe4\x5b\x3d\xc2\x00\x7c\xb8\xa1\x63\xbf\x05\x98\xda\x48\x36\x1c\x55\xd3\x9a\x69\x16\x3f\xa8\xfd\x24\xcf\x5f\x83\x65\x5d\x23\xdc\xa3\xad\x96\x1c\x62\xf3\x56\x20\x85\x52\xbb\x9e\xd5\x29\x07\x70\x96\x96\x6d\x67\x0c\x35\x4e\x4a\xbc\x98\x04\xf1\x74\x6c\x08\xca\x18\x21\x7c\x32\x90\x5e\x46\x2e\x36\xce\x3b\xe3\x9e\x77\x2c\x18\x0e\x86\x03\x9b\x27\x83\xa2\xec\x07\xa2\x8f\xb5\xc5\x5d\xf0\x6f\x4c\x52\xc9\xde\x2b\xcb\xf6\x95\x58\x17\x18\x39\x95\x49\x7c\xea\x95\x6a\xe5\x15\xd2\x26\x18\x98\xfa\x05\x10\x15\x72\x8e\x5a\x8a\xac\xaa\x68\xff\xff\xff\xff\xff\xff\xff\xff"

class DiffieHellman:
    _prime: int
    _private_key: int
    _public_key: int
    _shared_key: int

    # @staticmethod
    # def _to_bytes(a: int) -> bytes:
    #     return a.to_bytes((a.bit_length() + 7) // 8, byteorder="big")

    def __init__(self, private_key: int, prime: int, g: int) -> None:
        self._prime = prime
        print('Prime:', self._prime)
        print('g:', g)
        self.generate_private_key(private_key, g)

    def generate_private_key(self, private_key: int, g: int) -> int:
        self.set_private_key(private_key, g)
        return self.get_private_key()

    def set_private_key(self, key: int, g: int) -> None:
        self._private_key = key
        print('Private key:', self._private_key)
        self._public_key = pow(g, self._private_key, self._prime)
        print('Public key:', self._public_key)

    def generate_shared_key(self, other_public_key: int) -> int:
        remote_key = other_public_key
        self._shared_key = pow(remote_key, self._private_key, self._prime)
        return self.get_shared_key()

    def get_private_key(self) -> int:
        return self._private_key

    def get_public_key(self) -> int:
        return self._public_key

    def get_shared_key(self) -> int:
        return self._shared_key


def primRoots(prime):
    required_set = {num for num in range(1, prime) if bltin_gcd(num, prime)}
    return [g for g in range(1, prime) if required_set == {pow(g, powers, prime) for powers in range(1, prime)}]

if __name__ == '__main__':
    prime = 17

    list_of_g = primRoots(prime)
    print('gs = ', list_of_g)
    g = random.sample(list_of_g, 1)[0]
    print('g = ', g)

    dh1 = DiffieHellman(3, prime, g)
    dh2 = DiffieHellman(7, prime, g)

    # get both public keys
    dh1_public = dh1.get_public_key()
    dh2_public = dh2.get_public_key()

    # generate shared key based on the other side's public key
    dh1_shared = dh1.generate_shared_key(dh2_public)
    dh2_shared = dh2.generate_shared_key(dh1_public)

    # the shared keys should be equal
    assert dh1_shared == dh2_shared
    print(dh1_shared)
