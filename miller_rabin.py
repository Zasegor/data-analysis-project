import random
import multiprocessing


def primality_test(num, s, t):
    if num == 2:
        return True
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


def worker_function(n, s, t, stop_event):
    if stop_event.is_set():
        return None
    if not primality_test(n, s, t):
        stop_event.set()
        return False
    return True


def miller_rabin_primality_test(num, times=5):
    s = 0
    t = num - 1
    while t % 2 == 0:
        s += 1
        t = t // 2
    manager = multiprocessing.Manager()
    stop_event = manager.Event()
    processes = []
    for _ in range(times):
        p = multiprocessing.Process(target=worker_function, args=(num, s, t, stop_event))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
        if stop_event.is_set():
            for p in processes:
                if p.is_alive():
                    p.terminate()
            return False
    return True


if __name__ == "__main__":
    print(miller_rabin_primality_test(13, times=5))
    print(miller_rabin_primality_test(2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550077, 3))
