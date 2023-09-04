from des import des_crypt, des_decrypt
from dh import DiffieHellman, primRoots

if __name__ == '__main__':
    prime = 17

    list_of_g = primRoots(prime)
    g = list_of_g[0]

    pk1 = 3
    pk2 = 7

    dh1 = DiffieHellman(pk1, prime, g)
    dh2 = DiffieHellman(pk2, prime, g)

    # get both public keys
    dh1_public = dh1.get_public_key()
    dh2_public = dh2.get_public_key()

    print('dh2 public', dh1_public)
    print('dh2 public', dh2_public)

    # generate shared key based on the other side's public key
    dh1_shared = dh1.generate_shared_key(dh2_public)
    dh2_shared = dh2.generate_shared_key(dh1_public)

    # the shared keys should be equal
    print('dh1 shared = ', dh1_shared)
    print('dh2 shared = ', dh2_shared)
    assert dh1_shared == dh2_shared

    block = [0, 1, 0, 0, 1, 0, 0, 1,
             0, 1, 0, 0, 1, 1, 0, 0,
             0, 1, 0, 0, 0, 0, 1, 1,
             0, 1, 0, 0, 1, 0, 0, 0,
             0, 1, 0, 0, 0, 1, 0, 1,
             0, 1, 0, 0, 1, 1, 1, 0,
             0, 1, 0, 0, 1, 0, 1, 1,
             0, 1, 0, 0, 1, 1, 1, 1]
    key = [int(x) for x in list('{0:056b}'.format(dh1_shared))]
    print('block = ', block)
    print('key = ', key)
    cipher = des_crypt(block, key)
    source = des_decrypt(cipher, key)
    print('cipher = ', cipher)
    print('source = ', source)
    print(source == block)

