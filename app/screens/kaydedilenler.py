from PyQt5 import QtWidgets, QtGui, QtCore
import requests
import os

class BookmarksScreen(QtWidgets.QWidget):
    def __init__(self, stacked_widget=None, main_window=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window
        self.saved_images = []
        self.images = []
        self.init_ui()

    def init_ui(self):
        # Arka plan
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, "FeelArt.png")
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setPixmap(QtGui.QPixmap(bg_path).scaled(420, 560, QtCore.Qt.KeepAspectRatioByExpanding))
        self.bg_label.setGeometry(0, 0, 420, 560)

        # Yarı saydam container
        self.container = QtWidgets.QWidget(self)
        self.container.setGeometry(15, 15, 390, 530)
        self.container.setStyleSheet("background-color: rgba(255,255,255,200); border-radius: 20px;")

        # Ana düzen
        main_layout = QtWidgets.QVBoxLayout(self.container)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Üst bar
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

        title = QtWidgets.QLabel("Kaydedilen Görseller")
        title.setStyleSheet("font: bold 14px 'Arial'; color: #b4462b;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Scroll alanı
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        self.scroll_area.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_area)

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(2)

    def update_saved_images(self, image_urls):
        self.saved_images = image_urls

        # Eski widget'ları temizle
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.images = []
        for url in self.saved_images:
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    print(f"HTTP {response.status_code} hatası: {url}")  # Sadece konsolda göster
                    continue  # Bu URL'yi atla

                img_data = response.content
                image = QtGui.QImage()
                if not image.loadFromData(img_data):
                        print(f"Resim verisi tanımlanamadı: {url}")
                        continue  # Bu URL'yi atla
                pixmap = QtGui.QPixmap.fromImage(image).scaled(
                    280, 160,
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation
                )

                container = QtWidgets.QWidget()
                container.setStyleSheet("background-color: #fffbe9; border-radius: 10px;")
                vbox = QtWidgets.QVBoxLayout(container)
                vbox.setContentsMargins(5, 5, 5, 5)
                vbox.setSpacing(5)

                img_label = QtWidgets.QLabel()
                img_label.setPixmap(pixmap)
                img_label.setAlignment(QtCore.Qt.AlignCenter)
                vbox.addWidget(img_label)

                remove_btn = QtWidgets.QPushButton("Kaydı İptal Et")
                remove_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: red;
                        font: 11px 'Arial';
                        border: none;
                    }
                    QPushButton:hover {
                        text-decoration: underline;
                    }
                """)
                remove_btn.clicked.connect(lambda _, u=url: self.remove_saved_image(u))
                vbox.addWidget(remove_btn, alignment=QtCore.Qt.AlignCenter)

                self.scroll_layout.addWidget(container)
                self.images.append(pixmap)

            except Exception as e:
                print(f"Hata oluştu: {e}")
                continue  # Bu URL'yi atla

    def remove_saved_image(self, url):

        if self.main_window and hasattr(self.main_window, "saved_images"):
            if url in self.main_window.saved_images:
                self.main_window.saved_images.remove(url)
                self.update_saved_images(self.main_window.saved_images)
                self.main_window.save_data()
        else:
            QtWidgets.QMessageBox.warning(self, "Hata", "Ana pencere tanımlı değil!")
