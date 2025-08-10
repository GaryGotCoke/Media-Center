import sys
from PyQt5 import QtWidgets, QtCore, QtGui

from pdf_split import PDFSplitterUI
from tiktok_download import TikTokDownloaderUI
from music_player import MusicPlayerUI
from youtube_download import YouTubeDownloaderUI
from image_convert import ImageConverterUI
from pdf_merge import PDFMergeUI
from video_player import VideoPlayer
from bilibili_download import BilibiliDownloaderUI
from pptx_to_pdf import PPTXtoPDFUI
from image_compress import ImageCompressorUI
from pdf_compress import PDFCompressorUI
from torrent_download import TorrentDownloaderUI

class HomePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Welcome Title ---
        title = QtWidgets.QLabel("Welcome to Coke's Media Center!")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(35)
        layout.addWidget(title)
        layout.addSpacing(25)

        # --- About/Intro Section ---
        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff; font-size:21px;'>About this app</b><br>"
            "<span style='color:#e2e2f3; font-size:17px;'>"
            "Coke's Media Center is an all-in-one toolkit for downloading, converting, and managing your medias.<br><br>"

            "<b style='color:#d6bfff;'>Before you start:</b><br>"
            "* This app is for <b>Windows only</b> (other platforms not supported)<br>"
            "* <b>Download and install the following programs for best results (detailed instructions in the tabs):</b><br><br>"
            "&nbsp;&nbsp;1. <b>VLC Media Player</b> <a href='https://www.videolan.org/vlc/' style='color:#bd93f9;'>(Download VLC)</a> - required for music/video playback<br>"
            "&nbsp;&nbsp;2. <b>qBittorrent</b> <a href='https://www.qbittorrent.org/download.php' style='color:#bd93f9;'>(Download qBittorrent)</a> - required for torrent downloads<br>"
            "&nbsp;&nbsp;3. <b>FFmpeg</b> <a href='https://ffmpeg.org/download.html' style='color:#bd93f9;'>(Download FFmpeg)</a> - required for video/audio downloads and conversion<br>"
            "&nbsp;&nbsp;4. <b>Ghostscript</b> <a href='https://ghostscript.com/releases/gsdnld.html' style='color:#bd93f9;'>(Download Ghostscript)</a> - required for PDF compression<br><br>"
            "* <b>All other Python packages are automatically managed by the app (or included in the EXE version)</b><br><br>"

            "<b style='color:#d6bfff;'>How to use:</b><br>"
            "* Explore all tools using the sidebar (left side of this window)<br>"
            "* Every tool page includes detailed instructions and requirements<br>"
            "* Use the '<b>Check Packages Updates</b>' button below <b style='color:#d6bfff;'>if running from source code</b><br><br>"

            "Designed and coded by <b style='color:#fa78d9;'>GotCoke</b>, <b style='color:#fa78d9;'>Nova</b> (AI)<br>"
            "Everything is coded in Python 3, you can download the <b>source code</b> on Github, link in <b>Developer</b> tab.<br>"
            "</span>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 36px; padding-right: 12px; color: #e2e2f3;")
        desc.setOpenExternalLinks(True)
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)

        layout.addWidget(desc)
        layout.addSpacing(10)

        # --- Check for Update Button ---
        update_btn = QtWidgets.QPushButton("Check Packages Updates")
        update_btn.setFixedHeight(35)
        update_btn.setStyleSheet(
            "font-size: 15px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 10px;")
        update_btn.clicked.connect(self.check_for_updates)
        layout.addWidget(update_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(20)
        #layout.addStretch(1)

    def check_for_updates(self):
        import subprocess
        import sys
        checking = QtWidgets.QMessageBox(self)
        checking.setWindowTitle("Please Wait")
        checking.setIcon(QtWidgets.QMessageBox.Information)
        checking.setText("Checking for updates...\n\nThe app will continue automatically when done.")
        checking.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        checking.show()
        QtWidgets.QApplication.processEvents()  # Force immediate show

        to_update = [
            "PyQt5",
            "PyPDF2",
            "yt-dlp",
            "python-vlc",
            "pillow",
            "pikepdf",
            "qbittorrent-api",
            "pptxtopdf",
            "comtypes"
        ]
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Update Status")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", *to_update])
            checking.hide()
            msg.setText("All core packages are now up to date!\n\nYou may need to restart the app.")
        except Exception as e:
            checking.hide()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText(f"Update failed:\n{e}")
        msg.exec_()



class TorrentPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Top Title ---
        title = QtWidgets.QLabel("Torrent Downloader")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        # --- Middle Description ---
        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Download torrents directly to your PC using the qBittorrent client.<br>"
            "Easily add [.torrent] files and monitor download progress from this app.</b><br><br>"
            "<b>What you can do:</b><br>"
            "* Add any <b>[.torrent] file</b> to download movies, games, music, etc.<br>"
            "* View progress and status of your downloads.<br>"
            "* No need to open qBittorrent manually — just run the WebUI.<br><br>"
            "<b>How to use:</b><br>"
            "1. Make sure qBittorrent is installed and running with its WebUI enabled.<br>"
            "2. Default WebUI settings: <code style='color:#bd93f9;'>localhost:8080, user: admin, pass: adminadmin</code><br>"
            "3. Click 'Browse' or drag and drop a [.torrent] file.<br>"
            "4. Click 'Add Torrent' to start downloading.<br>"
            "5. Files are saved in your Downloads / [MyTorrents] folder.<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>qBittorrent</b> installed (from <a href='https://www.qbittorrent.org/download.php' style='color:#bd93f9;'>qbittorrent.org</a>)<br>"
            "* <b>WebUI enabled</b> (Options > Web UI, default settings are fine)<br>"
            "* <b>qbittorrent-api</b> Python package (auto-included with EXE, or install with:<br>"
            "<code style='color:#bd93f9; font-size:17px;'>pip install qbittorrent-api</code>)<br>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        # --- Bottom Launch Button ---
        self.launch_btn = QtWidgets.QPushButton("Launch Torrent Downloader")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_torrent_downloader)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.torrent_window = None

    def launch_torrent_downloader(self):
        self.torrent_window = TorrentDownloaderUI()
        self.torrent_window.show()



class VideoPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Top Title ---
        title = QtWidgets.QLabel("Video Player")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        # --- Middle Description ---
        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Play almost any video or audio file — with subtitles and full keyboard controls!</b><br><br>"
            "<b>What you can play:</b><br>"
            "* Video: mp4, mkv, avi, mov, webm, flv, and more<br>"
            "* Audio: mp3, flac, ogg, wav, m4a, etc.<br>"
            "* Subtitles: SRT/ASS (auto-load and select track)<br><br>"
            "<b>Features:</b><br>"
            "* Timeline seeking, volume, and subtitle selection<br>"
            "* Keyboard shortcuts (Space = Play/Pause, F11 = Fullscreen, ←/→ = Seek)<br>"
            "* Shows track info and time remaining<br>"
            "<br>"
            "<b>How to use:</b><br>"
            "1. Click 'Open' to choose a media file.<br>"
            "2. Use playback and subtitle controls at the bottom.<br>"
            "3. First launch takes a few seconds, please wait and do not close.<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>python-vlc</b> Python package (auto-included with EXE, or install with:<br>"
            "<code style='color:#bd93f9; font-size:17px;'>pip install python-vlc</code>)<br>"
            "* <b>VLC Media Player</b> must be installed.<br>"
            "<span style='color:#d6bfff;'>"
            "(Install from <a href='https://www.videolan.org/vlc/' style='color:#bd93f9;'>videolan.org/vlc</a>)"
            "</span>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        # --- Bottom Launch Button ---
        self.launch_btn = QtWidgets.QPushButton("Launch Video Player")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_video_player)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.video_window = None

    def launch_video_player(self):
        self.video_window = VideoPlayer()
        self.video_window.show()



class YouTubePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Top Title ---
        title = QtWidgets.QLabel("YouTube Downloader")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        # --- Middle Description ---
        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Download audio or video from YouTube links.<br>"
            "Supports playlists, audio extraction, and high quality video.</b><br><br>"
            "<b>What you can download:</b><br>"
            "* <b>Audio (mp3)</b> — Downloads only the audio track as an MP3 file.<br>"
            "* <b>Video + Audio (mp4)</b> — Downloads the best video up to 1080p and merges with the best audio (MP4 format).<br>"
            "* <b>Video Only (WebM)</b> — Downloads only the highest-quality video (no audio) in WebM format.<br><br>"
            "<b>How to use:</b><br>"
            "1. Paste any YouTube link (single video or playlist).<br>"
            "2. Select your preferred format from the dropdown.<br>"
            "3. Click 'Download' — the progress bar will show status.<br>"
            "4. Files are saved to your Downloads / [Downloads From YouTube] folder.<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>yt-dlp</b> Python package (auto-included with EXE version, or install with:<br>"
            "<code style='color:#bd93f9; font-size:17px;'>pip install yt-dlp</code>)<br>"
            "* <b>FFmpeg</b> must be installed and added to your system <b>PATH</b>.<br>"
            "   <span style='color:#d6bfff'>(FFmpeg is required for all formats and must be accessible from the command line.)</span>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        # --- Bottom Launch Button ---
        self.launch_btn = QtWidgets.QPushButton("Launch YouTube Downloader")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_youtube_downloader)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.yt_window = None

    def launch_youtube_downloader(self):
        self.yt_window = YouTubeDownloaderUI()
        self.yt_window.show()



class MusicPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Top Title ---
        title = QtWidgets.QLabel("Music Player")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        # --- Middle Description ---
        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Play all your MP3 music with a beautiful, fast, and searchable player.</b><br><br>"
            "<b>What you can play:</b><br>"
            "* MP3 audio files (add a folder to load your library)<br><br>"
            "<b>Features:</b><br>"
            "* Playlist view and instant search<br>"
            "* Track info display, timeline seeking, repeat/loop<br>"
            "* Keyboard shortcuts (Space = Play/Pause, F11 = Fullscreen, ←/→ = Seek)<br>"
            "<br>"
            "<b>How to use:</b><br>"
            "1. Click 'Select Music Folder' and choose any folder with MP3 files.<br>"
            "2. Search, select, and play your favorite tracks.<br>"
            "3. Use playback controls at the bottom — Loop/Next/Prev/Stop.<br>"
            "4. First launch takes a few seconds, please wait and do not close.<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>python-vlc</b> Python package (auto-included with EXE, or install with:<br>"
            "<code style='color:#bd93f9; font-size:17px;'>pip install python-vlc</code>)<br>"
            "* <b>VLC Media Player</b> must be installed.<br>"
            "<span style='color:#d6bfff;'>"
            "(Install from <a href='https://www.videolan.org/vlc/' style='color:#bd93f9;'>videolan.org/vlc</a>)"
            "</span>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        # --- Bottom Launch Button ---
        self.launch_btn = QtWidgets.QPushButton("Launch Music Player")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_music_player)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.music_window = None

    def launch_music_player(self):
        self.music_window = MusicPlayerUI()
        self.music_window.show()

      

class TikTokPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Top Title ---
        title = QtWidgets.QLabel("TikTok Downloader")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        # --- Middle Description ---
        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Download TikTok videos or extract audio with a single click!<br>"
            "Easily grab content in high quality — supports both video and MP3 download.</b><br><br>"
            "<b>What you can download:</b><br>"
            "* <b>Audio (mp3)</b> — Downloads only the sound from any TikTok as an MP3.<br>"
            "* <b>Video + Audio (mp4)</b> — Downloads the full TikTok video in MP4 format (up to 1080p).<br><br>"
            "<b>How to use:</b><br>"
            "1. Copy and paste a TikTok video link (or click 'Paste' to grab from clipboard).<br>"
            "2. Select your preferred format from the dropdown.<br>"
            "3. Click 'Download' — the progress bar will show status.<br>"
            "4. Files are saved to your Downloads / [Downloads From TikTok] folder.<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>yt-dlp</b> Python package (auto-included with EXE, or install with:<br>"
            "<code style='color:#bd93f9; font-size:17px;'>pip install yt-dlp</code>)<br>"
            "* <b>FFmpeg</b> must be installed and added to your system <b>PATH</b>.<br>"
            "<span style='color:#d6bfff;'>(FFmpeg is required for all downloads. TikTok download may not work for private or region-locked videos.)</span><br>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        # --- Bottom Launch Button ---
        self.launch_btn = QtWidgets.QPushButton("Launch TikTok Downloader")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_tiktok_downloader)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.tiktok_window = None

    def launch_tiktok_downloader(self):
        self.tiktok_window = TikTokDownloaderUI()
        self.tiktok_window.show()



class BilibiliPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Top Title ---
        title = QtWidgets.QLabel("Bilibili Downloader")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        # --- Middle Description ---
        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Download public videos from Bilibili (哔哩哔哩) — in full quality or audio only!<br>"
            "Easily save videos for offline use, or extract music from your favorite creators.</b><br><br>"
            "<b>What you can download:</b><br>"
            "* <b>Audio (mp3)</b> — Downloads just the audio from a Bilibili video as MP3.<br>"
            "* <b>Video + Audio (mp4)</b> — Downloads the full video (up to 1080p) as MP4.<br><br>"
            "<b>How to use:</b><br>"
            "1. Copy and paste a public Bilibili video link (or b23.tv short link).<br>"
            "2. Select your preferred format from the dropdown.<br>"
            "3. Click 'Download' — the progress bar will show status.<br>"
            "4. Files are saved to your Downloads / [Downloads From Bilibili] folder.<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>yt-dlp</b> Python package (auto-included with EXE, or install with:<br>"
            "<code style='color:#bd93f9; font-size:17px;'>pip install yt-dlp</code>)<br>"
            "* <b>FFmpeg</b> must be installed and added to your system <b>PATH</b>.<br>"
            "<span style='color:#d6bfff;'>(FFmpeg is required for all downloads. No support for Bangumi, member-only, or region-locked videos.)</span><br>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        # --- Bottom Launch Button ---
        self.launch_btn = QtWidgets.QPushButton("Launch Bilibili Downloader")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_bilibili_downloader)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.bilibili_window = None

    def launch_bilibili_downloader(self):
        self.bilibili_window = BilibiliDownloaderUI()
        self.bilibili_window.show()



class PDFmergePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QtWidgets.QLabel("PDF Merger")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Combine multiple PDF files into a single PDF in seconds.</b><br><br>"
            "<b>What you can do:</b><br>"
            "* Merge any number of PDF files into one file<br>"
            "* Reorder PDFs as you like before merging<br>"
            "* Save the merged result anywhere you want<br><br>"
            "<b>How to use:</b><br>"
            "1. Click 'Add PDFs' to select your PDF files.<br>"
            "2. Use 'Move Up' or 'Move Down' to order them.<br>"
            "3. Choose your output file name and location.<br>"
            "4. Click 'Merge PDFs' and you’re done!<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>PyPDF2</b> Python package (auto-included with EXE, or install with:<br>"
            "<code style='color:#bd93f9; font-size:17px;'>pip install PyPDF2</code>)<br>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        self.launch_btn = QtWidgets.QPushButton("Launch PDF Merger")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_pdf_merger)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.merger_window = None

    def launch_pdf_merger(self):
        self.merger_window = PDFMergeUI()
        self.merger_window.show()



class PDFsplitPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QtWidgets.QLabel("PDF Splitter")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Extract specific pages from a PDF and save them as a new file.</b><br><br>"
            "<b>What you can do:</b><br>"
            "* Keep only the pages you need from any PDF<br>"
            "* Enter page ranges (like 1-3,5,8-10) to split<br>"
            "* Save your split document anywhere<br><br>"
            "<b>How to use:</b><br>"
            "1. Click 'Select PDF' and choose your file.<br>"
            "2. Type which pages you want (e.g., 2-5 or 1,3,8-10).<br>"
            "3. Set the output file name and location.<br>"
            "4. Click 'Split PDF' to create your new file.<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>PyPDF2</b> Python package (auto-included with EXE, or install with:<br>"
            "<code style='color:#bd93f9; font-size:17px;'>pip install PyPDF2</code>)<br>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        self.launch_btn = QtWidgets.QPushButton("Launch PDF Splitter")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_pdf_splitter)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.splitter_window = None

    def launch_pdf_splitter(self):
        self.splitter_window = PDFSplitterUI()
        self.splitter_window.show()



class PptxToPdfPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QtWidgets.QLabel("PPTX to PDF Converter")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Convert PowerPoint presentations (.pptx) to PDF quickly and easily.</b><br><br>"
            "<b>What you can do:</b><br>"
            "* Convert one or many PPTX files to PDF at once<br>"
            "* Keep your original formatting and layout<br>"
            "* Save output PDFs anywhere you like<br><br>"
            "<b>How to use:</b><br>"
            "1. Click 'Add PPTXs' and select your files.<br>"
            "2. Choose an output folder for the PDFs.<br>"
            "3. Click 'Convert to PDFs' — that's it!<br>"
            "4. First launch takes a few seconds, please wait and do not close.<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>pptxtopdf</b> Python package (auto-included with EXE, or install with:<br>"
            "<code style='color:#bd93f9; font-size:17px;'>pip install pptxtopdf</code>)<br>"
            "* <b>Microsoft PowerPoint</b> (Windows only) must be installed and activated.<br>"
            "* <b>comtypes</b> Python package (<code style='color:#bd93f9; font-size:17px;'>pip install comtypes</code>)<br>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        self.launch_btn = QtWidgets.QPushButton("Launch PPTX to PDF Converter")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_pptx_to_pdf)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.pptx_window = None

    def launch_pptx_to_pdf(self):
        self.pptx_window = PPTXtoPDFUI()
        self.pptx_window.show()



class PDFCompressorPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QtWidgets.QLabel("PDF Compressor")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Reduce the file size of PDFs to save space and make sharing easy.</b><br><br>"
            "<b>What you can do:</b><br>"
            "* Compress large PDF files (choose quality level)<br>"
            "* Make files easier to send by email or upload<br>"
            "* Batch compress multiple PDFs at once<br><br>"
            "<b>How to use:</b><br>"
            "1. Click 'Add PDFs' to select files.<br>"
            "2. Set compression quality from the dropdown.<br>"
            "3. Choose an output folder.<br>"
            "4. Click 'Compress PDFs' — finished files appear in your folder.<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>Ghostscript</b> (must be installed and in your PATH — "
            "<a href='https://ghostscript.com/releases/gsdnld.html' style='color:#bd93f9;'>Download here</a>)<br>"
            "* No Python package needed for compression, but you need the <b>gswin64c</b> command (Windows).<br>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        self.launch_btn = QtWidgets.QPushButton("Launch PDF Compressor")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_pdf_compressor)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.compressor_window = None

    def launch_pdf_compressor(self):
        self.compressor_window = PDFCompressorUI()
        self.compressor_window.show()



class ImageCompressPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QtWidgets.QLabel("Image Compressor")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Reduce image file sizes while keeping good quality.</b><br><br>"
            "<b>What you can do:</b><br>"
            "* Compress JPG, JPEG, WEBP, and other images<br>"
            "* Choose your desired quality (20–95%)<br>"
            "* Batch process multiple images at once<br><br>"
            "<b>How to use:</b><br>"
            "1. Click 'Add Images' and select your files.<br>"
            "2. Move the quality slider to set your compression level.<br>"
            "3. Choose an output folder.<br>"
            "4. Click 'Compress Images' to finish.<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>Pillow</b> Python package (auto-included with EXE, or install with:<br>"
            "<code style='color:#bd93f9; font-size:17px;'>pip install pillow</code>)<br>"
            "* For best results, use JPG or WEBP format, before compress PNG, recommand convert to other formats.<br>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        self.launch_btn = QtWidgets.QPushButton("Launch Image Compressor")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_image_compressor)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.compressor_window = None

    def launch_image_compressor(self):
        self.compressor_window = ImageCompressorUI()
        self.compressor_window.show()


class ImageConvertPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QtWidgets.QLabel("Image Converter")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(30)

        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff;'>Convert images between formats, resize, and crop with ease.</b><br><br>"
            "<b>What you can do:</b><br>"
            "* Convert between JPG, PNG, WEBP<br>"
            "* Resize images to common resolutions or keep original<br>"
            "* Center-crop images to popular ratios (square, 16:9, etc)<br>"
            "* Batch process multiple images<br><br>"
            "<b>How to use:</b><br>"
            "1. Click 'Add Images' and pick your files.<br>"
            "2. Select the output format, resize, and crop options.<br>"
            "3. Choose your output folder.<br>"
            "4. Click 'Convert Images' to finish.<br><br>"
            "<b style='color:#faad8d;'>Requirements:</b><br>"
            "* <b>Pillow</b> Python package (auto-included with EXE, or install with:<br>"
            "<code style='color:#bd93f9; font-size:17px;'>pip install pillow</code>)<br>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 30px; padding-right: 10px; color: #e2e2f3;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)

        self.launch_btn = QtWidgets.QPushButton("Launch Image Converter")
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet(
            "font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 11px;"
        )
        self.launch_btn.clicked.connect(self.launch_image_converter)
        layout.addWidget(self.launch_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addSpacing(70)

        self.converter_window = None

    def launch_image_converter(self):
        self.converter_window = ImageConverterUI()
        self.converter_window.show()


class DeveloperPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QtWidgets.QLabel("Developer & Credits")
        title.setStyleSheet("font-size: 42px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addSpacing(35)
        layout.addWidget(title)
        layout.addSpacing(30)

        desc = QtWidgets.QLabel(
            "<div style='text-align:left;'>"
            "<b style='color:#d6bfff; font-size:22px;'>Coke Media Center</b><br>"
            "<span style='color:#e2e2f3; font-size:17px;'>"
            "<b>Made by:</b> <span style='color:#fa78d9;'>GotCoke</span><br>"
            "Contact: <a href='mailto:panguogary@outlook.com' style='color:#bd93f9;'>panguogary@outlook.com</a><br>"
            "GitHub: <a href='https://github.com/GaryGotCoke' style='color:#bd93f9;'>github.com/GaryGotCoke</a><br><br>"

            "<b>Why I built this project:</b><br>"
            "* I always wanted an all-in-one toolkit for media, downloads, and file conversion that’s actually easy to use.<br>"
            "* Every feature here is something I wanted in my own daily life.<br>"
            "* <span style='color:#fa78d9;'>Nova</span> (AI) was my tireless partner: reviewing, brainstorming, and solving any coding problem I threw at it.<br>"
            "* I hope you find this app as useful and fun as I do!<br><br>"

            "<b>Mini-Changelog:</b><br>"
            "* v1.0 - Torrent downloader, Video player, dark UI<br>"
            "* v1.1 - Added YouTube, TikTok, Bilibili downloaders<br>"
            "* v1.2 - Added Music player, Home page<br>"
            "* v1.3 - Added PDF tools, Images tools<br>"
            "* v1.4 - UI polish, detailed help pages, launch-from-lobby<br><br>"

            "<b>Major open-source libraries used:</b><br>"
            "* PyQt5, yt-dlp, python-vlc, PyPDF2, Pillow<br>"
            "* qbittorrent-api, ffmpeg, pptxtopdf, comtypes, Ghostscript<br><br>"

            "All code, design, and late-night debugging by GotCoke. If you have suggestions or spot bugs, just reach out!<br>"
            "</span>"
            "</div>"
        )
        desc.setStyleSheet("font-size: 18px; padding-left: 36px; padding-right: 12px; color: #e2e2f3;")
        desc.setOpenExternalLinks(True)  # Enable clickable links!
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(desc)
        layout.addStretch(2)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coke Media Center")
        self.resize(1000, 760)

        # --- Central widget & main layout ---
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)

        # --- Navigation bar (sidebar) ---
        self.nav = QtWidgets.QListWidget()
        self.nav.setFixedWidth(220)
        self.nav.setStyleSheet("""
            QListWidget {
                background: #181a20;
                color: #f8f8f2;
                border: none;
                font-size: 20px;
                padding: 0px;
            }
            QListWidget::item {
                height: 52px;
                padding-left: 18px;
                border-radius: 8px;
                margin-bottom: 4px;
            }
            QListWidget::item:selected {
                background: #bd93f9;
                color: #23272f;
            }
        """)
        self.nav.addItem("Home")
        self.nav.addItem("Torrent Downloader")
        self.nav.addItem("YouTube Downloader")
        self.nav.addItem("TikTok Downloader")
        self.nav.addItem("Bilibili Downloader")
        self.nav.addItem("Video Player")
        self.nav.addItem("Music Player")
        self.nav.addItem("PDF Merger")
        self.nav.addItem("PDF Splitter")
        self.nav.addItem("PPTX to PDF")
        self.nav.addItem("PDF Compressor")
        self.nav.addItem("Image Compressor")
        self.nav.addItem("Image Converter")
        self.nav.addItem("Developer")
        self.nav.setCurrentRow(0)

        # --- Stacked pages ---
        self.pages = QtWidgets.QStackedWidget()
        self.pages.addWidget(HomePage())
        self.pages.addWidget(TorrentPage())
        self.pages.addWidget(YouTubePage())
        self.pages.addWidget(TikTokPage())
        self.pages.addWidget(BilibiliPage())
        self.pages.addWidget(VideoPage())
        self.pages.addWidget(MusicPage())
        self.pages.addWidget(PDFmergePage())
        self.pages.addWidget(PDFsplitPage())
        self.pages.addWidget(PptxToPdfPage())
        self.pages.addWidget(PDFCompressorPage())
        self.pages.addWidget(ImageCompressPage())
        self.pages.addWidget(ImageConvertPage())
        self.pages.addWidget(DeveloperPage())

        main_layout.addWidget(self.nav)
        main_layout.addWidget(self.pages, 1)

        

        # Make sure every item has the same size for bigger touch/click targets
        for i in range(self.nav.count()):
            self.nav.item(i).setSizeHint(QtCore.QSize(120, 52))

        # --- Connect navigation ---
        self.nav.currentRowChanged.connect(self.pages.setCurrentIndex)

        # --- Global Dark Theme ---
        self.setStyleSheet("""
            QWidget { background: #23272f; color: #f8f8f2; }
            QFrame { background: #181a20; }
            QPushButton { 
                background: #282a36; 
                color: #f8f8f2; 
                border: 1px solid #44475a;
                border-radius: 6px;
                padding: 5px 16px;
            }
            QPushButton:hover { background: #44475a; }
            QSlider::groove:horizontal { background: #44475a; height: 6px; border-radius: 3px; }
            QSlider::handle:horizontal { background: #bd93f9; width: 16px; border-radius: 8px; }
            QLabel#TimeLabel { color: #d6bfff; padding-left:6px; font-family: Consolas; font-size: 10pt;}
            QComboBox { background: #282a36; color: #f8f8f2; border-radius: 4px; padding: 2px 12px; }
        """)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
