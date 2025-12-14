# Progetto_studio_GC57
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk, filedialog
import secrets
import random
import os
import platform
import subprocess
from math import gcd

# --- GLOBAL STATE VARIABLES ---
SharedData = {
    "a": None,
    "b": None,
    "field": None,
    "hidden_x": None,
    "hidden_y": None,
    "p_prime": None,
    "q_prime": None,
    "semiprime": None 
}

# --- 1. MATHEMATICAL ENGINE (Standard Python) ---
def is_probably_prime(n, k=10):
    """Miller-Rabin primality test."""
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n < 2: return False
    r, d = 0, n - 1
    while d % 2 == 0: r += 1; d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def get_next_prime(start_num):
    """Finds the next prime number >= start_num."""
    if start_num % 2 == 0: candidate = start_num + 1
    else: candidate = start_num
    while not is_probably_prime(candidate): candidate += 2
    return candidate

# --- 2. BACKGROUND LOGIC ---
MIN_BIT_A = 64
MIN_BIT_DIFF = 50
MAX_BIT_LIMIT = 7000

def verify_metrics(a, b):
    bit_a = a.bit_length()
    bit_b = b.bit_length()
    if bit_a < MIN_BIT_A: return False, f"ERROR: A is too small ({bit_a} < {MIN_BIT_A} bits)."
    if bit_b <= (bit_a + MIN_BIT_DIFF): return False, f"ERROR: B is too close to A (Diff < {MIN_BIT_DIFF} bits)."
    return True, "Metrics OK."

def generate_secrets_with_target(target_bits):
    variation = secrets.randbelow(5) - 2
    bits_per_a = target_bits + variation
    if bits_per_a < MIN_BIT_A: bits_per_a = MIN_BIT_A
    a = secrets.randbits(bits_per_a) | 1
    bits_per_b = bits_per_a + 50 + secrets.randbelow(51)
    b = secrets.randbits(bits_per_b) | 1
    return a, b

def calculate_gc57_field(a, b):
    key = b - 1
    try:
        modulo_val = ((a + 1) * (b + 1)) % key
        if modulo_val == 0: return None, None, "Math Error: Modulo is 0."
        field = (key // modulo_val) * 2
        return field, f"Length: {field.bit_length()} bits | Digits: {len(str(field))}", None
    except Exception as e: return None, None, f"Unexpected Error: {e}"

def generate_challenge_semiprime(val_a, val_b, val_field):
    if val_field <= 2: return None, None, None, None, None, "Error: Field is too small."
    offset_x = secrets.randbelow(val_field - 1) + 1
    offset_y = secrets.randbelow(val_field - 1) + 1
    p_prime = get_next_prime(val_a + offset_x)
    q_prime = get_next_prime(val_b + offset_y)
    final_x = p_prime - val_a
    final_y = q_prime - val_b
    semiprime = p_prime * q_prime
    return final_x, final_y, p_prime, q_prime, semiprime, None

# --- SYSTEM FUNCTIONS ---
def open_pdf_file(filename):
    if not os.path.exists(filename):
        messagebox.showerror("File Missing", f"Cannot find file: {filename}")
        return
    try:
        if platform.system() == 'Windows': os.startfile(filename)
        elif platform.system() == 'Darwin': subprocess.call(('open', filename))
        else: subprocess.call(('xdg-open', filename))
        write_log(f"Opening document: {filename}", "normal")
    except Exception as e: write_log(f"PDF Error: {e}", "error")

def save_log_to_file():
    content = log_area.get("1.0", tk.END)
    if not content.strip():
        messagebox.showinfo("Empty Log", "Nothing to save.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt"), ("All Files", "*.*")],
        title="Save Operation Log"
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f: f.write(content)
            messagebox.showinfo("Success", f"Log saved to:\n{file_path}")
        except Exception as e: messagebox.showerror("Error", f"Cannot save file:\n{e}")

# --- GUI HELPERS ---
def show_help_a(): 
    msg = "Value A must be significantly smaller than B in bits, but at least 64 bits."
    messagebox.showinfo("Info Coefficient A", msg)

def show_help_b(): 
    msg = "Value B must be significantly larger than A (at least +50 bits).\nThis difference directly impacts the Field size."
    messagebox.showinfo("Info Coefficient B", msg)

def show_help_field(): 
    msg = ("The Field is calculated based on the distance between coefficients and the Key (B-1).\n\n"
           "FORMULA:\n"
           "Field = ((B-1) // (((A + 1) * (B + 1)) % (B-1))) * 2")
    messagebox.showinfo("Info Field", msg)

