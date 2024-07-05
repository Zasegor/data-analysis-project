import numpy as np
import multiprocessing as mp


def miller_primality_test_worker(num, s, t, a_range, result_queue):

    for a in a_range:
        x = pow(a, t, num)
        y = 0
        for _ in range(s):
            y = pow(x, 2, num)
            if y == 1 and x != 1 and x != num - 1:
                result_queue.put(False)
                return
            x = y
        if y != 1:
            result_queue.put(False)
            return
    result_queue.put(True)


def miller_primality_test(num):
    if num == 2:
        return True

    s = 0
    t = num - 1
    while t % 2 == 0:
        s += 1
        t = t // 2

    num_cores = mp.cpu_count()
    a_max = min(num - 2, int(2 * pow(np.log(num), 2)))
    chunk_size = a_max // num_cores
    result_queue = mp.Queue()

    processes = []
    for i in range(num_cores):
        start = i * chunk_size + 2
        end = (i + 1) * chunk_size + 2 if i != num_cores - 1 else a_max
        a_range = range(start, end)
        p = mp.Process(target=miller_primality_test_worker, args=(num, s, t, a_range, result_queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while not result_queue.empty():
        if not result_queue.get():
            return False
    return True


if __name__ == "__main__":
    print(miller_primality_test(2))
    print(miller_primality_test(6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151))
