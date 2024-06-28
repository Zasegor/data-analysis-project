import random


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


def solovay_strassen_primality_test(num, times=1):
    if num == 2:
        return True
    for _ in range(times):
        a = random.randint(2, num-1)
        x = jacobi(a, num)
        if x % num != pow(a, (num - 1) // 2, num):
            return False
    return True


if __name__ == "__main__":
    print(solovay_strassen_primality_test(14, 4))
    print(solovay_strassen_primality_test(13, 12))