def write_log(message, type="normal"):
    log_area.configure(state="normal")
    tag = None
    if type == "error": tag = "tag_error"
    elif type == "success": tag = "tag_success"
    elif type == "input_data": tag = "tag_input"
    elif type == "calc_xy": tag = "tag_xy"
    log_area.insert(tk.END, ">> " + message + "\n", tag)
    log_area.see(tk.END)
    log_area.configure(state="disabled")

# --- GUI ACTIONS ---
def command_generate():
    try: bit_target = int(entry_bits.get())
    except ValueError: write_log("Invalid Target Bits.", "error"); return
    if bit_target > MAX_BIT_LIMIT or bit_target < MIN_BIT_A: write_log("Bits out of range.", "error"); return

    a, b = generate_secrets_with_target(bit_target)
    text_a.delete("1.0", tk.END); text_a.insert("1.0", str(a))
    text_b.delete("1.0", tk.END); text_b.insert("1.0", str(b))
    text_field.configure(state="normal"); text_field.delete("1.0", tk.END); text_field.configure(state="disabled")
    lbl_stats_field.config(text="")
    
    # Reset Globals
    for key in SharedData: SharedData[key] = None
    write_log(f"Generated new values (Target ~{bit_target} bits).", "normal")

def command_analyze_and_calculate():
    val_a_str = text_a.get("1.0", "end-1c").strip()
    val_b_str = text_b.get("1.0", "end-1c").strip()
    if not val_a_str or not val_b_str: write_log("Empty fields.", "error"); return
    try: val_a = int(val_a_str); val_b = int(val_b_str)
    except ValueError: write_log("Invalid numbers.", "error"); return

    write_log(f"INPUT -> A: {val_a.bit_length()} bits | B: {val_b.bit_length()} bits", "input_data")
    success, msg = verify_metrics(val_a, val_b)
    if not success: write_log(msg, "error"); return
    
    # 1. Calculate Field
    field, stats, error = calculate_gc57_field(val_a, val_b)
    if error: write_log(error, "error"); return

    text_field.configure(state="normal"); text_field.delete("1.0", tk.END); text_field.insert("1.0", str(field)); text_field.configure(state="disabled")
    lbl_stats_field.config(text=stats)
    write_log(f"FIELD CALCULATED -> {stats}", "success")

    # 2. Generate Semiprime (Background)
    write_log("Auto-generating Semiprime N...", "normal")
    root.update()
    x, y, p, q, semiprime, err_gen = generate_challenge_semiprime(val_a, val_b, field)
    
    if err_gen: write_log(err_gen, "error"); return

    # 3. Save Data
    SharedData["a"] = val_a
    SharedData["b"] = val_b
    SharedData["field"] = field
    SharedData["hidden_x"] = x
    SharedData["hidden_y"] = y
    SharedData["p_prime"] = p
    SharedData["q_prime"] = q
    SharedData["semiprime"] = semiprime
    
    write_log(f"SEMIPRIME GENERATED ({semiprime.bit_length()} bits).", "success")
    write_log("Data ready. Proceed to Step 2 or jump to Step 3.", "normal")

def command_show_challenge():
    a = SharedData["a"]; b = SharedData["b"]; semiprime = SharedData["semiprime"]
    if a is None or semiprime is None:
        messagebox.showwarning("Missing Data", "Go back to Step 1 and click 'Analyze & Calculate Field'!")
        return

    text_a_sfida.configure(state="normal"); text_a_sfida.delete("1.0", tk.END); text_a_sfida.insert("1.0", str(a)); text_a_sfida.configure(state="disabled")
    text_b_sfida.configure(state="normal"); text_b_sfida.delete("1.0", tk.END); text_b_sfida.insert("1.0", str(b)); text_b_sfida.configure(state="disabled")
    text_semi.configure(state="normal"); text_semi.delete("1.0", tk.END); text_semi.insert("1.0", str(semiprime)); text_semi.configure(state="disabled")
    lbl_info_semi.config(text=f"Semiprime N ({semiprime.bit_length()} bits)")
    
    text_x.configure(state="normal"); text_x.delete("1.0", tk.END); text_x.insert("1.0", "???"); text_x.configure(state="disabled")
    text_y.configure(state="normal"); text_y.delete("1.0", tk.END); text_y.insert("1.0", "???"); text_y.configure(state="disabled")
    btn_reveal.config(state="normal", bg="orange")
    write_log("Step 2: Challenge displayed.", "calc_xy")

