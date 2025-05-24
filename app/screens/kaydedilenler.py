from PyQt5 import QtWidgets, QtGui, QtCore
import requests
from io import BytesIO
from PIL import Image, ImageQt

class BookmarksScreen(QtWidgets.QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.saved_images = []
        self.images = []
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #fffbe9;")
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Üst başlık
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

        # Scrollable alan
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        self.scroll_area.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_area)

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(2)  # örneğin MainScreen index

    def update_saved_images(self, image_urls):
        self.saved_images = image_urls

        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.images = []
        for url in self.saved_images:
            try:
                img_data = requests.get(url).content
                img = Image.open(BytesIO(img_data)).resize((280, 160))
                qimage = ImageQt.ImageQt(img)
                pixmap = QtGui.QPixmap.fromImage(qimage)

                container = QtWidgets.QWidget()
                container.setStyleSheet("background-color: #fffbe9;")
                vbox = QtWidgets.QVBoxLayout(container)

                img_label = QtWidgets.QLabel()
                img_label.setPixmap(pixmap)
                img_label.setAlignment(QtCore.Qt.AlignCenter)
                vbox.addWidget(img_label)

                remove_btn = QtWidgets.QPushButton("Kaydı İptal Et")
                remove_btn.setStyleSheet("background-color: transparent; color: red; font: 11px 'Arial';")
                remove_btn.clicked.connect(lambda _, u=url: self.remove_saved_image(u))
                vbox.addWidget(remove_btn)

                self.scroll_layout.addWidget(container)
                self.images.append(pixmap)

            except Exception as e:
                error_label = QtWidgets.QLabel(f"Hata: {e}")
                error_label.setStyleSheet("color: red; font: 11px 'Arial';")
                self.scroll_layout.addWidget(error_label)

    def remove_saved_image(self, url):
        if url in self.saved_images:
            self.saved_images.remove(url)
            self.update_saved_images(self.saved_images)