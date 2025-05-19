import tkinter as tk
from tkinter import messagebox

class ProfileScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#fffbe9")
        self.controller = controller

        text_color = "#b4462b"
        btn_color = "#eba94d"
        btn_text = "black"

        # Üst ikonlar
        top_frame = tk.Frame(self, bg="#fffbe9")
        top_frame.pack(fill="x", padx=10, pady=(5, 10))

        back_btn = tk.Label(top_frame, text="←", font=("Arial", 12), bg="#fffbe9", fg=text_color, cursor="hand2")
        back_btn.pack(side="left")
        back_btn.bind("<Button-1>", lambda e: controller.show_frame("MainScreen"))

        share_btn = tk.Label(top_frame, text="⇪", font=("Arial", 12), bg="#fffbe9", fg=text_color, cursor="hand2")
        share_btn.pack(side="right")

        # Kullanıcı simgesi
        avatar = tk.Canvas(self, width=120, height=120, bg="#f0d58c", highlightthickness=0)
        avatar.create_oval(20, 20, 100, 100, fill="#f0d58c", outline="#f0d58c")
        avatar.create_oval(45, 35, 75, 65, fill="#fffbe9", outline=text_color)
        avatar.create_arc(40, 70, 80, 100, start=0, extent=180, style="arc", outline=text_color, width=3)
        avatar.pack()

        # İsim & düzenleme
        name_label = tk.Label(self, text="Name-Surname", font=("Arial", 10, "bold"), bg="#fffbe9", fg="black")
        name_label.pack(pady=(10, 5))

        edit_btn = tk.Button(self, text="edit profile", command=self.edit_profile, font=("Arial", 9), bg=btn_color, fg=btn_text, bd=1, relief="ridge", width=12)
        edit_btn.pack()

        # Bilgi alanları
        info_frame = tk.Frame(self, bg="#fffbe9")
        info_frame.pack(pady=20, anchor="w", padx=30)

        infos = [
            ("e -posta:", ""),
            ("change password:", ""),
            ("language:", ""),
            ("delete history:", "")
        ]

        for label, _ in infos:
            tk.Label(info_frame, text=label, font=("Arial", 9, "italic"), fg="black", bg="#fffbe9").pack(anchor="w", pady=5)

        # Alt butonlar
        bottom_frame = tk.Frame(self, bg="#fffbe9")
        bottom_frame.pack(side="bottom", fill="x", pady=15, padx=15)

        change_account_btn = tk.Button(bottom_frame, text="change\naccount", command=self.change_account, font=("Arial", 8, "bold"),
                                       bg=btn_color, fg=btn_text, bd=1, relief="ridge", width=10, height=2)
        change_account_btn.pack(side="left")

        exit_btn = tk.Button(bottom_frame, text="exit", command=self.exit_app, font=("Arial", 8, "bold"),
                             bg=btn_color, fg=btn_text, bd=1, relief="ridge", width=10, height=2)
        exit_btn.pack(side="right")

    def edit_profile(self):
        messagebox.showinfo("Profil Düzenle", "Profil düzenleme ekranı (örnek)")

    def change_account(self):
        self.controller.show_frame("LoginScreen")

    def exit_app(self):
        self.controller.quit()
