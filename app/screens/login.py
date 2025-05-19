import tkinter as tk
from tkinter import font

class LoginScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.configure(bg="#fbefff")  # Tatlı, pastel lavanta arka plan

        # Başlık yazısı (koyu mor, büyük font)
        try:
            title_font = font.Font(family="Segoe Script", size=40, weight="bold")
        except:
            title_font = ("Arial", 32, "bold")

        tk.Label(self, text="FeelArt", font=title_font,
                 fg="#4b296b", bg="#fbefff").pack(pady=(70, 40))

        # Ortak buton stili
        btn_common = {
            "font": ("Arial", 12, "bold"),
            "fg": "#ffffff",
            "width": 20,
            "height": 2,
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
            "highlightthickness": 0
        }

        # Giriş Butonu (mor ton)
        login_btn = tk.Button(self, text="Giriş Yap",
                              command=lambda: controller.show_frame("LoginPanelScreen"),
                              bg="#a86bd8", activebackground="#9e57d5", **btn_common)
        login_btn.pack(pady=10)
        self.make_rounded(login_btn)

        # Kayıt Ol Butonu (pembe ton)
        signup_btn = tk.Button(self, text="Kayıt Ol",
                               command=lambda: controller.show_frame("SignupScreen"),
                               bg="#db8adf", activebackground="#d073d4", **btn_common)
        signup_btn.pack(pady=10)
        self.make_rounded(signup_btn)

        # Alt yazı
        tk.Label(self, text="Sanatla hisset, kendini keşfet.",
                 font=("Arial", 10, "italic"),
                 fg="#7e6799", bg="#fbefff").pack(side="bottom", pady=30)

    def make_rounded(self, button):
        """Tkinter'da oval buton desteği doğrudan yoktur, ama paddingle ve canvas üzerinden yapılabilir.
           Burada sadece tasarım yumuşak dursun diye fonksiyon bırakılmıştır."""
        button.configure(highlightbackground=button["bg"], pady=10, padx=5)
