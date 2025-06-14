# ** Questo programma è un test basato sulla chiave B-1, dotato di interfaccia grafica.
# ** Il programma permette di inserire due numeri interi, A e B, con B maggiore di A in termini di bit o cifre.
# **? Giugno 2025
import tkinter as tk
from tkinter import messagebox
from math import gcd, log
from random import randint, seed
import time
from gmpy2 import next_prime as nprime
from gmpy2 import is_prime as isprime


# Creazione della finestra principale


def gc57_b1_factorization(a, b, x, y):
    """
    Esegue la generazione dei primi e la fattorizzazione GC57 su chiave B-1

    a: valore base per p
    b: valore base per q
    x: incremento casuale per p
    y: incremento casuale per q

    Restituisce:
    - p: primo calcolato con next_prime(a + x)
    - q: primo calcolato con next_prime(b + y)
    - s: semiprimo generato p * q
    - r: divisore calcolato via GC57 (gcd(s, s % (b - 1)))
    """
    p = nprime(a + x)
    q = nprime(b + y)
    s = p * q
    r = gcd(s, s % (b - 1))
    return p, q, s, r


def esegui(a, b, I):
    if a == "" or b == "" or I=="":
        messagebox.showerror(
            "Errore", "Manca uno o più campi compilati: A,B,intervallo "
        )
        return
    # ** imposto il seme random della funzione randint
    T = int(time.time())
    seed(T)
    try:
        a = int(eval(a))
    except:
        messagebox.showerror("Errore", "Input non valido: inserisci numeri corretti")
        return
    b = int(eval(b))
    I = int(eval(I))
    x = randint(0, I)
    y = randint(0, I)
    e4.delete(0, tk.END)
    e4.insert(0, str(x))
    e5.delete(0, tk.END)
    e5.insert(0, str(y))
    #p=nprime(a + x)
    #q=nprime(b + y)
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
    if not a.isdigit() or not b.isdigit():
        messagebox.showerror(
            "Errore",
            "Entrambi i campi devono essere compilati con numeri interi",
        )       
        return 
    if a == "" or b == "":
        messagebox.showerror(
            "Errore",
            "Entrambi i campi devono essere compilati con numeri interi",
        )
        return
    try:
        a = int(eval(a))
    except:
        messagebox.showerror("Errore", "Input non valido: inserisci numeri corretti")
        return

    b = int(eval(b))
    if a >= b or len(str(b))<= len(str(a)):
        messagebox.showerror(
            "Errore",
            "Il primo numero deve essere minore del secondo in termini di bit, o lungheza di cifre",
        )
        return   
    chiave = b - 1
    intervallo = (chiave // (((a + 1) * (b + 1)) % chiave)) * 2
    e3.delete(0, tk.END)
    e3.insert(0, str(intervallo))


window = tk.Tk()

window.title("Test sulla base del'esempio riportato nel saggio")
window.geometry("500x750")

# Creazione di una label
px=10
py=30
label = tk.Label(window, text="Inserisci due numeri interi, con B maggiore di A in termini di bit, o cifre")
label.place(x=px, y=py)
py=py+20
label = tk.Label(
    window,
    text="un esempio potrebbe essere A=123456 e B=123456789, oppure",
)
label.place(x=px, y=py)

py = py + 20
label = tk.Label(
    window,
    text="A**6 e B**10 con A =< di B",
    )
label.place(x=px, y=py)
py = py + 20
label = tk.Label(
    window,
    text="Puoi inserire direttamente la potenza, per esempio, 'A**n' e poi premi verifica" ,
)
label.place(x=px, y=py)

py = py + 20
label = tk.Label(
    window,
    text="Il tasto verifica ti dirà quanto è grande l'intervallo di risoluzione",
)
label.place(x=px, y=py)

# Creazione delle due entry
py=py+20
e1 = tk.Entry(window,width=50)
e1.place(x=px, y=py)
py=py+30
e2 = tk.Entry(window, width=50)
e2.place(x=px, y=py)
py=py+30
px=px+60
b1=tk.Button(
    window,
    text="Verifica Intervallo",
    command=lambda: verifica(e1.get(), e2.get())
    )
b1.place(x=px, y=py)
py=py+30
e3 = tk.Entry(window, width=50)
e3.place(x=px, y=py)
py = py + 20
label = tk.Label(
    window,
    text="Se ritieni sufficiente la grandezza dell'intervallo prosegui\nma ricorda che se l'intervallo è molto piccolo\n potresti non trovare i numeri primi",
)
label.place(x=px, y=py)
py=py+60
b2 = tk.Button(window, text="Esegui", command=lambda: esegui(e1.get(), e2.get(), e3.get()))
b2.place(x=px, y=py)
px=10

py = py + 60
label = tk.Label(
    window,
    text="Numero X random preso dall'intervallo",
)
label.place(x=px, y=py)
py=py+20
e4 = tk.Entry(window, width=50)
e4.place(x=px, y=py)

py = py + 30
label = tk.Label(
    window,
    text="Numero Y random preso dall'intervallo",
)
label.place(x=px, y=py)
py = py + 20
e5 = tk.Entry(window, width=50)
e5.place(x=px, y=py)

py = py + 30
label = tk.Label(
    window,
    text="Numero primo trovato con Next Prime(A+x)",
)
label.place(x=px, y=py)
py = py + 20
e6 = tk.Entry(window, width=50)
e6.place(x=px, y=py)

py = py + 30
label = tk.Label(
    window,
    text="Numero primo trovato con Next Prime(B+Y)",
)
label.place(x=px, y=py)
py = py + 20
e7 = tk.Entry(window, width=50)
e7.place(x=px, y=py)

py = py + 30
label = tk.Label(
    window,
    text="Semiprimo creato",
)
label.place(x=px, y=py)
py = py + 20
e8 = tk.Entry(window, width=50)
e8.place(x=px, y=py)

py = py + 40
px=px+60
label = tk.Label(
    window,
    text="Soluzione trovata dal GC57",
)
label.place(x=px, y=py)
py = py + 20
e9 = tk.Entry(window, width=50)
e9.place(x=px, y=py)

py = py + 40
px=10
label = tk.Label(
    window,
    text="Nota: Continuando a premere su ESEGUI, il programma continuerà a generare\nnuovi numeri primi ma utilizzarà sempre la stessa chiave per fattorizzare il Semiprimo"
)
label.place(x=px, y=py)

window.mainloop()
