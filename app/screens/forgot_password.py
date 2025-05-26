from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5 import QtWidgets, QtGui, QtCore
import os

class ForgotPasswordScreen(QtWidgets.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setFixedSize(420, 700)
        self.setWindowTitle("FeelArt | Şifre Sıfırlama")

        # 🌄 Arka plan resmi
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, "FeelArt.png")
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setPixmap(QtGui.QPixmap(bg_path).scaled(420,700, QtCore.Qt.KeepAspectRatioByExpanding))
        self.bg_label.setGeometry(0, 0, 420, 700)

        # 🪟 Saydam form kutusu
        self.form = QtWidgets.QWidget(self)
        self.form.setGeometry(40, 120, 340, 320)
        self.form.setStyleSheet("background-color: rgba(255, 255, 255, 160); border-radius: 20px;")

        layout = QtWidgets.QVBoxLayout(self.form)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # ⬅️ Geri Butonu
        back_btn = QtWidgets.QPushButton("←")
        back_btn.setCursor(QtCore.Qt.PointingHandCursor)
        back_btn.setStyleSheet("background-color: transparent; border: none; font: 16px 'Arial'; color: #b4462b;")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn, alignment=QtCore.Qt.AlignLeft)

        # 🔒 Başlık
        title = QtWidgets.QLabel("Şifreni mi unuttun?")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #7b4caf;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        """)
        layout.addWidget(title)

        # 📝 Açıklama
        info = QtWidgets.QLabel("E-posta adresini gir,\nşifre sıfırlama bağlantısı gönderilsin.")
        info.setAlignment(QtCore.Qt.AlignCenter)
        info.setStyleSheet("font: 12px 'Arial'; color: gray;")
        layout.addWidget(info)

        # ✉️ E-posta girişi
        self.entry_email = QtWidgets.QLineEdit()
        self.entry_email.setPlaceholderText("E-posta adresiniz")
        self.entry_email.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: none;
                border-radius: 15px;
                padding: 10px;
                font-size: 13px;
                color: #4d3f63;
            }
        """)
        layout.addWidget(self.entry_email)

        # 📤 Gönder Butonu
        send_btn = QtWidgets.QPushButton("Bağlantıyı Gönder")
        send_btn.setCursor(QtCore.Qt.PointingHandCursor)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #a782e6;
                color: white;
                border: none;
                border-radius: 18px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #9d6de0;
            }
        """)
        send_btn.clicked.connect(self.send_reset_link)
        layout.addWidget(send_btn)

    def go_back(self):
        self.stacked_widget.setCurrentIndex(1)  # LoginPanelScreen

    def send_reset_link(self):
        email = self.entry_email.text().strip()
        if email:
            QtWidgets.QMessageBox.information(self, "Şifre Sıfırlama", f"{email} adresine bağlantı gönderildi!")
        else:
            QtWidgets.QMessageBox.warning(self, "Eksik Bilgi", "Lütfen e-posta adresinizi girin.")
