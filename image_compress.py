import sys
import os
from PyQt5 import QtWidgets, QtCore
from PIL import Image

class ImageCompressorUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coke Image Compressor")
        self.resize(800, 600)
        self.image_files = []
        self.output_dir = None

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(22)

        button_style = """
            QPushButton {
                font-size: 18px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 7px;
            }
            QPushButton:hover { background: #b4aaff; }
        """

        # Title
        title = QtWidgets.QLabel("Image Compressor")
        title.setStyleSheet("font-size: 40px; color: #b4aaff; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # File list
        self.file_list = QtWidgets.QListWidget()
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
        layout.addWidget(self.file_list, 1)

        # PNG warning label
        self.png_warning = QtWidgets.QLabel("")
        self.png_warning.setStyleSheet("font-size: 16px; color: #fdcb6e;")
        layout.addWidget(self.png_warning)

        # Add & Remove buttons row
        btn_row = QtWidgets.QHBoxLayout()
        add_btn = QtWidgets.QPushButton("Add Images")
        add_btn.setStyleSheet(button_style)
        add_btn.setFixedHeight(38)
        add_btn.clicked.connect(self.add_files)
        btn_row.addWidget(add_btn)

        remove_btn = QtWidgets.QPushButton("Remove Selected")
        remove_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px; background: #44475a; color: #f8f8f2; font-weight: bold; border-radius: 7px;
            }
            QPushButton:hover { background: #bd93f9; }
        """)
        remove_btn.setFixedHeight(38)
        remove_btn.clicked.connect(self.remove_selected)
        btn_row.addWidget(remove_btn)
        layout.addLayout(btn_row)

        # Quality slider row (20-95, snaps to nearest 5)
        quality_row = QtWidgets.QHBoxLayout()
        qual_label = QtWidgets.QLabel("Quality:")
        qual_label.setStyleSheet("font-size: 17px; color: #f8f8f2;")
        quality_row.addWidget(qual_label)

        self.quality_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.quality_slider.setRange(20, 95)
        self.quality_slider.setValue(55)
        self.quality_slider.setTickInterval(5)
        self.quality_slider.setSingleStep(5)
        self.quality_slider.setPageStep(5)
        self.quality_slider.setFixedWidth(600)
        self.quality_slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #44475a; height: 6px; border-radius: 3px; }
            QSlider::handle:horizontal { background: #bd93f9; width: 16px; border-radius: 8px; }
        """)
        quality_row.addWidget(self.quality_slider)
        
        value_box = QtWidgets.QHBoxLayout()
        value_box.setSpacing(0)
        value_box.setContentsMargins(0, 0, 0, 0)
        self.quality_value = QtWidgets.QLabel("55")
        self.quality_value.setStyleSheet("font-size: 17px; color: #b4aaff; min-width: 32px;")
        qual_pct = QtWidgets.QLabel("%")
        qual_pct.setStyleSheet("font-size: 17px; color: #b4aaff;")
        value_box.addWidget(self.quality_value)
        value_box.addWidget(qual_pct)
        quality_row.addLayout(value_box)


        layout.addLayout(quality_row)

        # Connect slider snap
        self.quality_slider.valueChanged.connect(self.on_slider_quality_change)
        self.status = QtWidgets.QLabel("")
        self.status.setStyleSheet("font-size: 18px; color: #d6bfff;")

        # Output folder
        output_row = QtWidgets.QHBoxLayout()
        self.output_path = QtWidgets.QLineEdit()
        self.output_path.setPlaceholderText("Output folder for compressed images")
        self.output_path.setStyleSheet("background: #181a20; color: #b4aaff; font-size: 17px; border-radius: 7px; border: 1.5px solid #bd93f9; padding-left: 10px;")
        output_row.addWidget(self.output_path, 1)
        browse_btn = QtWidgets.QPushButton("Browse")
        browse_btn.setStyleSheet(button_style)
        browse_btn.setFixedHeight(32)
        browse_btn.setFixedWidth(100)
        browse_btn.clicked.connect(self.select_output_folder)
        output_row.addWidget(browse_btn)
        layout.addLayout(output_row)

        # Compress button
        compress_btn = QtWidgets.QPushButton("Compress Images")
        compress_btn.setStyleSheet("""
            QPushButton {
                font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 8px;
            }
            QPushButton:hover { background: #b4aaff; }
        """)
        compress_btn.setFixedHeight(48)
        compress_btn.clicked.connect(self.compress_images)
        layout.addWidget(compress_btn)

        layout.addWidget(self.status)

        self.setStyleSheet("""
            QWidget { background: #23272f; color: #f8f8f2; }
        """)

    def add_files(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select image files", "", "Images (*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.gif)"
        )
        added_png = False
        for f in files:
            if f and f not in self.get_current_files():
                self.file_list.addItem(f)
                if f.lower().endswith('.png'):
                    added_png = True
        if added_png:
            self.png_warning.setText(
                "Note: For smaller PNG files, convert to JPG/WebP or resize, both in the Image Converter."
            )
        else:
            self.png_warning.setText("")

    def get_current_files(self):
        return [self.file_list.item(i).text() for i in range(self.file_list.count())]

    def remove_selected(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def select_output_folder(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select output folder", ""
        )
        if path:
            self.output_path.setText(path)

    def on_slider_quality_change(self, v):
        # Snap to nearest multiple of 5, within 20–95
        snapped = round((v - 20) / 5) * 5 + 20
        snapped = max(20, min(95, snapped))
        if snapped != v:
            self.quality_slider.setValue(snapped)
            return  # Let the event fire again at snapped value
        self.quality_value.setText(str(snapped))
        self.status.setText("")

    def compress_images(self):
        files = self.get_current_files()
        outdir = self.output_path.text().strip()
        quality = int(self.quality_value.text())
        if not files:
            self.status.setText("Please add images.")
            return
        if not outdir or not os.path.isdir(outdir):
            self.status.setText("Please select a valid output folder.")
            return
        ok, fail = 0, 0
        for f in files:
            try:
                with Image.open(f) as img:
                    ext = os.path.splitext(f)[1].lower()
                    fname = os.path.basename(f)
                    name, ext = os.path.splitext(fname)
                    outname = f"{name}_compressed{ext}"
                    outpath = os.path.join(outdir, outname)
                    save_args = {}
                    if ext in [".jpg", ".jpeg", ".webp"]:
                        save_args["quality"] = quality
                        save_args["optimize"] = True
                    if ext in [".jpg", ".jpeg"]:
                        save_args["progressive"] = True
                    img.save(outpath, **save_args)
                    ok += 1
            except Exception as e:
                fail += 1
        self.status.setText(f"Compression finished. {ok} succeeded, {fail} failed.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = ImageCompressorUI()
    win.show()
    sys.exit(app.exec_())
