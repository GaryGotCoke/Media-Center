import sys
import vlc
from PyQt5 import QtWidgets, QtCore, QtGui

class ClickableSlider(QtWidgets.QSlider):
    clickedValue = QtCore.pyqtSignal(int)
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            val = QtWidgets.QStyle.sliderValueFromPosition(
                self.minimum(), self.maximum(), event.x(), self.width()
            )
            self.setValue(val)
            self.clickedValue.emit(val)
        super().mousePressEvent(event)

class VideoPlayer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python VLC Media Player")
        self.setGeometry(150, 150, 900, 550)
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.is_fullscreen = False

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()

        # --- Layout ---
        self.videoframe = QtWidgets.QFrame(self)
        self.videoframe.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.videoframe.mousePressEvent = self.refocus_main

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)

        self.audio_msg = QtWidgets.QLabel("Audio file playing", self.videoframe)
        self.audio_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.audio_msg.setStyleSheet("color: #b4aaff; font-size: 35px; font-weight: bold; background: transparent;")
        self.audio_msg.hide()

        self.audio_filename = QtWidgets.QLabel("",self.videoframe)
        self.audio_filename.setAlignment(QtCore.Qt.AlignCenter)
        self.audio_filename.setStyleSheet("color: #abb2bf; font-size: 22px; background: transparent;")
        self.audio_filename.hide()

        self.videoframe_layout = QtWidgets.QVBoxLayout(self.videoframe)
        self.videoframe_layout.setContentsMargins(0, 0, 0, 0)
        self.videoframe_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.videoframe_layout.addWidget(self.audio_msg)
        self.videoframe_layout.addWidget(self.audio_filename)

        # Timeline row: slider (expand) + time label (right)
        timeline_row = QtWidgets.QHBoxLayout()
        timeline_row.setContentsMargins(0, 0, 0, 0)
        timeline_row.setSpacing(8)

        self.timeline = ClickableSlider(QtCore.Qt.Horizontal, self)
        self.timeline.setMaximum(1000)
        self.timeline.clickedValue.connect(self.set_position)
        self.timeline.sliderMoved.connect(self.set_position)
        self.timeline.setFixedHeight(12)

        self.time_label = QtWidgets.QLabel("00:00 / 00:00", self)
        self.time_label.setObjectName("TimeLabel")
        self.time_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.time_label.setFont(QtGui.QFont("Consolas", 9))
        self.time_label.setFixedWidth(155)
        self.time_label.setFixedHeight(18)

        timeline_row.addWidget(self.timeline, 1)
        timeline_row.addWidget(self.time_label, 0)

        timeline_widget = QtWidgets.QWidget()
        timeline_widget.setLayout(timeline_row)
        timeline_widget.setFixedHeight(22)
        self.vboxlayout.addWidget(timeline_widget)

        # Controls
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.open_btn = QtWidgets.QPushButton("Open")
        self.play_btn = QtWidgets.QPushButton("Play")
        self.pause_btn = QtWidgets.QPushButton("Pause")
        self.stop_btn = QtWidgets.QPushButton("Stop")
        self.replay_btn = QtWidgets.QPushButton("Replay")
        self.fullscreen_btn = QtWidgets.QPushButton("Fullscreen")
        self.vol_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.vol_slider.setMaximum(100)
        self.vol_slider.setValue(80)
        self.vol_slider.setFixedWidth(100)

        # Subtitle track selection
        self.sub_track_combo = QtWidgets.QComboBox()
        self.sub_track_combo.setFixedWidth(160)

        self.hboxlayout.addWidget(self.open_btn)
        self.hboxlayout.addWidget(self.play_btn)
        self.hboxlayout.addWidget(self.pause_btn)
        self.hboxlayout.addWidget(self.stop_btn)
        self.hboxlayout.addWidget(self.replay_btn)
        self.hboxlayout.addWidget(self.fullscreen_btn)
        self.hboxlayout.addWidget(QtWidgets.QLabel("Volume"))
        self.hboxlayout.addWidget(self.vol_slider)
        self.hboxlayout.addWidget(QtWidgets.QLabel("Subtitles"))
        self.hboxlayout.addWidget(self.sub_track_combo)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.setLayout(self.vboxlayout)

        # --- Dark theme style ---
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

        # --- Button Connections ---
        self.open_btn.clicked.connect(self.open_file)
        self.play_btn.clicked.connect(self.play)
        self.pause_btn.clicked.connect(self.pause)
        self.stop_btn.clicked.connect(self.stop)
        self.replay_btn.clicked.connect(self.replay)
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        self.vol_slider.valueChanged.connect(self.set_volume)
        self.sub_track_combo.currentIndexChanged.connect(self.change_subtitle_track)

        # --- Timer for updating timeline and time display ---
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_ui)

        self.media = None

        # --- Embed VLC video in frame ---
        self.update_vlc_window()
        self.videoframe.installEventFilter(self)

        # Keyboard shortcuts for fullscreen (F11/Esc)
        QtWidgets.QShortcut(QtGui.QKeySequence("F11"), self, activated=self.toggle_fullscreen)
        QtWidgets.QShortcut(QtGui.QKeySequence("Escape"), self, activated=self.exit_fullscreen)

        # Capture arrow keys everywhere
        self.installEventFilter(self)

    def refocus_main(self, event):
        self.setFocus()
        QtWidgets.QFrame.mousePressEvent(self.videoframe, event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            if self.media_player.is_playing():
                self.pause()
            else:
                self.play()
        else:
            super().keyPressEvent(event)

    def eventFilter(self, source, event):
        # Handle keyboard navigation keys globally!
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Left:
                current = self.media_player.get_time()
                self.media_player.set_time(max(0, current - 5000))
                return True
            elif event.key() == QtCore.Qt.Key_Right:
                current = self.media_player.get_time()
                total = self.media_player.get_length()
                self.media_player.set_time(min(total, current + 5000))
                return True
        if source is self.videoframe and event.type() == QtCore.QEvent.Resize:
            self.update_vlc_window()
        return super().eventFilter(source, event)

    def update_vlc_window(self):
        if sys.platform.startswith('linux'):
            self.media_player.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":
            self.media_player.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin":
            self.media_player.set_nsobject(int(self.videoframe.winId()))

    def open_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Media", "",
            "Media Files (*.mp4 *.avi *.mkv *.mp3 *.wav *.mov *.flac *.ogg *.webm);;All Files (*)")
        if filename:
            self.current_media_path = filename
            self.audio_msg.hide()
            self.audio_filename.hide()
            self.media = self.instance.media_new(filename)
            self.media_player.set_media(self.media)
            self.update_vlc_window()
            self.play()
            self.setFocus()

        self.audio_msg.hide()

    def play(self):
        if self.media:
            self.media_player.play()
            self.set_volume(self.vol_slider.value())
            self.timer.start()
            QtCore.QTimer.singleShot(800, self.refresh_subtitle_tracks)
            self.setFocus()
            QtCore.QTimer.singleShot(500, self.check_video_presence)

    def check_video_presence(self):
        has_video = self.media_player.video_get_track_count() > 0
        if not has_video:
            self.audio_msg.show()
            if hasattr(self, "current_media_path") and self.current_media_path:
                import os
                filename = os.path.basename(self.current_media_path)
                self.audio_filename.setText(filename)
                self.audio_filename.show()
            else:
                self.audio_filename.hide()
        else:
            self.audio_msg.hide()
            self.audio_filename.hide()

    def pause(self):
        self.media_player.pause()

    def stop(self):
        self.media_player.stop()
        self.timer.stop()
        self.timeline.setValue(0)
        self.time_label.setText("00:00 / 00:00")
        self.audio_msg.hide()
        self.audio_filename.hide()

    def replay(self):
        if self.media:
            self.media_player.stop()
            self.media_player.set_time(0)
            self.media_player.play()
            self.set_volume(self.vol_slider.value())
            self.timer.start()
            QtCore.QTimer.singleShot(800, self.refresh_subtitle_tracks)
            self.setFocus()

    def toggle_fullscreen(self):
        if not self.is_fullscreen:
            self.showFullScreen()
            self.is_fullscreen = True
            self.fullscreen_btn.setText("Exit Fullscreen")
        else:
            self.exit_fullscreen()

    def exit_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
            self.is_fullscreen = False
            self.fullscreen_btn.setText("Fullscreen")

    def set_position(self, position):
        self.media_player.set_position(position / 1000.0)

    def set_volume(self, volume):
        self.media_player.audio_set_volume(volume)

    def refresh_subtitle_tracks(self):
        self.sub_track_combo.blockSignals(True)
        self.sub_track_combo.clear()
        self.sub_track_combo.addItem("No subtitles", -1)
        descs = self.media_player.video_get_spu_description()
        current_spu = self.media_player.video_get_spu()
        if descs:
            for id, name in descs:
                if isinstance(name, bytes):
                    name = name.decode('utf-8', errors='replace')
                self.sub_track_combo.addItem(name, id)
            ids = [-1] + [id for id, _ in descs]
            if current_spu in ids:
                idx = ids.index(current_spu)
                self.sub_track_combo.setCurrentIndex(idx)
            else:
                self.sub_track_combo.setCurrentIndex(0)
        else:
            self.sub_track_combo.setCurrentIndex(0)
        self.sub_track_combo.blockSignals(False)

    def change_subtitle_track(self, index):
        spu_id = self.sub_track_combo.itemData(index)
        self.media_player.video_set_spu(spu_id)

    def update_ui(self):
        if self.media_player.is_playing():
            pos = self.media_player.get_position()
            self.timeline.setValue(int(pos * 1000))
            # Time display update
            current_time = int(self.media_player.get_time() / 1000)
            total_time = int(self.media_player.get_length() / 1000)
            self.time_label.setText(f"{self.format_time(current_time)} / {self.format_time(total_time)}")
        else:
            # Check if video ended
            state = self.media_player.get_state()
            if state == vlc.State.Ended:
                self.timer.stop()
            elif state == vlc.State.Stopped:
                self.timer.stop()
            # Optional: keep showing last frame/time

    def format_time(self, secs):
        if secs <= 0 or secs is None:
            return "00:00"
        m, s = divmod(secs, 60)
        return f"{int(m):02d}:{int(s):02d}"

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())

