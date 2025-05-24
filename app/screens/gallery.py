from PyQt5 import QtWidgets, QtGui, QtCore
import requests
import uuid
from io import BytesIO
from PIL import Image, ImageQt

class GalleryScreen(QtWidgets.QWidget):
    def __init__(self, stacked_widget=None, emotion_text="mutlu"):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.emotion = emotion_text
        self.images = []
        self.saved_images = []
        self.liked_images = []

        self.init_ui()
        self.fetch_images()

    def init_ui(self):
        self.setStyleSheet("background-color: #fffbe9;")
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Üst çubuk
        top_bar = QtWidgets.QHBoxLayout()

        back_btn = QtWidgets.QPushButton("←")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #b4462b;
                font: bold 14px 'Arial';
            }
            QPushButton:hover {
                color: #d65c37;
            }
        """)
        back_btn.clicked.connect(self.go_back)
        top_bar.addWidget(back_btn, alignment=QtCore.Qt.AlignLeft)

        title = QtWidgets.QLabel(f"'{self.emotion}' için sanat önerileri")
        title.setStyleSheet("font: bold 14px 'Arial'; color: #b4462b;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        top_bar.addWidget(title)

        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Scrollable area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        self.scroll_area.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_area)

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(2)  # örneğin MainScreen index 2

    def fetch_images(self):
        try:
            response = requests.get(
                "http://127.0.0.1:8000/api/images",
                params={"query": self.emotion, "seed": str(uuid.uuid4())}
            )
            if response.status_code == 200:
                data = response.json()
                image_urls = data.get('images', [])
                for url in image_urls:
                    self.display_image(url)
            else:
                self.add_error_label("Görseller alınamadı.")
        except Exception as e:
            self.add_error_label(f"Bağlantı hatası: {e}")

    def display_image(self, url):
        try:
            img_data = requests.get(url).content
            img = Image.open(BytesIO(img_data)).resize((300, 180))
            qimage = ImageQt.ImageQt(img)
            pixmap = QtGui.QPixmap.fromImage(qimage)

            container = QtWidgets.QWidget()
            container.setStyleSheet("background-color: #fffbe9;")
            vbox = QtWidgets.QVBoxLayout(container)

            img_label = QtWidgets.QLabel()
            img_label.setPixmap(pixmap)
            img_label.setAlignment(QtCore.Qt.AlignCenter)
            vbox.addWidget(img_label)

            btn_box = QtWidgets.QHBoxLayout()

            like_btn = QtWidgets.QPushButton("❤️")
            like_btn.setStyleSheet("background-color: transparent; border: none; font: 12px; color: #e0554a;")
            like_btn.clicked.connect(lambda: self.like_image(url))

            save_btn = QtWidgets.QPushButton("🔖")
            save_btn.setStyleSheet("background-color: transparent; border: none; font: 12px; color: #b4462b;")
            save_btn.clicked.connect(lambda: self.save_image(url))

            btn_box.addWidget(like_btn)
            btn_box.addWidget(save_btn)
            vbox.addLayout(btn_box)

            self.scroll_layout.addWidget(container)
            self.images.append(pixmap)

        except Exception as e:
            self.add_error_label(f"Hata: {e}")

    def add_error_label(self, text):
        error_label = QtWidgets.QLabel(text)
        error_label.setStyleSheet("color: red; font: 11px 'Arial';")
        self.scroll_layout.addWidget(error_label)

    def save_image(self, url):
        if url not in self.saved_images:
            self.saved_images.append(url)
            QtWidgets.QMessageBox.information(self, "Kaydedildi", "Görsel kaydedildi.")
        else:
            QtWidgets.QMessageBox.warning(self, "Zaten kaydedilmiş", "Bu görsel zaten kaydedilmiş.")

    def like_image(self, url):
        if url not in self.liked_images:
            self.liked_images.append(url)
            QtWidgets.QMessageBox.information(self, "Beğenildi", "Görsel beğenildi.")
        else:
            QtWidgets.QMessageBox.warning(self, "Zaten beğenilmiş", "Bu görsel zaten beğenilmiş.")
