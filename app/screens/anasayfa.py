import tkinter as tk
from tkinter import messagebox
import json
from screens.gallery import GalleryScreen # Bu satırın doğru yolu gösterdiğinden emin olun
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

    def _analyze_emotion(self, text):
        """
        Verilen metinden anahtar duygu kelimesini analiz eder ve döndürür.
        Bu kısım, sizin görsel oluşturma için kullandığınız gerçek duygu analizi mantığını içermelidir.
        Şu anki implementasyon basit bir anahtar kelime eşleştirmesidir.
        Daha gelişmiş bir NLP modeli (örn. NLTK, spaCy, TextBlob) veya özel bir duygu sınıflandırma modeli
        kullanarak daha doğru sonuçlar alabilirsiniz.
        """
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
            return "şaşırmış"
        elif "tiksinti" in text_lower or "iğrenme" in text_lower:
            return "tiksinti"
        # Eğer yukarıdaki kelimelerden hiçbiri bulunamazsa
        return "nötr" # Varsayılan olarak "nötr" döndür

    def add_action(self):
        emotion_text = self.search_entry.get().strip()
        if not emotion_text:
            messagebox.showwarning("Uyarı", "Lütfen bir duygu durumu girin.")
            return

        # Geçmişe ekleme ve Galeriye geçme işlemleri
        # (Bu kısım _analyze_emotion'dan bağımsız olarak çalışabilir,
        # ancak eğer görsel API'si de tek kelime bekliyorsa
        # burada da analyzed_emotion kullanmanız gerekebilir)

        # === Geçmişe ekle ===
        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError): # JSON dosyası yoksa veya bozuksa
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

        # === Galeriye geç ===
        # Burada GalleryScreen'e gönderilen emotion_text'in
        # görsel API'si için analiz edilmiş hali mi yoksa ham hali mi olması gerektiğine
        # sizin backend'iniz karar verecektir. Genelde ham metin gönderilir ve
        # backend tarafında analiz yapılır. Ancak eğer frontend'de bu analiz
        # görsel için de yapılıyorsa, burada da _analyze_emotion çıktısı kullanılabilir.
        # Şimdilik mevcut haliyle bırakıyorum.
        gallery_screen = GalleryScreen(self.controller, self.controller, emotion_text)
        self.controller.frames["GalleryScreen"] = gallery_screen
        self.controller.show_frame("GalleryScreen")
        gallery_screen.place(relwidth=1, relheight=1) # place çağrısını show_frame'den sonra yapın


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
        except (FileNotFoundError, json.JSONDecodeError):
            history_items = []

        for item in history_items:
            lbl = tk.Label(self.sidebar_frame, text=f"• {item}", bg="#f5e2a9", fg="black", font=("Arial", 9), anchor="w", cursor="hand2")
            lbl.pack(fill="x", padx=15, pady=2)

            # 🟢 Tıklanınca galeriye gitmesini sağla
            lbl.bind("<Button-1>", lambda e, emotion=item: self.open_gallery_from_history(emotion))

            self.history_labels.append(lbl)
    
    def open_gallery_from_history(self, emotion_text):
        gallery_screen = GalleryScreen(self.controller, self.controller, emotion_text)
        self.controller.frames["GalleryScreen"] = gallery_screen
        self.controller.show_frame("GalleryScreen")
        gallery_screen.place(relwidth=1, relheight=1) # place çağrısını show_frame'den sonra yapın

        # İsteğe bağlı: geçmişi güncelle (aynı şey üstte olsun)
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

    # anasayfa.py içindeki get_recommendations metodu
    def get_recommendations(self):
        user_input_text = self.search_entry.get().strip()
        if not user_input_text:
            messagebox.showwarning("Uyarı", "Lütfen bir duygu durumu girin.")
            return

        # Kullanıcının girdiği metinden anahtar duygu kelimesini analiz et
        emotion_to_send = self._analyze_emotion(user_input_text)
        
        # Eğer analizden geçerli bir duygu çıkmazsa kullanıcıya bilgi ver
        if not emotion_to_send or emotion_to_send == "nötr":
             messagebox.showinfo("Bilgi", "Girdiğiniz metinden belirgin bir duygu çıkarılamadı. Lütfen daha net bir ifade kullanın veya doğrudan bir duygu kelimesi girin.")
             return # Duygu yoksa API çağrısını yapma

        try:
            # Backend API endpoint'i
            # Analiz edilmiş tek kelimelik duygu durumunu API'ye gönderiyoruz
            response = requests.get("http://127.0.0.1:5000/api/recommendations", params={"emotion": emotion_to_send})
            response.raise_for_status()  # HTTP 4xx veya 5xx hatalarında exception fırlatır
            data = response.json()
            print("API'den gelen yanıt (Film Öneri):", data) # Hata ayıklama için konsola yazdır

        except requests.exceptions.ConnectionError as e:
            messagebox.showerror("Hata", f"API sunucusuna bağlanılamadı.\nSunucunun çalıştığından emin olun.\n{e}")
            return
        except requests.exceptions.Timeout as e:
            messagebox.showerror("Hata", f"API isteği zaman aşımına uğradı.\n{e}")
            return
        except requests.exceptions.HTTPError as e:
            try:
                error_data = response.json()
                api_error_message = error_data.get('error', 'Detay yok')
                messagebox.showerror("Hata", f"API Hatası (HTTP {response.status_code}): {api_error_message}\n{e}")
            except json.JSONDecodeError: # API'den gelen yanıt JSON değilse
                messagebox.showerror("Hata", f"API Hatası (HTTP {response.status_code}).\nYanıt: {response.text}\n{e}")
            return
        except json.JSONDecodeError as e: # Yanıt JSON değilse
            messagebox.showerror("Hata", f"API'den gelen yanıt okunamadı (JSON formatında değil).\nYanıt: {response.text}\n{e}")
            return
        except Exception as e: # Diğer beklenmedik hatalar
            messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu.\n{e}")
            return

        # 'recommendations' anahtarı yoksa veya boşsa
        if 'recommendations' not in data or not data['recommendations']:
            info_message = data.get('message', "Girdiğiniz duygu için uygun film önerisi bulunamadı.")
            messagebox.showinfo("Bilgi", info_message)
            return

        recommendations = data['recommendations']
        self.show_recommendations_popup(recommendations)


    def show_recommendations_popup(self, recommendations):
        popup = tk.Toplevel(self)
        popup.title("Film Önerileri")
        popup.configure(bg="#fffbe9")
        popup.transient(self.master) # Ana pencere üzerinde kalmasını sağlar
        popup.grab_set() # Ana pencere etkileşimini engeller
        popup.resizable(False, False) # Boyutlandırmayı kapat

        # Scrollbar için bir canvas ve frame oluşturun
        canvas = tk.Canvas(popup, bg="#fffbe9")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        # canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
        # Yukarıdaki satırı kaldırıp aşağıdaki daha kontrollü mekanizmayı kullanacağız

        # Önerileri göstermek için frame
        # canvas.create_window'u daha sonra, canvas'ın genişliğini bildiğimizde çağıracağız.
        recommendations_frame = tk.Frame(canvas, bg="#fffbe9")
        
        # Bu window_id'yi saklayalım ki daha sonra güncelleyebilelim
        window_id = canvas.create_window((0, 0), window=recommendations_frame, anchor="nw")

        # recommendations_frame'in boyutunu güncellediğinde canvas'ın scrollregion'ını güncelleyin
        recommendations_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Canvas'ın boyutu değiştiğinde, recommendations_frame'in genişliğini canvas'ın genişliğine eşitle
        def _on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)
            canvas.configure(scrollregion=canvas.bbox("all")) # Her boyutta scrollregion'ı güncelleyin
        canvas.bind('<Configure>', _on_canvas_configure)


        if not recommendations: # Eğer boş liste geldiyse
            tk.Label(recommendations_frame, text="Bu duyguya uygun film önerisi bulunamadı.",
                     bg="#fffbe9", fg="#b4462b", font=("Arial", 11)).pack(padx=10, pady=10)
        else:
            for movie in recommendations:
                title = movie.get('title', 'Başlık Bilinmiyor')
                overview = movie.get('overview', 'Açıklama Bilinmiyor')
                
                tk.Label(recommendations_frame, text=title, font=("Arial", 11, "bold"), bg="#fffbe9", fg="#b4462b").pack(anchor="w", padx=10, pady=(10, 0))
                tk.Label(recommendations_frame, text=overview, wraplength=400, justify="left", bg="#fffbe9").pack(anchor="w", padx=10)
                tk.Frame(recommendations_frame, height=1, bg="#f0d58c").pack(fill="x", padx=10, pady=5) # Ayırıcı çizgi

        # Tüm widget'lar yerleştirildikten sonra pop-up'ı ve canvas'ı güncelleyin
        # Bu kritik bir adımdır!
        popup.update_idletasks() # Pop-up'ın içindeki widget'ların boyutlarını ve yerleşimlerini güncelleyin
        canvas.configure(scrollregion=canvas.bbox("all")) # Scrollbarı doğru ayarlamak için son kez güncelleyin


        # Pop-up kapatılınca odak ana pencereye geri dönsün
        popup.protocol("WM_DELETE_WINDOW", lambda: self.close_popup_and_release_grab(popup))
        
        # İlk açıldığında recommendations_frame'in genişliğini canvas'a eşitlemek için
        # küçük bir gecikmeyle çağrı yapabiliriz veya _on_canvas_configure'un çağrılmasını bekleyebiliriz.
        # Genellikle _on_canvas_configure ilk boyutlandırmada da tetiklenir.

    def close_popup_and_release_grab(self, popup):
        if popup.winfo_exists(): # Pencere hala mevcutsa
            popup.grab_release()
            popup.destroy()