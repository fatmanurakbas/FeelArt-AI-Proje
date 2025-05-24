from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PIL import Image, ImageQt
import json
import os

USER_DATA_PATH = "user_data.json"

def load_user_data():
    if not os.path.exists(USER_DATA_PATH):
        return {"name": "", "email": "", "profile_image": "", "history": []}
    with open(USER_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_user_data(data):
    with open(USER_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class ProfileScreen(QtWidgets.QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.data = load_user_data()

        self.name = self.data.get("name", "")
        self.email = self.data.get("email", "")
        self.profile_image_path = self.data.get("profile_image", "")

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(420, 560)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, "FeelArt.png")

        # Background
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setPixmap(QtGui.QPixmap(bg_path).scaled(420, 560, QtCore.Qt.KeepAspectRatioByExpanding))
        self.bg_label.setGeometry(0, 0, 420, 560)

        # Foreground Container
        self.container = QtWidgets.QWidget(self)
        self.container.setGeometry(20, 20, 380, 520)
        self.container.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 20px;")

        layout = QtWidgets.QVBoxLayout(self.container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QtWidgets.QLabel("Profil")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font: bold italic 24px 'Segoe UI'; color: #7b4caf;")
        layout.addWidget(title)

        # Avatar
        self.avatar_label = QtWidgets.QLabel()
        self.avatar_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.avatar_label)
        self.update_avatar()

        select_btn = QtWidgets.QPushButton("Fotoğraf Seç")
        select_btn.clicked.connect(self.select_photo)
        select_btn.setStyleSheet("padding: 6px; background-color: #f5e2a9; font-weight: bold; border-radius: 10px;")
        layout.addWidget(select_btn)

        # User Info
        form_layout = QtWidgets.QFormLayout()
        self.name_input = QtWidgets.QLineEdit(self.name)
        self.email_input = QtWidgets.QLineEdit(self.email)
        form_layout.addRow("Ad:", self.name_input)
        form_layout.addRow("E-posta:", self.email_input)
        layout.addLayout(form_layout)

        save_btn = QtWidgets.QPushButton("Profili Kaydet")
        save_btn.clicked.connect(self.save_profile)
        save_btn.setStyleSheet("padding: 6px; background-color: #a782e6; color: white; font-weight: bold; border-radius: 10px;")
        layout.addWidget(save_btn)

        # Settings
        settings_layout = QtWidgets.QVBoxLayout()
        for text, handler in [("Şifre Değiştir", None), ("Dil Seçimi", None), ("Geçmişi Temizle", self.clear_history)]:
            btn = QtWidgets.QPushButton(text)
            if handler:
                btn.clicked.connect(handler)
            btn.setStyleSheet("padding: 6px; background-color: #f5e2a9; font-weight: bold; border-radius: 10px;")
            settings_layout.addWidget(btn)
        layout.addLayout(settings_layout)

        # Navigation
        nav_layout = QtWidgets.QHBoxLayout()
        home_btn = QtWidgets.QPushButton("Ana Sayfa")
        logout_btn = QtWidgets.QPushButton("Çıkış")
        home_btn.setStyleSheet("background-color: #f0d58c; color: #b4462b; font-weight: bold; border-radius: 8px;")
        logout_btn.setStyleSheet("background-color: #f0d58c; color: #b4462b; font-weight: bold; border-radius: 8px;")
        home_btn.clicked.connect(self.go_home)
        logout_btn.clicked.connect(QtWidgets.qApp.quit)
        nav_layout.addWidget(home_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(logout_btn)
        layout.addLayout(nav_layout)

    def update_avatar(self):
        if self.profile_image_path and os.path.exists(self.profile_image_path):
            try:
                img = Image.open(self.profile_image_path).resize((100, 100))
                qimage = ImageQt.ImageQt(img)
                pixmap = QtGui.QPixmap.fromImage(qimage)
                self.avatar_label.setPixmap(pixmap)
            except:
                self.avatar_label.setText("[Resim Yüklenemedi]")
        else:
            self.avatar_label.setText("[Profil Fotoğrafı Yok]")

    def select_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Fotoğraf Seç", "", "Resimler (*.jpg *.png *.jpeg)")
        if file_path:
            self.profile_image_path = file_path
            self.update_avatar()

    def save_profile(self):
        self.data["name"] = self.name_input.text()
        self.data["email"] = self.email_input.text()
        self.data["profile_image"] = self.profile_image_path
        save_user_data(self.data)
        QMessageBox.information(self, "Başarılı", "Profil başarıyla güncellendi.")

    def clear_history(self):
        self.data["history"] = []
        save_user_data(self.data)
        QMessageBox.information(self, "Geçmiş Silindi", "Tüm geçmiş başarıyla temizlendi.")

    def go_home(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(2)
