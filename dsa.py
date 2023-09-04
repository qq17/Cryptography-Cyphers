import random
import sha1
from prettytable import PrettyTable


def sludv(a, b, m, prnt = True):
    i = 0
    av = [a]
    bv = [b]
    bs = ['-']
    cv = [0]
    cs = ['-']

    while av[i] != 1:
        bs[i] = (bv[i] * 2)
        cs[i] = (cv[i] + bv[i] * (av[i] % 2))

        av.append(av[i] // 2)
        bv.append(bs[i] % m)
        cv.append(cs[i] % m)
        bs.append('-')
        cs.append('-')
        i += 1

    if prnt == True:
        print((a * b) % m)
        print([av, bv, bs, cv, cs])

        t = PrettyTable(['i'] + list(range(i + 1)))
        t.add_row(['a', *av])
        t.add_row(['b', *bv])
        t.add_row(['b\'', *bs])
        t.add_row(['c', *cv])
        t.add_row(['c\'', *cs])
        print(t)
    return (a * b) % m

def stepen(num, stpn, m, prnt=True):
    i = 0
    av = [stpn]
    bv = [num]
    cv = [1]

    while av[i] != 1:
        av.append(av[i] // 2)
        bv.append(sludv(bv[i], bv[i], m, prnt=prnt))
        cv.append(sludv(cv[i], bv[i] ** (av[i] % 2), m, prnt=prnt))
        i += 1

    if prnt == True:
        print([av, bv, cv])

        t = PrettyTable(['i'] + list(range(i + 1)))
        t.add_row(['a', *av])
        t.add_row(['b', *bv])
        t.add_row(['c', *cv])
        print(t)

        print('ans', sludv(cv[i], bv[i], m))
    return sludv(cv[i], bv[i], m, prnt=False)

def HashMessage(messageBytes):
    return sha1.SHA1Hash(messageBytes).final_hash()

def _random_k(minNumber, maxNumber):
    return random.randint(minNumber, maxNumber - 1)

def obr(a, m):
    i = 1
    q = ['-', '-']
    u = [1, 0]
    v = [0, 1]
    r = [m, a]

    while r[i] != 1:
        q.append(r[i - 1] // r[i])
        u.append(u[i - 1] - u[i] * q[i + 1])
        v.append(v[i - 1] - v[i] * q[i + 1])
        r.append(r[i - 1] % r[i])
        i += 1

    # t = PrettyTable(['i'] + list(range(i + 1)))
    # t.add_row(['q', *q])
    # t.add_row(['u', *u])
    # t.add_row(['v', *v])
    # t.add_row(['r', *r])
    # print(t)

    return v[i]

def generate_pair(p, g, q):
    x = _random_k(1, q - 1)
    y = stepen(g, x, p, prnt=False)
    return x, y

def dsa_sign(q, p, g, x, h, k=None):
    print('q = ', q)
    print('p = ', p)
    print('g = ', g)
    print('x = ', x)
    print('h =  {:x}'.format(h))

    if k is None:
        k = _random_k(1, q)

    print('k = ', k)

    r = 0
    s = 0
    while True:
        m = stepen(g, k, p, prnt=False)
        r = m % q
        print('r = ', r)
        if r == 0:
            k = _random_k(1, q)
            print('k = ', k)
            continue

        k = obr(k, q) * (h + x * r)
        s = k % q
        print('s = ', s)
        if s == 0:
            k = _random_k(1, q)
            print('k = ', k)
            continue
        print('SIGN: r = ', r, ' s = ', s)
        return (r, s)


def dsa_verify(r, s, g, p, q, y, h):
    print('q = ', q)
    print('p = ', p)
    print('g = ', g)
    print('y = ', y)
    print('h =  {:x}'.format(h))
    print('r = ', r)
    print('s = ', s)
    if not r > 0:
        return False
    if not r < q:
        return False
    if not s > 0:
        return False
    if not s < q:
        return False
    w = obr(s, q)
    print('w = ', w)
    u1 = (h * w) % q
    u2 = (r * w) % q

    u1 = pow(g, u1, p)
    print('u1 = ', u1)
    u2 = pow(y, u2, p)
    print('u2 = ', u2)
    v = ((u1 * u2) % p) % q
    print('v = ', v)
    if v == r:
        return True
    return False

if __name__ == "__main__":
    dsa_key = {
    'Q': 11,
    'P': 23,
    'G': 4,
    'pub': stepen(4, 7, 23, prnt=False),
    'priv': 7}

    a = dsa_sign(dsa_key['Q'], dsa_key['P'], dsa_key['G'], dsa_key['priv'], HashMessage(bytes('Hi,how are you?', "utf-8")))
    print(dsa_verify(a[0], a[1], dsa_key['G'], dsa_key['P'], dsa_key['Q'], dsa_key['pub'], HashMessage(bytes('Hi,how are you?', "utf-8"))))
    print(a)