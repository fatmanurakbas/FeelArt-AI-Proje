import tkinter as tk

# Ekranları screens klasöründen import et
from screens.login import LoginScreen
from screens.loginpanel import LoginPanelScreen
from screens.signup_screen import SignupScreen
from screens.anasayfa import MainScreen
from screens.kaydedilenler import BookmarksScreen
from screens.begeniler import LikesScreen
from screens.profil import ProfileScreen
from screens.forgot_password import ForgotPasswordScreen
from screens.gallery import GalleryScreen



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FeelArt")
        self.geometry("280x580")
        self.frames = {}

        # Tüm ekranları başlat ve sözlüğe ekle
        for F in (
            LoginScreen, LoginPanelScreen, SignupScreen, ForgotPasswordScreen,GalleryScreen,
            MainScreen, BookmarksScreen, LikesScreen, ProfileScreen
        ):
            frame = F(self, self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("LoginScreen")  # İlk açılan ekran

    def show_frame(self, name):
        print("Görüntülenmek istenen ekran:", name)
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
