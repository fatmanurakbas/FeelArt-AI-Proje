import tkinter as tk
from tkinter import messagebox

class ForgotPasswordScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#fffbe9")
        self.controller = controller

        text_color = "#b4462b"
        entry_bg = "#eba94d"
        btn_bg1 = "#f5e2a9"
        btn_text = "black"

        # Geri Dön Butonu
        back_btn = tk.Button(self, text="←", font=("Arial", 12), bg="#fffbe9", fg=text_color, bd=0,
                             command=lambda: controller.show_frame("LoginPanelScreen"))
        back_btn.pack(anchor="w", padx=10, pady=5)

        # Başlık
        title = tk.Label(self, text="Şifreni mi unuttun?", font=("Arial", 14, "bold"), fg=text_color, bg="#fffbe9")
        title.pack(pady=(30, 10))

        info = tk.Label(self, text="E-posta adresini gir,\nşifre sıfırlama bağlantısı gönderilsin.",
                        font=("Arial", 9), fg="gray", bg="#fffbe9")
        info.pack(pady=(0, 20))

        # E-posta alanı
        self.entry_email = tk.Entry(self, bg=entry_bg, relief="flat", font=("Arial", 10), width=28)
        self.entry_email.pack(pady=(0, 20), ipady=5)

        # Gönder butonu
        send_btn = tk.Button(self, text="Bağlantıyı Gönder", font=("Arial", 10, "bold"),
                             bg=btn_bg1, fg=btn_text, bd=1, relief="ridge", width=20,
                             command=self.send_reset_link)
        send_btn.pack()

    def send_reset_link(self):
        email = self.entry_email.get()
        if email:
            messagebox.showinfo("Şifre Sıfırlama", f"{email} adresine şifre sıfırlama bağlantısı gönderildi!")
        else:
            messagebox.showwarning("Eksik Bilgi", "Lütfen e-posta adresinizi girin.")
