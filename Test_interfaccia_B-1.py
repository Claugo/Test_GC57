# GC57 — Test sperimentale B-1 con interfaccia grafica
# Versione stabile - Giugno 2025

import tkinter as tk
from tkinter import messagebox
from math import gcd, log
from random import randint, seed
import time
from gmpy2 import next_prime as nprime


def gc57_b1_factorization(a, b, x, y):
    p = nprime(a + x)
    q = nprime(b + y)
    s = p * q
    r = gcd(s, s % (b - 1))
    return p, q, s, r


def esegui(a, b, I):
    if a == "" or b == "" or I == "":
        messagebox.showerror(
            "Errore", "Manca uno o più campi compilati: A, B, intervallo"
        )
        return

    T = int(time.time())
    seed(T)

    try:
        a = int(eval(a))
        b = int(eval(b))
        I = int(eval(I))
    except:
        messagebox.showerror(
            "Errore", "Input non valido: inserisci numeri o espressioni corrette"
        )
        return

    x = randint(0, I)
    y = randint(0, I)

    e4.delete(0, tk.END)
    e4.insert(0, str(x))
    e5.delete(0, tk.END)
    e5.insert(0, str(y))

    p, q, s, r = gc57_b1_factorization(a, b, x, y)

    e6.delete(0, tk.END)
    e6.insert(0, str(p))
    e7.delete(0, tk.END)
    e7.insert(0, str(q))
    e8.delete(0, tk.END)
    e8.insert(0, str(s))
    e9.delete(0, tk.END)
    e9.insert(0, str(r))


def verifica(a, b):
    if a == "" or b == "":
        messagebox.showerror("Errore", "Entrambi i campi devono essere compilati")
        return

    try:
        a = int(eval(a))
        b = int(eval(b))
    except:
        messagebox.showerror(
            "Errore", "Input non valido: inserisci numeri o espressioni corrette"
        )
        return

    if a >= b or len(str(b)) <= len(str(a)):
        messagebox.showerror(
            "Errore",
            "Il primo numero deve essere minore del secondo in termini di bit o cifre",
        )
        return

    chiave = b - 1
    intervallo = (chiave // (((a + 1) * (b + 1)) % chiave)) * 2
    e3.delete(0, tk.END)
    e3.insert(0, str(intervallo))


# Creazione della finestra
window = tk.Tk()
window.title("GC57 — Test interfaccia B-1 (sperimentale)")
window.geometry("500x780")

px = 10
py = 30

tk.Label(
    window,
    text="Inserisci due numeri interi, con B maggiore di A in termini di bit o cifre",
).place(x=px, y=py)
py += 20
tk.Label(
    window, text="Esempi: A=123456 e B=123456789, oppure A**6 e B**10 con A <= B"
).place(x=px, y=py)
py += 20
tk.Label(
    window, text="Puoi inserire espressioni tipo 'A**n' e poi premere verifica"
).place(x=px, y=py)
py += 20
tk.Label(
    window, text="Il tasto verifica calcola la dimensione dell’intervallo di ricerca"
).place(x=px, y=py)
py += 20

e1 = tk.Entry(window, width=50)
e1.place(x=px, y=py)
py += 30

e2 = tk.Entry(window, width=50)
e2.place(x=px, y=py)
py += 40
px+=100
b1 = tk.Button(
    window, text="Verifica Intervallo", command=lambda: verifica(e1.get(), e2.get())
)
b1.place(x=px + 60, y=py)
py += 30
px-=40
e3 = tk.Entry(window, width=50)
e3.place(x=px, y=py)
py += 20

tk.Label(
    window,
    text="Se ritieni sufficiente la grandezza dell'intervallo prosegui\nma ricorda che se l'intervallo è molto piccolo\n potresti non trovare i numeri primi",
).place(x=px, y=py)
py += 80
px+=60
b2 = tk.Button(
    window, text="Esegui", command=lambda: esegui(e1.get(), e2.get(), e3.get())
)
b2.place(x=px + 60, y=py)
py += 60
px=10
# Entry risultati (dichiarati esplicitamente)
tk.Label(window, text="Numero X random preso dall’intervallo").place(x=px, y=py)
py += 20
e4 = tk.Entry(window, width=50)
e4.place(x=px, y=py)
py += 30

tk.Label(window, text="Numero Y random preso dall’intervallo").place(x=px, y=py)
py += 20
e5 = tk.Entry(window, width=50)
e5.place(x=px, y=py)
py += 30

tk.Label(window, text="Numero primo trovato con Next Prime(A+x)").place(x=px, y=py)
py += 20
e6 = tk.Entry(window, width=50)
e6.place(x=px, y=py)
py += 30

tk.Label(window, text="Numero primo trovato con Next Prime(B+y)").place(x=px, y=py)
py += 20
e7 = tk.Entry(window, width=50)
e7.place(x=px, y=py)
py += 50
px+=70
tk.Label(window, text="Semiprimo generato").place(x=px, y=py)
py += 20
e8 = tk.Entry(window, width=50)
e8.place(x=px, y=py)
py += 40

tk.Label(window, text="Soluzione trovata dal GC57").place(x=px, y=py)
py += 20
e9 = tk.Entry(window, width=50)
e9.place(x=px, y=py)
py += 40

tk.Label(
    window,
    text="Nota: ogni esecuzione genera nuovi primi casuali\nma usa sempre la stessa chiave B-1.",
).place(x=px, y=py)

window.mainloop()
