#Progetto risoluzione GC57 equazione cubica diofantea
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import csv
import os
from datetime import datetime
from random import randint
from gmpy2 import next_prime as nprime
from gmpy2 import is_prime as iprime
import secrets
from math import gcd
def genera_numero_cifre(n):
    minimo = 10 ** (n - 1)
    massimo = 10**n - 1
    ampiezza_intervallo = massimo - minimo + 1
    return secrets.randbelow(ampiezza_intervallo) + minimo


def _change_text_height(widget, delta, min_h=4, max_h=40):
    try:
        cur = int(widget.cget('height'))
    except Exception:
        cur = 4
    new_h = max(min_h, min(max_h, cur + delta))
    widget.config(height=new_h)


def genera_A_B_D(cifre_A, cifre_B, cifre_D):
    return (
        genera_numero_cifre(cifre_A),
        genera_numero_cifre(cifre_B),
        genera_numero_cifre(cifre_D),
    )


# --- Funzione per aprire la finestra dei risultati (Toplevel) ---
def apri_finestra_test(A_val=None, B_val=None, D_val=None, Cb_val=None, Cd_val=None, S_val=None):
    # Se i valori A,B,D sono passati come argomenti (lambda del bottone), usali;
    # altrimenti leggili dalle entry (compatibilità con comportamento precedente).
    if A_val is None or B_val is None or D_val is None:
        try:
            A_str = entry_valore_A.get().strip()
            B_str = entry_valore_B.get().strip()
            D_str = entry_valore_D.get().strip()
        except Exception:
            messagebox.showerror("Attenzione", "Widget entry mancanti")
            return

        if not all((A_str, B_str, D_str)):
            messagebox.showerror("Attenzione", "Nessun Dato da Analizzare")
            return

        try:
            A_val = int(A_str)
            B_val = int(B_str)
            D_val = int(D_str)
        except ValueError:
            messagebox.showerror("Attenzione", "Valori A, B, D non validi")
            return

    # S and Cb/Cd must exist to compute p_1,q_1,p_2,q_2 — compute them after S_val is determined

    # postponing primality checks until after p_1, q_1, p_2, q_2 are computed

    # Crea una nuova finestra (Toplevel) con parametri di ingrandimento
    finestra_test = tk.Toplevel()
    finestra_test.title("GC57 - Risultati Dettagliati del Test")

    # Imposta la dimensione iniziale e la rende ridimensionabile
    finestra_test.geometry("900x800")

    # Aggiunge un Frame per il contenuto (Placeholder per ora)
    frame_contenuto = ttk.Frame(finestra_test, padding="15")
    frame_contenuto.pack(fill="both", expand=True)
    ttk.Label(
        frame_contenuto,
        text="Pagina di Output: Esecuzione TEST, Visualizza Risultati",
        font=("Helvetica", 14, "bold"),
    ).pack(pady=10)

    # Mostra solo il semiprimo S in un widget multilinea (il resto è calcolato in segreto)
    ttk.Label(frame_contenuto, text="Prodotto Composto Da tre numeri Primi (A+x)(B+y)(D+z)", font=("Helvetica", 14, "bold")).pack(pady=6)

    text_frame_test = ttk.Frame(frame_contenuto)
    # Limitare l'espansione verticale del Text: usare fill x e non expand
    text_frame_test.pack(fill="x", expand=False, padx=5, pady=5)

    text_s = tk.Text(text_frame_test, wrap="char", height=8, font=("Courier", 10))
    # Fill only horizontally; vertical size controlled by 'height' and buttons
    text_s.pack(side="left", fill="x", expand=True)
    scroll_s = ttk.Scrollbar(text_frame_test, orient="vertical", command=text_s.yview)
    scroll_s.pack(side="right", fill="y")
    text_s.config(yscrollcommand=scroll_s.set, state="normal")

    # S: usa valore passato se presente, altrimenti calcola internamente senza mostrare i fattori
    try:
        if S_val is None:
            # prova a leggere A,B,D dalle entry (ma non mostrare i valori)
            A_try = entry_valore_A.get().strip()
            B_try = entry_valore_B.get().strip()
            D_try = entry_valore_D.get().strip()
            if all((A_try, B_try, D_try)):
                S_val = int(A_try) * int(B_try) * int(D_try)
            else:
                S_val = "(non disponibile)"

        text_s.delete("1.0", tk.END)
        text_s.insert(tk.END, str(S_val))

        # controlli interni: se sono passati A,B,D controlla coerenza e parità
        warnings = []
        try:
            if A_val is not None and B_val is not None and D_val is not None and S_val != "(non disponibile)":
                prod = int(A_val) * int(B_val) * int(D_val)
                if str(S_val) != str(prod):
                    warnings.append("S non corrisponde al prodotto interno")
                if prod % 2 == 0:
                    warnings.append("S è pari — possibile fattore 2 o dato non primo")
        except Exception:
            pass

        if warnings:
            text_s.insert(tk.END, "\n\nNOTE:\n" + "\n".join(warnings))

        # Adatta l'altezza del Text in base al numero di righe inserite
        try:
            last_index = text_s.index('end-1c')
            num_lines = int(last_index.split('.')[0])
            new_height = max(8, min(40, num_lines + 1))
            text_s.config(height=new_height)
        except Exception:
            pass

        # Insert warnings and adjust height; keep Text controlled vertically
        try:
            last_index = text_s.index('end-1c')
            num_lines = int(last_index.split('.')[0])
            new_height = max(8, min(40, num_lines + 1))
            text_s.config(height=new_height)
        except Exception:
            pass
        text_s.config(state="disabled")

        # assicurarsi che Cb_val/Cd_val siano definiti (se mancanti, ricaviamoli dalle entry)
        if Cb_val is None and B_val is not None:
            try:
                Cb_val = int(B_val) - 1
            except Exception:
                pass
        if Cd_val is None and D_val is not None:
            try:
                Cd_val = int(D_val) - 1
            except Exception:
                pass

        # ora possiamo calcolare p_1, q_1, p_2, q_2 in sicurezza
        try:
            p_1 = gcd(int(S_val), int(S_val) % int(Cd_val))
            q_1 = int(S_val) // p_1
            p_2 = gcd(p_1, p_1 % int(Cb_val))
            q_2 = p_1 // p_2
        except Exception:
            p_1 = q_1 = p_2 = q_2 = None

        # ora i primi sono calcolati: controlliamo la primalità prima di mostrarli
        try:
            if p_1 is None or q_1 is None or p_2 is None or q_2 is None:
                messagebox.showwarning("Attenzione", "Impossibile calcolare i fattori p/q")
                return
            if iprime(q_1) == False or iprime(p_2) == False or iprime(q_2) == False:
                messagebox.showwarning(
                    "Test non riuscito",
                    "Perché il test è fallito?\n\n"
                    "L'unico motivo del fallimento è la ricerca dei numeri primi "
                    "all'interno dell'intervallo selezionato.\n\n"
                    "• Se l'intervallo è troppo piccolo, la ricerca potrebbe non "
                    "restituire il numero primo richiesto.\n"
                    "• Verificare che A non sia troppo piccolo rispetto a B "
                    "(esempio: A = 13 cifre, B = 30 cifre).\n"
                    "  In questo caso la distanza tra A e B è superiore ad A stesso.\n"
                    "• Un altro caso possibile è che A sia troppo piccolo: "
                    "provare ad aumentare il valore di A.\n\n"
                    "Si consiglia di ripetere il test con gli stessi parametri "
                    "per verificare che la scelta random dell'intervallo "
                    "non abbia restituito un valore troppo vicino ai limiti, "
                    "facendo uscire la ricerca del numero primo dall'intervallo."
                )
                return
        except Exception:
            pass
    except Exception:
        text_s.config(state="disabled")

    # (Text P1 verrà creato dopo il blocco try/except per evitare collisione di indentazione)

    # --- NUOVO: Text P1 ---
    p1_frame = ttk.Frame(frame_contenuto)
    p1_frame.pack(fill="x", padx=5, pady=(6, 10))
    ttk.Label(p1_frame, text="P1 (numero composto da (A+x)(B+y))", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 4))
    text_p1 = tk.Text(p1_frame, wrap="char", height=4, font=("Courier", 10))
    text_p1.pack(side="left", fill="x", expand=True)
    scroll_p1 = ttk.Scrollbar(p1_frame, orient="vertical", command=text_p1.yview)
    scroll_p1.pack(side="right", fill="y")
    text_p1.config(yscrollcommand=scroll_p1.set)
    try:
        text_p1.config(state="normal")
        text_p1.insert(tk.END, str(p_1))
    finally:
        text_p1.config(state="disabled")

    # --- NUOVO: Text Q1 ---
    q1_frame = ttk.Frame(frame_contenuto)
    q1_frame.pack(fill="x", padx=5, pady=(6, 10))
    ttk.Label(
        q1_frame,
        text="Q1 (numero Primo D+z)",
        font=("Helvetica", 12, "bold"),
    ).pack(anchor="w", pady=(0, 4))
    text_q1 = tk.Text(q1_frame, wrap="char", height=4, font=("Courier", 10))
    text_q1.pack(side="left", fill="x", expand=True)
    scroll_q1 = ttk.Scrollbar(q1_frame, orient="vertical", command=text_q1.yview)
    scroll_q1.pack(side="right", fill="y")
    text_q1.config(yscrollcommand=scroll_q1.set)
    try:
        text_q1.config(state="normal")
        text_q1.insert(tk.END, str(q_1))
    finally:
        text_q1.config(state="disabled")

    # --- NUOVO: Text P ---
    p_frame = ttk.Frame(frame_contenuto)
    p_frame.pack(fill="x", padx=5, pady=(6, 10))
    ttk.Label(
        p_frame,
        text="P (numero Primo (A+x))",
        font=("Helvetica", 12, "bold"),
    ).pack(anchor="w", pady=(0, 4))
    text_p = tk.Text(p_frame, wrap="char", height=4, font=("Courier", 10))
    text_p.pack(side="left", fill="x", expand=True)
    scroll_p = ttk.Scrollbar(p_frame, orient="vertical", command=text_p.yview)
    scroll_p.pack(side="right", fill="y")
    text_p.config(yscrollcommand=scroll_p.set)
    try:
        text_p.config(state="normal")
        text_p.insert(tk.END, str(p_2))
    finally:
        text_p.config(state="disabled")

    # --- NUOVO: Text Q ---
    q_frame = ttk.Frame(frame_contenuto)
    q_frame.pack(fill="x", padx=5, pady=(6, 10))
    ttk.Label(
        q_frame,
        text="Q (numero Primo B+y)",
        font=("Helvetica", 12, "bold"),
    ).pack(anchor="w", pady=(0, 4))
    text_q = tk.Text(q_frame, wrap="char", height=4, font=("Courier", 10))
    text_q.pack(side="left", fill="x", expand=True)
    scroll_q = ttk.Scrollbar(q_frame, orient="vertical", command=text_q.yview)
    scroll_q.pack(side="right", fill="y")
    text_q.config(yscrollcommand=scroll_q.set)
    try:
        text_q.config(state="normal")
        text_q.insert(tk.END, str(q_2))
    finally:
        text_q.config(state="disabled")

    # --- Caselle primalità (p1,q1,p,q) sulla stessa linea ---
    primality_frame = ttk.Frame(frame_contenuto)
    primality_frame.pack(fill="x", padx=5, pady=(6, 10))
    ttk.Label(primality_frame, text="Test primo:", font=("Helvetica", 12, "bold")).pack(side="left", padx=(0,6))
    var_p1_prime = tk.BooleanVar(value=False)
    var_q1_prime = tk.BooleanVar(value=False)
    var_p_prime = tk.BooleanVar(value=False)
    var_q_prime = tk.BooleanVar(value=False)
    cb_p1 = ttk.Checkbutton(primality_frame, text="p1", variable=var_p1_prime, state="disabled", style="Primality.TCheckbutton")
    cb_q1 = ttk.Checkbutton(primality_frame, text="q1", variable=var_q1_prime, state="disabled", style="Primality.TCheckbutton")
    cb_p = ttk.Checkbutton(primality_frame, text="p", variable=var_p_prime, state="disabled", style="Primality.TCheckbutton")
    cb_q = ttk.Checkbutton(primality_frame, text="q", variable=var_q_prime, state="disabled", style="Primality.TCheckbutton")
    cb_p1.pack(side="left", padx=4)
    cb_q1.pack(side="left", padx=4)
    cb_p.pack(side="left", padx=4)
    cb_q.pack(side="left", padx=4)

    def salva_risultati():
        try:
            if S_val is None or S_val == "(non disponibile)" or p_1 is None:
                messagebox.showwarning(
                    "Attenzione", "Nessun risultato disponibile da salvare"
                )
                return

            filename = filedialog.asksaveasfilename(
                defaultextension=".txt", filetypes=[("File di testo", ".txt")]
            )     
            if not filename:
                return

            # Lettura valori base
            try:
                var_A = int(entry_valore_A.get().strip())
            except Exception:
                var_A = None
            try:
                var_B = int(entry_valore_B.get().strip())
            except Exception:
                var_B = None
            try:
                var_D = int(entry_valore_D.get().strip())
            except Exception:
                var_D = None

            # Calcoli di supporto
            intervallo_AB = abs(B_val - A_val) if A_val and B_val else None
            intervallo_ABD = (
                abs(D_val - (A_val * B_val)) if A_val and B_val and D_val else None
            )

            # Ricostruzione x, y, z
            found_x = found_y = found_z = None
            try:
                if var_A is not None:
                    found_x = A_val - var_A
            except Exception:
                pass
            try:
                if var_B is not None:
                    found_y = B_val - var_B
            except Exception:
                pass
            try:
                if var_D is not None:
                    found_z = D_val - var_D
            except Exception:
                pass

            from datetime import datetime

            testo = f"""
    ================================================================================
    TEST GC57
    Data e ora: {datetime.now().isoformat()}
    
    Numero creato su A         {A_val}
    lunghezza in cifre di A=   {len(str(A_val))}

    Numero creato su B         {B_val}
    lunghezza in cifre di B=   {len(str(B_val))}

    Numero creato su A*B       {A_val * B_val}
    lunghezza in cifre di A*b= {len(str(A_val * B_val))}

    Numero creato su D         {D_val}
    lunghezza in cifre di D=   {len(str(D_val))}

    intervallo tra A e B =           {intervallo_AB}
    Lunghezza intervallo in cifre =  {len(str(intervallo_AB)) if intervallo_AB else '-'}

    intervallo tra (A*B) e D =       {intervallo_ABD}
    Lunghezza intervallo in cifre =  {len(str(intervallo_ABD)) if intervallo_ABD else '-'}

    semiprimo= {S_val}

    Soluzione GC57 sul primo divisore step1  = {p_1}
    Verifica se è primo:   {iprime(p_1)}

    soluzione GC57 sul secondo divisore step1 = {q_1}
    Verifica se è primo:   {iprime(q_1)}

    soluzione GC57 sul primo divisore step2  = {p_2}
    Verifica se è primo:   {iprime(p_2)}

    soluzione GC57 sul secondo divisore step2 = {q_2}
    Verifica se è primo:   {iprime(q_2)}

    L'equazione (A+x)(B+y)(D+z)=S viene risolta:

    (A+x)= {var_A} + {found_x}
    (B+y)= {var_B} + {found_y}
    (D+z)= {var_D} + {found_z}

    S= {S_val}
    ================================================================================
    """

            with open(filename, "a", encoding="utf-8") as f:
                f.write(testo)

            messagebox.showinfo("Salvato", f"Risultati salvati in {filename}")

        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il salvataggio: {e}")

    # Pulsante per salvare i risultati
    btn_salva = ttk.Button(primality_frame, text="Salva risultati", command=salva_risultati, style='Accent.TButton')
    btn_salva.pack(side='right', padx=8)

    try:
        var_p1_prime.set(bool(iprime(p_1)))
    except Exception:
        var_p1_prime.set(False)
    try:
        var_q1_prime.set(bool(iprime(q_1)))
    except Exception:
        var_q1_prime.set(False)
    try:
        var_p_prime.set(bool(iprime(p_2)))
    except Exception:
        var_p_prime.set(False)
    try:
        var_q_prime.set(bool(iprime(q_2)))
    except Exception:
        var_q_prime.set(False)


