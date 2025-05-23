import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io
import uuid

class GalleryScreen(tk.Frame):
    def __init__(self, master, controller, emotion_text="mutlu"):
        super().__init__(master, bg="#fffbe9")
        self.controller = controller
        self.emotion = emotion_text
        self.images = []
        self.saved_images = []
        self.liked_images = []
        self.create_scrollable_widgets()
        self.fetch_images()

    def create_scrollable_widgets(self):
        # Üst kısım (başlık ve geri tuşu)
        top_frame = tk.Frame(self, bg="#fffbe9")
        top_frame.pack(fill="x", pady=5)

        back_btn = tk.Button(top_frame, text="←", bg="#fffbe9", fg="#b4462b", font=("Arial", 10, "bold"), bd=0,
                             command=lambda: self.controller.show_frame("MainScreen"))
        back_btn.pack(side="left", padx=10)

        title = tk.Label(
            top_frame, text=f"'{self.emotion}' için sanat önerileri",
            font=("Arial", 12, "bold"), bg="#fffbe9", fg="#b4462b", wraplength=250, justify="center"
        )
        title.pack(side="left", expand=True)

        # Canvas + scrollbar + iç frame
        self.canvas = tk.Canvas(self, bg="#fffbe9", highlightthickness=0)
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas, bg="#fffbe9")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # İçeriği canvas'a göre genişlet
        def on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind("<Configure>", on_canvas_configure)

        # Scroll bölgesini güncelle
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Mouse scroll desteği
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def fetch_images(self):
        try:
            response = requests.get(
                "http://127.0.0.1:8000/api/images",
                 params={"query": self.emotion, "seed": str(uuid.uuid4())}
            )
            if response.status_code == 200:
                data = response.json()
                image_urls = data.get('images', [])

                for url in image_urls:
                    self.display_image(url)
            else:
                messagebox.showerror("Hata", "Görseller alınamadı.")
        except Exception as e:
            messagebox.showerror("Bağlantı Hatası", str(e))

    def display_image(self, url):
        try:
            img_data = requests.get(url).content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((300, 180))
            photo = ImageTk.PhotoImage(img)
            self.images.append(photo)

            container = tk.Frame(self.inner_frame, bg="#fffbe9")
            container.pack(pady=10)

            img_label = tk.Label(container, image=photo, bg="#fffbe9")
            img_label.image = photo
            img_label.pack()

            btn_frame = tk.Frame(container, bg="#fffbe9")
            btn_frame.pack(pady=2)

            like_btn = tk.Button(
                btn_frame, text="❤️", bg="#fffbe9", fg="#e0554a", font=("Arial", 10), bd=0,
                command=lambda u=url: self.like_image(u)
            )
            like_btn.pack(side="left", padx=5)

            save_btn = tk.Button(
                btn_frame, text="🔖", bg="#fffbe9", fg="#b4462b", font=("Arial", 9, "bold"), bd=0,
                command=lambda u=url: self.save_image(u)
            )
            save_btn.pack(side="left", padx=5)

        except Exception as e:
            tk.Label(self.inner_frame, text=f"Hata: {e}", bg="#fffbe9", fg="red").pack()

    def save_image(self, url):
        if url not in self.saved_images:
            self.saved_images.append(url)
            messagebox.showinfo("Kaydedildi", "Görsel kaydedildi.")
        else:
            messagebox.showwarning("Zaten kaydedilmiş", "Bu görsel zaten kaydedilmiş.")

        if hasattr(self.controller.frames["BookmarksScreen"], "update_saved_images"):
            self.controller.frames["BookmarksScreen"].update_saved_images(self.saved_images)

    def like_image(self, url):
        if url not in self.liked_images:
            self.liked_images.append(url)
            messagebox.showinfo("Beğenildi", "Görsel beğenildi.")
        else:
            messagebox.showwarning("Zaten beğenilmiş", "Bu görsel zaten beğenilmiş.")

        if hasattr(self.controller.frames["LikesScreen"], "update_liked_images"):
            self.controller.frames["LikesScreen"].update_liked_images(self.liked_images)
