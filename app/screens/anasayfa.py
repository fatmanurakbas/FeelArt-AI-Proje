import tkinter as tk
from tkinter import messagebox
import json
from screens.gallery import GalleryScreen
import requests


class MainScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#fffbe9")
        self.controller = controller
        self.sidebar_open = False
        self.history_labels = []

        bg_color = "#fffbe9"
        accent_color = "#f0d58c"
        text_color = "#b4462b"
        sidebar_bg = "#f5e2a9"

        # === Sidebar ===
        self.sidebar_frame = tk.Frame(self, width=130, bg=sidebar_bg, height=580)
        sidebar_title = tk.Label(self.sidebar_frame, text="Sohbet Geçmişi", bg=sidebar_bg, fg=text_color,
                                 font=("Arial", 10, "bold"))
        sidebar_title.pack(pady=10)

        self.load_history()

        # === Ana İçerik ===
        self.main_frame = tk.Frame(self, bg=bg_color)
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Üst Bar
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

        tk.Button(self.main_frame, text="Galeri Oluştur", bg="#f5e2a9", fg=text_color,
                  command=self.add_action, font=("Arial", 11)).pack(pady=10)
        
        tk.Button(self.main_frame, text="Film Öner", bg="#f5e2a9", fg=text_color,
          command=self.get_recommendations, font=("Arial", 11)).pack(pady=(0, 20))


        # Alt Navigasyon
        bottom_nav = tk.Frame(self.main_frame, bg=bg_color)
        bottom_nav.pack(side="bottom", pady=15)

        tk.Button(bottom_nav, text="Kaydedilenler", bg=accent_color, fg=text_color,
                  command=lambda: self.controller.show_frame("BookmarksScreen")).pack(side="left", padx=10)

        tk.Button(bottom_nav, text="Beğeniler", bg=accent_color, fg=text_color,
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
        emotion_text = self.search_entry.get().strip()
        if not emotion_text:
            messagebox.showwarning("Uyarı", "Lütfen bir duygu durumu girin.")
            return

        # === Geçmişe ekle ===
        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}

        history = data.get("history", [])
        if emotion_text in history:
            history.remove(emotion_text)
        history.insert(0, emotion_text)
        data["history"] = history[:10]

        try:
            with open("user_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except:
            pass

        self.load_history()

        # === Galeriye geç ===
        gallery_screen = GalleryScreen(self.controller, self.controller, emotion_text)
        gallery_screen.place(relwidth=1, relheight=1)
        self.controller.frames["GalleryScreen"] = gallery_screen
        self.controller.show_frame("GalleryScreen")

        # Chat alanını temizle
        self.search_entry.delete(0, tk.END)

    def load_history(self):
        for label in self.history_labels:
            label.destroy()
        self.history_labels.clear()

        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                history_items = data.get("history", [])
        except:
            history_items = []

        for item in history_items:
            lbl = tk.Label(self.sidebar_frame, text=f"• {item}", bg="#f5e2a9", fg="black", font=("Arial", 9), anchor="w", cursor="hand2")
            lbl.pack(fill="x", padx=15, pady=2)

            # 🟢 Tıklanınca galeriye gitmesini sağla
            lbl.bind("<Button-1>", lambda e, emotion=item: self.open_gallery_from_history(emotion))

            self.history_labels.append(lbl)
    
    def open_gallery_from_history(self, emotion_text):
        gallery_screen = GalleryScreen(self.controller, self.controller, emotion_text)
        gallery_screen.place(relwidth=1, relheight=1)
        self.controller.frames["GalleryScreen"] = gallery_screen
        self.controller.show_frame("GalleryScreen")

        # İsteğe bağlı: geçmişi güncelle (aynı şey üstte olsun)
        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}

        history = data.get("history", [])
        if emotion_text in history:
            history.remove(emotion_text)
        history.insert(0, emotion_text)
        data["history"] = history[:10]

        try:
            with open("user_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except:
            pass

        self.load_history()

    # anasayfa.py içindeki get_recommendations metodu
    def get_recommendations(self):
        emotion_text = self.search_entry.get().strip()
        if not emotion_text:
            messagebox.showwarning("Uyarı", "Lütfen bir duygu durumu girin.")
            return

        try:
            # Backend API endpoint'i
            response = requests.get("http://127.0.0.1:5000/api/recommendations", params={"emotion": emotion_text})
            response.raise_for_status()  # HTTP 4xx veya 5xx hatalarında exception fırlatır
            data = response.json()
        except requests.exceptions.ConnectionError as e:
            messagebox.showerror("Hata", f"API sunucusuna bağlanılamadı.\nSunucunun çalıştığından emin olun.\n{e}")
            return
        except requests.exceptions.Timeout as e:
            messagebox.showerror("Hata", f"API isteği zaman aşımına uğradı.\n{e}")
            return
        except requests.exceptions.HTTPError as e:
            # API'den gelen hata mesajını göstermeye çalışalım (eğer JSON ise)
            try:
                error_data = response.json()
                api_error_message = error_data.get('error', 'Detay yok')
                messagebox.showerror("Hata", f"API Hatası (HTTP {response.status_code}): {api_error_message}\n{e}")
            except json.JSONDecodeError:
                messagebox.showerror("Hata", f"API Hatası (HTTP {response.status_code}).\nYanıt: {response.text}\n{e}")
            return
        except json.JSONDecodeError as e: # Yanıt JSON değilse
            messagebox.showerror("Hata", f"API'den gelen yanıt okunamadı (JSON formatında değil).\nYanıt: {response.text}\n{e}")
            return
        except Exception as e: # Diğer beklenmedik hatalar
            messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu.\n{e}")
            return

        if 'recommendations' not in data or not data['recommendations']:
            # API'den boş liste veya 'message' geliyorsa onu da gösterebiliriz
            info_message = data.get('message', "Uygun film önerisi bulunamadı.")
            messagebox.showinfo("Bilgi", info_message)
            return

        recommendations = data['recommendations']
        self.show_recommendations_popup(recommendations)


    def show_recommendations_popup(self, recommendations):
        popup = tk.Toplevel(self)
        popup.title("Film Önerileri")
        popup.configure(bg="#fffbe9")

        for movie in recommendations:
            title = movie['title']
            overview = movie['overview']
            tk.Label(popup, text=title, font=("Arial", 11, "bold"), bg="#fffbe9", fg="#b4462b").pack(anchor="w", padx=10, pady=(10, 0))
            tk.Label(popup, text=overview, wraplength=400, justify="left", bg="#fffbe9").pack(anchor="w", padx=10)
