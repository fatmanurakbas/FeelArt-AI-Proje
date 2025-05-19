import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
from screens.gallery import GalleryScreen

class MainScreen(tk.Frame):  # ← Frame olarak tanımlandı
    def __init__(self, master, controller):
        super().__init__(master, bg="#fffbe9")
        self.controller = controller
        self.sidebar_open = False

        # Renkler
        bg_color = "#fffbe9"
        accent_color = "#f0d58c"
        text_color = "#b4462b"
        sidebar_bg = "#f5e2a9"

        # === Sidebar ===
        self.sidebar_frame = tk.Frame(self, width=130, bg=sidebar_bg, height=580)
        sidebar_title = tk.Label(self.sidebar_frame, text="Sohbet Geçmişi", bg=sidebar_bg, fg=text_color, font=("Arial", 10, "bold"))
        sidebar_title.pack(pady=10)

        history_items = ["• Günlük 1", "• Duygu Günlüğü", "• Renk Terapisi", "• Anksiyete Kaydı", "• Geri Bildirim"]
        for item in history_items:
            lbl = tk.Label(self.sidebar_frame, text=item, bg=sidebar_bg, fg="black", font=("Arial", 9), anchor="w")
            lbl.pack(fill="x", padx=15, pady=3)

        # === Ana İçerik ===
        self.main_frame = tk.Frame(self, bg=bg_color)
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Üst Bar (Menü ve Profil)
        top_bar = tk.Frame(self.main_frame, bg=bg_color)
        top_bar.pack(fill="x", pady=10, padx=10)

        menu_btn = tk.Label(top_bar, text="≡", font=("Arial", 14), bg=bg_color, fg=text_color, cursor="hand2")
        menu_btn.pack(side="left")
        menu_btn.bind("<Button-1>", lambda e: self.toggle_sidebar())

        profile_btn = tk.Label(top_bar, text="👤", font=("Arial", 12), bg=bg_color, fg=text_color, cursor="hand2")
        profile_btn.pack(side="right")
        profile_btn.bind("<Button-1>", lambda e: self.controller.show_frame("ProfileScreen"))

        # Başlık
        tk.Label(self.main_frame, text="Feel", font=("Brush Script MT", 28), fg=text_color, bg=bg_color).pack(pady=(10, 0))
        tk.Label(self.main_frame, text="Art", font=("Brush Script MT", 24), fg=text_color, bg=bg_color).pack(pady=(0, 20))

        # Chat-like Giriş
        chat_frame = tk.Frame(self.main_frame, bg=accent_color)
        chat_frame.pack(padx=20, pady=20, fill="x")

        tk.Label(chat_frame, text="Senin ruh halin bugün nasıl?", bg=accent_color, font=("Arial", 10)).pack(anchor="w", padx=10, pady=(10, 0))
        self.search_entry = tk.Entry(chat_frame, font=("Arial", 10), relief="flat", bg="white")
        self.search_entry.pack(padx=10, pady=10, fill="x")

        tk.Button(self.main_frame, text="🎨 Galeri Oluştur", bg="#f5e2a9", fg=text_color,
                  command=self.add_action, font=("Arial", 11)).pack(pady=10)

        # Alt Navigasyon
        bottom_nav = tk.Frame(self.main_frame, bg=bg_color)
        bottom_nav.pack(side="bottom", pady=15)

        tk.Button(bottom_nav, text="🔖 Kaydedilenler", bg=accent_color, fg=text_color,
                  command=lambda: self.controller.show_frame("BookmarksScreen")).pack(side="left", padx=10)

        tk.Button(bottom_nav, text="❤️ Beğeniler", bg=accent_color, fg=text_color,
                  command=lambda: self.controller.show_frame("LikesScreen")).pack(side="left", padx=10)

    
    def toggle_sidebar(self):
        if self.sidebar_open:
            self.sidebar_frame.place_forget()
            self.main_frame.place(x=0, y=0)
        else:
            self.sidebar_frame.place(x=0, y=0, relheight=1)
            self.main_frame.place(x=130, y=0)
        self.sidebar_open = not self.sidebar_open

    def add_action(self):
        emotion_text = self.search_entry.get()
        if not emotion_text.strip():
            messagebox.showwarning("Uyarı", "Lütfen bir duygu durumu girin.")
            return

        # Galeri ekranını dinamik olarak oluştur ve göster
        gallery_screen = GalleryScreen(self.controller, self.controller, emotion_text)
        gallery_screen.place(relwidth=1, relheight=1)

        self.controller.frames["GalleryScreen"] = gallery_screen
        self.controller.show_frame("GalleryScreen")