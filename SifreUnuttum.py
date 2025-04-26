import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# Pencereyi ekranın sol-orta konumuna yerleştir
def center_window(window, width=250, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = 100
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def send_reset_link():
    email = entry_email.get()
    if email:
        messagebox.showinfo("Şifre Sıfırlama", f"{email} adresine şifre sıfırlama bağlantısı gönderildi!")
    else:
        messagebox.showwarning("Eksik Bilgi", "Lütfen e-posta adresinizi girin.")

def back_to_login():
    geometry = root.geometry()
    root.destroy()
    subprocess.run(["python", r"loginpanel.py", geometry])

# Ana pencere
root = tk.Tk()
root.title("Şifremi Unuttum")
root.configure(bg="#fffbe9")

# Konumlandırma (gönderilmiş argüman varsa kullan, yoksa ortala)
if len(sys.argv) > 1:
    root.geometry(sys.argv[1])
else:
    center_window(root)

# Renk paleti
text_color = "#b4462b"
entry_bg = "#eba94d"
btn_bg1 = "#f5e2a9"
btn_text = "black"

# Geri Dön Butonu
back_btn = tk.Button(root, text="←", font=("Arial", 12), bg="#fffbe9", fg=text_color, bd=0, command=back_to_login)
back_btn.pack(anchor="w", padx=10, pady=5)

# Başlık
title = tk.Label(root, text="Şifreni mi unuttun?", font=("Arial", 14, "bold"), fg=text_color, bg="#fffbe9")
title.pack(pady=(30, 10))

info = tk.Label(root, text="E-posta adresini gir,\nşifre sıfırlama bağlantısı gönderilsin.", font=("Arial", 9), fg="gray", bg="#fffbe9")
info.pack(pady=(0, 20))

# E-posta alanı
entry_email = tk.Entry(root, bg=entry_bg, relief="flat", font=("Arial", 10), width=28)
entry_email.pack(pady=(0, 20), ipady=5)

# Gönder butonu
send_btn = tk.Button(root, text="Bağlantıyı Gönder", font=("Arial", 10, "bold"), bg=btn_bg1, fg=btn_text, bd=1, relief="ridge", width=20, command=send_reset_link)
send_btn.pack()

root.mainloop()
