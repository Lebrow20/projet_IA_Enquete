import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
from pyswip import Prolog

prolog = Prolog()
prolog.consult("projetIA.pl")

class SuspectCarousel:
    def __init__(self, parent):
        self.suspects = ["John", "Mary", "Alice", "Bruno", "Sophie"]
        self.current_index = 0
        self.parent = parent
        
        self.carousel_frame = tk.Frame(parent)
        self.carousel_frame.pack(pady=20)
        
        self.btn_prev = tk.Button(self.carousel_frame, text="◄", font=("Arial", 16), 
                                 command=self.previous_suspect, bg="#f0f0f0")
        self.btn_prev.pack(side=tk.LEFT, padx=10)
        
        self.image_frame = tk.Frame(self.carousel_frame)
        self.image_frame.pack(side=tk.LEFT, padx=20)
        
        self.image_label = tk.Label(self.image_frame, bg="white", relief="raised", bd=2)
        self.image_label.pack()
        
        self.name_label = tk.Label(self.image_frame, font=("Arial", 14, "bold"), 
                                  fg="#2E86AB", pady=5)
        self.name_label.pack()
        
        self.btn_next = tk.Button(self.carousel_frame, text="►", font=("Arial", 16), 
                                 command=self.next_suspect, bg="#f0f0f0")
        self.btn_next.pack(side=tk.LEFT, padx=10)
        
        self.load_images()
        self.update_display()
    
    def load_images(self):
        self.images = {}
        avatar_path = "avatar"
        
        for suspect in self.suspects:
            image_file = f"{suspect}.jpg"
            image_path = os.path.join(avatar_path, image_file)
            
            try:
                img = Image.open(image_path)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                self.images[suspect] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Erreur lors du chargement de {image_path}: {e}")
                default_img = Image.new('RGB', (150, 150), color='lightgray')
                self.images[suspect] = ImageTk.PhotoImage(default_img)
    
    def update_display(self):
        current_suspect = self.suspects[self.current_index]
        
        self.image_label.config(image=self.images[current_suspect])
        
        self.name_label.config(text=current_suspect)
    
    def previous_suspect(self):
        self.current_index = (self.current_index - 1) % len(self.suspects)
        self.update_display()
    
    def next_suspect(self):
        self.current_index = (self.current_index + 1) % len(self.suspects)
        self.update_display()
    
    def get_current_suspect(self):
        return self.suspects[self.current_index].lower()

def get_evidence(suspect, crime):
    evidence = []
    
    query_motive = f"has_motive({suspect}, {crime})"
    if list(prolog.query(query_motive)):
        evidence.append(f"✓ Motif pour {crime}")
    
    query_scene = f"was_near_crime_scene({suspect}, {crime})"
    if list(prolog.query(query_scene)):
        evidence.append(f"✓ Présence sur la scène de crime")
    
    query_fingerprint = f"has_fingerprint_on_weapon({suspect}, {crime})"
    if list(prolog.query(query_fingerprint)):
        evidence.append(f"✓ Empreintes digitales sur l'arme")
    
    if crime == "assassinat":
        query_eyewitness = f"eyewitness_identification({suspect}, {crime})"
        if list(prolog.query(query_eyewitness)):
            evidence.append(f"✓ Identification par témoin oculaire")
    
    if crime == "escroquerie":
        query_bank = f"has_bank_transaction({suspect}, {crime})"
        if list(prolog.query(query_bank)):
            evidence.append(f"✓ Transactions bancaires suspectes")
    
    if crime == "escroquerie":
        query_identity = f"owns_fake_identity({suspect}, {crime})"
        if list(prolog.query(query_identity)):
            evidence.append(f"✓ Possession de fausse identité")
    
    if crime == "escroquerie":
        if list(prolog.query(f"has_bank_transaction({suspect}, {crime})")):
            query_complicity = f"""
                suspect(Other),
                Other \\= {suspect},
                has_motive(Other, {crime}),
                owns_fake_identity(Other, {crime})
            """
            if list(prolog.query(query_complicity)):
                evidence.append(f"✓ Complicité détectée (transactions + complice avec fausse identité)")
        
        if list(prolog.query(f"owns_fake_identity({suspect}, {crime})")):
            query_complicity2 = f"""
                suspect(Other),
                Other \\= {suspect},
                has_motive(Other, {crime}),
                has_bank_transaction(Other, {crime})
            """
            if list(prolog.query(query_complicity2)):
                evidence.append(f"✓ Complicité détectée (fausse identité + complice avec transactions)")
    
    return evidence

