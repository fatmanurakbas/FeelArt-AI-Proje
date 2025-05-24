import tkinter as tk
from tkinter import messagebox
import json
from screens.gallery import GalleryScreen
from screens.oneripaneli import OneriPaneliScreen

class MainScreen(tk.Frame):
    def __init__(self, master, controller): 
        super().__init__(master, bg="#fffbe9")
        self.controller = controller 
        
        
        self.sidebar_open = False
        self.history_labels = []

        bg_color = "#fffbe9"
        accent_color = "#a782e6"
        text_color = "#7b4caf"
        sidebar_bg = "#f5e2a9"

        # 🟨 Sidebar
        self.sidebar_frame = tk.Frame(self, width=130, bg=sidebar_bg, height=580)
        sidebar_title = tk.Label(self.sidebar_frame, text="Sohbet Geçmişi", bg=sidebar_bg, fg=text_color,
                                 font=("Arial", 10, "bold"))
        sidebar_title.pack(pady=10)
        self.load_history()

        # 🌇 Ana Alan
        self.main_frame = tk.Frame(self, bg=bg_color)
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # 🔝 Üst Bar
        top_bar = tk.Frame(self.main_frame, bg=bg_color)
        top_bar.pack(fill="x", pady=10, padx=10)

        menu_btn = tk.Label(top_bar, text="≡", font=("Arial", 14), bg=bg_color, fg=text_color, cursor="hand2")
        menu_btn.pack(side="left")
        menu_btn.bind("<Button-1>", lambda e: self.toggle_sidebar())

        profile_btn = tk.Label(top_bar, text="👤", font=("Arial", 12), bg=bg_color, fg=text_color, cursor="hand2")
        profile_btn.pack(side="right")
        profile_btn.bind("<Button-1>", lambda e: self.controller.show_frame("ProfileScreen"))

        # 🎨 Başlık
        tk.Label(self.main_frame, text="Feel", font=("Brush Script MT", 28), fg=text_color, bg=bg_color).pack(pady=(10, 0))
        tk.Label(self.main_frame, text="Art", font=("Brush Script MT", 24), fg=text_color, bg=bg_color).pack(pady=(0, 20))

        # 💬 Soru & Giriş Alanı
        chat_frame = tk.Frame(self.main_frame, bg="white", bd=0, highlightthickness=0)
        chat_frame.pack(padx=30, pady=10, fill="x")

        tk.Label(chat_frame, text="Senin ruh halin bugün nasıl?", bg="white", font=("Arial", 10), fg=text_color)            .pack(anchor="w", padx=10, pady=(10, 0))

        self.search_entry = tk.Entry(chat_frame, font=("Arial", 10), relief="flat", bg="white", fg="#333")
        self.search_entry.pack(padx=10, pady=10, fill="x")

        # 🎯 Aksiyon Butonları
        tk.Button(self.main_frame, text="Galeri Oluştur", bg=accent_color, fg="white",
                  font=("Arial", 11, "bold"), relief="flat", command=self.add_action)            .pack(padx=40, pady=8, ipadx=10, ipady=5, fill="x")

        tk.Button(self.main_frame, text="Film Öner", bg=accent_color, fg="white",
                  font=("Arial", 11, "bold"), relief="flat", command=self.get_recommendations)            .pack(padx=40, pady=0, ipadx=10, ipady=5, fill="x")

        # 🔻 Alt Menü
        bottom_nav = tk.Frame(self.main_frame, bg=bg_color)
        bottom_nav.pack(side="bottom", pady=20)

        tk.Button(bottom_nav, text="Kaydedilenler", bg=accent_color, fg="white", font=("Arial", 10),
                  relief="flat", command=lambda: self.controller.show_frame("BookmarksScreen")).pack(side="left", padx=15, ipadx=10, ipady=3)

        tk.Button(bottom_nav, text="Beğeniler", bg=accent_color, fg="white", font=("Arial", 10),
                  relief="flat", command=lambda: self.controller.show_frame("LikesScreen")).pack(side="left", padx=15, ipadx=10, ipady=3)

    def toggle_sidebar(self):
        if self.sidebar_open:
            self.sidebar_frame.place_forget()
            self.main_frame.place(x=0, y=0)
        else:
            self.sidebar_frame.place(x=0, y=0, relheight=1)
            self.main_frame.place(x=130, y=0)
        self.sidebar_open = not self.sidebar_open

    def _analyze_emotion(self, text):
        text_lower = text.lower()
        if "üzgün" in text_lower or "mutsuz" in text_lower or "depresif" in text_lower or "hüzünlü" in text_lower:
            return "üzgün"
        elif "mutlu" in text_lower or "neşeli" in text_lower or "keyifli" in text_lower or "sevinçli" in text_lower:
            return "mutlu"
        elif "kızgın" in text_lower or "sinirli" in text_lower or "öfkeli" in text_lower:
            return "kızgın"
        elif "heyecanlı" in text_lower or "enerjik" in text_lower or "coşkulu" in text_lower:
            return "heyecanlı"
        elif "korkmuş" in text_lower or "tedirgin" in text_lower or "endişeli" in text_lower:
            return "korkmuş"
        elif "şok" in text_lower or "şaşırmış" in text_lower:
            return "şaşkın"
        elif "tiksinti" in text_lower or "iğrenme" in text_lower:
            return "tiksinti"
        return "nötr"

    def add_action(self):
        emotion_text = self.search_entry.get().strip()
        if not emotion_text:
            messagebox.showwarning("Uyarı", "Lütfen bir duygu durumu girin.")
            return

        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        history = data.get("history", [])
        if emotion_text in history:
            history.remove(emotion_text)
        history.insert(0, emotion_text)
        data["history"] = history[:10]

        try:
            with open("user_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Hata", f"Geçmiş kaydedilirken bir hata oluştu: {e}")

        self.load_history()

        gallery_screen = GalleryScreen(self.controller, self.controller, emotion_text)
        self.controller.frames["GalleryScreen"] = gallery_screen
        self.controller.show_frame("GalleryScreen")
        gallery_screen.place(relwidth=1, relheight=1)

        self.search_entry.delete(0, tk.END)

    def load_history(self):
        for label in self.history_labels:
            label.destroy()
        self.history_labels.clear()

        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                history_items = data.get("history", [])
        except (FileNotFoundError, json.JSONDecodeError):
            history_items = []

        for item in history_items:
            lbl = tk.Label(self.sidebar_frame, text=f"• {item}", bg="#f5e2a9", fg="black", font=("Arial", 9), anchor="w", cursor="hand2")
            lbl.pack(fill="x", padx=15, pady=2)
            lbl.bind("<Button-1>", lambda e, emotion=item: self.open_gallery_from_history(emotion))
            self.history_labels.append(lbl)

    def open_gallery_from_history(self, emotion_text):
        gallery_screen = GalleryScreen(self.controller, self.controller, emotion_text)
        self.controller.frames["GalleryScreen"] = gallery_screen
        self.controller.show_frame("GalleryScreen")
        gallery_screen.place(relwidth=1, relheight=1)

        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        history = data.get("history", [])
        if emotion_text in history:
            history.remove(emotion_text)
        history.insert(0, emotion_text)
        data["history"] = history[:10]

        try:
            with open("user_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Hata", f"Geçmiş güncellenirken bir hata oluştu: {e}")

        self.load_history()

    def get_recommendations(self):
        user_input_text = self.search_entry.get().strip()
        if not user_input_text:
            messagebox.showwarning("Uyarı", "Lütfen bir duygu durumu girin.")
            return

        emotion_to_send = self._analyze_emotion(user_input_text)
        if not emotion_to_send or emotion_to_send == "nötr":
            messagebox.showinfo("Bilgi", "Girdiğiniz metinden belirgin bir duygu çıkarılamadı.")
            return

        oneri_ekrani = OneriPaneliScreen(self.controller, self.controller, emotion_to_send)
        self.controller.frames["OneriPaneliScreen"] = oneri_ekrani
        self.controller.show_frame("OneriPaneliScreen")
        oneri_ekrani.place(relwidth=1, relheight=1)
