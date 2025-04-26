# KayitOl.py
import tkinter as tk
from tkinter import messagebox
import sys

print("Kayıt paneli başlatılıyor...")

def center_window(window, width=250, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = 100
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def submit_signup():
    print("Kayıt gönderildi.")
    messagebox.showinfo("Kayıt Olundu", "Kayıt işlemi tamamlandı!")

def back_to_login():
    print("Login paneline geri dönülüyor.")
    root.destroy()
    import subprocess
    subprocess.run(["python", r"login.py"])

root = tk.Tk()

# Eğer bir konum parametresi varsa onu uygula
if len(sys.argv) > 1:
    root.geometry(sys.argv[1])
else:
    root.geometry("250x500")
    
root.title("Kayıt Ol")
root.geometry("250x500")
root.configure(bg="#fffbe9")

# Geri Dön Butonu
back_btn = tk.Button(root, text="←", font=("Arial", 12), bg="#fffbe9", fg="#943126", bd=0, command=back_to_login)
back_btn.pack(anchor="w", padx=10, pady=5)

# Başlık
title = tk.Label(root, text="Hesap Oluşturun!", font=("Arial", 14, "bold"), fg="#943126", bg="#fffbe9")
title.pack(pady=(20, 10))

# Form Alanları
def create_field(label_text):
    label = tk.Label(root, text=label_text, font=("Arial", 9, "bold"), fg="#943126", bg="#fffbe9")
    label.pack(pady=(10, 0))
    entry = tk.Entry(root, bg="#eba94d", relief="flat", font=("Arial", 10), width=28)
    entry.pack(ipady=5)
    return entry

entry_name = create_field("Kullanıcı Adı")
entry_email = create_field("Email")
entry_pass = create_field("Şifre")

# Signup Button
signup_button = tk.Button(root, text="Kayıt Ol", font=("Arial", 10), bg="#f5e2a9", fg="black", bd=1, relief="ridge", width=15, command=submit_signup)
signup_button.pack(pady=20)

root.mainloop()