# --- Funzione per aprire la finestra di aiuto ---
def apri_finestra_help():
    # Crea una nuova finestra (Toplevel)
    finestra_help = tk.Toplevel()
    finestra_help.title("Guida all'Input - GC57 Test")
    finestra_help.geometry("500x350")

    # Crea un Frame per il contenuto
    frame_contenuto = ttk.Frame(finestra_help, padding="15")
    frame_contenuto.pack(fill="both", expand=True)

    # 1. Titolo
    ttk.Label(
        frame_contenuto,
        text="Guida all'Inserimento Dati",
        font=("Helvetica", 14, "bold"),
    ).pack(pady=10)

    # 2. Spiegazione dei Campi
    testo_spiegazione = (
        "Questa sezione serve per generare i tre numeri base A, B, D e creare da questi le chiavi e "
        "i numeri primi che verranno trovati all'interno di un intervallo per poi creare S.\n\n"
        "Non si inseriscono direttamente i numeri ma per praticità gli si dà il valore in cifre nella casella piccola a fianco\n\n"
        "Questo perchè se vogliamo che il sistema funzioni, i numeri devono avere una lontananza in cifre minima.\n"
        "Questa differenza di cifre è obbligatoria solo in basso, cioè una tolleraza minima. In alto, cioè più grande, non ha limiti se non che un numero troppo grande\n"
        "rispetto a quello più piccolo, produrrebbe comunque un errore in quanto l'intervallo prodotto da questo numero supererebbe la capacità\n"
        "di capienza sul numero piccolo. Il programma è impostato sulla differenza minima di 10 cifre tra A e B e di 10 cifre tra (AB e D)\n"
        "Per tanto: Inserite le cifre nella casella corrispondente ad A\n"
        "Inserite le cifre con distanza minima 10 nella casella corrispondente B\n"
        "Inserite le cifre nella casella corrispondente D tenendo conto della somma A+B+10\n\n"
        "Poi premete 'CREA' per avviare il calcolo"
    )

    # L'area di testo accetta testo formattato
    text_widget = tk.Text(frame_contenuto, wrap="word", height=12, width=60)
    text_widget.insert(tk.END, testo_spiegazione)

    # Rende il testo non modificabile
    text_widget.config(state=tk.DISABLED, font=("Arial", 10))
    text_widget.pack(fill="both", expand=True, pady=10)

    # Pulsante per chiudere la finestra
    ttk.Button(frame_contenuto, text="Chiudi", command=finestra_help.destroy).pack(
        pady=10
    )


