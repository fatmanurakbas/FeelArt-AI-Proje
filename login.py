import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import subprocess  # Yeni pencere açmak için

def center_window(window, width=250, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = 100
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")
    
def login():
    root.destroy()  # Bu pencereyi kapat
    subprocess.run(["python", r"loginpanel.py"])  # Yeni pencere aç

def signup():
    root.destroy()  # Bu pencereyi kapat
    subprocess.run(["python", r"KayitOl.py"])  # Yeni pencere a9ç

def open_link(url):
    webbrowser.open_new(url)

root = tk.Tk()
root.title("Feel Art")
root.geometry("250x500")
root.configure(bg="#fffbe9")  # Arka plan rengi

# Başlık
title1 = tk.Label(root, text="feel", font=("Brush Script MT", 28), fg="#b4462b", bg="#fffbe9")
title1.pack(pady=(40, 0))

title2 = tk.Label(root, text="art", font=("Brush Script MT", 24), fg="#b4462b", bg="#fffbe9")
title2.pack(pady=(0, 20))

# Login Button
login_btn = tk.Button(root, text="Giriş", command=login, font=("Arial", 10), bg="#eba94d", fg="black", bd=1, relief="ridge", width=20)
login_btn.pack(pady=10)

# Signup Button
signup_btn = tk.Button(root, text="Kayıt Ol", command=signup, font=("Arial", 10), bg="#f5e2a9", fg="black", bd=1, relief="ridge", width=20)
signup_btn.pack(pady=10)

# Sosyal medya ikonları
frame = tk.Frame(root, bg="#fffbe9")
frame.pack(pady=30)

icons = {
    "instagram": ("https://www.instagram.com", "📷"),
    "twitter": ("https://www.twitter.com", "🐦"),
    "linkedin": ("https://www.linkedin.com/in/fatmanurakbas16/", "💼")
}

for name, (url, symbol) in icons.items():
    btn = tk.Button(frame, text=symbol, font=("Arial", 12), width=4, command=lambda u=url: open_link(u))
    btn.pack(side="left", padx=10)

root.mainloop()
