import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

class OneriPaneliScreen(tk.Frame):
    def __init__(self, master, controller, emotion):
        super().__init__(master, bg="#fffbe9")
        self.controller = controller
        self.emotion = emotion
        self.film_index = 0
        self.kitap_index = 0
        self.filmler = []
        self.kitaplar = self.get_kitaplar()
        self.film_imgtk = None
        self.kitap_imgtk = None

        self.build_ui()
        self.load_filmler()

    def build_ui(self):
                # ==== Üst Başlık ve Geri Butonu ====
        top_frame = tk.Frame(self, bg="#fffbe9")
        top_frame.pack(fill="x", pady=(10, 5), padx=10)

        back_btn = tk.Label(top_frame, text="← Geri", font=("Arial", 10, "bold"), fg="#b4462b",
                            bg="#fffbe9", cursor="hand2")
        back_btn.pack(side="left")
        back_btn.bind("<Button-1>", lambda e: self.controller.show_frame("MainScreen"))
        
        tk.Label(self, text="Film Serisi", font=("Brush Script MT", 18), bg="#f0d58c", fg="#b4462b").pack(fill="x", pady=(10, 5))

        self.film_frame = tk.Frame(self, bg="#fffbe9")
        self.film_frame.pack()

        tk.Button(self.film_frame, text="‹", font=("Arial", 12), bg="#fffbe9", fg="#b4462b", bd=0,
                  command=self.geri_film).pack(side="left", padx=5)

        self.film_content = tk.Frame(self.film_frame, bg="#fffbe9")
        self.film_content.pack(side="left", pady=10)

        self.film_label = tk.Label(self.film_content, bg="#fffbe9")
        self.film_label.pack()

        self.film_puan_label = tk.Label(self.film_content, font=("Arial", 8), bg="#fffbe9", fg="black")
        self.film_puan_label.pack()

        self.film_ad_label = tk.Label(self.film_content, font=("Arial", 9, "bold"), bg="#fffbe9", fg="black")
        self.film_ad_label.pack()

        self.film_button_frame = tk.Frame(self.film_content, bg="#fffbe9")
        self.film_button_frame.pack(pady=4)

        tk.Button(self.film_frame, text="›", font=("Arial", 12), bg="#fffbe9", fg="#b4462b", bd=0,
                  command=self.ileri_film).pack(side="left", padx=5)

        # Kitap Serisi
        tk.Label(self, text="Kitap Serisi", font=("Brush Script MT", 18), bg="#f0d58c", fg="#b4462b").pack(fill="x", pady=(15, 5))

        self.kitap_frame = tk.Frame(self, bg="#fffbe9")
        self.kitap_frame.pack()

        tk.Button(self.kitap_frame, text="‹", font=("Arial", 12), bg="#fffbe9", fg="#b4462b", bd=0,
                  command=self.geri_kitap).pack(side="left", padx=5)

        self.kitap_content = tk.Frame(self.kitap_frame, bg="#fffbe9")
        self.kitap_content.pack(side="left", pady=10)

        self.kitap_label = tk.Label(self.kitap_content, bg="#fffbe9")
        self.kitap_label.pack()

        self.kitap_ad_label = tk.Label(self.kitap_content, font=("Arial", 9, "bold"), bg="#fffbe9", fg="black")
        self.kitap_ad_label.pack()

        self.kitap_yazar_label = tk.Label(self.kitap_content, font=("Arial", 8), bg="#fffbe9", fg="gray")
        self.kitap_yazar_label.pack()

        tk.Button(self.kitap_frame, text="›", font=("Arial", 12), bg="#fffbe9", fg="#b4462b", bd=0,
                  command=self.ileri_kitap).pack(side="left", padx=5)

    def get_kitaplar(self):
        return [
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

    def load_filmler(self):
        try:
            response = requests.get("http://127.0.0.1:8000/api/recommendations", params={"emotion": self.emotion})
            response.raise_for_status()
            data = response.json()
            self.filmler = data.get("recommendations", [])
            self.guncelle_film()
        except Exception as e:
            messagebox.showerror("Hata", f"Film önerileri alınamadı: {e}")
            self.filmler = []

    def guncelle_film(self):
        if not self.filmler:
            self.film_ad_label.config(text="Film bulunamadı.")
            self.film_puan_label.config(text="")
            self.film_label.config(image="", text="[Görsel Yok]")
            return

        film = self.filmler[self.film_index]
        try:
            response = requests.get(film["poster"])
            img = Image.open(BytesIO(response.content)).resize((100, 140))
            self.film_imgtk = ImageTk.PhotoImage(img)
            self.film_label.config(image=self.film_imgtk)
        except:
            self.film_label.config(text="[Görsel Yok]", font=("Arial", 10), image="", width=12, height=8)

        self.film_ad_label.config(text=film["title"])
        self.film_puan_label.config(text=film.get("overview", "")[:100])

    def ileri_film(self):
        if self.filmler:
            self.film_index = (self.film_index + 1) % len(self.filmler)
            self.guncelle_film()

    def geri_film(self):
        if self.filmler:
            self.film_index = (self.film_index - 1) % len(self.filmler)
            self.guncelle_film()

    def guncelle_kitap(self):
        kitap = self.kitaplar[self.kitap_index]
        try:
            response = requests.get(kitap["görsel"])
            img = Image.open(BytesIO(response.content)).resize((100, 140))
            self.kitap_imgtk = ImageTk.PhotoImage(img)
            self.kitap_label.config(image=self.kitap_imgtk)
        except:
            self.kitap_label.config(text="[Görsel Yok]", font=("Arial", 10), image="", width=12, height=8)

        self.kitap_ad_label.config(text=kitap["isim"])
        self.kitap_yazar_label.config(text=kitap["yazar"])

    def ileri_kitap(self):
        self.kitap_index = (self.kitap_index + 1) % len(self.kitaplar)
        self.guncelle_kitap()

    def geri_kitap(self):
        self.kitap_index = (self.kitap_index - 1) % len(self.kitaplar)
        self.guncelle_kitap()

    def place(self, **kwargs):
        super().place(**kwargs)
        self.guncelle_kitap()
