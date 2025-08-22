import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pyswip import Prolog

prolog = Prolog()
prolog.consult("projetIA.pl")

def verifier():
    suspect = entry_suspect.get().strip().lower()
    crime = combo_crime.get().strip().lower()
    
    query = f"is_guilty({suspect}, {crime})"
    print("Requête :", query)

    result = list(prolog.query(query))
    if result:
        messagebox.showinfo("Résultat", f"{suspect} est coupable de {crime}")
    else:
        messagebox.showwarning("Résultat", f"{suspect} n'est pas coupable de {crime}")

root = tk.Tk()
root.title("Détective IA - Prolog")
root.geometry("400x300")  
root.resizable(True, True)  

tk.Label(root, text="Nom du suspect :", font=("Arial", 12)).pack(pady=10)
entry_suspect = tk.Entry(root, font=("Arial", 11), width=25)
entry_suspect.pack(pady=5)

tk.Label(root, text="Type de crime :", font=("Arial", 12)).pack(pady=(20, 5))
combo_crime = ttk.Combobox(root, values=["vol", "assassinat", "escroquerie"], 
                          state="readonly", font=("Arial", 11), width=22)
combo_crime.pack(pady=5)
combo_crime.current(0)  

tk.Button(root, text="Vérifier la culpabilité", command=verifier, 
          font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
          padx=20, pady=10).pack(pady=30)

root.mainloop()
