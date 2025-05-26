import os
import uuid
import requests
from io import BytesIO
from PyQt5 import QtWidgets, QtGui, QtCore

class GalleryScreen(QtWidgets.QWidget):
    def __init__(self, stacked_widget=None, main_window=None, emotion_text="mutlu"):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window
        self.emotion = emotion_text
        self.images = []

        self.init_ui()
        self.fetch_images()

    def init_ui(self):
        self.setFixedSize(420, 700)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, "FeelArt.png")

        # Arka plan
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setPixmap(QtGui.QPixmap(bg_path).scaled(420,700, QtCore.Qt.KeepAspectRatioByExpanding))
        self.bg_label.setGeometry(0, 0, 420, 700)

        # Yarı saydam container
        self.container = QtWidgets.QWidget(self)
        self.container.setGeometry(20, 70, 380, 520)
        self.container.setStyleSheet("background-color: rgba(255,255,255,200); border-radius: 20px;")

        layout = QtWidgets.QVBoxLayout(self.container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Üst bar
        top_bar = QtWidgets.QHBoxLayout()
        back_btn = QtWidgets.QPushButton("←")
        back_btn.setStyleSheet("background-color: transparent; border: none; font: bold 16px; color: #b4462b;")
        back_btn.clicked.connect(self.go_back)
        top_bar.addWidget(back_btn, alignment=QtCore.Qt.AlignLeft)

        title = QtWidgets.QLabel("Sanat Galerisi")
        title.setStyleSheet("font: bold 16px 'Arial'; color: #b4462b;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        top_bar.addWidget(title)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        # Scroll alanı
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        self.scroll_area.setWidget(scroll_content)
        layout.addWidget(self.scroll_area)

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(2)

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
            image = QtGui.QImage()
            image.loadFromData(img_data)
            pixmap = QtGui.QPixmap.fromImage(image).scaled(300, 180, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

            container = QtWidgets.QWidget()
            container.setStyleSheet("background-color: #fffbe9; border-radius: 12px;")
            vbox = QtWidgets.QVBoxLayout(container)
            vbox.setContentsMargins(5, 5, 5, 5)
            vbox.setSpacing(5)

            img_label = QtWidgets.QLabel()
            img_label.setPixmap(pixmap)
            img_label.setAlignment(QtCore.Qt.AlignCenter)
            vbox.addWidget(img_label)

            btn_box = QtWidgets.QHBoxLayout()
            like_btn = QtWidgets.QPushButton("❤️")
            like_btn.setStyleSheet("background-color: transparent; border: none; font: 14px; color: #e0554a;")
            like_btn.clicked.connect(lambda: self.like_image(url))

            save_btn = QtWidgets.QPushButton("🔖")
            save_btn.setStyleSheet("background-color: transparent; border: none; font: 14px; color: #b4462b;")
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
        try:
            if not self.main_window:
                QtWidgets.QMessageBox.warning(self, "Hata", "Ana pencere tanımlı değil!")
                return

            if url not in self.main_window.saved_images:
                self.main_window.saved_images.append(url)
                QtWidgets.QMessageBox.information(self, "Kaydedildi", "Görsel kaydedildi.")

                # JSON'a kaydet:
                self.main_window.save_data()

                # Bookmarks ekranını güncelle
                if self.main_window.bookmarks_screen:
                    print("BookmarksScreen güncelleniyor...")
                    self.main_window.bookmarks_screen.update_saved_images(self.main_window.saved_images)
                else:
                    QtWidgets.QMessageBox.warning(self, "Hata", "Bookmarks ekranı tanımlı değil!")
            else:
                QtWidgets.QMessageBox.information(self, "Zaten kaydedilmiş", "Bu görsel zaten kaydedilmiş.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata!", f"Bir hata oluştu:\n{e}")

    def like_image(self, url):
        try:
            if self.main_window and hasattr(self.main_window, "liked_images"):
                if url not in self.main_window.liked_images:
                    self.main_window.liked_images.append(url)
                    QtWidgets.QMessageBox.information(self, "Beğenildi", "Görsel beğenildi.")

                    # JSON'a kaydet
                    if hasattr(self.main_window, "save_data"):
                        self.main_window.save_data()

                    # Likes ekranını güncelle
                    if hasattr(self.main_window, "likes_screen"):
                        self.main_window.likes_screen.update_liked_images(self.main_window.liked_images)
                    else:
                        QtWidgets.QMessageBox.warning(self, "Hata", "Beğenilenler ekranı tanımlı değil!")
                else:
                    QtWidgets.QMessageBox.warning(self, "Zaten beğenilmiş", "Bu görsel zaten beğenilmiş.")
            else:
                QtWidgets.QMessageBox.warning(self, "Hata", "Ana pencere tanımlı değil!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata!", f"Bir hata oluştu:\n{e}")
