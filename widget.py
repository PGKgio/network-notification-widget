import sys
import textwrap
import requests
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSystemTrayIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QColor, QIcon

SERVER_URL = "http://127.0.0.1:5000/notification"
WIDGET_WIDTH = 300
LINE_LENGTH = 35
MARGIN = 40
ICON_SIZE = 40

def get_local_ip():
    """Vrátí lokální IP adresu v síti 192.168.x.x"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Nepodařilo se zjistit"

class NotificationThread(QThread):
    new_message = pyqtSignal(str)

    def run(self):
        last_msg = None
        while True:
            try:
                r = requests.get(SERVER_URL)
                if r.status_code == 200:
                    msg = r.text.strip()
                    if msg != last_msg:
                        self.new_message.emit(msg)
                        last_msg = msg
            except:
                pass
            self.msleep(3000)

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.expanded = True
        self.stored_msg = ""

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(WIDGET_WIDTH)

        self.bg_color = QColor(30, 30, 30, 200)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        self.ip_label = QLabel("IP: Načítám...")
        self.ip_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.ip_label.setStyleSheet("color: #00ffcc;")
        self.ip_label.setWordWrap(True)

        self.notif_label = QLabel("Žádné zprávy")
        self.notif_label.setFont(QFont("Segoe UI", 11))
        self.notif_label.setStyleSheet("color: white;")
        self.notif_label.setWordWrap(True)

        # Layout pro šipku
        self.circle_layout = QHBoxLayout()
        self.circle_layout.setContentsMargins(0, 10, 0, 0)
        self.circle_layout.setAlignment(Qt.AlignCenter)

        self.toggle_button = QPushButton("–")
        self.toggle_button.setFixedSize(ICON_SIZE, ICON_SIZE)
        self.toggle_button.setStyleSheet(f"""
            QPushButton {{
                border-radius: {ICON_SIZE//2}px;
                background-color: #444;
                color: white;
                font-weight: bold;
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: #666;
            }}
        """)
        self.toggle_button.clicked.connect(self.minimize_to_icon)
        self.circle_layout.addWidget(self.toggle_button)

        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.notif_label)
        self.layout.addLayout(self.circle_layout)
        self.setLayout(self.layout)

        screen_geometry = QApplication.desktop().screenGeometry()
        x = screen_geometry.width() - self.width() - 20
        y = 20
        self.move(x, y)

        self.get_ip()

        self.tray = QSystemTrayIcon(QIcon())
        self.tray.show()

        self.thread = NotificationThread()
        self.thread.new_message.connect(self.notify)
        self.thread.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

    def get_ip(self):
        ip = get_local_ip()
        self.ip_label.setText(f"🌐 IP: {ip}")

    def notify(self, msg):
        if not msg:
            self.notif_label.setText("Žádné zprávy")
            self.stored_msg = ""
            return

        self.stored_msg = msg

        # rozdělit zprávy podle řádků (\n)
        lines = msg.split("\n")
        wrapped_lines = []

        for line in lines:
            text_only = line.split(" (do")[0]
            wrapped = textwrap.wrap(text_only, LINE_LENGTH)
            for i, wline in enumerate(wrapped):
                if i == 0:
                    wrapped_lines.append(f"📢 {wline}")
                else:
                    wrapped_lines.append(f"   {wline}")

        self.notif_label.setText("\n".join(wrapped_lines))

        # systémová notifikace
        self.tray.showMessage("Nová zpráva", msg, QSystemTrayIcon.Information, 5000)

        # pokud je minimalizován, rozbalíme
        if not self.expanded:
            self.restore_from_icon()
        else:
            # pokud je rozbalený, jen aktualizujeme velikost
            self.adjustSize()
            total_height = self.layout.sizeHint().height() + MARGIN
            self.setFixedHeight(total_height)
            self.setFixedWidth(WIDGET_WIDTH)

    def minimize_to_icon(self):
        if self.expanded:
            self.expanded = False
            self.hide()
            self.icon_widget = QWidget()
            self.icon_widget.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
            self.icon_widget.setAttribute(Qt.WA_TranslucentBackground)
            self.icon_widget.setFixedSize(ICON_SIZE, ICON_SIZE)

            btn = QPushButton("⬅", self.icon_widget)
            btn.setGeometry(0, 0, ICON_SIZE, ICON_SIZE)
            btn.setStyleSheet(f"""
                QPushButton {{
                    border-radius: {ICON_SIZE//2}px;
                    background-color: #444;
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
                }}
                QPushButton:hover {{
                    background-color: #666;
                }}
            """)
            btn.clicked.connect(self.restore_from_icon)
            screen_geometry = QApplication.desktop().screenGeometry()
            x = screen_geometry.width() - ICON_SIZE - 20
            y = 20
            self.icon_widget.move(x, y)
            self.icon_widget.show()

    def restore_from_icon(self):
        if not self.expanded:
            self.expanded = True
            if hasattr(self, 'icon_widget'):
                self.icon_widget.close()
                del self.icon_widget
            self.show()
            self.adjustSize()
            total_height = self.layout.sizeHint().height() + MARGIN
            self.setFixedHeight(total_height)
            self.setFixedWidth(WIDGET_WIDTH)
            screen_geometry = QApplication.desktop().screenGeometry()
            x = screen_geometry.width() - self.width() - 20
            y = 20
            self.move(x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
