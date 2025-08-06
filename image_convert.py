import sys
import os
from PyQt5 import QtWidgets, QtCore
from PIL import Image

class ImageConverterUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coke Image Converter")
        self.resize(800, 600)

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
        title = QtWidgets.QLabel("Image Converter")
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

        # Convert + Resize + Crop row
        convrow = QtWidgets.QHBoxLayout()

        # Format dropdown
        fmt_label = QtWidgets.QLabel("Convert to:")
        fmt_label.setStyleSheet("font-size: 17px; color: #f8f8f2;")
        convrow.addWidget(fmt_label)
        self.format_combo = QtWidgets.QComboBox()
        self.format_combo.addItems([
            "Original format", "JPG", "PNG", "WEBP"
        ])
        self.format_combo.setStyleSheet("""
            QComboBox { background: #282a36; color: #b4aaff; font-size: 18px; border-radius: 7px; padding: 4px 16px; }
            QComboBox QAbstractItemView { background: #282a36; color: #b4aaff; }
        """)
        convrow.addWidget(self.format_combo)
        self.format_combo.currentIndexChanged.connect(self.clear_status)  # <-- Clear status on change

        # Resize dropdown
        resize_label = QtWidgets.QLabel("Resize:")
        resize_label.setStyleSheet("font-size: 16px; color: #f8f8f2; padding-left:20px;")
        convrow.addWidget(resize_label)
        self.resize_combo = QtWidgets.QComboBox()
        self.resize_combo.addItems([
            "Original size",
            "1920 x 1080",
            "1280 x 720",
            "800 x 800",
            "640 x 480",
            "320 x 320"
        ])
        self.resize_combo.setStyleSheet("""
            QComboBox { background: #282a36; color: #b4aaff; font-size: 16px; border-radius: 7px; padding: 4px 10px; }
            QComboBox QAbstractItemView { background: #282a36; color: #b4aaff; }
        """)
        convrow.addWidget(self.resize_combo)
        self.resize_combo.currentIndexChanged.connect(self.clear_status)  # <-- Clear status on change

        # Crop dropdown
        crop_label = QtWidgets.QLabel("Center Crop:")
        crop_label.setStyleSheet("font-size: 16px; color: #f8f8f2; padding-left:20px;")
        convrow.addWidget(crop_label)
        self.crop_combo = QtWidgets.QComboBox()
        self.crop_combo.addItems([
            "No crop",
            "1:1 (Square)",
            "16:9",
            "4:3",
            "3:2",
            "9:16"
        ])
        self.crop_combo.setStyleSheet("""
            QComboBox { background: #282a36; color: #b4aaff; font-size: 16px; border-radius: 7px; padding: 4px 10px; }
            QComboBox QAbstractItemView { background: #282a36; color: #b4aaff; }
        """)
        convrow.addWidget(self.crop_combo)
        self.crop_combo.currentIndexChanged.connect(self.clear_status)  # <-- Clear status on change
        convrow.addStretch(1)
        layout.addLayout(convrow)

        # Output folder
        output_row = QtWidgets.QHBoxLayout()
        self.output_path = QtWidgets.QLineEdit()
        self.output_path.setPlaceholderText("Output folder for converted images")
        self.output_path.setStyleSheet("background: #181a20; color: #b4aaff; font-size: 17px; border-radius: 7px; border: 1.5px solid #bd93f9; padding-left: 10px;")
        output_row.addWidget(self.output_path, 1)
        browse_btn = QtWidgets.QPushButton("Browse")
        browse_btn.setStyleSheet(button_style)
        browse_btn.setFixedHeight(32)
        browse_btn.setFixedWidth(100)
        browse_btn.clicked.connect(self.select_output_folder)
        output_row.addWidget(browse_btn)
        layout.addLayout(output_row)

        # Convert button
        convert_btn = QtWidgets.QPushButton("Convert Images")
        convert_btn.setStyleSheet("""
            QPushButton {
                font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 8px;
            }
            QPushButton:hover { background: #b4aaff; }
        """)
        convert_btn.setFixedHeight(48)
        convert_btn.clicked.connect(self.convert_images)
        layout.addWidget(convert_btn)

        # Status
        self.status = QtWidgets.QLabel("")
        self.status.setStyleSheet("font-size: 18px; color: #d6bfff;")
        layout.addWidget(self.status)

        self.setStyleSheet("""
            QWidget { background: #23272f; color: #f8f8f2; }
        """)

    def clear_status(self):
        self.status.setText("")

    def add_files(self):
        self.clear_status()
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select image files", "", "Images (*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.gif)"
        )
        for f in files:
            if f and f not in self.get_current_files():
                self.file_list.addItem(f)

    def get_current_files(self):
        return [self.file_list.item(i).text() for i in range(self.file_list.count())]

    def remove_selected(self):
        self.clear_status()
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def select_output_folder(self):
        self.clear_status()
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select output folder", ""
        )
        if path:
            self.output_path.setText(path)

    def get_resize_tuple(self):
        idx = self.resize_combo.currentIndex()
        sizes = [
            None,  # original
            (1920, 1080),
            (1280, 720),
            (800, 800),
            (640, 480),
            (320, 320)
        ]
        return sizes[idx]

    def get_crop_ratio(self):
        crop_map = {
            0: None,        # No crop
            1: (1, 1),      # Square
            2: (16, 9),
            3: (4, 3),
            4: (3, 2),
            5: (9, 16)
        }
        return crop_map[self.crop_combo.currentIndex()]

    def crop_center(self, img, target_ratio):
        w, h = img.size
        trw, trh = target_ratio
        # If aspect ratio matches (allow for rounding), do nothing
        if abs((w / h) - (trw / trh)) < 1e-4:
            return img
        if w * trh > h * trw:
            # Width is too big, crop sides
            new_w = int(h * trw / trh)
            left = (w - new_w) // 2
            box = (left, 0, left + new_w, h)
        else:
            # Height is too big, crop top/bottom
            new_h = int(w * trh / trw)
            top = (h - new_h) // 2
            box = (0, top, w, top + new_h)
        return img.crop(box)

    def convert_images(self):
        files = self.get_current_files()
        outdir = self.output_path.text().strip()
        fmtidx = self.format_combo.currentIndex()
        resize_tuple = self.get_resize_tuple()
        crop_ratio = self.get_crop_ratio()
        ok, fail = 0, 0
        error_msgs = []
        if not files:
            self.status.setText("Please add images.")
            return
        if not outdir or not os.path.isdir(outdir):
            self.status.setText("Please select a valid output folder.")
            return
        for f in files:
            try:
                with Image.open(f) as img:
                    # Crop first if needed
                    if crop_ratio:
                        img = self.crop_center(img, crop_ratio)
                    # Then resize if needed
                    if resize_tuple:
                        img.thumbnail(resize_tuple, Image.LANCZOS)
                    # Figure out output format & file extension
                    if fmtidx == 0:
                        out_ext = os.path.splitext(f)[1].lower().replace('.', '')
                        out_fmt_save = img.format if img.format else out_ext.upper()
                    else:
                        out_fmt = self.format_combo.currentText().upper()
                        if out_fmt == "JPG":
                            out_ext = "jpg"
                            out_fmt_save = "JPEG"
                        else:
                            out_ext = out_fmt.lower()
                            out_fmt_save = out_fmt
                    fname = os.path.basename(f)
                    name, _ = os.path.splitext(fname)
                    outname = f"{name}_converted.{out_ext}"
                    outpath = os.path.join(outdir, outname)
                    save_args = {}
                    if out_fmt_save in ["JPEG", "WEBP"]:
                        save_args["quality"] = 90
                        save_args["optimize"] = True
                    # Robust flatten for JPEG (PNG/WEBP → JPEG)
                    if out_fmt_save == "JPEG":
                        img = img.convert("RGBA")
                        bg = Image.new("RGB", img.size, (255, 255, 255))
                        bg.paste(img, mask=img.split()[-1])
                        img = bg
                    img.save(outpath, out_fmt_save, **save_args)
                    if not os.path.isfile(outpath) or os.path.getsize(outpath) == 0:
                        raise Exception("Output file missing or empty")
                    ok += 1
            except Exception as e:
                fail += 1
                msg = f"{os.path.basename(f)}: {str(e)}"
                if fmtidx > 0 and self.format_combo.currentText().upper() in ["JPG"]:
                    msg += " (PNG/WEBP may have transparency (alpha channel) or unsupported mode for JPG.)"
                error_msgs.append(msg)
        msg = f"Conversion finished. {ok} succeeded, {fail} failed."
        if error_msgs:
            msg += "\n" + "\n".join(error_msgs)
        self.status.setText(msg)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = ImageConverterUI()
    win.show()
    sys.exit(app.exec_())
