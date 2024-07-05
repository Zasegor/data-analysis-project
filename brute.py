import multiprocessing as mp
import math


def is_prime_worker(num, start, end, result_queue):
    for i in range(start, end):
        if num % i == 0:
            result_queue.put((False, i))
            return
    result_queue.put((True, None))


def brute_force_primality_test(num):
    if num == 2:
        return True, None
    if num < 2:
        return False, None

    num_cores = mp.cpu_count()
    chunk_size = int(math.sqrt(num)) // num_cores
    result_queue = mp.Queue()

    processes = []
    for i in range(num_cores):
        start = i * chunk_size + 2
        end = (i + 1) * chunk_size + 2 if i != num_cores - 1 else int(math.sqrt(num)) + 1
        p = mp.Process(target=is_prime_worker, args=(num, start, end, result_queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while not result_queue.empty():
        is_prime, divisor = result_queue.get()
        if not is_prime:
            return False, divisor

    return True, None



if __name__ == "__main__":
    print(brute_force_primality_test(7369))
    print(brute_force_primality_test(133))
