import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyPDF2 import PdfReader, PdfWriter

class PDFSplitterUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coke PDF Splitter")
        self.resize(800, 600)
        self.pdf_path = None
        self.total_pages = 0

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(25)

        # Button styles to match merger (with hover)
        button_style = """
            QPushButton {
                font-size: 18px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 7px;
            }
            QPushButton:hover { background: #b4aaff; }
        """
        button_style1 = """
            QPushButton {
                font-size: 17px; background: #bd93f9; color: #23272f; font-weight: thin; border-radius: 7px;
            }
            QPushButton:hover { background: #b4aaff; }
        """
        button_style2 = """
            QPushButton {
                font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 7px;
            }
            QPushButton:hover { background: #b4aaff; }
        """

        # Title
        label = QtWidgets.QLabel("PDF Splitter")
        label.setStyleSheet("font-size: 40px; color: #b4aaff; font-weight: bold;")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        # PDF File picker row
        file_row = QtWidgets.QHBoxLayout()

        # Frame for label
        self.file_frame = QtWidgets.QFrame()
        self.file_frame.setStyleSheet("""
            QFrame {
                background: #181a20;
                border-radius: 10px;
                padding: 5px 14px;
            }
        """)
        self.file_frame.setFixedHeight(50)
        file_frame_layout = QtWidgets.QHBoxLayout(self.file_frame)
        file_frame_layout.setContentsMargins(0, 0, 0, 0)
        file_frame_layout.setSpacing(0)

        self.file_label = QtWidgets.QLabel("No PDF selected")
        self.file_label.setStyleSheet("font-size: 19px; color: #d6bfff;")
        file_frame_layout.addWidget(self.file_label)

        file_row.addWidget(self.file_frame, 1)

        file_btn = QtWidgets.QPushButton("Select PDF")
        file_btn.setStyleSheet(button_style)
        file_btn.setFixedHeight(50)
        file_btn.setFixedWidth(100)
        file_btn.clicked.connect(self.select_pdf)
        file_row.addWidget(file_btn)
        layout.addLayout(file_row)

        # Page info row
        self.pages_info = QtWidgets.QLabel("")
        self.pages_info.setStyleSheet("font-size: 18px; color: #b4aaff;")
        layout.addWidget(self.pages_info)

        # Page selection row
        select_row = QtWidgets.QHBoxLayout()
        select_label = QtWidgets.QLabel("Pages to keep (e.g. 1,3,5-7):")
        select_label.setStyleSheet("font-size: 17px; color: #f8f8f2;")
        select_row.addWidget(select_label)
        self.page_input = QtWidgets.QLineEdit()
        self.page_input.setStyleSheet("background: #181a20; color: #b4aaff; font-size: 17px; border-radius: 7px; border: 1.5px solid #bd93f9; padding-left: 10px;")
        self.page_input.setPlaceholderText("e.g. 2-4 or 1,5,7-8")
        select_row.addWidget(self.page_input, 1)
        layout.addLayout(select_row)

        # Output file selector
        output_row = QtWidgets.QHBoxLayout()
        self.output_path = QtWidgets.QLineEdit()
        self.output_path.setPlaceholderText("Output PDF path (e.g., split.pdf)")
        self.output_path.setStyleSheet("background: #181a20; color: #b4aaff; font-size: 17px; border-radius: 7px; border: 1.5px solid #bd93f9; padding-left: 10px;")
        output_row.addWidget(self.output_path, 1)
        browse_btn = QtWidgets.QPushButton("Browse")
        browse_btn.setStyleSheet(button_style1)
        browse_btn.setFixedHeight(30)
        browse_btn.setFixedWidth(90)
        browse_btn.clicked.connect(self.select_output_path)
        output_row.addWidget(browse_btn)
        layout.addLayout(output_row)

        # Split button
        split_btn = QtWidgets.QPushButton("Split PDF")
        split_btn.setStyleSheet(button_style2)
        split_btn.setFixedHeight(52)
        split_btn.clicked.connect(self.split_pdf)
        layout.addWidget(split_btn)

        # Status label
        self.status = QtWidgets.QLabel("")
        self.status.setStyleSheet("font-size: 17px; color: #d6bfff;")
        layout.addWidget(self.status)

        self.setStyleSheet("""
            QWidget { background: #23272f; color: #f8f8f2; }
        """)

    def select_pdf(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select a PDF file", "", "PDF Files (*.pdf)"
        )
        if path:
            self.pdf_path = path
            self.file_label.setText(os.path.basename(path))
            try:
                with open(path, 'rb') as f:
                    pdf = PdfReader(f)
                    self.total_pages = len(pdf.pages)
                self.pages_info.setText(f"Total pages: {self.total_pages}")
            except Exception as e:
                self.status.setText(f"Failed to open PDF: {e}")
                self.total_pages = 0
                self.pages_info.setText("")
        else:
            self.pdf_path = None
            self.file_label.setText("No PDF selected")
            self.total_pages = 0
            self.pages_info.setText("")

    def select_output_path(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save split PDF as...", "split.pdf", "PDF Files (*.pdf)"
        )
        if filename:
            self.output_path.setText(filename)

    def parse_pages(self, s):
        # Parses "1,3,5-7" to [1,3,5,6,7] (1-based, but pdf is 0-based)
        result = []
        try:
            parts = [x.strip() for x in s.split(',') if x.strip()]
            for part in parts:
                if '-' in part:
                    start, end = part.split('-')
                    start, end = int(start), int(end)
                    if start > end:
                        start, end = end, start
                    result.extend(range(start, end+1))
                else:
                    result.append(int(part))
            # Remove duplicates and sort
            return sorted(set(result))
        except Exception:
            return []

    def split_pdf(self):
        self.status.setText("")
        if not self.pdf_path or self.total_pages == 0:
            self.status.setText("Please select a valid PDF.")
            return
        output = self.output_path.text().strip()
        if not output:
            self.status.setText("Please select output file.")
            return
        page_str = self.page_input.text().strip()
        if not page_str:
            self.status.setText("Please enter pages to keep (e.g. 2-5 or 1,3,8-12).")
            return
        pages = self.parse_pages(page_str)
        if not pages:
            self.status.setText("Invalid page input.")
            return
        # Ensure all in range
        valid = [p for p in pages if 1 <= p <= self.total_pages]
        if not valid:
            self.status.setText("No valid pages in the given range.")
            return
        try:
            with open(self.pdf_path, 'rb') as f:
                pdf = PdfReader(f)
                writer = PdfWriter()
                for p in valid:
                    writer.add_page(pdf.pages[p-1])
                with open(output, 'wb') as out:
                    writer.write(out)
            self.status.setText(f"Split and saved:\n{output}")
        except Exception as e:
            self.status.setText(f"Failed to split: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = PDFSplitterUI()
    win.show()
    sys.exit(app.exec_())
