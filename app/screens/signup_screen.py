import tkinter as tk
from tkinter import messagebox, font

class SignupScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#fceeff")  # Soft pastel mor arka plan
        self.controller = controller

        # Geri butonu (sol üstte ok)
        tk.Button(self, text="←", font=("Arial", 14), bg="#fceeff", fg="#6a4e76",
                  bd=0, command=lambda: controller.show_frame("LoginScreen")).pack(anchor="w", padx=10, pady=(10, 0))

        # Başlık
        try:
            title_font = font.Font(family="Segoe UI", size=20, weight="bold")
        except:
            title_font = ("Arial", 20, "bold")

        tk.Label(self, text="Hesap Oluştur", font=title_font, fg="#843b62", bg="#fceeff").pack(pady=(10, 20))

        # Form alanları
        self.entry_name = self.create_input("Ad Soyad")
        self.entry_email = self.create_input("Email")
        self.entry_password = self.create_input("Şifre (min. 8 karakter)", show="*")

        # Kayıt Ol Butonu
        tk.Button(self, text="Kayıt Ol", font=("Arial", 11, "bold"), bg="#c97fd9",
                  fg="white", activebackground="#b064c2", width=28, height=2,
                  bd=0, relief="flat", cursor="hand2", command=self.submit_signup).pack(pady=20)

        # Alternatif kayıtlar (örn. sosyal medya)
        tk.Label(self, text="veya", bg="#fceeff", fg="#7e5e91", font=("Arial", 10, "italic")).pack()

        self.create_social_button("Facebook ile Kayıt Ol", "facebook")
        self.create_social_button("Apple ile Kayıt Ol", "apple")

        # Giriş linki
        tk.Label(self, text="Zaten hesabın var mı?", font=("Arial", 9),
                 bg="#fceeff", fg="#6a4e76").pack(pady=(20, 0))
        tk.Button(self, text="Giriş Yap", font=("Arial", 9, "underline"),
                  fg="#843b62", bg="#fceeff", bd=0,
                  command=lambda: controller.show_frame("LoginScreen"), cursor="hand2").pack()

    def create_input(self, placeholder, show=None):
        entry = tk.Entry(self, font=("Arial", 10), bg="#f9f4fd", fg="#333",
                         width=30, bd=1, relief="solid", show=show)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event, e=entry, p=placeholder: self.on_focus_in(e, p))
        entry.bind("<FocusOut>", lambda event, e=entry, p=placeholder: self.on_focus_out(e, p))
        entry.pack(pady=5, ipady=6)
        return entry

    def on_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#000")

    def on_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="#999")

    def create_social_button(self, text, platform):
        tk.Button(self, text=text, font=("Arial", 10, "bold"),
                  bg="white", fg="#4a2c4c", width=28, height=2,
                  bd=1, relief="solid", cursor="hand2").pack(pady=8)

    def submit_signup(self):
        messagebox.showinfo("Kayıt Olundu", "Kayıt işlemi başarıyla tamamlandı!")
        self.controller.show_frame("LoginScreen")
