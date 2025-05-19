import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import io
import json



def center_window(window, width=280, height=580):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = 100
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

# Sidebar durumu için global değişken
sidebar_open = False

# Buton işlevleri
def open_profile():
    geometry = root.geometry()
    root.destroy()
    subprocess.run(["python", "profil.py", geometry])

def open_bookmarks():
    geometry = root.geometry()
    root.destroy()
    subprocess.run(["python", "kaydedilenler.py", geometry])

def open_likes():
    geometry = root.geometry()
    root.destroy()
    subprocess.run(["python", "begeniler.py", geometry])

def search_action():
    keyword = search_entry.get()
    messagebox.showinfo("Arama", f"'{keyword}' ile arama yapılıyor...")

def add_action():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if file_path:
        try:
            with open(file_path, "rb") as f:
                files = {"image": f}
                response = requests.post("http://127.0.0.1:5000/analyze", files=files)
                if response.status_code == 200:
                    data = response.json()
                    emotion = data.get("emotion", "Duygu algılanamadı")
                    all_emotions = data.get("emotions", {})
                    formatted_emotions = "\n".join([f"{k}: {round(v, 2)}%" for k, v in all_emotions.items()])
                    messagebox.showinfo("Duygu Analizi", f"Algılanan duygu: {emotion}\n\nTüm oranlar:\n{formatted_emotions}")
                else:
                    messagebox.showerror("Hata", f"Sunucu hatası: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Hata", f"Görsel gönderilemedi: {e}")



def toggle_sidebar():
    global sidebar_open
    if sidebar_open:
        sidebar_frame.place_forget()
        main_frame.place(x=0, y=0)  # Ana içerik eski yerine döner
        sidebar_open = False
    else:
        sidebar_frame.place(x=0, y=0, relheight=1)
        main_frame.place(x=150, y=0)  # Ana içerik sağa kayar
        sidebar_open = True

# Ana pencere
root = tk.Tk()
center_window(root)
root.title("Feel Art Ana Sayfa")
root.configure(bg="#fffbe9")

# Renkler
bg_color = "#fffbe9"
accent_color = "#f0d58c"
text_color = "#b4462b"
sidebar_bg = "#f5e2a9"

# --- SIDEBAR (başlangıçta gizli) ---
sidebar_frame = tk.Frame(root, width=150, bg=sidebar_bg, height=580)

sidebar_title = tk.Label(sidebar_frame, text="Sohbet Geçmişim", bg=sidebar_bg, fg=text_color, font=("Arial", 10, "bold"))
sidebar_title.pack(pady=10)

history_items = ["• Günlük 1", "• Duygu Günlüğü", "• Renk Terapisi", "• Anksiyete Kaydı", "• Geri Bildirim"]

for item in history_items:
    lbl = tk.Label(sidebar_frame, text=item, bg=sidebar_bg, fg="black", font=("Arial", 9), anchor="w", justify="left")
    lbl.pack(fill="x", padx=15, pady=3)

# Ana içerik çerçevesi (main_frame)
main_frame = tk.Frame(root, bg=bg_color)
main_frame.place(x=0, y=0, relwidth=1, relheight=1)

# Üst bar
top_bar = tk.Frame(main_frame, bg=bg_color)
top_bar.pack(fill="x", pady=10, padx=10)

menu_btn = tk.Label(top_bar, text="≡", font=("Arial", 14), bg=bg_color, fg=text_color, cursor="hand2")
menu_btn.pack(side="left")
menu_btn.bind("<Button-1>", lambda e: toggle_sidebar())

profile_btn = tk.Label(top_bar, text="👤", font=("Arial", 12), bg=bg_color, fg=text_color, cursor="hand2")
profile_btn.pack(side="right")
profile_btn.bind("<Button-1>", lambda e: open_profile())

# Orta başlık
title1 = tk.Label(main_frame, text="feel", font=("Brush Script MT", 28), fg=text_color, bg=bg_color)
title1.pack(pady=(50, 0))

title2 = tk.Label(main_frame, text="art", font=("Brush Script MT", 24), fg=text_color, bg=bg_color)
title2.pack(pady=(0, 20))

# Arama alanı
preview_frame = tk.Frame(main_frame, bg=bg_color)
preview_frame.pack(pady=10)

search_frame = tk.Frame(main_frame, bg=accent_color, bd=0, relief="ridge")
search_frame.pack(pady=20, padx=20, fill="x")

search_icon = tk.Label(search_frame, text="🔍", bg=accent_color, font=("Arial", 10))
search_icon.pack(side="left", padx=10)

search_entry = tk.Entry(search_frame, font=("Arial", 10), relief="flat", bg=accent_color)
search_entry.pack(side="left", fill="x", expand=True)

add_btn = tk.Button(search_frame, text="+", font=("Arial", 10), bg=accent_color, fg=text_color, bd=0, command=add_action)
add_btn.pack(side="right", padx=10)

# Alt bar
bottom_bar = tk.Frame(main_frame, bg=bg_color)
bottom_bar.pack(side="bottom", fill="x", pady=15)

bookmark_btn = tk.Label(bottom_bar, text="🔖", font=("Arial", 14), bg=bg_color, fg=accent_color, cursor="hand2")
bookmark_btn.pack(side="left", padx=20)
bookmark_btn.bind("<Button-1>", lambda e: open_bookmarks())

like_btn = tk.Label(bottom_bar, text="❤", font=("Arial", 14), bg=bg_color, fg=accent_color, cursor="hand2")
like_btn.pack(side="left", padx=20)
like_btn.bind("<Button-1>", lambda e: open_likes())

root.mainloop()
