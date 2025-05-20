import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json
import os
import tkinter as tk


USER_DATA_PATH = "user_data.json"

def load_user_data():
    if not os.path.exists(USER_DATA_PATH):
        return {"name": "", "email": "", "profile_image": "", "history": []}
    with open(USER_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_user_data(data):
    with open(USER_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class ProfileScreen(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.data = load_user_data()

        # Canvas ve scrollbar
        canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollable iç çerçeve
        self.scroll_frame = ttk.Frame(canvas)
        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Scroll frame'i canvas içine yerleştir
        self.scroll_window = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Scroll-frame genişliğini canvas'a uydur
        def _on_canvas_resize(event):
            canvas.itemconfig(self.scroll_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_resize)

        # Scroll için mousewheel desteği
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Aşağıda kalan tüm kod, self.scroll_frame içine yazılacak
        self.name = ttk.StringVar(value=self.data.get("name", ""))
        self.email = ttk.StringVar(value=self.data.get("email", ""))
        self.profile_image_path = self.data.get("profile_image", "")

        self.avatar_label = ttk.Label(self.scroll_frame)
        self.avatar_label.pack(pady=(5, 10))
        self.after(100, self.update_avatar)

        ttk.Button(self.scroll_frame, text="Select Photo", command=self.select_photo, bootstyle="info-outline").pack(pady=(0, 15))
        ttk.Label(self.scroll_frame, text="Profile", font=("Helvetica", 16, "bold"), bootstyle="dark").pack(pady=(0, 10))

        profile_card = ttk.Labelframe(self.scroll_frame, text="User Info", padding=10, bootstyle="info")
        profile_card.pack(fill="x", pady=10)

        ttk.Label(profile_card, text="Name:", font=("Arial", 10)).pack(anchor="w")
        ttk.Entry(profile_card, textvariable=self.name, width=30).pack(fill="x", pady=(0, 10))

        ttk.Label(profile_card, text="Email:", font=("Arial", 10)).pack(anchor="w")
        ttk.Entry(profile_card, textvariable=self.email, width=30).pack(fill="x")

        ttk.Button(profile_card, text="Save Profile", bootstyle="success-outline", command=self.save_profile).pack(pady=10)

        settings_card = ttk.Labelframe(self.scroll_frame, text="Settings", padding=10, bootstyle="secondary")
        settings_card.pack(fill="x", pady=10)

        ttk.Button(settings_card, text="Change Password", bootstyle="light").pack(fill="x", pady=5)
        ttk.Button(settings_card, text="Language", bootstyle="light").pack(fill="x", pady=5)
        ttk.Button(settings_card, text="Clear History", bootstyle="danger-outline", command=self.clear_history).pack(fill="x", pady=5)

        bottom_frame = ttk.Frame(self.scroll_frame)
        bottom_frame.pack(fill="x", pady=20)

        ttk.Button(bottom_frame, text="Home", bootstyle="info", command=lambda: self.controller.show_frame("MainScreen")).pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="Logout", bootstyle="danger", command=self.exit_app).pack(side="right", padx=10)

    def update_avatar(self):
        if self.profile_image_path and os.path.exists(self.profile_image_path):
            try:
                img = Image.open(self.profile_image_path)
                img = img.resize((100, 100))
                self.avatar_image = ImageTk.PhotoImage(img)
                self.avatar_label.configure(image=self.avatar_image)
            except:
                self.avatar_label.configure(text="No Image", image="", width=20)
        else:
            self.avatar_label.configure(text="No Image", image="", width=20)

    def select_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.profile_image_path = file_path
            self.update_avatar()

    def save_profile(self):
        self.data["name"] = self.name.get()
        self.data["email"] = self.email.get()
        self.data["profile_image"] = self.profile_image_path
        save_user_data(self.data)
        messagebox.showinfo("Success", "Profile updated successfully")

    def clear_history(self):
        self.data["history"] = []
        save_user_data(self.data)

        # MainScreen varsa, onun history içeriğini güncelle
        main_screen = self.controller.frames.get("MainScreen")
        if main_screen and hasattr(main_screen, "load_history"):
            main_screen.load_history()

        messagebox.showinfo("Geçmiş Silindi", "Tüm sohbet geçmişi temizlendi.")



    def exit_app(self):
        self.controller.quit()
