import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class ProfileScreen(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, padding=20)
        self.controller = controller


        self.name = ttk.StringVar(value="Miranda West")
        self.email = ttk.StringVar(value="miranda@example.com")

        ttk.Label(self, text="Profile", font=("Helvetica", 16, "bold"), bootstyle="dark").pack(pady=(0, 20))

        # Kartlar
        profile_card = ttk.Labelframe(self, text="User Info", padding=10, bootstyle="info")
        profile_card.pack(fill="x", pady=10)

        ttk.Label(profile_card, text="Name:", font=("Arial", 10)).pack(anchor="w")
        ttk.Entry(profile_card, textvariable=self.name, width=30).pack(fill="x", pady=(0, 10))

        ttk.Label(profile_card, text="Email:", font=("Arial", 10)).pack(anchor="w")
        ttk.Entry(profile_card, textvariable=self.email, width=30).pack(fill="x")

        ttk.Button(profile_card, text="Save Profile", bootstyle="success-outline", command=self.save_profile).pack(pady=10)

        settings_card = ttk.Labelframe(self, text="Settings", padding=10, bootstyle="secondary")
        settings_card.pack(fill="x", pady=10)

        ttk.Button(settings_card, text="Change Password", bootstyle="light", command=self.change_password).pack(fill="x", pady=5)
        ttk.Button(settings_card, text="Language", bootstyle="light", command=self.change_language).pack(fill="x", pady=5)
        ttk.Button(settings_card, text="Clear History", bootstyle="danger-outline", command=self.clear_history).pack(fill="x", pady=5)

        # Alt butonlar
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill="x", pady=20)

        ttk.Button(bottom_frame, text="Logout", bootstyle="danger", command=self.exit_app).pack(side="right", padx=10)
        ttk.Button(bottom_frame, text="Home", bootstyle="info", command=lambda: self.controller.show_frame("MainScreen")).pack(side="left", padx=10)

    def save_profile(self):
        messagebox.showinfo("Success", f"Saved profile:\nName: {self.name.get()}\nEmail: {self.email.get()}")

    def change_password(self):
        messagebox.showinfo("Password", "Change password clicked")

    def change_language(self):
        messagebox.showinfo("Language", "Language settings opened")

    def clear_history(self):
        messagebox.showinfo("History", "Browsing history cleared")

    def exit_app(self):
        self.controller.quit()
