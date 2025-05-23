import tkinter as tk
from PIL import Image, ImageTk
import requests
import io

class BookmarksScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#fffbe9")
        self.controller = controller
        self.saved_images = []
        self.images = []
        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self, bg="#fffbe9")
        top_frame.pack(fill="x")

        back_btn = tk.Button(top_frame, text="←", bg="#fffbe9", fg="#b4462b", font=("Arial", 12), bd=0,
                             command=lambda: self.controller.show_frame("MainScreen"))
        back_btn.pack(side="left", padx=10, pady=5)

        title = tk.Label(top_frame, text="Kaydedilen Görseller", font=("Arial", 14, "bold"), bg="#fffbe9", fg="#b4462b")
        title.pack(side="left", pady=10)

        self.canvas = tk.Canvas(self, bg="#fffbe9", highlightthickness=0)
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas, bg="#fffbe9")

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def update_saved_images(self, image_urls):
        self.saved_images = image_urls
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.images = []
        for url in self.saved_images:
            try:
                img_data = requests.get(url).content
                img = Image.open(io.BytesIO(img_data))
                img = img.resize((280, 160))
                photo = ImageTk.PhotoImage(img)
                self.images.append(photo)

                container = tk.Frame(self.frame, bg="#fffbe9")
                container.pack(pady=10)

                lbl = tk.Label(container, image=photo, bg="#fffbe9")
                lbl.image = photo
                lbl.pack()

                remove_btn = tk.Button(container, text="Kayıtı İptal Et", bg="#fffbe9", fg="red", font=("Arial", 9), bd=0,
                                       command=lambda u=url: self.remove_saved_image(u))
                remove_btn.pack(pady=2)

            except Exception as e:
                tk.Label(self.frame, text=f"Hata: {e}", bg="#fffbe9", fg="red").pack()

    def remove_saved_image(self, url):
        if url in self.saved_images:
            self.saved_images.remove(url)
            self.update_saved_images(self.saved_images)
