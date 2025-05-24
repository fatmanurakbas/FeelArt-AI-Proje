
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QComboBox, QPushButton
from PIL import Image, ImageQt, ImageDraw
import json
import os

USER_DATA_PATH = "user_data.json"

def load_user_data():
    if not os.path.exists(USER_DATA_PATH):
        return {"name": "", "email": "", "profile_image": "", "history": [], "language": "Türkçe", "theme": "light"}
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
        self.language = self.data.get("language", "Türkçe")
        self.theme = self.data.get("theme", "light")

        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        self.setFixedSize(420, 560)
        bg_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../assets/FeelArt.png"))

        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(bg_path)))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

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

        self.avatar_label = QtWidgets.QLabel()
        self.avatar_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.avatar_label)

        self.name_label = QtWidgets.QLabel(self.name)
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setStyleSheet("color: #7b4caf; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.name_label)

        form_layout = QtWidgets.QFormLayout()
        self.name_input = QtWidgets.QLineEdit(self.name)
        self.email_input = QtWidgets.QLineEdit(self.email)
        form_layout.addRow("Ad:", self.name_input)
        form_layout.addRow("E-posta:", self.email_input)
        layout.addLayout(form_layout)

        self.update_avatar()

        layout.addWidget(self.icon_button("📸 Fotoğraf Seç", self.select_photo))
        layout.addWidget(self.icon_button("💾 Profili Kaydet", self.save_profile, primary=True))

        settings_layout = QtWidgets.QVBoxLayout()
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Türkçe", "English", "Español"])
        self.language_combo.setCurrentText(self.language)
        self.language_combo.currentTextChanged.connect(self.change_language)
        settings_layout.addWidget(self.label_with_icon("🌍 Dil Seçimi"))
        settings_layout.addWidget(self.language_combo)
        settings_layout.addWidget(self.icon_button("🌗 Tema Değiştir", self.toggle_theme))
        settings_layout.addWidget(self.icon_button("🗑️ Geçmişi Temizle", self.clear_history))
        layout.addLayout(settings_layout)

        nav_layout = QtWidgets.QHBoxLayout()
        nav_layout.addWidget(self.icon_button("🏠 Ana Sayfa", self.go_home))
        nav_layout.addStretch()
        nav_layout.addWidget(self.icon_button("🚪 Çıkış", QtWidgets.qApp.quit))
        layout.addLayout(nav_layout)

    def icon_button(self, text, handler=None, primary=False):
        btn = QPushButton(text)
        if handler:
            btn.clicked.connect(handler)
        btn.setStyleSheet(f"""
            QPushButton {{
                padding: 10px;
                border-radius: 18px;
                font-weight: bold;
                font-size: 14px;
                color: {'white' if primary else '#7b4caf'};
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 {'#c77dff' if primary else '#fbeaff'},
                    stop:1 {'#ffafcc' if primary else '#ffe5ec'}
                );
                border: none;
            }}
            QPushButton:hover {{
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 {'#b86ee0' if primary else '#f5d6ff'},
                    stop:1 {'#ff90b3' if primary else '#ffc9dc'}
                );
            }}
        """)
        return btn

    def label_with_icon(self, text):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet("font-weight: bold; color: #7b4caf;")
        return label

    def update_avatar(self):
        if self.profile_image_path and os.path.exists(self.profile_image_path):
            try:
                img = Image.open(self.profile_image_path).convert("RGBA").resize((100, 100))
                mask = Image.new("L", (100, 100), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 100, 100), fill=255)
                img.putalpha(mask)
                qimage = ImageQt.ImageQt(img)
                pixmap = QtGui.QPixmap.fromImage(qimage)
                self.avatar_label.setPixmap(pixmap)
            except Exception as e:
                print("Resim yüklenemedi:", e)
                self.avatar_label.setText("[Resim Yüklenemedi]")
        else:
            self.avatar_label.setText("[Profil Fotoğrafı Yok]")

        self.name_label.setText(self.name_input.text())

    def select_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Fotoğraf Seç", "", "Resimler (*.jpg *.png *.jpeg)")
        if file_path:
            self.profile_image_path = file_path
            self.update_avatar()

    def save_profile(self):
        self.data["name"] = self.name_input.text()
        self.data["email"] = self.email_input.text()
        self.data["profile_image"] = self.profile_image_path
        self.data["language"] = self.language
        self.data["theme"] = self.theme
        save_user_data(self.data)
        self.update_avatar()
        QMessageBox.information(self, "Başarılı", "Profil başarıyla güncellendi.")

    def change_language(self, lang):
        self.language = lang

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        if self.theme == "dark":
            self.container.setStyleSheet("background-color: rgba(40, 40, 40, 200); border-radius: 20px; color: white;")
        else:
            self.container.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 20px; color: black;")

    def clear_history(self):
        self.data["history"] = []
        save_user_data(self.data)
        QMessageBox.information(self, "Geçmiş Silindi", "Tüm geçmiş başarıyla temizlendi.")

    def go_home(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(2)
