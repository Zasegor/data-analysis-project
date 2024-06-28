import numpy as np


def miller_primality_test(num):
    if num == 2:
        return True

    s = 0
    t = num - 1
    while t % 2 == 0:
        s += 1
        t = t // 2

    for a in range(2, min(num - 2, int(2 * pow(np.log(num), 2)))):
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
    print(miller_primality_test(2))
    print(miller_primality_test(13))
