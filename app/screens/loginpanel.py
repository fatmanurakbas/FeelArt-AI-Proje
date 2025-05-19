import tkinter as tk
from tkinter import messagebox

class LoginPanelScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#fffbe9")
        self.controller = controller

        text_color = "#b4462b"
        entry_bg = "#eba94d"
        btn_bg = "#f5e2a9"

        # Geri Butonu
        tk.Button(self, text="←", command=lambda: controller.show_frame("LoginScreen"),
                  font=("Arial", 12), bg="#fffbe9", fg=text_color, bd=0).pack(anchor="w", padx=10, pady=5)

        tk.Label(self, text="E-posta ile Giriş", font=("Arial", 14, "bold"), fg=text_color, bg="#fffbe9").pack(pady=(10, 20))

        # Form alanları
        self.entry_email = self.create_field("E-posta")
        self.entry_pass = self.create_field("Şifre", show="*")

        # 🔽 Şifremi Unuttum butonunu buraya ekle
        forgot = tk.Label(self, text="Şifremi Unuttum!", font=("Arial", 8, "italic"), fg="gray", bg="#fffbe9", cursor="hand2")
        forgot.pack(anchor="e", padx=20, pady=(0, 20))
        forgot.bind("<Button-1>", lambda e: controller.show_frame("ForgotPasswordScreen"))

        # Giriş Butonu
        tk.Button(self, text="Giriş Yap", command=self.login_action, font=("Arial", 10, "bold"),
                  bg=btn_bg, fg="black", bd=1, relief="ridge", width=15).pack(pady=20)

    def create_field(self, label_text, show=None):
        tk.Label(self, text=label_text, font=("Arial", 9, "bold"), fg="#b4462b", bg="#fffbe9").pack(anchor="w", padx=20)
        entry = tk.Entry(self, bg="#eba94d", relief="flat", font=("Arial", 10), width=28, show=show)
        entry.pack(pady=(0, 10), ipady=5)
        return entry

    def login_action(self):
        email = self.entry_email.get()
        password = self.entry_pass.get()

        if email == "test@test.com" and password == "1234":
           self.controller.show_frame("MainScreen")
        else:
            messagebox.showerror("Hata", "Geçersiz e-posta ya da şifre.")

