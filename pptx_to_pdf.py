import sys
import os
import time
from PyQt5 import QtWidgets, QtCore

try:
    from pptxtopdf import convert
except ImportError:
    convert = None

def is_powerpoint_available():
    try:
        import comtypes.client
        ppt = comtypes.client.CreateObject("Powerpoint.Application")
        ppt.Quit()
        return True, "PowerPoint detected! Ready to convert."
    except Exception as e:
        return False, "Microsoft Office PowerPoint is not installed or cannot be accessed."

class PPTXtoPDFUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coke PPTX to PDF Converter")
        self.resize(800, 600)
        self.powerpoint_ok, status_msg = is_powerpoint_available()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(28)

        label = QtWidgets.QLabel("PPTX to PDF Converter")
        label.setStyleSheet("font-size: 40px; color: #b4aaff; font-weight: bold;")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        self.file_list = QtWidgets.QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                background: #181a20;
                color: #f8f8f2;
                font-size: 19px;
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

        btn_row = QtWidgets.QHBoxLayout()
        add_btn = QtWidgets.QPushButton("Add PPTXs")
        add_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 7px;
            }
            QPushButton:hover { background: #b4aaff; }
        """)
        add_btn.setFixedHeight(44)
        add_btn.clicked.connect(self.add_files)
        btn_row.addWidget(add_btn)

        remove_btn = QtWidgets.QPushButton("Remove Selected")
        remove_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px; background: #44475a; color: #f8f8f2; font-weight: bold; border-radius: 7px;
            }
            QPushButton:hover { background: #bd93f9; }
        """)
        remove_btn.setFixedHeight(44)
        remove_btn.clicked.connect(self.remove_selected)
        btn_row.addWidget(remove_btn)
        layout.addLayout(btn_row)

        output_row = QtWidgets.QHBoxLayout()
        self.output_path = QtWidgets.QLineEdit()
        self.output_path.setPlaceholderText("Output folder for PDF files")
        self.output_path.setStyleSheet("background: #181a20; color: #b4aaff; font-size: 17px; border-radius: 7px; border: 1.5px solid #bd93f9; padding-left: 10px;")
        output_row.addWidget(self.output_path, 1)
        browse_btn = QtWidgets.QPushButton("Browse")
        browse_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 7px;
            }
            QPushButton:hover { background: #b4aaff; }
        """)
        browse_btn.setFixedHeight(32)
        browse_btn.setFixedWidth(100)
        browse_btn.clicked.connect(self.select_output_folder)
        output_row.addWidget(browse_btn)
        layout.addLayout(output_row)

        self.convert_btn = QtWidgets.QPushButton("Convert to PDFs")
        self.convert_btn.setStyleSheet("""
            QPushButton {
                font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 8px;
            }
            QPushButton:hover { background: #b4aaff; }
        """)
        self.convert_btn.setFixedHeight(52)
        self.convert_btn.clicked.connect(self.convert_all)
        layout.addWidget(self.convert_btn)

        # Status label
        self.status = QtWidgets.QLabel(status_msg)
        self.status.setStyleSheet("font-size: 18px; color: #d6bfff;")
        layout.addWidget(self.status)

        self.setStyleSheet("""
            QWidget { background: #23272f; color: #f8f8f2; }
        """)

        # Disable convert if not OK
        self.convert_btn.setEnabled(self.powerpoint_ok)

    def add_files(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select PPTX files", "", "PowerPoint (*.pptx)"
        )
        for f in files:
            if f and f not in self.get_current_files():
                self.file_list.addItem(f)

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

    def convert_all(self):
        files = self.get_current_files()
        outdir = self.output_path.text().strip()
        if not files:
            self.status.setText("Please add at least one PPTX file.")
            return
        if not outdir or not os.path.isdir(outdir):
            self.status.setText("Please select a valid output folder.")
            return

        # Always use a subfolder for output
        final_outdir = os.path.join(outdir, "pptxs convert to pdfs")
        os.makedirs(final_outdir, exist_ok=True)

        ok, fail = 0, 0
        fail_files = []
        import time

        for f in files:
            try:
                self.status.setText(f"Converting: {os.path.basename(f)}...")
                QtWidgets.QApplication.processEvents()
                pptx_name = os.path.splitext(os.path.basename(f))[0]
                out_pdf = os.path.join(final_outdir, pptx_name + ".pdf")
                # Use output folder, let pptxtopdf auto-name the file
                convert(f, final_outdir)
                # Wait up to 2s for the file to be created
                for _ in range(20):
                    if os.path.isfile(out_pdf) and os.path.getsize(out_pdf) > 0:
                        ok += 1
                        break
                    time.sleep(0.1)
                else:
                    fail += 1
                    fail_files.append(os.path.basename(f))
            except Exception as e:
                fail += 1
                fail_files.append(f"{os.path.basename(f)}: {e}")
        msg = f"Conversion finished. {ok} succeeded, {fail} failed."
        if fail_files:
            msg += "\n" + "\n".join(fail_files)
        self.status.setText(msg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = PPTXtoPDFUI()
    win.show()
    sys.exit(app.exec_())
