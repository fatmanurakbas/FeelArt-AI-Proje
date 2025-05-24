from PyQt5 import QtWidgets, QtGui, QtCore
import json
import os
from screens.gallery import GalleryScreen
from screens.oneripaneli import OneriPaneliScreen

class MainScreen(QtWidgets.QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.sidebar_open = False
        self.history_labels = []

        self.setFixedSize(420, 560)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, "FeelArt.png")

        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setPixmap(QtGui.QPixmap(bg_path).scaled(420, 560, QtCore.Qt.KeepAspectRatioByExpanding))
        self.bg_label.setGeometry(0, 0, 420, 560)

        # Sidebar Frame
        self.sidebar_frame = QtWidgets.QFrame(self)
        self.sidebar_frame.setGeometry(-200, 0, 200, 560)
        self.sidebar_frame.setStyleSheet("background-color: rgba(245, 245, 245, 245); border-right: 2px solid #ccc;")

        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(12, 20, 12, 20)
        self.sidebar_layout.setSpacing(12)

        # Close Button inside Sidebar
        self.close_btn = QtWidgets.QPushButton("≡")
        self.close_btn.setStyleSheet("background-color: transparent; font: bold 14px 'Arial'; color: #7b4caf;")
        self.close_btn.clicked.connect(self.toggle_sidebar)
        self.sidebar_layout.addWidget(self.close_btn, alignment=QtCore.Qt.AlignLeft)

        self.sidebar_title = QtWidgets.QLabel("Sohbet Geçmişi")
        self.sidebar_title.setStyleSheet("font-weight: bold; color: #7b4caf; font: 13px 'Arial';")
        self.sidebar_layout.addWidget(self.sidebar_title)

        self.history_scroll = QtWidgets.QScrollArea()
        self.history_scroll.setWidgetResizable(True)
        self.history_inner = QtWidgets.QWidget()
        self.history_vlayout = QtWidgets.QVBoxLayout(self.history_inner)
        self.history_scroll.setWidget(self.history_inner)
        self.sidebar_layout.addWidget(self.history_scroll)

        self.load_history()

        # Main container
        self.container = QtWidgets.QWidget(self)
        self.container.setGeometry(20, 20, 380, 520)
        self.container.setStyleSheet("background-color: rgba(255, 255, 255, 170); border-radius: 20px;")

        main_layout = QtWidgets.QVBoxLayout(self.container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Top Bar
        top_bar = QtWidgets.QHBoxLayout()
        self.menu_btn = QtWidgets.QPushButton("≡")
        self.menu_btn.setFixedWidth(30)
        self.menu_btn.setStyleSheet("background-color: transparent; font: bold 16px 'Arial'; color: #7b4caf;")
        self.menu_btn.clicked.connect(self.toggle_sidebar)
        top_bar.addWidget(self.menu_btn)

        top_bar.addStretch()
        profile_btn = QtWidgets.QPushButton("👤")
        profile_btn.setFixedWidth(30)
        profile_btn.setStyleSheet("background-color: transparent; font: 14px 'Arial'; color: #7b4caf;")
        profile_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(9))
        top_bar.addWidget(profile_btn)
        main_layout.addLayout(top_bar)

        title = QtWidgets.QLabel("FeelArt")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font: bold italic 30px 'Segoe UI'; color: #7b4caf;")
        main_layout.addWidget(title)

        self.search_entry = QtWidgets.QLineEdit()
        self.search_entry.setPlaceholderText("Senin ruh halin bugün nasıl?")
        self.search_entry.setStyleSheet("padding: 10px; font: 12px 'Arial'; background-color: white; border-radius: 10px;")
        main_layout.addWidget(self.search_entry)

        for text, handler in [("Galeri Oluştur", self.add_action), ("Film Öner", self.get_recommendations)]:
            btn = QtWidgets.QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #a782e6;
                    font: bold 13px 'Arial';
                    color: white;
                    border-radius: 18px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #9b6bd8;
                }
            """)
            btn.clicked.connect(handler)
            main_layout.addWidget(btn)

        bottom_nav = QtWidgets.QHBoxLayout()
        for label, index in [("Kaydedilenler", 7), ("Beğeniler", 8)]:
            nav_btn = QtWidgets.QPushButton(label)
            nav_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0d58c;
                    color: #b4462b;
                    font: 11px 'Arial';
                    padding: 6px;
                    border-radius: 8px;
                }
            """)
            nav_btn.clicked.connect(lambda _, i=index: self.stacked_widget.setCurrentIndex(i))
            bottom_nav.addWidget(nav_btn)
        main_layout.addLayout(bottom_nav)

    def toggle_sidebar(self):
        anim = QtCore.QPropertyAnimation(self.sidebar_frame, b"geometry")
        anim.setDuration(300)
        if self.sidebar_open:
            anim.setStartValue(QtCore.QRect(0, 0, 200, 560))
            anim.setEndValue(QtCore.QRect(-200, 0, 200, 560))
        else:
            anim.setStartValue(QtCore.QRect(-200, 0, 200, 560))
            anim.setEndValue(QtCore.QRect(0, 0, 200, 560))
        anim.start()
        self.sidebar_open = not self.sidebar_open
        self.anim = anim

    def _analyze_emotion(self, text):
        emotion_map = {
            "üzgün": ["üzgün", "mutsuz", "depresif", "hüzünlü"],
            "mutlu": ["mutlu", "neşeli", "keyifli", "sevinçli"],
            "kızgın": ["kızgın", "sinirli", "öfkeli"],
            "heyecanlı": ["heyecanlı", "enerjik", "coşkulu"],
            "korkmuş": ["korkmuş", "tedirgin", "endişeli"],
            "şaşkın": ["şok", "şaşırmış"],
            "tiksinti": ["tiksinti", "iğrenme"]
        }
        for emotion, keywords in emotion_map.items():
            if any(k in text.lower() for k in keywords):
                return emotion
        return "nötr"

    def add_action(self):
        text = self.search_entry.text().strip()
        if not text:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen bir duygu durumu girin.")
            return
        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}
        history = data.get("history", [])
        if text in history:
            history.remove(text)
        history.insert(0, text)
        data["history"] = history[:10]
        with open("user_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        self.load_history()
        g = GalleryScreen(self.stacked_widget, text)
        self.stacked_widget.addWidget(g)
        self.stacked_widget.setCurrentWidget(g)
        self.search_entry.clear()

    def load_history(self):
        for l in self.history_labels:
            l.setParent(None)
        self.history_labels.clear()
        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                items = json.load(f).get("history", [])
        except:
            items = []
        for item in items:
            lbl = QtWidgets.QLabel(f"• {item}")
            lbl.setStyleSheet("color: black; font: 11px 'Arial'; padding: 2px;")
            lbl.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            lbl.mousePressEvent = lambda e, t=item: self.open_gallery_from_history(t)
            self.history_vlayout.addWidget(lbl)
            self.history_labels.append(lbl)

    def open_gallery_from_history(self, emotion_text):
        g = GalleryScreen(self.stacked_widget, emotion_text)
        self.stacked_widget.addWidget(g)
        self.stacked_widget.setCurrentWidget(g)
        self.search_entry.clear()

    def get_recommendations(self):
        txt = self.search_entry.text().strip()
        if not txt:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen bir duygu durumu girin.")
            return
        emo = self._analyze_emotion(txt)
        if emo == "nötr":
            QtWidgets.QMessageBox.information(self, "Bilgi", "Duygusal analiz yapılamadı.")
            return
        o = OneriPaneliScreen(self.stacked_widget, emo)
        self.stacked_widget.addWidget(o)
        self.stacked_widget.setCurrentWidget(o)
