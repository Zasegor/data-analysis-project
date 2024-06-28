import random
import psutil
import time

import customtkinter
from customtkinter import *

import threading

from brute import brute_force_primality_test
from miller_rabin import miller_rabin_primality_test
from miller import miller_primality_test
from solovay_strassen import solovay_strassen_primality_test
from baillie_psw import baillie_psw_primality_test
from adleman_pomerance_rumely import adleman_pomerance_rumely_primality_test


def clicked():
    res.configure(text="")
    num = int(txt.get())
    mod = random.choice(["Brute",
                         "Miller-Rabin",
                         "Miller",
                         "Solovay-Strassen",
                         "Baillie-PSW",
                         "Adleman-Pomerance-Rumely"]) if (combo.get() == "Auto") else combo.get()

    def wrapper(m):
        btn.configure(state="disabled")
        txt.delete(0, 'end')
        check = None
        res.configure(text=f"Checking {num} on primality using \"{mod} test\".\nPlease wait...")
        match m:
            case "Brute":
                check = brute_force_primality_test(num)
            case "Miller-Rabin":
                check = miller_rabin_primality_test(num, 10000000)
            case "Miller":
                check = miller_primality_test(num)
            case "Solovay-Strassen":
                check = solovay_strassen_primality_test(num)
            case "Baillie_PSW":
                check = baillie_psw_primality_test(num)
            case "Adleman-Pomerance-Rumely":
                check = adleman_pomerance_rumely_primality_test(num)
        primality = "PRIME" if check else "COMPOUND"
        pr = "Number {} is {}\nMode: {}".format(str(num), primality, m)
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


customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

window = CTk()
window.title("PrimeQ")
window.geometry('400x550')

txt = CTkEntry(window, width=300, placeholder_text="Enter number to check its primality")
txt.pack(pady=10,padx=10)

combo = CTkComboBox(window,width=150, values=["Auto", "Brute", "Miller-Rabin", "Miller", "Solovay-Strassen", "Baillie_PSW", "Adleman-Pomerance-Rumely"])
combo.pack(pady=10,padx=10)

btn = CTkButton(window, text="Check", command=clicked,width=150)
btn.pack(pady=10,padx=10)

res = CTkLabel(window, width=300, height=200, text="")
res.pack(pady=10,padx=10)

progress = CTkLabel(window, width=300, height=200, text="")
progress.pack(pady=10,padx=10)

window.mainloop()
