from PyQt5.QtWidgets import QApplication, QStackedWidget, QMessageBox
from screens.login import LoginScreen
from screens.loginpanel import LoginPanelScreen
from screens.signup_screen import SignupScreen
from screens.forgot_password import ForgotPasswordScreen
from screens.anasayfa import MainScreen
from screens.gallery import GalleryScreen
from screens.oneripaneli import OneriPaneliScreen
from screens.kaydedilenler import BookmarksScreen
from screens.begeniler import LikesScreen
from screens.profil import ProfileScreen
import json
import os

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FeelArt")
        self.setFixedSize(420, 560)

        # Ortak veri listeleri
        self.saved_images = []
        self.liked_images = []

        # JSON verilerini yükle
        self.load_data()

        # Ekranları oluştur ve referans vererek sırayla ekle
        self.login_screen = LoginScreen(self)
        self.login_panel_screen = LoginPanelScreen(self)
        self.signup_screen = SignupScreen(self)
        self.forgot_password_screen = ForgotPasswordScreen(self)
        self.main_screen = MainScreen(self)
        self.gallery_screen = GalleryScreen(stacked_widget=self, main_window=self, emotion_text="mutlu")
        self.oneri_screen = OneriPaneliScreen(self)
        self.bookmarks_screen = BookmarksScreen(self, self)
        self.likes_screen = LikesScreen(self, self)
        self.profile_screen = ProfileScreen(self, self)

        # Stack içine ekle
        self.addWidget(self.login_screen)            # index 0
        self.addWidget(self.login_panel_screen)      # index 1
        self.addWidget(self.main_screen)             # index 2
        self.addWidget(self.forgot_password_screen)  # index 3
        self.addWidget(self.signup_screen)           # index 4
        self.addWidget(self.gallery_screen)          # index 5
        self.addWidget(self.oneri_screen)            # index 6
        self.addWidget(self.bookmarks_screen)        # index 7
        self.addWidget(self.likes_screen)            # index 8
        self.addWidget(self.profile_screen)          # index 9

        # Başlangıç ekranı
        self.setCurrentWidget(self.login_screen)

    def load_data(self):
        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.saved_images = data.get("saved_images", [])
                self.liked_images = data.get("liked_images", [])
        except FileNotFoundError:
            # Dosya yoksa boş listelerle başla
            self.saved_images = []
            self.liked_images = []
        except Exception as e:
            print("Veri yüklenirken hata:", e)
            self.saved_images = []
            self.liked_images = []

    def save_data(self):
        data = {
            "saved_images": self.saved_images,
            "liked_images": self.liked_images
        }
        try:
            with open("user_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print("Veri kaydedilirken hata:", e)

    def switch_screen(self, screen_widget):
        self.setCurrentWidget(screen_widget)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
