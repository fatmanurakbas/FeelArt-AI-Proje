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
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)

        self.avatar_label = QtWidgets.QLabel()
        scroll_layout.addWidget(self.avatar_label, alignment=QtCore.Qt.AlignCenter)
        self.update_avatar()

        select_btn = QtWidgets.QPushButton("Fotoğraf Seç")
        select_btn.clicked.connect(self.select_photo)
        scroll_layout.addWidget(select_btn)

        title = QtWidgets.QLabel("Profil")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font: bold 16px;")
        scroll_layout.addWidget(title)

        profile_box = QtWidgets.QGroupBox("Kullanıcı Bilgileri")
        profile_layout = QtWidgets.QFormLayout(profile_box)

        self.name_input = QtWidgets.QLineEdit(self.name)
        self.email_input = QtWidgets.QLineEdit(self.email)

        profile_layout.addRow("Ad:", self.name_input)
        profile_layout.addRow("E-posta:", self.email_input)

        save_btn = QtWidgets.QPushButton("Profili Kaydet")
        save_btn.clicked.connect(self.save_profile)
        profile_layout.addRow(save_btn)

        scroll_layout.addWidget(profile_box)

        settings_box = QtWidgets.QGroupBox("Ayarlar")
        settings_layout = QtWidgets.QVBoxLayout(settings_box)

        pw_btn = QtWidgets.QPushButton("Şifre Değiştir")
        lang_btn = QtWidgets.QPushButton("Dil Seçimi")
        clear_btn = QtWidgets.QPushButton("Geçmişi Temizle")
        clear_btn.clicked.connect(self.clear_history)

        settings_layout.addWidget(pw_btn)
        settings_layout.addWidget(lang_btn)
        settings_layout.addWidget(clear_btn)

        scroll_layout.addWidget(settings_box)

        nav_layout = QtWidgets.QHBoxLayout()
        home_btn = QtWidgets.QPushButton("Ana Sayfa")
        logout_btn = QtWidgets.QPushButton("Çıkış")
        home_btn.clicked.connect(self.go_home)
        logout_btn.clicked.connect(QtWidgets.qApp.quit)
        nav_layout.addWidget(home_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(logout_btn)

        scroll_layout.addLayout(nav_layout)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

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
