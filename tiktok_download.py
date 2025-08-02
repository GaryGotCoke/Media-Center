import sys
import os
import yt_dlp
from PyQt5 import QtWidgets, QtCore

def get_tiktok_download_path():
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    tiktok_folder = os.path.join(downloads, "Downloads From TikTok")
    os.makedirs(tiktok_folder, exist_ok=True)
    return tiktok_folder

class TikTokDlpWorker(QtCore.QThread):
    progress_signal = QtCore.pyqtSignal(int)
    status_signal = QtCore.pyqtSignal(str)
    finished_signal = QtCore.pyqtSignal()
    error_signal = QtCore.pyqtSignal(str)

    def __init__(self, url, fmt, outdir):
        super().__init__()
        self.url = url
        self.fmt = fmt
        self.outdir = outdir
        self._stop_requested = False
        self._partial_file = None

    def run(self):
        ydl_opts = {
            'outtmpl': os.path.join(self.outdir, '%(title)s.%(ext)s'),
            'progress_hooks': [self.hook],
            'quiet': True,
        }
        if self.fmt.startswith("Audio (mp3)"):
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            })
        else:
            ydl_opts['format'] = 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/mp4'

        error_occurred = False
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.status_signal.emit("Starting download...")
                ydl.download([self.url])
                if not self._stop_requested:
                    self.progress_signal.emit(100)
                    self.status_signal.emit("Download finished!")
        except Exception as e:
            error_occurred = True
            self._last_error = str(e)
        finally:
            if (self._stop_requested or error_occurred) and self._partial_file:
                try:
                    if os.path.exists(self._partial_file):
                        os.remove(self._partial_file)
                        if self._stop_requested:
                            self.status_signal.emit("Cancelled. Partial file deleted.")
                        else:
                            self.status_signal.emit(f"Error occurred. Partial file deleted.\n({self._last_error})")
                except Exception as del_e:
                    self.status_signal.emit(f"Partial file could not be deleted: {del_e}\n"
                                            f"Please delete manually:\n{self._partial_file}")
            elif error_occurred:
                self.status_signal.emit(f"Error: {self._last_error}")
        self.finished_signal.emit()

    def stop(self):
        self._stop_requested = True

    def hook(self, d):
        if 'filename' in d:
            self._partial_file = d['filename'] + '.part' if not d['filename'].endswith('.part') else d['filename']
        if self._stop_requested:
            raise Exception("Download stopped by user")
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes') or 0
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            if total > 0:
                percent = int(downloaded / total * 100)
            else:
                percent = 0
                if '_percent_str' in d:
                    try:
                        percent = int(float(d['_percent_str'].replace('%', '').strip()))
                    except:
                        percent = 0
            self.progress_signal.emit(percent)
            eta = d.get('eta')
            if eta:
                self.status_signal.emit(f"Downloading... ETA: {eta}s")
            else:
                self.status_signal.emit("Downloading...")
        elif d['status'] == 'finished':
            self.status_signal.emit("Download finished!")

class TikTokDownloaderUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coke TikTok Downloader")
        self.resize(800, 600)

        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setAlignment(QtCore.Qt.AlignCenter)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        container = QtWidgets.QWidget()
        container.setFixedWidth(650)
        container.setStyleSheet("background: transparent;")
        layout = QtWidgets.QVBoxLayout(container)
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setSpacing(45)
        layout.setContentsMargins(32, 32, 32, 32)
        outer_layout.addWidget(container, 0, QtCore.Qt.AlignCenter)

        label = QtWidgets.QLabel("TikTok Downloader")
        label.setStyleSheet("font-size: 40px; color: #b4aaff; font-weight: bold;")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        self.url_input = QtWidgets.QLineEdit(self)
        self.url_input.setPlaceholderText("Paste TikTok video link here...")
        self.url_input.setStyleSheet(
            "background: #181a20; color: #f8f8f2; border: 1.5px solid #bd93f9; border-radius: 6px; padding: 8px; font-size: 20px;")
        self.url_input.setFixedHeight(70)

        paste_btn = QtWidgets.QPushButton("Paste")
        paste_btn.setFixedWidth(100)
        paste_btn.setStyleSheet("""
            QPushButton { background: #282a36; color: #b4aaff; font-weight: bold; border-radius: 6px; font-size: 25px; }
            QPushButton:hover { background: #44475a; }
        """)
        paste_btn.clicked.connect(self.paste_clipboard)

        url_row = QtWidgets.QHBoxLayout()
        url_row.addWidget(self.url_input, 1)
        url_row.addWidget(paste_btn)
        layout.addLayout(url_row)

        self.format_combo = QtWidgets.QComboBox()
        self.format_combo.addItems(["Audio (mp3) -- up to 192kpbs",
                                   "Video + Audio(mp4) -- up to 1080p"])
        self.format_combo.setStyleSheet("""
            QComboBox { background: #282a36; color: #f8f8f2; font-size: 20px; border-radius: 6px; padding: 6px 20px; }
            QComboBox QAbstractItemView { background: #282a36; color: #f8f8f2; }
        """)
        self.format_combo.setFixedHeight(44)
        layout.addWidget(self.format_combo)

        btn_row = QtWidgets.QHBoxLayout()
        self.dl_btn = QtWidgets.QPushButton("Download")
        self.dl_btn.setStyleSheet("font-size: 25px; font-weight: bold; background: #bd93f9; color: #23272f; border-radius: 7px;")
        self.dl_btn.setFixedHeight(45)
        self.dl_btn.clicked.connect(self.download_tiktok)
        btn_row.addWidget(self.dl_btn)

        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("font-size: 25px; font-weight: bold; background: #44475a; color: #f8f8f2; border-radius: 7px;")
        self.cancel_btn.setFixedHeight(45)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_download)
        btn_row.addWidget(self.cancel_btn)

        layout.addLayout(btn_row)

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

        self.status = QtWidgets.QLabel("")
        self.status.setStyleSheet("font-size: 20px; color: #f8f8f2;")
        layout.addWidget(self.status)
        layout.addStretch(1)

        self.setStyleSheet("""
            QWidget { background: #23272f; color: #f8f8f2; }
        """)

        self.worker = None

    def paste_clipboard(self):
        cb = QtWidgets.QApplication.clipboard()
        self.url_input.setText(cb.text())

    def download_tiktok(self):
        url = self.url_input.text().strip()
        fmt = self.format_combo.currentText()
        outdir = get_tiktok_download_path()
        if not url or "tiktok.com" not in url.lower():
            self.status.setText("Please enter a valid TikTok link.")
            return

        self.progress.setValue(0)
        self.progress.setFormat("Starting...")
        self.status.setText("Preparing download...")

        self.dl_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)

        self.worker = TikTokDlpWorker(url, fmt, outdir)
        self.worker.progress_signal.connect(self.progress.setValue)
        self.worker.status_signal.connect(self.status.setText)
        self.worker.finished_signal.connect(self.on_download_finished)
        self.worker.error_signal.connect(self.status.setText)
        self.worker.start()

    def cancel_download(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.status.setText("Cancelling...")
            self.cancel_btn.setEnabled(False)

    def on_download_finished(self):
        self.dl_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress.setFormat("Done")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = TikTokDownloaderUI()
    win.show()
    sys.exit(app.exec_())