# --- Funzione che sarà chiamata quando si preme il pulsante ---
def genera_prodotto():
    # Usiamo 'prodotto' perché ora abbiamo tre fattori: S = A * B * r

    try:
        # 1. Recupera i valori di input
        cifre_A = int(entry_cifre_A.get())
        cifre_B = int(entry_cifre_B.get())
        cifre_D = int(entry_cifre_D.get())

        if not all((cifre_A, cifre_B, cifre_D)):
            messagebox.showerror(
                "Attenzione", "Tutti e tre i campi delle cifre\ndevono essere impostati"
            )
            return
        if cifre_A < 13:
            messagebox.showerror("Attenzione:", "Valore minimo di cifre in A è 13")
            return

        if cifre_B - cifre_A < 10:
            messagebox.showerror(
                "Attenzione", "La differenza tra Cifre B e Cifre A, minimo 10"
            )
            return
        if cifre_D < (cifre_A + cifre_B + 10):
            messagebox.showerror(
                "Attenzione", "La differenza tra Cifre A+B e Cifre D, minimo 10"
            )
            return

        var_A, var_B, var_D = genera_A_B_D(cifre_A, cifre_B, cifre_D)

        # 4. Simula il calcolo e la visualizzazione dei risultati

        entry_valore_A.delete(0, tk.END)
        entry_valore_A.insert(0, str(var_A))

        entry_valore_B.delete(0, tk.END)
        entry_valore_B.insert(0, str(var_B))

        entry_valore_D.delete(0, tk.END)  # Aggiornamento del terzo fattore
        entry_valore_D.insert(0, str(var_D))

        # Generazione chiavi GC57
        Cb = var_B - 1
        Cd = var_D - 1

        # Calcolo A*B
        B_sost = var_A * var_B

        # Calcolo intervallo B
        Nb = (var_A + 1) * (var_B + 1)
        Ib = (Cb // (Nb % Cb)) * 2

        # Calcolo intervallo D
        Nd = (B_sost + 1) * (var_D + 1)
        Id = (Cd // (Nd % Cd)) * 2

        if Nb < 100 or Nd < 100:
            messagebox.showerror(
                "Attenzione",
                "Non è stato trovato un campo idoneo per il test\nAumentare il valore di A",
            )
            return
        # calcolo numeri primi
        x = randint(0, Ib)
        y = randint(0, Ib)
        z = randint(0, Id)
        A = nprime(var_A + x)
        B = nprime(var_B + y)
        D = nprime(var_D + z)
        S = A * B * D

        # Popola il widget Text multilina per S
        text_valore_S.config(state="normal")
        text_valore_S.delete("1.0", tk.END)
        text_valore_S.insert(tk.END, str(S))
        # Adatta altezza in base al contenuto (min 4 righe, max 20)
        try:
            last_index = text_valore_S.index('end-1c')
            num_lines = int(last_index.split('.')[0])
            new_height = max(4, min(20, num_lines + 1))
            text_valore_S.config(height=new_height)
        except Exception:
            pass
        text_valore_S.config(state="disabled")

        # Imposta il comando del pulsante Esegui Test con i primi appena calcolati
        try:
            btn_esegui_test.config(command=lambda A=A, B=B, D=D, Cb=Cb, Cd=Cd, S=S: apri_finestra_test(A, B, D, Cb, Cd, S))
            btn_esegui_test.config(state="normal")
        except Exception:
            # Se il pulsante non esiste ancora (o altro errore), non fallire
            pass

    except ValueError:
        label_messaggio.config(
            text="ERRORE: Inserisci numeri interi validi nel campo cifre.",
            foreground="red",
        )


# --- Funzione per l'aggiunta di elementi (widgets) ---
def crea_elementi_grafici(root):
    # Dichiariamo le variabili globali necessarie per essere accessibili da 'genera_prodotto'
    global entry_cifre_A, entry_cifre_B, entry_cifre_D
    global entry_valore_A, entry_valore_B, entry_valore_D
    global text_valore_S
    global label_messaggio  # Nuovo label per i messaggi di errore
    global btn_esegui_test  # Pulsante Esegui Test (assegnato qui alla creazione)

    # --- 1. Frame per la Sezione di Generazione ---
    frame_generazione = ttk.LabelFrame(
        root,
        text="Generazione del Prodotto di Test a partire da A,B,D",
        padding="10 10 10 10",
    )
    frame_generazione.pack(pady=20, padx=20, fill="x")

    # Configura il peso delle colonne nel Frame per un layout a griglia efficiente
    frame_generazione.columnconfigure(0, weight=1)
    frame_generazione.columnconfigure(1, weight=1)
    frame_generazione.columnconfigure(2, weight=1)
    frame_generazione.columnconfigure(
        3, weight=3
    )  # Colonna 3 più larga per la descrizione

    riga = 0

    # --- 2. Elementi per il Fattore A ---
    ttk.Label(
        frame_generazione, text="Fattore (A)", font=("Helvetica", 10, "bold")
    ).grid(row=riga, column=0, sticky="w", padx=5, pady=5)

    entry_cifre_A = ttk.Entry(frame_generazione, width=10)
    entry_cifre_A.grid(row=riga, column=1, sticky="w", padx=5, pady=5)
    ttk.Label(frame_generazione, text="N. Cifre: esempio Minimo Valori").grid(
        row=riga, column=2, sticky="w", padx=5, pady=5
    )

    riga += 1

    entry_valore_A = ttk.Entry(frame_generazione, width=40)
    entry_valore_A.grid(row=riga, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

    riga += 1

    # --- 3. Elementi per il Fattore B ---
    ttk.Label(
        frame_generazione, text="Fattore (B)", font=("Helvetica", 10, "bold")
    ).grid(row=riga, column=0, sticky="w", padx=5, pady=5)

    entry_cifre_B = ttk.Entry(frame_generazione, width=10)
    entry_cifre_B.grid(row=riga, column=1, sticky="w", padx=5, pady=5)
    ttk.Label(frame_generazione, text="N. Cifre").grid(
        row=riga, column=2, columnspan=2, sticky="w", padx=5, pady=5
    )

    riga += 1

    entry_valore_B = ttk.Entry(frame_generazione, width=40)
    entry_valore_B.grid(row=riga, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

    riga += 1

    # --- 4. Elementi per il Fattore D ---
    ttk.Label(
        frame_generazione, text="Fattore (D)", font=("Helvetica", 10, "bold")
    ).grid(row=riga, column=0, sticky="w", padx=5, pady=5)

    entry_cifre_D = ttk.Entry(frame_generazione, width=10)
    entry_cifre_D.grid(row=riga, column=1, sticky="w", padx=5, pady=5)
    ttk.Label(frame_generazione, text="N. Cifre").grid(
        row=riga, column=2, sticky="w", padx=5, pady=5
    )

    riga += 1

    entry_valore_D = ttk.Entry(frame_generazione, width=40)
    entry_valore_D.grid(row=riga, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

    riga += 2  # Salta una riga per separazione

    # --- 5. Pulsanti "Genera" e "Help" ---

    # Pulsante Genera (occupa le colonne 0 e 1)
    btn_crea = ttk.Button(
        frame_generazione,
        text="CREA",
        width=18,
        command=genera_prodotto,
        style="Accent.TButton",
    )
    btn_crea.grid(row=riga, column=0, columnspan=2, pady=10, padx=5)

    # Pulsante Help (occupa le colonne 2 e 3)
    btn_help = ttk.Button(frame_generazione, text="Help", command=apri_finestra_help)
    btn_help.grid(row=riga, column=2, columnspan=2, pady=10, padx=5, sticky="ew")

    riga += 1

    # Etichetta per i messaggi di errore/stato
    label_messaggio = ttk.Label(frame_generazione, text="", foreground="red")
    label_messaggio.grid(row=riga, column=0, columnspan=4, sticky="w", padx=5, pady=5)

    riga += 1

    # --- NUOVO: Pulsante "Esegui Test" ---
    btn_esegui_test = ttk.Button(
        frame_generazione,
        text="Esegui Test",
        command=apri_finestra_test,
        style="Accent.TButton",
        width=25,
        state="disabled",
    )
    # Posizionato al centro, occupa tutte le 4 colonne
    btn_esegui_test.grid(row=riga, column=0, columnspan=4, pady=10)

    riga += 1

    # --- 6. Output del Prodotto Finale S (Spostato in basso) ---
    ttk.Label(
        frame_generazione, text="Prodotto Generato S=(A+x)(B+y)(D+z)", font=("Helvetica", 12, "bold")
    ).grid(row=riga, column=0, sticky="w", padx=5, pady=10)

    riga += 1

    # Spazio verticale prima dell'output multilina
    riga += 1

    # Widget multilinea per S (wrap e scrollbar) - evita overflow con valori molto grandi
    text_frame = ttk.Frame(frame_generazione)
    text_frame.grid(row=riga, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
    text_frame.columnconfigure(0, weight=1)
    # Text occupies row 0, col 0; scrollbar in col 1; controls (▲ ▼) in row 1 col 0
    text_valore_S = tk.Text(text_frame, wrap="char", height=4, font=("Courier", 9))
    text_valore_S.grid(row=0, column=0, sticky="ew")
    scroll_s = ttk.Scrollbar(text_frame, orient="vertical", command=text_valore_S.yview)
    scroll_s.grid(row=0, column=1, sticky="ns")
    text_valore_S.config(yscrollcommand=scroll_s.set, state="disabled")
    control_frame = ttk.Frame(text_frame)
    control_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=2)
    btn_increase = ttk.Button(control_frame, text="▲", width=3, command=lambda: _change_text_height(text_valore_S, 3))
    btn_decrease = ttk.Button(control_frame, text="▼", width=3, command=lambda: _change_text_height(text_valore_S, -3))
    btn_increase.pack(side="left", padx=2)
    btn_decrease.pack(side="left", padx=2)

    riga += 1

    # Etichetta per la regola di calcolo delle cifre di S
    ttk.Label(
        frame_generazione, text=""
    ).grid(row=riga, column=0, columnspan=4, sticky="w", padx=5, pady=5)


# --- Funzione principale per l'applicazione (come prima) ---
def main():
    # Inizializzazione delle variabili globali (necessarie se si usano funzioni)
    global entry_cifre_A, entry_cifre_B, entry_cifre_D
    global entry_valore_A, entry_valore_B, entry_valore_D
    global label_messaggio

    finestra_principale = tk.Tk()
    finestra_principale.title("GC57 - Strumento Test di Fattorizzazione su equazioni diofantee cubiche")

    # 🚫 Nota: Lasciamo che la finestra principale si adatti automaticamente al contenuto

    # Stile per il pulsante azzurro (Accent)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Accent.TButton",
        background="light blue",
        foreground="black",
        font=("Helvetica", 10, "bold"),
    )
    # Style for primality checkboxes to ensure contrast on light background
    style.configure("Primality.TCheckbutton", foreground="black")
    style.map("Primality.TCheckbutton", foreground=[('disabled', 'black'), ('!disabled', 'black')])

    crea_elementi_grafici(finestra_principale)

    # Imposta valori di default per iniziare subito a testare
    entry_cifre_A.insert(0, "13")
    entry_cifre_B.insert(0, "23")
    entry_cifre_D.insert(0, "46")

    finestra_principale.mainloop()

# Definiamo le variabili globali qui per la scope
entry_cifre_A = None
entry_cifre_B = None
entry_cifre_D = None
entry_valore_A = None
entry_valore_B = None
entry_valore_D = None
label_messaggio = None
btn_esegui_test = None

# --- Esecuzione del programma ---
if __name__ == "__main__":
    main()
