import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys

def center_window(window, width=320, height=580):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = 100
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def go_back():
    geometry = root.geometry()
    root.destroy()
    subprocess.run([sys.executable, "anasayfa.py", geometry])

def on_image_click(index):
    messagebox.showinfo("Detay", f"{index+1}. görsel seçildi.")

# Ana pencere
root = tk.Tk()
center_window(root)
root.title("Sanat Galerisi")
root.configure(bg="#fffbe9")

text_color = "#b4462b"
accent_color = "#f0d58c"
icon_color = "#e39f3c"

# Üst bar
top_frame = tk.Frame(root, bg="#fffbe9")
top_frame.pack(fill="x", padx=10, pady=(5, 10))

back_btn = tk.Label(top_frame, text="←", font=("Arial", 12), bg="#fffbe9", fg=text_color, cursor="hand2")
back_btn.pack(side="left")
back_btn.bind("<Button-1>", lambda e: go_back())

# Arama kutusu
search_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
search_frame.pack(padx=10, fill="x")

search_entry = tk.Entry(search_frame, font=("Arial", 10), relief="flat", bg="white")
search_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=4)

search_icon = tk.Label(search_frame, text="🔍", font=("Arial", 10), bg="white")
search_icon.pack(side="right", padx=5)

# Galeri alanı (scrollable canvas)
canvas = tk.Canvas(root, bg="#fffbe9", highlightthickness=0)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas, bg="#fffbe9")

scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# Görsellerin listesi (örnek – backend ile güncellenecek)
dummy_images = [
    "images/art1.jpg", "images/art2.jpg", "images/art3.jpg",
    "images/art4.jpg", "images/art5.jpg", "images/art6.jpg",
    "images/art7.jpg", "images/art8.jpg", "images/art9.jpg"
]

# Galeriyi oluştur
columns = 3
image_size = (80, 100)
for i, img_path in enumerate(dummy_images):
    frame = tk.Frame(scroll_frame, bg="white", bd=1, relief="flat")
    frame.grid(row=i // columns, column=i % columns, padx=6, pady=6)

    try:
        img = Image.open(img_path)
        img = img.resize(image_size)
        img_tk = ImageTk.PhotoImage(img)
    except:
        img_tk = tk.PhotoImage(width=80, height=100)  # Yer tutucu

    img_label = tk.Label(frame, image=img_tk, cursor="hand2")
    img_label.image = img_tk  # referansı koru
    img_label.pack()
    img_label.bind("<Button-1>", lambda e, idx=i: on_image_click(idx))

    # Alt ikonlar
    icons = tk.Frame(frame, bg="white")
    icons.pack(pady=2)
    for symbol in ["♡", "🔖", "↗"]:
        tk.Label(icons, text=symbol, fg=icon_color, font=("Arial", 9), bg="white").pack(side="left", padx=3)

root.mainloop()
