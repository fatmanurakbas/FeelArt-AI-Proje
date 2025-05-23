from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os
import subprocess

class KayitEkrani(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FeelArt | Kayıt Ol")
        self.setFixedSize(420, 560)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, "FeelArt.png")

        if not os.path.exists(bg_path):
            QtWidgets.QMessageBox.critical(self, "HATA", f"Görsel bulunamadı:\n{bg_path}")
            sys.exit()

        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setPixmap(QtGui.QPixmap(bg_path).scaled(420, 560, QtCore.Qt.KeepAspectRatioByExpanding))
        self.bg_label.setGeometry(0, 0, 420, 560)

        self.form = QtWidgets.QWidget(self)
        self.form.setGeometry(40, 100, 340, 380)
        self.form.setStyleSheet("background-color: rgba(255, 255, 255, 160); border-radius: 20px;")

        layout = QtWidgets.QVBoxLayout(self.form)
        layout.setSpacing(15)

        # Başlık
        title = QtWidgets.QLabel("Kayıt Ol")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 38px;
            font-weight: bold;
            font-style: italic;
            color: #7b4caf;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        """)
        layout.addWidget(title)

        # Ad alanı
        self.ad = QtWidgets.QLineEdit()
        self.ad.setPlaceholderText("Ad Soyad")
        self.ad.setStyleSheet(self.input_style())
        layout.addWidget(self.ad)

        # E-posta alanı
        self.email = QtWidgets.QLineEdit()
        self.email.setPlaceholderText("E-posta")
        self.email.setStyleSheet(self.input_style())
        layout.addWidget(self.email)

        # Şifre alanı
        self.sifre = QtWidgets.QLineEdit()
        self.sifre.setPlaceholderText("Şifre")
        self.sifre.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sifre.setStyleSheet(self.input_style())
        layout.addWidget(self.sifre)

        # Kayıt butonu
        kayit = QtWidgets.QPushButton("Kayıt Ol")
        kayit.setStyleSheet(self.button_style())
        kayit.clicked.connect(self.kayit_ol)
        layout.addWidget(kayit)

        # Giriş bağlantısı
        giris = QtWidgets.QPushButton("Zaten hesabın var mı? Giriş yap")
        giris.setCursor(QtCore.Qt.PointingHandCursor)
        giris.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #7b4caf;
                font-size: 12px;
                font-style: italic;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #9c6de4;
            }
        """)
        giris.clicked.connect(self.giris_ekranina_don)
        layout.addWidget(giris, alignment=QtCore.Qt.AlignCenter)

    def input_style(self):
        return """
            QLineEdit {
                background-color: rgba(255, 255, 255, 220);
                border: none;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                color: #4d3f63;
            }
        """

    def button_style(self):
        return """
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
        """

    def kayit_ol(self):
        if not self.ad.text() or not self.email.text() or not self.sifre.text():
            QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")
        else:
            QtWidgets.QMessageBox.information(self, "Başarılı", "Kayıt başarılı!")

    def giris_ekranina_don(self):
        try:
            subprocess.Popen(["python", "login.py"])
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "HATA", f"Giriş ekranı açılamadı:\n{e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pencere = KayitEkrani()
    pencere.show()
    sys.exit(app.exec_())
