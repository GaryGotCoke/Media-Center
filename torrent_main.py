import sys
import os
import qbittorrentapi
from PyQt5 import QtWidgets, QtCore

def get_downloads_path():
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    torrents = os.path.join(downloads, "MyTorrents")
    os.makedirs(torrents, exist_ok=True)
    return torrents

class TorrentDownloaderUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coke Torrent Downloader")
        self.resize(800, 600)

        # --- Centered Container ---
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setAlignment(QtCore.Qt.AlignCenter)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        container = QtWidgets.QWidget()
        container.setFixedWidth(800)   # Set width of UI content (adjust as you like)
        container.setStyleSheet("background: transparent;")
        layout = QtWidgets.QVBoxLayout(container)
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setSpacing(45)
        layout.setContentsMargins(32, 32, 32, 32)
        outer_layout.addWidget(container, 0, QtCore.Qt.AlignCenter)

        # --- qBittorrent WebUI defaults for public use ---
        self.qb_host = "localhost"
        self.qb_port = 8080
        self.qb_user = "admin"
        self.qb_pass = "adminadmin"
        self.save_path = get_downloads_path()

        # --- UI Elements ---
        label = QtWidgets.QLabel("Torrent Downloader")
        label.setStyleSheet("font-size: 40px; color: #b4aaff; font-weight: bold;")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        # Torrent file input row
        self.torrent_input = QtWidgets.QLineEdit(self)
        self.torrent_input.setPlaceholderText("Drag & drop or click 'Browse' to select a .torrent file...")
        self.torrent_input.setStyleSheet(
            "background: #181a20; color: #f8f8f2; border: 1.5px solid #bd93f9; border-radius: 6px; padding: 8px; font-size: 20px;")
        self.torrent_input.setReadOnly(True)
        self.torrent_input.setFixedHeight(70)

        browse_btn = QtWidgets.QPushButton("Browse")
        browse_btn.setFixedWidth(100)
        browse_btn.setStyleSheet("""
            QPushButton { background: #282a36; color: #b4aaff; font-weight: bold; border-radius: 6px; font-size: 25px; }
            QPushButton:hover { background: #44475a; }
        """)
        browse_btn.clicked.connect(self.browse_torrent)

        file_row = QtWidgets.QHBoxLayout()
        file_row.addWidget(self.torrent_input, 1)
        file_row.addWidget(browse_btn)
        layout.addLayout(file_row)

        # Add Torrent button
        self.add_btn = QtWidgets.QPushButton("Add Torrent")
        self.add_btn.setStyleSheet("font-size: 25px; font-weight: bold; background: #bd93f9; color: #23272f; border-radius: 7px;")
        self.add_btn.setFixedHeight(45)
        self.add_btn.clicked.connect(self.add_torrent)
        layout.addWidget(self.add_btn)

        # Progress bar
        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setFormat("Not started")
        self.progress.setFixedHeight(25)
        self.progress.setStyleSheet("""
            QProgressBar { background: #23272f; border: 1px solid #44475a; border-radius: 8px; color: #d6bfff; font-size: 15px; }
            QProgressBar::chunk { background: #bd93f9; border-radius: 8px; }
        """)
        layout.addWidget(self.progress)

        # Status label
        self.status = QtWidgets.QLabel("")
        self.status.setStyleSheet("font-size: 20px; color: #f8f8f2;")
        layout.addWidget(self.status)

        layout.addStretch(1)

        # Drag & Drop for .torrent files
        self.setAcceptDrops(True)

        # qBittorrent API setup
        self.client = qbittorrentapi.Client(
            host=f"http://{self.qb_host}:{self.qb_port}/",
            username=self.qb_user,
            password=self.qb_pass
        )
        try:
            self.client.auth_log_in()
            self.status.setText("Connected to qBittorrent")
        except qbittorrentapi.LoginFailed:
            self.status.setText("Login failed! Is qBittorrent WebUI running on localhost:8080?")
            self.add_btn.setEnabled(False)

        self.torrent_hash = None
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1200)
        self.timer.timeout.connect(self.check_progress)

        self.setStyleSheet("""
            QWidget { background: #23272f; color: #f8f8f2; }
        """)

    # Drag & drop for .torrent file
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith('.torrent'):
                    event.accept()
                    return
        event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith('.torrent'):
                self.torrent_input.setText(path)
                break

    def browse_torrent(self):
        fn, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Torrent File", "", "Torrent Files (*.torrent)")
        if fn:
            self.torrent_input.setText(fn)

    def add_torrent(self):
        path = self.torrent_input.text().strip()
        if not path or not os.path.isfile(path):
            self.status.setText("Please select a .torrent file.")
            return

        self.status.setText("Adding torrent...")
        self.progress.setFormat("Starting...")
        self.progress.setValue(0)
        try:
            self.client.torrents_add(
                torrent_files=path,
                save_path=self.save_path
            )
            QtCore.QTimer.singleShot(1600, self.find_new_torrent)
        except Exception as e:
            self.status.setText(f"Failed to add torrent: {e}")

    def find_new_torrent(self):
        torrents = list(self.client.torrents_info())
        if not torrents:
            self.status.setText("No torrents found.")
            return
        latest = max(torrents, key=lambda t: t.added_on)
        self.torrent_hash = latest.hash
        self.status.setText(f"Downloading: {latest.name}")
        self.timer.start()

    def check_progress(self):
        try:
            t = self.client.torrents_info(torrent_hashes=self.torrent_hash)[0]
            pct = int(t.progress * 100)
            self.progress.setValue(pct)
            self.progress.setFormat(f"{t.name[:28]}...  {pct}%")
            if pct >= 100:
                self.status.setText(f"Download finished: {t.name}")
                self.progress.setFormat("Done")
                self.timer.stop()
                # Remove torrent from qBittorrent to stop seeding, but keep files
                self.client.torrents_delete(torrent_hashes=t.hash, delete_files=False)
                self.status.setText("Download finished and stopped seeding.")
        except Exception as e:
            self.status.setText(f"Error: {e}")
            self.timer.stop()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = TorrentDownloaderUI()
    win.show()
    sys.exit(app.exec_())