def command_reveal_solution():
    x = SharedData["hidden_x"]; y = SharedData["hidden_y"]
    if x is None: return
    text_x.configure(state="normal"); text_x.delete("1.0", tk.END); text_x.insert("1.0", str(x)); text_x.configure(state="disabled")
    text_y.configure(state="normal"); text_y.delete("1.0", tk.END); text_y.insert("1.0", str(y)); text_y.configure(state="disabled")
    btn_reveal.config(state="disabled", bg="#DDDDDD")
    write_log(f"SOLUTION REVEALED: x={x}", "success")
    write_log(f"SOLUTION REVEALED: y={y}", "success")

def jump_to_method(): notebook.select(2)

def update_tab3_data(event):
    if notebook.index(notebook.select()) == 2: # Step 3
        a = SharedData["a"]
        b = SharedData["b"]
        n = SharedData["semiprime"]
        
        t3_a.config(state="normal"); t3_a.delete("1.0", tk.END)
        t3_b.config(state="normal"); t3_b.delete("1.0", tk.END)
        t3_n.config(state="normal"); t3_n.delete("1.0", tk.END)
        t3_key.config(state="normal"); t3_key.delete("1.0", tk.END)
        
        if a and b and n:
            t3_a.insert("1.0", str(a))
            t3_b.insert("1.0", str(b))
            key = b - 1
            t3_key.insert("1.0", str(key))
            t3_n.insert("1.0", str(n))
            btn_solve.config(state="normal", bg="red")
        else:
            t3_a.insert("1.0", "Missing Data. Run Step 1.")
            btn_solve.config(state="disabled", bg="gray")
        
        t3_a.config(state="disabled"); t3_b.config(state="disabled")
        t3_n.config(state="disabled"); t3_key.config(state="disabled")

def command_solve_gc57():
    write_log("Starting GC57 Method Procedure...", "normal")
    if not SharedData["semiprime"]: return

    N = SharedData["semiprime"]
    A = SharedData["a"]
    B = SharedData["b"]
    key = B - 1

    write_log(f"Calculated Key (B-1): {key}", "input_data")

    # GC57 ALGORITHM
    factor_p = gcd(N, N % key)
    factor_q = N // factor_p
    x_found = factor_p - A
    y_found = factor_q - B

    write_log("-" * 40)
    write_log(f"Analyzed Semiprime: N={N}", "normal")
    write_log(f"RESULT GCD (P): {factor_p}", "success")
    write_log(f"Derived Factor Q: {factor_q}", "success")
    write_log(f"Identified x: {x_found}", "calc_xy")
    write_log(f"Identified y: {y_found}", "calc_xy")
    write_log("-" * 40)

    if factor_p * factor_q == N and factor_p > 1:
        msg = (f"FACTORIZATION SUCCESSFUL!\n\n"
               f"P (GCD): {factor_p}\n"
               f"Q: {factor_q}\n\n"
               f"x: {x_found}\n"
               f"y: {y_found}")
        messagebox.showinfo("GC57 Success", msg)
    else:
        write_log("WARNING: Method failed to split the number (GCD=1).", "error")
        messagebox.showwarning("Failed", "Method resulted in GCD=1.\nTry adjusting parameters A and B.")

# --- GUI CONSTRUCTION ---
root = tk.Tk()
root.title("GC57 Project - Full Demonstrator")
root.geometry("900x750")
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[10, 5])

# -- LOG --
frame_log = tk.LabelFrame(root, text=" Operation Log ", font=("Arial", 10, "bold"), height=130)
frame_log.pack(side=tk.BOTTOM, fill="x", padx=10, pady=10); frame_log.pack_propagate(False)

btn_save_log = tk.Button(frame_log, text="Save Log to File", command=save_log_to_file, font=("Arial", 8), bg="#e0e0e0")
btn_save_log.pack(anchor="ne", padx=5, pady=0)

log_area = scrolledtext.ScrolledText(frame_log, font=("Consolas", 9)); log_area.pack(fill="both", expand=True, padx=5, pady=5); log_area.configure(state="disabled")
log_area.tag_config("tag_error", foreground="red"); log_area.tag_config("tag_success", foreground="green"); log_area.tag_config("tag_input", foreground="blue"); log_area.tag_config("tag_xy", foreground="purple")

notebook = ttk.Notebook(root); notebook.pack(fill="both", expand=True, padx=10, pady=5)
notebook.bind("<<NotebookTabChanged>>", update_tab3_data)

