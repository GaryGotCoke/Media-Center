import os
import sys
import vlc
from PyQt5 import QtWidgets, QtCore, QtGui

class MusicPlayerUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coke Music Player")
        self.fixed_width = 1000
        self.fixed_height = 600

        # --- Centered fixed-size main container ---
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setFixedSize(self.fixed_width, self.fixed_height)
        root_layout = QtWidgets.QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addStretch(1)
        root_layout.addWidget(self.central_widget, alignment=QtCore.Qt.AlignCenter)
        root_layout.addStretch(1)

        # --- VLC Setup ---
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()

        self.playlist = []
        self.playlist_names = []
        self.filtered_indices = []
        self.current_index = -1
        self.repeat_one = False  # Make sure this is initialized

        # --- Main Layout for central_widget ---
        outer_layout = QtWidgets.QVBoxLayout(self.central_widget)
        outer_layout.setContentsMargins(24, 24, 24, 24)
        outer_layout.setSpacing(16)

        # --- Folder Picker Row ---
        folder_row = QtWidgets.QHBoxLayout()
        self.folder_btn = QtWidgets.QPushButton("Select Music Folder")
        self.folder_btn.setFixedHeight(38)
        self.folder_btn.setFixedWidth(210)
        self.folder_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 7px;
            }
            QPushButton:checked {
                background: #b4aaff; color: #23272f;
            }
            QPushButton:hover { background: #b4aaff; }
        """)
        self.folder_btn.clicked.connect(self.select_folder)
        folder_row.addWidget(self.folder_btn, 0, QtCore.Qt.AlignLeft)

        self.folder_label = QtWidgets.QLabel("No folder selected")
        self.folder_label.setStyleSheet("font-size: 18px; color: #d6bfff;")
        folder_row.addWidget(self.folder_label, 1, QtCore.Qt.AlignVCenter)
        outer_layout.addLayout(folder_row)

        # --- Main Content Row (List + Right Panel) ---
        content_row = QtWidgets.QHBoxLayout()
        content_row.setSpacing(28)

        # --- File List + Search ---
        left_panel = QtWidgets.QVBoxLayout()
        left_panel.setSpacing(8)

        # Search bar
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search…")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setFixedHeight(36)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background: #181a20; color: #b4aaff; font-size: 18px; border-radius: 7px;
                border: 1.5px solid #bd93f9; padding-left: 16px;
            }
        """)
        self.search_bar.textChanged.connect(self.update_file_list)
        left_panel.addWidget(self.search_bar)

        # File List
        self.file_list = QtWidgets.QListWidget()
        self.file_list.setFixedWidth(400)
        self.file_list.setStyleSheet("""
            QListWidget {
                background: #181a20;
                color: #f8f8f2;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                padding: 8px;
            }
            QListWidget::item:selected {
                background: #bd93f9;
                color: #23272f;
                border-radius: 8px;
            }
        """)
        self.file_list.itemDoubleClicked.connect(self.play_selected_file)
        left_panel.addWidget(self.file_list, 1)
        content_row.addLayout(left_panel, 0)

        # --- Right Panel: Filename (top), Controls/timeline/vol (bottom) ---
        right_panel = QtWidgets.QVBoxLayout()
        right_panel.setSpacing(12)
        right_panel.setContentsMargins(0, 0, 0, 0)

        # Track Info (Independent section, with word wrap)
        self.track_label = QtWidgets.QLabel("No track selected")
        self.track_label.setStyleSheet(
            "font-size: 24px; color: #b4aaff; font-weight: bold; padding: 18px 16px; background: #181a20; border-radius: 10px;")
        self.track_label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.track_label.setWordWrap(True)
        self.track_label.setMinimumHeight(350)
        self.track_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        right_panel.addWidget(self.track_label, 0)

        right_panel.addStretch(1)  # Push controls to bottom

        # --- Controls/timeline/volume group (at bottom) ---
        bottom_group = QtWidgets.QVBoxLayout()
        bottom_group.setSpacing(10)
        bottom_group.setContentsMargins(0, 0, 0, 0)

        # Progress Bar
        progress_row = QtWidgets.QHBoxLayout()
        self.progress_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.progress_slider.setRange(0, 1000)
        self.progress_slider.setFixedHeight(15)
        self.progress_slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #44475a; height: 6px; border-radius: 3px; }
            QSlider::handle:horizontal { background: #bd93f9; width: 16px; border-radius: 8px; }
        """)
        self.progress_slider.sliderMoved.connect(self.set_position)

        self.time_label = QtWidgets.QLabel("00:00 / 00:00")
        self.time_label.setStyleSheet("color: #d6bfff; font-size: 16px; font-family: Consolas; padding-left: 10px;")
        self.time_label.setFixedWidth(130)
        progress_row.addWidget(self.progress_slider, 1)
        progress_row.addWidget(self.time_label, 0)
        bottom_group.addLayout(progress_row)

        # Controls Row
        controls_row = QtWidgets.QHBoxLayout()
        button_style = """
            QPushButton {
                font-size: 18px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 7px;
            }
            QPushButton:checked {
                background: #b4aaff; color: #23272f;
            }
            QPushButton:hover { background: #b4aaff; }
        """
        self.prev_btn = QtWidgets.QPushButton("Prev")
        self.prev_btn.setStyleSheet(button_style)
        self.play_btn = QtWidgets.QPushButton("Play")
        self.play_btn.setStyleSheet(button_style)
        self.pause_btn = QtWidgets.QPushButton("Pause")
        self.pause_btn.setStyleSheet(button_style)
        self.stop_btn = QtWidgets.QPushButton("Stop")
        self.stop_btn.setStyleSheet(button_style)
        self.next_btn = QtWidgets.QPushButton("Next")
        self.next_btn.setStyleSheet(button_style)
        self.repeat_btn = QtWidgets.QPushButton("Loop")
        self.repeat_btn.setCheckable(True)
        self.repeat_btn.setChecked(False)
        self.repeat_btn.clicked.connect(self.toggle_repeat)
        self.repeat_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 7px;
            }
            QPushButton:checked {
                background: #fa78d9; color: #23272f;
            }
            QPushButton:hover { background: #b4aaff; }
        """)

        for btn in [self.prev_btn, self.play_btn, self.pause_btn, self.stop_btn, self.next_btn, self.repeat_btn]:
            btn.setFixedSize(80, 38)
        controls_row.addWidget(self.prev_btn)
        controls_row.addWidget(self.play_btn)
        controls_row.addWidget(self.pause_btn)
        controls_row.addWidget(self.stop_btn)
        controls_row.addWidget(self.next_btn)
        controls_row.addWidget(self.repeat_btn)
        bottom_group.addLayout(controls_row)

        # Volume Row
        volume_row = QtWidgets.QHBoxLayout()
        vol_label = QtWidgets.QLabel("Volume")
        vol_label.setStyleSheet("font-size: 16px; color: #d6bfff;")
        self.vol_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(80)
        self.vol_slider.setFixedWidth(140)
        self.vol_slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #44475a; height: 6px; border-radius: 3px; }
            QSlider::handle:horizontal { background: #bd93f9; width: 16px; border-radius: 8px; }
        """)
        self.vol_slider.valueChanged.connect(self.set_volume)
        volume_row.addWidget(vol_label)
        volume_row.addWidget(self.vol_slider)
        bottom_group.addLayout(volume_row)

        right_panel.addLayout(bottom_group)

        content_row.addLayout(right_panel, 1)
        outer_layout.addLayout(content_row)

        # --- Theme ---
        self.setStyleSheet("""
            QWidget { background: #23272f; color: #f8f8f2; }
        """)

        # --- Connections ---
        self.play_btn.clicked.connect(self.play)
        self.pause_btn.clicked.connect(self.pause)
        self.stop_btn.clicked.connect(self.stop)
        self.next_btn.clicked.connect(self.play_next)
        self.prev_btn.clicked.connect(self.play_prev)
        self.file_list.itemClicked.connect(self.sync_selection_to_list)

        # --- Timer for UI update ---
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start()

        self.set_volume(self.vol_slider.value())

        # --- Fullscreen handling ---
        self.is_fullscreen = False
        self.shortcut_fullscreen = QtWidgets.QShortcut(QtGui.QKeySequence("F11"), self, activated=self.toggle_fullscreen)
        self.shortcut_exitfs = QtWidgets.QShortcut(QtGui.QKeySequence("Escape"), self, activated=self.exit_fullscreen)

    # ---------------- UI + Logic Methods ----------------

    def toggle_repeat(self):
        self.repeat_one = self.repeat_btn.isChecked()

    def select_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Music Folder", "")
        if folder:
            self.folder_label.setText(folder)
            self.load_folder(folder)

    def load_folder(self, folder):
        self.playlist = []
        self.playlist_names = []
        self.filtered_indices = []
        self.current_index = -1
        for fname in sorted(os.listdir(folder)):
            if fname.lower().endswith(".mp3"):
                path = os.path.join(folder, fname)
                self.playlist.append(path)
                self.playlist_names.append(fname)
        self.update_file_list()
        if not self.playlist:
            self.track_label.setText("No mp3 files found in this folder.")
        else:
            self.track_label.setText("No track selected")

    def update_file_list(self):
        query = self.search_bar.text().strip().lower()
        self.file_list.clear()
        self.filtered_indices = []
        if not self.playlist_names:
            return
        for i, name in enumerate(self.playlist_names):
            if not query or query in name.lower():
                self.file_list.addItem(name)
                self.filtered_indices.append(i)

    def get_real_index(self, list_row):
        if 0 <= list_row < len(self.filtered_indices):
            return self.filtered_indices[list_row]
        return -1

    def get_list_row_by_real_index(self, idx):
        try:
            return self.filtered_indices.index(idx)
        except ValueError:
            return -1

    def play_selected_file(self, item):
        row = self.file_list.row(item)
        idx = self.get_real_index(row)
        self.start_play(idx)

    def play(self):
        selected_items = self.file_list.selectedItems()
        if selected_items:
            idx = self.get_real_index(self.file_list.currentRow())
            self.start_play(idx)
        elif self.current_index < 0 and self.playlist:
            if self.filtered_indices:
                self.start_play(self.filtered_indices[0])
            else:
                self.start_play(0)
        else:
            self.media_player.play()

    def sync_selection_to_list(self, item):
        idx = self.get_real_index(self.file_list.row(item))
        self.file_list.setCurrentRow(self.get_list_row_by_real_index(idx))

    def start_play(self, idx):
        if not self.playlist or idx < 0 or idx >= len(self.playlist):
            return
        self.current_index = idx
        path = self.playlist[idx]
        self.media_player.set_media(self.vlc_instance.media_new(path))
        self.media_player.play()
        self.track_label.setText(os.path.basename(path))
        list_row = self.get_list_row_by_real_index(idx)
        if list_row != -1:
            self.file_list.setCurrentRow(list_row)
        self.set_volume(self.vol_slider.value())

    def pause(self):
        self.media_player.pause()

    def stop(self):
        self.media_player.stop()

    def play_next(self):
        if self.repeat_one:
            # Restart the current song if loop is enabled
            self.start_play(self.current_index)
            return
        if not self.playlist or not self.filtered_indices:
            return
        try:
            pos = self.filtered_indices.index(self.current_index)
            next_pos = (pos + 1) % len(self.filtered_indices)
            idx = self.filtered_indices[next_pos]
        except ValueError:
            idx = self.filtered_indices[0]
        self.start_play(idx)

    def play_prev(self):
        if self.repeat_one:
            # Restart the current song if loop is enabled
            self.start_play(self.current_index)
            return
        if not self.playlist or not self.filtered_indices:
            return
        try:
            pos = self.filtered_indices.index(self.current_index)
            prev_pos = (pos - 1) % len(self.filtered_indices)
            idx = self.filtered_indices[prev_pos]
        except ValueError:
            idx = self.filtered_indices[0]
        self.start_play(idx)

    def set_volume(self, value):
        self.media_player.audio_set_volume(value)

    def set_position(self, val):
        if self.media_player.get_length() > 0:
            pos = val / 1000.0
            self.media_player.set_position(pos)

    def update_ui(self):
        # Update slider and time label
        if self.media_player.is_playing():
            pos = self.media_player.get_position()
            self.progress_slider.blockSignals(True)
            self.progress_slider.setValue(int(pos * 1000))
            self.progress_slider.blockSignals(False)
            current = int(self.media_player.get_time() / 1000)
            total = int(self.media_player.get_length() / 1000)
            self.time_label.setText(f"{self.format_time(current)} / {self.format_time(total)}")
        else:
            # Detect if finished and auto-next or repeat
            state = self.media_player.get_state()
            if state == vlc.State.Ended and self.playlist:
                if self.repeat_one:
                    self.start_play(self.current_index)
                else:
                    self.play_next()

    def format_time(self, secs):
        if secs <= 0 or secs is None:
            return "00:00"
        m, s = divmod(secs, 60)
        return f"{int(m):02d}:{int(s):02d}"

    def closeEvent(self, event):
        try:
            self.media_player.stop()
        except Exception:
            pass
        event.accept()

    # --- Fullscreen logic: center fixed-size widget ---
    def toggle_fullscreen(self):
        if not self.is_fullscreen:
            self.showFullScreen()
            self.is_fullscreen = True

    def exit_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
            self.is_fullscreen = False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MusicPlayerUI()
    win.show()
    sys.exit(app.exec_())


