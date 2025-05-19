import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Öneri listeleri
film_önerileri = [
    {
        "isim": "Stranger Things",
        "ülke": "USA, 2016 - Current",
        "puan": "8.6 / 10",
        "görsel": "https://upload.wikimedia.org/wikipedia/en/f/f7/Stranger_Things_season_4.jpg"
    },
    {
        "isim": "Inside Out",
        "ülke": "USA, 2015",
        "puan": "8.1 / 10",
        "görsel": "https://upload.wikimedia.org/wikipedia/en/0/0a/Inside_Out_%282015_film%29_poster.jpg"
    }
]

kitap_önerileri = [
    {
        "isim": "The Art of Happiness",
        "yazar": "Dalai Lama",
        "görsel": "https://m.media-amazon.com/images/I/41j9pWb6V2L.jpg"
    },
    {
        "isim": "Emotional Intelligence",
        "yazar": "Daniel Goleman",
        "görsel": "https://m.media-amazon.com/images/I/41GDikzI7PL.jpg"
    }
]

film_index = 0
kitap_index = 0
film_begeni = False
film_kayit = False
kitap_begeni = False
kitap_kayit = False

def center_window(window, width=320, height=620):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = 100
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

# ---- Film Fonksiyonları ----
def guncelle_film():
    global film_imgtk
    film = film_önerileri[film_index]
    try:
        response = requests.get(film["görsel"])
        img = Image.open(BytesIO(response.content)).resize((100, 140))
        film_imgtk = ImageTk.PhotoImage(img)
        film_label.config(image=film_imgtk)
    except:
        film_label.config(text="[Görsel Yok]", font=("Arial", 10), image="", width=12, height=8)

    film_ad_label.config(text=film["isim"])
    film_puan_label.config(text=f"IMDb: {film['puan']}")
    film_ülke_label.config(text=film["ülke"])
    film_begeni_btn.config(text="❤️" if film_begeni else "🤍")
    film_kayit_btn.config(text="🔖" if film_kayit else "📑")

def ileri_film():
    global film_index
    film_index = (film_index + 1) % len(film_önerileri)
    guncelle_film()

def geri_film():
    global film_index
    film_index = (film_index - 1) % len(film_önerileri)
    guncelle_film()

def toggle_film_begeni():
    global film_begeni
    film_begeni = not film_begeni
    film_begeni_btn.config(text="❤️" if film_begeni else "🤍")

def toggle_film_kayit():
    global film_kayit
    film_kayit = not film_kayit
    film_kayit_btn.config(text="🔖" if film_kayit else "📑")

# ---- Kitap Fonksiyonları ----
def guncelle_kitap():
    global kitap_imgtk
    kitap = kitap_önerileri[kitap_index]
    try:
        response = requests.get(kitap["görsel"])
        img = Image.open(BytesIO(response.content)).resize((100, 140))
        kitap_imgtk = ImageTk.PhotoImage(img)
        kitap_label.config(image=kitap_imgtk)
    except:
        kitap_label.config(text="[Görsel Yok]", font=("Arial", 10), image="", width=12, height=8)

    kitap_ad_label.config(text=kitap["isim"])
    kitap_yazar_label.config(text=kitap["yazar"])
    kitap_begeni_btn.config(text="❤️" if kitap_begeni else "🤍")
    kitap_kayit_btn.config(text="🔖" if kitap_kayit else "📑")

def ileri_kitap():
    global kitap_index
    kitap_index = (kitap_index + 1) % len(kitap_önerileri)
    guncelle_kitap()

def geri_kitap():
    global kitap_index
    kitap_index = (kitap_index - 1) % len(kitap_önerileri)
    guncelle_kitap()

def toggle_kitap_begeni():
    global kitap_begeni
    kitap_begeni = not kitap_begeni
    kitap_begeni_btn.config(text="❤️" if kitap_begeni else "🤍")

def toggle_kitap_kayit():
    global kitap_kayit
    kitap_kayit = not kitap_kayit
    kitap_kayit_btn.config(text="🔖" if kitap_kayit else "📑")

