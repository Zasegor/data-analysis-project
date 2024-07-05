import psutil
import time

import customtkinter
from customtkinter import *

import threading
import multiprocessing

from brute import brute_force_primality_test
from miller_rabin import miller_rabin_primality_test
from miller import miller_primality_test
from solovay_strassen import solovay_strassen_primality_test
from baillie_psw import baillie_psw_primality_test
from adleman_pomerance_rumely import adleman_pomerance_rumely_primality_test


def is_mersenne_number(num, queue):
    if num < 1:
        queue.put("")
    n = 1
    while (1 << n) - 1 <= num:  # 1 << n это то же самое, что и 2^n
        if (1 << n) - 1 == num:
            queue.put(f"\nMersenne Number (n = {n})")
        n += 1
        temp = (pow(2, n) - 1)
    queue.put("")


def is_fermat_number(num, queue):
    if num < 1:
        queue.put("")
    n = 0
    while (1 << (1 << n)) + 1 <= num:  # 1 << (1 << n) это то же самое, что и 2^(2^n)
        if (1 << (1 << n)) + 1 == num:
            queue.put(f"\nFermat Number (n = {n})")
        n += 1
    queue.put("")


def is_woodall_number(num, queue):
    if num < 1:
        queue.put("")
    n = 1
    while (n << n) - 1 <= num:  # n << n это то же самое, что и n * 2^n
        if (n << n) - 1 == num:
            queue.put(f"\nWoodall Number (n = {n})")
        n += 1
    queue.put("")


def is_proth_number(num, queue):
    if num < 1:
        queue.put("")
    k = 1
    while k < num:
        n = 1
        while (k << n) + 1 <= num:  # k << n это то же самое, что и k * 2^n
            if (k << n) + 1 == num:
                queue.put(f"\nProth Number (k = {k}, n = {n})")
            n += 1
        k += 2
    queue.put("")


def special_types(n):
    processes = []
    results = []
    queue = multiprocessing.Queue()

    # Создаем процессы для разных задач
    # p4 = multiprocessing.Process(target=is_proth_number, args=(n, queue))
    p3 = multiprocessing.Process(target=is_woodall_number, args=(n, queue))
    p2 = multiprocessing.Process(target=is_fermat_number, args=(n, queue))
    p1 = multiprocessing.Process(target=is_mersenne_number, args=(n, queue))

    processes.extend([p1, p2, p3])

    for p in processes:
        p.start()
    for p in processes:
        p.join()
    results = []
    while not queue.empty():
        results.append(queue.get())
    result = ""
    for r in results:
        result += r
    return result


def clicked():
    res.configure(text="")
    num = int(txt.get())

    def auto(n):
        len_bin_n = len(bin(n)[2:])
        if len_bin_n < 15:
            return "Brute"
        elif len_bin_n < 50:
            return "Miller"
        elif len_bin_n < 100:
            return "Solovay-Strassen"
        elif len_bin_n < 150:
            return "Baillie_PSW"
        else:
            return "Miller-Rabin"

    mod = auto(num) if (combo.get() == "Auto") else combo.get()
    primality = ""

    def wrapper(m):
        btn.configure(state="disabled")
        txt.delete(0, 'end')
        pr = ""
        nonlocal primality
        res.configure(text=f"Checking {num} on primality using \"{mod} test\".\nPlease wait...")
        match m:
            case "Brute":
                check = brute_force_primality_test(num)
                primality = "PRIME" + special_types(num) if check[0] else f"COMPOSITE\nFirst digit is {check[1]}"
                pr = "Number {} is \n{}\nMode: {}".format(str(num), primality, m)
            case "Miller-Rabin":
                check = miller_rabin_primality_test(num, 3)
                primality = "PRIME" + special_types(num) if check else "COMPOSITE"
                pr = "Number {} is \n{}\nMode: {}".format(str(num), primality, m)
            case "Miller":
                check = miller_primality_test(num)
                primality = "PRIME" + special_types(num) if check else "COMPOSITE"
                pr = "Number {} is \n{}\nMode: {}".format(str(num), primality, m)
            case "Solovay-Strassen":
                check = solovay_strassen_primality_test(num, 10)
                primality = "PRIME" + special_types(num) if check else "COMPOSITE"
                pr = "Number {} is \n{}\nMode: {}".format(str(num), primality, m)
            case "Baillie_PSW":
                check = baillie_psw_primality_test(num)
                primality = "PRIME" + special_types(num) if check else "COMPOSITE"
                pr = "Number {} is \n{}\nMode: {}".format(str(num), primality, m)
            case "Adleman-Pomerance-Rumely":
                check = adleman_pomerance_rumely_primality_test(num)
                primality = "PRIME" + special_types(num) if check else "COMPOSITE"
                pr = "Number {} is \n{}\nMode: {}".format(str(num), primality, m)
        res.configure(text=pr)
        btn.configure(state="normal")

    def time_control(thr):
        t = time.time()
        while thr.is_alive():
            cpu_percent = psutil.cpu_percent()
            text = "_\n"
            text += f"CPU Usage: {cpu_percent}%\n"
            memory_usage = psutil.virtual_memory()
            text += f"Memory Usage: {memory_usage.percent}%\n"
            text += f"Processing Time: {(time.time() - t)}s\n_"
            progress.configure(text=text)
            time.sleep(1)

    thread = threading.Thread(target=wrapper, args=(mod,), daemon=True)
    time_thread = threading.Thread(target=time_control, args=(thread,), daemon=True)
    thread.start()
    time_thread.start()


if __name__ == "__main__":
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("green")

    window = CTk()
    window.title("PrimeQ")
    window.geometry('400x550')

    txt = CTkEntry(window, width=300, placeholder_text="Enter number to check its primality")
    txt.pack(pady=10, padx=10)

    combo = CTkComboBox(window, width=150, values=["Auto", "Brute", "Miller-Rabin", "Miller", "Solovay-Strassen",
                                                   "Baillie_PSW", "Adleman-Pomerance-Rumely"])
    combo.pack(pady=10, padx=10)

    btn = CTkButton(window, text="Check", command=clicked, width=150)
    btn.pack(pady=10, padx=10)

    res = CTkLabel(window, width=300, height=200, text="")
    res.pack(pady=10, padx=10)

    progress = CTkLabel(window, width=300, height=200, text="")
    progress.pack(pady=10, padx=10)

    window.mainloop()
