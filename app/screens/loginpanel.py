from PyQt5 import QtWidgets, QtGui, QtCore
import os

class LoginPanelScreen(QtWidgets.QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setFixedSize(420, 560)

        # 🎨 Arka Plan Görseli
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, "FeelArt.png")

        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setPixmap(QtGui.QPixmap(bg_path).scaled(420, 560, QtCore.Qt.KeepAspectRatioByExpanding))
        self.bg_label.setGeometry(0, 0, 420, 560)

        # 🌟 Form Kutusu
        self.form = QtWidgets.QWidget(self)
        self.form.setGeometry(40, 110, 340, 360)
        self.form.setStyleSheet("background-color: rgba(255, 255, 255, 160); border-radius: 20px;")

        layout = QtWidgets.QVBoxLayout(self.form)
        layout.setSpacing(15)

        # 🔙 Geri Butonu
        back_btn = QtWidgets.QPushButton("←")
        back_btn.setCursor(QtCore.Qt.PointingHandCursor)
        back_btn.setStyleSheet("background-color: transparent; border: none; font: 16px 'Arial'; color: #b4462b;")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn, alignment=QtCore.Qt.AlignLeft)

        # Başlık
        title = QtWidgets.QLabel("E-posta ile Giriş")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #7b4caf;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        """)
        layout.addWidget(title)

        # 📧 E-posta
        self.entry_email = QtWidgets.QLineEdit()
        self.entry_email.setPlaceholderText("E-posta")
        self.entry_email.setStyleSheet(self.input_style())
        layout.addWidget(self.entry_email)

        # 🔒 Şifre
        self.entry_pass = QtWidgets.QLineEdit()
        self.entry_pass.setPlaceholderText("Şifre")
        self.entry_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.entry_pass.setStyleSheet(self.input_style())
        layout.addWidget(self.entry_pass)

        # 🔐 Şifremi Unuttum
        forgot = QtWidgets.QLabel("<u>Şifremi Unuttum!</u>")
        forgot.setStyleSheet("color: #7b4caf; font: italic 10px 'Arial';")
        forgot.setAlignment(QtCore.Qt.AlignRight)
        forgot.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        forgot.mousePressEvent = lambda e: self.stacked_widget.setCurrentIndex(3)
        layout.addWidget(forgot)


        # 🔓 Giriş Yap Butonu
        login_btn = QtWidgets.QPushButton("Giriş Yap")
        login_btn.setCursor(QtCore.Qt.PointingHandCursor)
        login_btn.setStyleSheet(self.button_style())
        login_btn.clicked.connect(self.login_action)
        layout.addWidget(login_btn)

    def input_style(self):
        return """
            QLineEdit {
                background-color: white;
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

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(0)  # Ana giriş ekranı

    def login_action(self):
        email = self.entry_email.text().strip()
        password = self.entry_pass.text().strip()

        if email == "a@a.com" and password == "1":
            self.stacked_widget.setCurrentWidget(self.stacked_widget.main_screen)
        else:
            QtWidgets.QMessageBox.critical(self, "Hata", "Geçersiz e-posta ya da şifre.")