# TAB 1
tab1 = tk.Frame(notebook); notebook.add(tab1, text="  Step 1: Input & Field  ")
frame_input = tk.Frame(tab1); frame_input.pack(pady=5, padx=20)
tk.Label(frame_input, text="Target Bits (A):", font=("Arial", 11, "bold"), fg="blue").grid(row=0, column=0, sticky="e", pady=5)
entry_bits = tk.Entry(frame_input, width=10, font=("Consolas", 11), justify="center"); entry_bits.insert(0, "150"); entry_bits.grid(row=0, column=1, sticky="w", pady=5)
tk.Label(frame_input, text="Value A:", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="ne", pady=5)
text_a = tk.Text(frame_input, width=70, height=3, font=("Consolas", 10)); text_a.grid(row=1, column=1, pady=5)
tk.Button(frame_input, text="?", width=3, bg="#DDDDDD", command=show_help_a).grid(row=1, column=2, padx=5, sticky="n", pady=5)
tk.Label(frame_input, text="Value B:", font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="ne", pady=5)
text_b = tk.Text(frame_input, width=70, height=3, font=("Consolas", 10)); text_b.grid(row=2, column=1, pady=5)
tk.Button(frame_input, text="?", width=3, bg="#DDDDDD", command=show_help_b).grid(row=2, column=2, padx=5, sticky="n", pady=5)
frame_btn1 = tk.Frame(tab1); frame_btn1.pack(pady=10)
tk.Button(frame_btn1, text="Generate Values", command=command_generate, bg="lightblue", font=("Arial", 10), padx=10).pack(side=tk.LEFT, padx=10)
tk.Button(frame_btn1, text="Analyze & Calculate Field", command=command_analyze_and_calculate, bg="lightgreen", font=("Arial", 10, "bold"), padx=10).pack(side=tk.LEFT, padx=10)
frame_res1 = tk.LabelFrame(tab1, text=" Result: FIELD ", font=("Arial", 10, "bold"), fg="darkblue"); frame_res1.pack(pady=10, padx=20, fill="x")
frame_res1.columnconfigure(1, weight=1)
lbl_stats_field = tk.Label(frame_res1, text="", font=("Arial", 9, "italic"), fg="#555555"); lbl_stats_field.grid(row=0, column=0, columnspan=2, sticky="w", padx=10)
text_field = tk.Text(frame_res1, width=80, height=5, font=("Consolas", 10), bg="#f0f0f0", state="disabled"); text_field.grid(row=1, column=0, padx=10, pady=5)
tk.Button(frame_res1, text="?", width=3, bg="#DDDDDD", command=show_help_field).grid(row=1, column=1, sticky="n", pady=5, padx=5)

# Note Step 1
text_msg1 = tk.Text(tab1, width=87, height=8, font=("arial", 10, "bold"), bg="#F69C00", fg="black", state="normal")
msg_step1 = ("NOTE: A and B values can be manually entered or generated by setting the Target Bits.\n"
             "For manual entry, respect the GC57 logic:\n"
             "- A must be sufficiently large (min 60 bits).\n"
             "- B must be significantly larger than A (at least +50 bits).\n"
             "Once values are set, click 'Analyze & Calculate Field'.\n"
             "Tip: Try reducing digits from A (or adding to B) to see how the GC57 Field expands.\n"
             "A and B do not require a specific pattern (can be odd or even).")
text_msg1.insert("1.0", msg_step1); text_msg1.configure(state="disabled"); text_msg1.pack(padx=10, pady=10)