# ---- Arayüz Başlangıcı ----
root = tk.Tk()
center_window(root)
root.title("Duyguya Göre Öneriler")
root.configure(bg="#fffbe9")

# --- Film Serisi ---
film_baslik = tk.Label(root, text="film serisi", font=("Brush Script MT", 18), bg="#f0d58c", fg="#b4462b")
film_baslik.pack(fill="x", pady=(0, 5))

film_frame = tk.Frame(root, bg="#fffbe9")
film_frame.pack()

tk.Button(film_frame, text="‹", font=("Arial", 12), bg="#fffbe9", fg="#b4462b", bd=0, command=geri_film).pack(side="left", padx=5)

film_content = tk.Frame(film_frame, bg="#fffbe9")
film_content.pack(side="left", pady=10)

film_label = tk.Label(film_content, bg="#fffbe9")
film_label.pack()

film_puan_label = tk.Label(film_content, font=("Arial", 8), bg="#fffbe9", fg="black")
film_puan_label.pack()

film_ad_label = tk.Label(film_content, font=("Arial", 9, "bold"), bg="#fffbe9", fg="black")
film_ad_label.pack()

film_ülke_label = tk.Label(film_content, font=("Arial", 8), bg="#fffbe9", fg="gray")
film_ülke_label.pack()

film_button_frame = tk.Frame(film_content, bg="#fffbe9")
film_button_frame.pack(pady=4)

film_begeni_btn = tk.Button(film_button_frame, text="🤍", font=("Arial", 10), bg="#fffbe9", fg="red", bd=0, command=toggle_film_begeni)
film_begeni_btn.pack(side="left", padx=5)

film_kayit_btn = tk.Button(film_button_frame, text="📑", font=("Arial", 10), bg="#fffbe9", fg="orange", bd=0, command=toggle_film_kayit)
film_kayit_btn.pack(side="left", padx=5)

tk.Button(film_frame, text="›", font=("Arial", 12), bg="#fffbe9", fg="#b4462b", bd=0, command=ileri_film).pack(side="left", padx=5)

# --- Kitap Serisi ---
kitap_baslik = tk.Label(root, text="kitap serisi", font=("Brush Script MT", 18), bg="#f0d58c", fg="#b4462b")
kitap_baslik.pack(fill="x", pady=(15, 5))

kitap_frame = tk.Frame(root, bg="#fffbe9")
kitap_frame.pack()

tk.Button(kitap_frame, text="‹", font=("Arial", 12), bg="#fffbe9", fg="#b4462b", bd=0, command=geri_kitap).pack(side="left", padx=5)

kitap_content = tk.Frame(kitap_frame, bg="#fffbe9")
kitap_content.pack(side="left", pady=10)

kitap_label = tk.Label(kitap_content, bg="#fffbe9")
kitap_label.pack()

kitap_ad_label = tk.Label(kitap_content, font=("Arial", 9, "bold"), bg="#fffbe9", fg="black")
kitap_ad_label.pack()

kitap_yazar_label = tk.Label(kitap_content, font=("Arial", 8), bg="#fffbe9", fg="gray")
kitap_yazar_label.pack()

kitap_button_frame = tk.Frame(kitap_content, bg="#fffbe9")
kitap_button_frame.pack(pady=4)

kitap_begeni_btn = tk.Button(kitap_button_frame, text="🤍", font=("Arial", 10), bg="#fffbe9", fg="red", bd=0, command=toggle_kitap_begeni)
kitap_begeni_btn.pack(side="left", padx=5)

kitap_kayit_btn = tk.Button(kitap_button_frame, text="📑", font=("Arial", 10), bg="#fffbe9", fg="orange", bd=0, command=toggle_kitap_kayit)
kitap_kayit_btn.pack(side="left", padx=5)

tk.Button(kitap_frame, text="›", font=("Arial", 12), bg="#fffbe9", fg="#b4462b", bd=0, command=ileri_kitap).pack(side="left", padx=5)

# Başlat
guncelle_film()
guncelle_kitap()
root.mainloop()
