import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Örnek beğenilen içerikler
begenilen_filmler = [
    {
        "isim": "Stranger Things",
        "ülke": "USA, 2016 - Current",
        "görsel": "https://upload.wikimedia.org/wikipedia/en/f/f7/Stranger_Things_season_4.jpg"
    }
]

begenilen_kitaplar = [
    {
        "isim": "The Art of Happiness",
        "yazar": "Dalai Lama",
        "görsel": "https://m.media-amazon.com/images/I/41j9pWb6V2L.jpg"
    }
]

begenilen_sanat = [
    {
        "isim": "Fire & Flow",
        "tarz": "Soyut - Kırmızı tonlar",
        "görsel": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Red_flames_abstract.jpg/800px-Red_flames_abstract.jpg"
    }
]

def back_to_login():
    print("Login paneline geri dönülüyor.")
    root.destroy()
    import subprocess
    subprocess.run(["python", r"anasayfa.py",])

def center_window(window, width=320, height=650):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = 100
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def load_image_from_url(url, size=(60, 90)):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).resize(size)
        return ImageTk.PhotoImage(img)
    except:
        return None

# Arayüz
root = tk.Tk()
center_window(root)
root.title("Beğeniler")
root.configure(bg="#fffbe9")

title = tk.Label(root, text="begenilenler", font=("Brush Script MT", 22), bg="#f0d58c", fg="#b4462b")
title.pack(fill="x", pady=(0, 10))

# Geri Dön Butonu
back_btn = tk.Button(root, text="←", font=("Arial", 12), bg="#fffbe9", fg="#943126", bd=0, command=back_to_login)
back_btn.pack(anchor="w", padx=10, pady=5)

# --- Beğenilen Filmler ---
film_baslik = tk.Label(root, text="🎬 filmler", font=("Arial", 10, "bold"), bg="#fffbe9", fg="#b4462b", anchor="w")
film_baslik.pack(fill="x", padx=10)

for film in begenilen_filmler:
    frame = tk.Frame(root, bg="#fffbe9", pady=5)
    frame.pack(fill="x", padx=10)
    image = load_image_from_url(film["görsel"])
    tk.Label(frame, image=image, bg="#fffbe9").pack(side="left")
    tk.Label(frame, text=f"{film['isim']}\n{film['ülke']}", font=("Arial", 9), justify="left", bg="#fffbe9").pack(side="left", padx=10)
    frame.image = image

# --- Beğenilen Kitaplar ---
kitap_baslik = tk.Label(root, text="📚 kitaplar", font=("Arial", 10, "bold"), bg="#fffbe9", fg="#b4462b", anchor="w")
kitap_baslik.pack(fill="x", padx=10, pady=(10, 0))

for kitap in begenilen_kitaplar:
    frame = tk.Frame(root, bg="#fffbe9", pady=5)
    frame.pack(fill="x", padx=10)
    image = load_image_from_url(kitap["görsel"])
    tk.Label(frame, image=image, bg="#fffbe9").pack(side="left")
    tk.Label(frame, text=f"{kitap['isim']}\n{kitap['yazar']}", font=("Arial", 9), justify="left", bg="#fffbe9").pack(side="left", padx=10)
    frame.image = image

# --- Beğenilen Sanat Eserleri ---
sanat_baslik = tk.Label(root, text="🎨 sanat galerisi", font=("Arial", 10, "bold"), bg="#fffbe9", fg="#b4462b", anchor="w")
sanat_baslik.pack(fill="x", padx=10, pady=(10, 0))

for eser in begenilen_sanat:
    frame = tk.Frame(root, bg="#fffbe9", pady=5)
    frame.pack(fill="x", padx=10)
    image = load_image_from_url(eser["görsel"])
    tk.Label(frame, image=image, bg="#fffbe9").pack(side="left")
    tk.Label(frame, text=f"{eser['isim']}\n{eser['tarz']}", font=("Arial", 9), justify="left", bg="#fffbe9").pack(side="left", padx=10)
    frame.image = image

root.mainloop()