# TAB 2
tab2 = tk.Frame(notebook); notebook.add(tab2, text="  Step 2: Challenge (Equation)  ")
frame_skip = tk.Frame(tab2, bg="#f9f9f9", bd=1, relief="solid"); frame_skip.pack(fill="x", padx=10, pady=5)
tk.Button(frame_skip, text="Optional: Skip Challenge and go directly to 'GC57 Method' >>", command=jump_to_method, bg="#e0e0e0", fg="#333", font=("Arial", 10)).pack(pady=5)
frame_sfida_header = tk.Frame(tab2); frame_sfida_header.pack(pady=5)
tk.Label(frame_sfida_header, text="N = (A + x)(B + y)  [P, Q are Primes]", font=("Arial", 14, "bold"), fg="darkblue").pack()
tk.Button(frame_sfida_header, text="DISPLAY GENERATED CHALLENGE", command=command_show_challenge, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5).pack(pady=5)
frame_n = tk.LabelFrame(tab2, text=" KNOWN DATA ", font=("Arial", 10, "bold")); frame_n.pack(pady=5, padx=20, fill="x")
tk.Label(frame_n, text="A:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10); text_a_sfida = tk.Text(frame_n, width=80, height=2, bg="#f0f0f0", state="disabled"); text_a_sfida.pack(padx=10)
tk.Label(frame_n, text="B:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10); text_b_sfida = tk.Text(frame_n, width=80, height=2, bg="#f0f0f0", state="disabled"); text_b_sfida.pack(padx=10)
tk.Label(frame_n, text="N:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10); text_semi = tk.Text(frame_n, width=80, height=3, bg="#e6f2ff", state="disabled"); text_semi.pack(padx=10)
lbl_info_semi = tk.Label(frame_n, text=""); lbl_info_semi.pack()
frame_soluzione = tk.LabelFrame(tab2, text=" SOLUTION ", font=("Arial", 10, "bold"), fg="#d9534f"); frame_soluzione.pack(pady=10, padx=20, fill="x")
btn_reveal = tk.Button(frame_soluzione, text="2. REVEAL SOLUTION", command=command_reveal_solution, bg="#DDDDDD", state="disabled", font=("Arial", 10, "bold")); btn_reveal.pack(anchor="w", padx=10, pady=5)
text_x = tk.Text(frame_soluzione, width=80, height=2, bg="#fff5e6", state="disabled"); text_x.pack(padx=10)
text_y = tk.Text(frame_soluzione, width=80, height=2, bg="#fff5e6", state="disabled"); text_y.pack(padx=10)

# TAB 3
tab3 = tk.Frame(notebook); notebook.add(tab3, text="  Step 3: GC57 Method  ")
tk.Label(tab3, text="GC57 Method: Analysis & Resolution", font=("Arial", 16, "bold"), fg="darkblue").pack(pady=15)
text_msg3 = tk.Text(tab3, width=90, height=6, font=("arial", 10, "bold"), bg="#F69C00", fg="black", state="normal")
msg_step3 = ("GC57 METHOD NOTE:\n"
             "In this section, the Semiprime N is analyzed using coefficients A and B.\n"
             "The GC57 method leverages the relationship between the Field and the Key (B-1).\n"
             "By applying the deterministic formula GCD(N, N % Key), the system can instantly\n"
             "retrieve the prime factor P, and consequently Q, x, and y.\n"
             "Click 'SOLVE' to execute the algorithm.")
text_msg3.insert("1.0", msg_step3); text_msg3.configure(state="disabled"); text_msg3.pack(padx=10, pady=10)

frame_dati_metodo = tk.LabelFrame(tab3, text=" Calculation Data ", font=("Arial", 11, "bold")); frame_dati_metodo.pack(fill="x", padx=20, pady=10)
tk.Label(frame_dati_metodo, text="Value A:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", padx=10)
t3_a = tk.Text(frame_dati_metodo, width=40, height=2, bg="#f0f0f0", state="disabled"); t3_a.grid(row=1, column=0, padx=10, pady=5)
tk.Label(frame_dati_metodo, text="Value B:", font=("Arial", 9, "bold")).grid(row=0, column=1, sticky="w", padx=10)
t3_b = tk.Text(frame_dati_metodo, width=40, height=2, bg="#f0f0f0", state="disabled"); t3_b.grid(row=1, column=1, padx=10, pady=5)
tk.Label(frame_dati_metodo, text="Semiprime N:", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky="w", padx=10)
t3_n = tk.Text(frame_dati_metodo, width=40, height=3, bg="#e6f2ff", state="disabled"); t3_n.grid(row=3, column=0, padx=10, pady=5)
tk.Label(frame_dati_metodo, text="Key (B-1):", font=("Arial", 9, "bold")).grid(row=2, column=1, sticky="w", padx=10)
t3_key = tk.Text(frame_dati_metodo, width=40, height=3, bg="#f0f0f0", state="disabled"); t3_key.grid(row=3, column=1, padx=10, pady=5)

btn_solve = tk.Button(tab3, text="SOLVE (Run GC57)", command=command_solve_gc57, bg="red", fg="white", font=("Arial", 12, "bold"), padx=30, pady=10); btn_solve.pack(pady=20)

frame_pdf = tk.Frame(tab3); frame_pdf.pack(pady=10)
# Ensure your PDF files are named exactly as below or change the names here
tk.Button(
    frame_pdf,
    text="Open PDF: Main Publication",
    command=lambda: open_pdf_file("gc57_deep_dive_Structure.pdf"),
    bg="#DDDDDD",
    padx=10,
).pack(side=tk.LEFT, padx=20)
tk.Button(
    frame_pdf,
    text="Open PDF: Deep Dive",
    command=lambda: open_pdf_file("gc57_deep_dive_Compartments.pdf"),
    bg="#DDDDDD",
    padx=10,
).pack(side=tk.LEFT, padx=20)

root.mainloop()
