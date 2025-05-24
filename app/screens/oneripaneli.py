from PyQt5 import QtWidgets, QtGui, QtCore
import requests
from io import BytesIO
from PIL import Image, ImageQt

class OneriPaneliScreen(QtWidgets.QWidget):
    def __init__(self, stacked_widget=None, emotion="mutlu"):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.emotion = emotion
        self.film_index = 0
        self.filmler = []
        self.film_pixmap = None

        self.build_ui()
        self.load_filmler()

    def build_ui(self):
        self.setStyleSheet("background-color: #fffbe9;")
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Üst başlık ve geri butonu
        top_bar = QtWidgets.QHBoxLayout()

        back_btn = QtWidgets.QPushButton("← Geri")
        back_btn.setStyleSheet("background-color: transparent; border: none; color: #b4462b; font: bold 12px 'Arial';")
        back_btn.clicked.connect(self.go_back)
        top_bar.addWidget(back_btn, alignment=QtCore.Qt.AlignLeft)

        main_layout.addLayout(top_bar)

        title = QtWidgets.QLabel("Film Serisi")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font: 18px 'Brush Script MT'; background-color: #f0d58c; color: #b4462b;")
        main_layout.addWidget(title)

        self.film_frame = QtWidgets.QHBoxLayout()

        self.left_btn = QtWidgets.QPushButton("‹")
        self.left_btn.setStyleSheet("background-color: transparent; font: 14px; color: #b4462b;")
        self.left_btn.clicked.connect(self.geri_film)
        self.film_frame.addWidget(self.left_btn)

        self.film_content = QtWidgets.QVBoxLayout()

        self.film_label = QtWidgets.QLabel()
        self.film_label.setAlignment(QtCore.Qt.AlignCenter)
        self.film_content.addWidget(self.film_label)

        self.film_ad_label = QtWidgets.QLabel()
        self.film_ad_label.setStyleSheet("font: bold 10px 'Arial'; color: black;")
        self.film_ad_label.setAlignment(QtCore.Qt.AlignCenter)
        self.film_content.addWidget(self.film_ad_label)

        self.film_overview_label = QtWidgets.QLabel()
        self.film_overview_label.setWordWrap(True)
        self.film_overview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.film_overview_label.setStyleSheet("font: 10px 'Arial'; color: black;")
        self.film_content.addWidget(self.film_overview_label)

        self.film_frame.addLayout(self.film_content)

        self.right_btn = QtWidgets.QPushButton("›")
        self.right_btn.setStyleSheet("background-color: transparent; font: 14px; color: #b4462b;")
        self.right_btn.clicked.connect(self.ileri_film)
        self.film_frame.addWidget(self.right_btn)

        main_layout.addLayout(self.film_frame)

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(2)  # Örnek: Ana ekran index

    def load_filmler(self):
        try:
            response = requests.get("http://127.0.0.1:8000/api/recommendations", params={"emotion": self.emotion})
            response.raise_for_status()
            data = response.json()
            self.filmler = data.get("recommendations", [])
            self.guncelle_film()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Film önerileri alınamadı: {e}")
            self.filmler = []

    def guncelle_film(self):
        if not self.filmler:
            self.film_ad_label.setText("Film bulunamadı.")
            self.film_overview_label.setText("")
            self.film_label.clear()
            self.film_label.setText("[Görsel Yok]")
            return

        film = self.filmler[self.film_index]
        try:
            response = requests.get(film["poster"])
            img = Image.open(BytesIO(response.content)).resize((100, 140))
            qimage = ImageQt.ImageQt(img)
            self.film_pixmap = QtGui.QPixmap.fromImage(qimage)
            self.film_label.setPixmap(self.film_pixmap)
        except:
            self.film_label.setText("[Görsel Yok]")

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
