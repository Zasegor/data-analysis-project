def brute_force_primality_test(num):
    if num == 2:
        return True
    for i in range(2, int(pow(num, 0.5)) + 1):

        if num % i == 0:
            return False
    return True


if __name__ == "__main__":
    print(brute_force_primality_test(7369))
    print(brute_force_primality_test(133))
