import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def center_window(window, width=250, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = 100
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")
def login_action():
    messagebox.showinfo("Giriş", "Giriş yapılıyor...")

def back_to_login():
    print("Login paneline geri dönülüyor.")
    root.destroy()
    import subprocess
    subprocess.run(["python", r"login.py",])

def open_forgot_password():
    geometry = root.geometry()
    root.destroy()
    subprocess.run(["python", r"SifreUnuttum.py", geometry])



def open_signup():
    geometry = root.geometry()
    root.destroy()
    subprocess.run(["python", r"KayitOl.py"])  # Yeni pencere aç

# Ana pencere
root = tk.Tk()
root.title("Feel Art - Login")
root.geometry("250x500")
root.configure(bg="#fffbe9")

# Geri Dön Butonu
back_btn = tk.Button(root, text="←", font=("Arial", 12), bg="#fffbe9", fg="#943126", bd=0, command=back_to_login)
back_btn.pack(anchor="w", padx=10, pady=5)

# Renk paleti
text_color = "#b4462b"
entry_bg = "#eba94d"
btn_bg1 = "#f5e2a9"
btn_text = "black"

# Başlık
welcome = tk.Label(root, text="Hoşgeldiniz!", font=("Arial", 14, "bold"), fg=text_color, bg="#fffbe9")
welcome.pack(pady=(30, 20))

# Form alanları
def form_field(label_text):
    label = tk.Label(root, text=label_text, font=("Arial", 9, "bold"), fg=text_color, bg="#fffbe9")
    label.pack(anchor="w", padx=20)
    entry = tk.Entry(root, bg=entry_bg, relief="flat", font=("Arial", 10), width=28)
    entry.pack(pady=(0, 10), ipady=5)
    return entry

entry_email = form_field("E-mail")
entry_password = form_field("Şifre")

# Forgot password
forgot = tk.Label(root, text="Şifremi Unuttum!", font=("Arial", 8, "italic"), fg="gray", bg="#fffbe9", cursor="hand2")
forgot.pack(anchor="e", padx=20, pady=(0, 20))
forgot.bind("<Button-1>", lambda e: open_forgot_password())

# Giriş Butonu
login_btn = tk.Button(root, text="Giriş", command=login_action, font=("Arial", 10, "bold"), bg=btn_bg1, fg=btn_text, bd=1, relief="ridge", width=15)
login_btn.pack(pady=5)

# Kayıt yönlendirmesi
bottom_text = tk.Label(root, text="Hesabınız yok mu?", font=("Arial", 9, "italic"), fg=text_color, bg="#fffbe9")
bottom_text.pack(pady=(20, 5))

signup_btn = tk.Button(root, text="Kayıt Ol", command=open_signup, font=("Arial", 10, "bold"), bg=btn_bg1, fg=btn_text, bd=1, relief="ridge", width=15)
signup_btn.pack()

root.mainloop()
