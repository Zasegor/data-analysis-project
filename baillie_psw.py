import time


def miller_rabin_primality_test(num, a):
    if num == 2:
        return True
    s = 0
    t = num - 1
    while t % 2 == 0:
        s += 1
        t = t // 2

    x = pow(a, t, num)
    y = 0
    for _ in range(s):
        y = pow(x, 2, num)
        if y == 1 and x != 1 and x != num - 1:
            return False
        x = y
    if y != 1:
        return False
    return True


def jacobi(a, n):
    a = a % n
    t = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        r = n
        n = a
        a = r
        if a % 4 == 3 and n % 4 == 3:
            t = -t
        a = a % n
    if n == 1:
        return t
    else:
        return 0


def gen_next(D):
    return -(D + 2) if D > 0 else -(D - 2)


def U(P, Q):
    u0 = 0
    u1 = 1
    yield u0
    yield u1
    while True:
        u3 = P * u1 - Q * u0
        yield u3
        u0 = u1
        u1 = u3


def V(P, Q):
    v0 = 2
    v1 = P
    yield v0
    yield v1
    while True:
        v3 = P * v1 - Q * v0
        yield v3
        v0 = v1
        v1 = v3


def lucas_pseudoprime(n, P, Q):
    s = 0
    t = n + 1
    while t % 2 == 0:
        s += 1
        t = t // 2
    u = U(P, Q)
    for _ in range(t):
        u.__next__()
    if u.__next__() % n == 0:
        return True
    else:
        v = V(P, Q)
        v.__next__()
        for i in range(s):
            for _ in range(int(pow(2, i - 1)) * t + 1,pow(2, i) * t):
                v.__next__()
            tar = v.__next__()
            if tar % n == 0:
                return True
    return False


def baillie_psw_primality_test(num):

    if num == 2:
        return 2
    elif num % 2 == 0:
        return False

    for i in range(3, min(int(pow(num, 1/2)+1), 1000), 2):
        if num % i == 0:
            return False

    if not miller_rabin_primality_test(num, 2):
        return False
    D = 5
    t = time.time()
    check = True
    while True:
        if jacobi(D, num) == -1:
            P = 1
            Q = (1 - D) // 4
            print(jacobi(D, num), D, P, Q)
            return lucas_pseudoprime(num, P, Q)

        D = gen_next(D)
        if time.time() - t > 1 and check:
            check = False
            if pow(int(pow(num, 0.5)), 2) == num:
                return False


if __name__ == "__main__":
    print(baillie_psw_primality_test(363))
