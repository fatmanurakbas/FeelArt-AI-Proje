from tkinter import Tk
from PyQt5.QtWidgets import QApplication, QStackedWidget
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


class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FeelArt")
        self.setFixedSize(420, 560)
        

        # Ekranları oluştur ve sırayla ekle
        self.login_screen = LoginScreen(self)
        self.login_panel_screen = LoginPanelScreen(self)
        self.signup_screen = SignupScreen(self)
        self.forgot_password_screen = ForgotPasswordScreen(self)
        self.main_screen = MainScreen(self)
        self.gallery_screen = GalleryScreen(self)
        self.oneri_screen = OneriPaneliScreen(self)
        self.bookmarks_screen = BookmarksScreen(self)
        self.likes_screen = LikesScreen(self)
        self.profile_screen = ProfileScreen(self)
        
        


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

        self.setCurrentWidget(self.login_screen)
                # MainScreen doğru şekilde başlatılıyor
    def switch_screen(self, screen_widget):
        self.setCurrentWidget(screen_widget)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())