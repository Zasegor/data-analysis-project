import random


def miller_rabin_primality_test(num, times=1):
    if num == 2:
        return True
    for _ in range(times):

        s = 0
        t = num - 1
        while t % 2 == 0:
            s += 1
            t = t // 2

        a = random.randint(2, num - 2)
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


if __name__ == "__main__":
    print(miller_rabin_primality_test(13,10))
    print(miller_rabin_primality_test(561))
