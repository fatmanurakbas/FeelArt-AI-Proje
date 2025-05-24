from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os
import subprocess

class LoginScreen(QtWidgets.QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("FeelArt")
        self.setFixedSize(420, 560)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, "FeelArt.png")

        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setPixmap(QtGui.QPixmap(bg_path).scaled(420, 560, QtCore.Qt.KeepAspectRatioByExpanding))
        self.bg_label.setGeometry(0, 0, 420, 560)

        # Saydam kutu
        self.form = QtWidgets.QWidget(self)
        self.form.setGeometry(40, 160, 340, 250)
        self.form.setStyleSheet("background-color: rgba(255, 255, 255, 160); border-radius: 20px;")

        layout = QtWidgets.QVBoxLayout(self.form)
        layout.setSpacing(20)

        # Başlık
        title = QtWidgets.QLabel("FeelArt")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 40px;
            font-weight: bold;
            font-style: italic;
            color: #7b4caf;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        """)
        layout.addWidget(title)

        # Giriş Butonu
        giris_btn = QtWidgets.QPushButton("Giriş Yap")
        giris_btn.clicked.connect(self.goto_login)
        giris_btn.setStyleSheet(self.button_style())
        layout.addWidget(giris_btn)

        # Kayıt Butonu
        kayit_btn = QtWidgets.QPushButton("Kayıt Ol")
        kayit_btn.clicked.connect(self.goto_signup)
        kayit_btn.setStyleSheet(self.button_style())
        layout.addWidget(kayit_btn)

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

    def goto_login(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(1)  # Giriş ekranı index

    def goto_signup(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(4)  # Kayıt ekranı index

