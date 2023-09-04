import itertools
import des
import sha1
import dsa
from des import des_crypt, des_decrypt
from dh import DiffieHellman, primRoots

def bytes_to_bits(b):
    return list(itertools.chain(*[[int(x) for x in list('{0:08b}'.format(int(i)))] for i in b]))

if __name__ == '__main__':
    message = 'The quick brown fox jumps over the lazy dog'
    print(message)

    print('----------HASH----------')
    bytes_message = bytes(message, "utf-8")
    hash = sha1.SHA1Hash(bytes_message).final_hash()
    print('HASH: ', hash)
    print('       {:x}'.format(hash))

    print('----------SIGN----------')
    q = 11
    p = 23
    g_ = 4
    x, y = dsa.generate_pair(p, g_, q)
    print('x = ', x,' y = ', y)

    sign = dsa.dsa_sign(q, p, g_, x, hash)
    print(dsa.dsa_verify(sign[0], sign[1], g_, p, q, y, hash))

    print('----------DIFFIE HELLMAN----------')
    prime = 17

    list_of_g = primRoots(prime)
    g = list_of_g[0]

    pk1 = 3
    pk2 = 7

    print('-----Alice-----')
    dh1 = DiffieHellman(pk1, prime, g)
    print('-----Bob-----')
    dh2 = DiffieHellman(pk2, prime, g)

    dh1_public = dh1.get_public_key()
    dh2_public = dh2.get_public_key()
    print('-------')

    print('Alice public = ', dh1_public)
    print('Bob public = ', dh2_public)

    dh1_shared = dh1.generate_shared_key(dh2_public)
    dh2_shared = dh2.generate_shared_key(dh1_public)

    print('Alice shared = ', dh1_shared)
    print('Bob shared = ', dh2_shared)
    assert dh1_shared == dh2_shared

    print('----------DES----------')
    print('-----ALICE-----')
    msg_to_send = bytes_to_bits(bytes_message)
    print(len(bytes_message))
    print(msg_to_send)
    print(len(msg_to_send))

    msg_to_send += [0]*(64 - len(msg_to_send) % 64)
    print(len(msg_to_send))

    sign_to_send = sign[0].to_bytes(length=20, byteorder='big') + sign[1].to_bytes(length=20, byteorder='big')
    print(sign_to_send)
    sign_to_send = bytes_to_bits(sign_to_send)
    print(sign_to_send)

    key = [int(x) for x in list('{0:056b}'.format(dh1_shared))]
    print('key = ', key)

    msg_blocks = list()
    block_size = 64
    for i in range(0, len(msg_to_send), block_size):
        msg_blocks.append(msg_to_send[i:i + block_size])

    msg_cipher = []
    for block in msg_blocks:
        print('block = ', block)
        msg_cipher += des_crypt(block, key)

    print('msg cipher = ', msg_cipher)
    print(len(msg_cipher))

    sign_blocks = list()
    block_size = 64
    for i in range(0, len(sign_to_send), block_size):
        sign_blocks.append(sign_to_send[i:i + block_size])

    sign_cipher = []
    for block in sign_blocks:
        print('block = ', block)
        sign_cipher += des_crypt(block, key)

    print('sign cipher = ', sign_cipher)
    print(len(sign_cipher))

    print('-----BOB-----')
    key = [int(x) for x in list('{0:056b}'.format(dh2_shared))]
    print('key = ', key)

    msg_blocks = list()
    block_size = 64
    for i in range(0, len(msg_cipher), block_size):
        msg_blocks.append(msg_cipher[i:i + block_size])

    msg_decipher = []
    for block in msg_blocks:
        print('block = ', block)
        msg_decipher += des_decrypt(block, key)


    sign_blocks = list()
    block_size = 64
    for i in range(0, len(sign_cipher), block_size):
        sign_blocks.append(sign_cipher[i:i + block_size])

    sign_decipher = []
    for block in sign_blocks:
        print('block = ', block)
        sign_decipher += des_decrypt(block, key)

    print('msg decipher = ', msg_decipher)
    print(msg_decipher == msg_to_send)
    print('sign decipher = ', sign_decipher)
    print(sign_decipher == sign_to_send)

    msg_got = sha1.SHA1Hash.bits_to_byte(msg_decipher)
    while msg_got[-1] == 0:
        msg_got.pop(-1)
    print('message got:', msg_got)
    r_got = int.from_bytes(sha1.SHA1Hash.bits_to_byte(sign_decipher[:160]), byteorder='big')
    print('r got:', r_got)
    s_got = int.from_bytes(sha1.SHA1Hash.bits_to_byte(sign_decipher[160:]), byteorder='big')
    print('s got:', s_got)

    print('----------HASH----------')
    hash_got = sha1.SHA1Hash(msg_got).final_hash()
    print('HASH: ', hash)
    print('       {:x}'.format(hash))
    print(hash_got == hash)

    print('----------SIGN CHECK----------')
    print('result of check:', dsa.dsa_verify(r_got, s_got, g_, p, q, y, hash_got))