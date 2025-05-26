from PyQt5 import QtWidgets, QtGui, QtCore
import requests
from PIL import Image
from io import BytesIO
import os
from PIL import Image
from PIL import ImageQt
class OneriPaneliScreen(QtWidgets.QWidget):
    def __init__(self, stacked_widget=None, emotion="mutlu"):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.emotion = emotion
        self.film_index = 0
        self.filmler = []

        self.init_ui()
        self.load_filmler()

    def init_ui(self):
        self.setFixedSize(420, 700)

        # === Arka plan görseli ===
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, "FeelArt.png")
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setPixmap(QtGui.QPixmap(bg_path).scaled(420, 700, QtCore.Qt.KeepAspectRatioByExpanding))
        self.bg_label.setGeometry(0, 0, 420, 700)

        # === Beyaz cam kutu ===
        self.container = QtWidgets.QWidget(self)
        self.container.setGeometry(20, 70, 380, 520)
        self.container.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 20px;")

        layout = QtWidgets.QVBoxLayout(self.container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # === Geri butonu ===
        back_btn = QtWidgets.QPushButton("← Geri")
        back_btn.setStyleSheet("background-color: transparent; color: #b4462b; font: bold 12px 'Arial'; border: none;")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn, alignment=QtCore.Qt.AlignLeft)

        # === Başlık ===
        title = QtWidgets.QLabel("Film Serisi")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font: bold 20px 'Brush Script MT'; color: #b4462b;")
        layout.addWidget(title)

        # === Film görseli ===
        self.poster_label = QtWidgets.QLabel("[Görsel Yok]")
        self.poster_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.poster_label)

        # === Film adı ===
        self.film_ad_label = QtWidgets.QLabel("")
        self.film_ad_label.setAlignment(QtCore.Qt.AlignCenter)
        self.film_ad_label.setStyleSheet("font: bold 11px 'Arial'; color: #b4462b;")
        layout.addWidget(self.film_ad_label)

        # === Film açıklama ===
        self.film_overview_label = QtWidgets.QLabel("")
        self.film_overview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.film_overview_label.setWordWrap(True)
        self.film_overview_label.setStyleSheet("font: 10px 'Arial'; color: #333;")
        layout.addWidget(self.film_overview_label)

        # === Navigasyon butonları ===
        nav_layout = QtWidgets.QHBoxLayout()

        self.left_btn = QtWidgets.QPushButton("⟨")
        self.right_btn = QtWidgets.QPushButton("⟩")

        for btn in [self.left_btn, self.right_btn]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f5e2a9;
                    font: bold 14px 'Arial';
                    color: #b4462b;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #f0d58c;
                }
            """)

        self.left_btn.clicked.connect(self.geri_film)
        self.right_btn.clicked.connect(self.ileri_film)

        nav_layout.addWidget(self.left_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.right_btn)

        layout.addLayout(nav_layout)

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(2)

    def load_filmler(self):
        try:
            response = requests.get("http://127.0.0.1:8000/api/recommendations", params={"emotion": self.emotion})
            response.raise_for_status()
            data = response.json()
            self.filmler = data.get("recommendations", [])
            self.guncelle_film()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Film önerileri alınamadı:\n{e}")
            self.filmler = []

    def guncelle_film(self):
        if not self.filmler:
            self.film_ad_label.setText("Film bulunamadı.")
            self.film_overview_label.setText("")
            self.poster_label.setText("[Görsel Yok]")
            return

        film = self.filmler[self.film_index]
        try:
            response = requests.get(film["poster"], timeout=5)
            image_data = response.content
            image = Image.open(BytesIO(image_data)).resize((100, 140))
            qimage = ImageQt.ImageQt(image)
            pixmap = QtGui.QPixmap.fromImage(qimage)
            self.poster_label.setPixmap(pixmap)
        except Exception:
            self.poster_label.setText("[Görsel Yok]")

        self.film_ad_label.setText(film["title"])
        self.film_overview_label.setText(film.get("overview", ""))

    def ileri_film(self):
        if self.filmler:
            self.film_index = (self.film_index + 1) % len(self.filmler)
            self.guncelle_film()

    def geri_film(self):
        if self.filmler:
            self.film_index = (self.film_index - 1) % len(self.filmler)
            self.guncelle_film()
