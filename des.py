import numpy as np
import itertools

IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17,  9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

C0 = [57, 49, 41, 33, 25, 17,  9,  1, 58, 50, 42, 34, 26, 18,
      10,  2, 59, 51, 43, 35, 27, 19, 11,  3, 60, 52, 44, 36]

D0 = [63, 55, 47, 39, 31, 23, 15,  7, 62, 54, 46, 38, 30, 22,
      14,  6, 61, 53, 45, 37, 29, 21, 13,  5, 28, 20, 12,  4]

SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

KEYTABLE = [14, 17, 11, 24,  1,  5,  3, 28, 15,  6, 21, 10, 23, 19, 12,  4,
            26,  8, 16,  7, 27, 20, 13,  2, 41, 52, 31, 37, 47, 55, 30, 40,
            51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

E = [32,  1,  2,  3,  4,  5,
      4,  5,  6,  7,  8,  9,
      8,  9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32,  1]

S = [[[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
      [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
      [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
      [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]],
     [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
      [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
      [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
      [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14, 9]],
     [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
      [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
      [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
      [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],
     [[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
      [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
      [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
      [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],
     [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
      [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
      [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
      [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],
     [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
      [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
      [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
      [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],
     [[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
      [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
      [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
      [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],
     [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
      [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
      [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
      [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]]

P = [16,  7, 20, 21, 29, 12, 28, 17,
      1, 15, 23, 26,  5, 18, 31, 10,
      2,  8, 24, 14, 32, 27,  3,  9,
     19, 13, 30,  6, 22, 11,  4, 25]

IP_f = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41,  9, 49, 17, 57, 25]

def permutation(block, perm):
    result = [block[i - 1] for i in perm]
    return result

def key_gen(key):
    # print('---------------KEY GENERATION---------------')
    # print('key = ', np.array(key).reshape(8, 7))
    keys = list(itertools.chain(*[[*key[i-7:i], (sum(key[i-7:i]) + 1) % 2] for i in range(7, 63, 7)]))
    # print('key with added bits = ', np.array(keys).reshape(8, 8))

    result = permutation(keys, C0 + D0)
    C = [result[:28]]
    D = [result[28:]]
    # print('C0 = ', np.array(C).reshape(4, 7))
    # print('D0 = ', np.array(D).reshape(4, 7))

    k = []
    for i in SHIFT:
        C.append(np.roll(C[-1], -i).tolist())
        D.append(np.roll(D[-1], -i).tolist())
        k.append(permutation(C[-1] + D[-1], KEYTABLE))
        # print('k = ', np.array(k[-1]).reshape(8, 6))

    # print('---------------KEY GENERATION DONE---------------')
    return k


def f(r, k):
    # print('r = ', r)
    er = permutation(r, E)
    # print('er = ', er)
    # print('k  = ', k)
    B = ((np.array(er)^np.array(k))%2).tolist()
    # print('b  = ', B)
    # print(np.array(B).reshape(8,6))

    b_ = []
    for i, bi in enumerate([B[i-6:i] for i in range(6, 49, 6)]):
        # print(bi)
        a = 2*bi[0] + bi[5]
        b = 8*bi[1] + 4*bi[2] + 2*bi[3] + bi[4]
        # print('a = ', a)
        # print('b = ', b)
        s = S[i][a][b]
        b_ += [int(x) for x in list('{0:04b}'.format(s))]
        # print('s = ', s)
        # print(b_)

    result = permutation(b_, P)
    # print('f result = ', result)
    return result

def des_crypt(subblock, key):
    # print('------------------------------DES CRYPT------------------------------------------------------')
    ipt = permutation(subblock, IP)
    l0 = ipt[:32]
    r0 = ipt[32:]
    # print('l0 = ', np.array(l0).reshape(4, 8))
    # print('r0 = ', np.array(r0).reshape(4, 8))

    k = key_gen(key)

    result = feistel_crypt(l0, r0, k)
    result = result[0] + result[1]
    # print(result)

    result = permutation(result, IP_f)
    # print('des crypt result = ', np.array(result).reshape(8, 8))
    # print('------------------------------DES CRYPT DONE------------------------------------------------------')
    return result

def des_decrypt(subblock, key):
    # print('------------------------------DES DECRYPT------------------------------------------------------')
    ipt = permutation(subblock, IP)
    l0 = ipt[:32]
    r0 = ipt[32:]
    # print('l0 = ', np.array(l0).reshape(4, 8))
    # print('r0 = ', np.array(r0).reshape(4, 8))

    k = key_gen(key)

    result = feistel_decrypt(l0, r0, k)
    result = result[0] + result[1]
    # print(result)

    result = permutation(result, IP_f)
    # print('des decrypt result = ', np.array(result).reshape(8, 8))
    # print('------------------------------DES DECRYPT DONE------------------------------------------------------')
    return result



    # return subblock^key

# Функция, выполняющая шифрование открытого текста
def feistel_crypt(left, right, key):
    # print('---------------FEISTEL---------------')
    for k in key:
        # print('k = ', np.array(k).reshape(8, 6))
        # print('left = ', np.array(left).reshape(4, 8))
        # print('right = ', np.array(right).reshape(4, 8))
        temp = (np.array(left) ^ np.array(f(right, k))).tolist()
        left = right
        right = temp
    # print('result left = ', np.array(left).reshape(4, 8))
    # print('result right = ', np.array(right).reshape(4, 8))
    # print('---------------FEISTEL DONE---------------')
    return left, right


# Функция, выполняющая расшифрование текста */
def feistel_decrypt(left, right, key):
    return feistel_crypt(right, left, key[::-1])[::-1]


if __name__ == '__main__':
    block = list(range(1, 65))
    block = [0, 1, 0, 0, 1, 0, 0, 1,
             0, 1, 0, 0, 1, 1, 0, 0,
             0, 1, 0, 0, 0, 0, 1, 1,
             0, 1, 0, 0, 1, 0, 0, 0,
             0, 1, 0, 0, 0, 1, 0, 1,
             0, 1, 0, 0, 1, 1, 1, 0,
             0, 1, 0, 0, 1, 0, 1, 1,
             0, 1, 0, 0, 1, 1, 1, 1]

    key = np.random.randint(2, size=56).tolist()
    key = [0, 0, 1, 1, 1, 0, 0, 0,
           0, 0, 1, 1, 0, 0, 1, 1,
           0, 0, 1, 1, 0, 1, 1, 0,
           0, 0, 1, 1, 0, 0, 0, 1,
           0, 0, 1, 1, 0, 0, 0, 0,
           0, 0, 1, 1, 1, 0, 0, 1,
           0, 1, 0, 1, 0, 1, 1, 0]
    # key = [0]*56
    print('block = ', block)
    print('key = ', key)
    cipher = des_crypt(block, key)
    source = des_decrypt(cipher, key)
    print('cipher = ', cipher)
    print('source = ', source)
    print(source == block)