def verifier():
    suspect = carousel.get_current_suspect()
    crime = combo_crime.get().strip().lower()
    
    query = f"is_guilty({suspect}, {crime})"
    print("Requête :", query)

    result = list(prolog.query(query))
    
    evidence = get_evidence(suspect, crime)
    
    if result:
        message = f"{suspect.capitalize()} est COUPABLE de {crime}\n\n"
        message += "🔍 Preuves trouvées :\n"
        if evidence:
            message += "\n".join(evidence)
        else:
            message += "Aucune preuve spécifique trouvée"
        
        messagebox.showinfo("Résultat - COUPABLE", message)
    else:
        message = f"{suspect.capitalize()} n'est PAS COUPABLE de {crime}\n\n"
        message += "❌ Preuves manquantes :\n"
        
        missing_evidence = []
        
        if crime == "vol":
            if not list(prolog.query(f"has_motive({suspect}, {crime})")):
                missing_evidence.append("• Motif")
            if not list(prolog.query(f"was_near_crime_scene({suspect}, {crime})")):
                missing_evidence.append("• Présence sur la scène de crime")
            if not list(prolog.query(f"has_fingerprint_on_weapon({suspect}, {crime})")):
                missing_evidence.append("• Empreintes digitales sur l'arme")
        
        elif crime == "assassinat":
            if not list(prolog.query(f"has_motive({suspect}, {crime})")):
                missing_evidence.append("• Motif")
            if not list(prolog.query(f"was_near_crime_scene({suspect}, {crime})")):
                missing_evidence.append("• Présence sur la scène de crime")
            if not list(prolog.query(f"has_fingerprint_on_weapon({suspect}, {crime})")) and \
               not list(prolog.query(f"eyewitness_identification({suspect}, {crime})")):
                missing_evidence.append("• Empreintes sur l'arme OU témoin oculaire")
        
        elif crime == "escroquerie":
            if not list(prolog.query(f"has_motive({suspect}, {crime})")):
                missing_evidence.append("• Motif")
            if not list(prolog.query(f"has_bank_transaction({suspect}, {crime})")) and \
               not list(prolog.query(f"owns_fake_identity({suspect}, {crime})")):
                missing_evidence.append("• Transactions bancaires OU fausse identité")
        
        if missing_evidence:
            message += "\n".join(missing_evidence)
        else:
            message += "Toutes les preuves individuelles sont présentes mais la logique ne permet pas de conclure à la culpabilité"
        
        messagebox.showwarning("Résultat - NON COUPABLE", message)

root = tk.Tk()
root.title("Détective IA - Prolog")
root.geometry("600x600")  
root.resizable(True, True)
root.configure(bg="#f5f5f5")

title_label = tk.Label(root, text="🕵️ Détective IA - Système d'enquête", 
                      font=("Arial", 18, "bold"), fg="#1B4332", bg="#f5f5f5")
title_label.pack(pady=20)

tk.Label(root, text="Sélectionnez un suspect :", font=("Arial", 14, "bold"), 
         fg="#2E86AB", bg="#f5f5f5").pack(pady=(10, 5))

carousel = SuspectCarousel(root)

tk.Label(root, text="Type de crime :", font=("Arial", 14, "bold"), 
         fg="#2E86AB", bg="#f5f5f5").pack(pady=(30, 10))

combo_crime = ttk.Combobox(root, values=["vol", "assassinat", "escroquerie"], 
                          state="readonly", font=("Arial", 12), width=20)
combo_crime.pack(pady=5)
combo_crime.current(0)

style = ttk.Style()
style.configure("Custom.TButton", font=("Arial", 12, "bold"))

verify_btn = tk.Button(root, text="🔍 Vérifier la culpabilité", command=verifier, 
                      font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", 
                      padx=30, pady=15, relief="raised", bd=3)
verify_btn.pack(pady=40)

root.mainloop()
