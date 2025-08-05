import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyPDF2 import PdfMerger

class PDFMergeUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coke PDF Merger")
        self.resize(800, 600)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(28)

        # Title
        label = QtWidgets.QLabel("PDF Merger")
        label.setStyleSheet("font-size: 40px; color: #b4aaff; font-weight: bold;")
        label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(label)

        # File list display
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
        main_layout.addWidget(self.file_list, 1)

        # Buttons row
        button_style = """
            QPushButton {
                font-size: 18px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 7px;
            }
            QPushButton:hover { background: #b4aaff; }
        """

        button_style1 = """
            QPushButton {
                font-size: 17px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 7px;
            }
            QPushButton:hover { background: #b4aaff; }
        """

        button_style2 = """
            QPushButton {
                font-size: 22px; background: #bd93f9; color: #23272f; font-weight: bold; border-radius: 7px;
            }
            QPushButton:hover { background: #b4aaff; }
        """

        btn_row = QtWidgets.QHBoxLayout()
        add_btn = QtWidgets.QPushButton("Add PDFs")
        add_btn.setStyleSheet(button_style)
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

        up_btn = QtWidgets.QPushButton("Move Up")
        up_btn.setStyleSheet(button_style)
        up_btn.setFixedHeight(44)
        up_btn.clicked.connect(self.move_up)
        btn_row.addWidget(up_btn)

        down_btn = QtWidgets.QPushButton("Move Down")
        down_btn.setStyleSheet(button_style)
        down_btn.setFixedHeight(44)
        down_btn.clicked.connect(self.move_down)
        btn_row.addWidget(down_btn)

        main_layout.addLayout(btn_row)

        # Output file selector
        output_row = QtWidgets.QHBoxLayout()
        self.output_path = QtWidgets.QLineEdit()
        self.output_path.setPlaceholderText("Output merged PDF path (e.g., merged.pdf)")
        self.output_path.setStyleSheet("background: #181a20; color: #b4aaff; font-size: 17px; border-radius: 7px; border: 1.5px solid #bd93f9; padding-left: 10px;")
        output_row.addWidget(self.output_path, 1)
        browse_btn = QtWidgets.QPushButton("Browse")
        browse_btn.setStyleSheet(button_style1)
        browse_btn.setFixedHeight(30)
        browse_btn.setFixedWidth(100)
        browse_btn.clicked.connect(self.select_output_path)
        output_row.addWidget(browse_btn)
        main_layout.addLayout(output_row)

        # Merge button
        merge_btn = QtWidgets.QPushButton("Merge PDFs")
        merge_btn.setStyleSheet(button_style2)
        merge_btn.setFixedHeight(52)
        merge_btn.clicked.connect(self.merge_pdfs)
        main_layout.addWidget(merge_btn)

        # Status label
        self.status = QtWidgets.QLabel("")
        self.status.setStyleSheet("font-size: 18px; color: #d6bfff;")
        main_layout.addWidget(self.status)

        self.setStyleSheet("""
            QWidget { background: #23272f; color: #f8f8f2; }
        """)

    def add_files(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select PDF files to merge", "", "PDF Files (*.pdf)"
        )
        for f in files:
            if f and f not in self.get_current_files():
                self.file_list.addItem(f)

    def get_current_files(self):
        return [self.file_list.item(i).text() for i in range(self.file_list.count())]

    def remove_selected(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def move_up(self):
        row = self.file_list.currentRow()
        if row > 0:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row - 1, item)
            self.file_list.setCurrentRow(row - 1)

    def move_down(self):
        row = self.file_list.currentRow()
        if 0 <= row < self.file_list.count() - 1:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row + 1, item)
            self.file_list.setCurrentRow(row + 1)

    def select_output_path(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save merged PDF as...", "merged.pdf", "PDF Files (*.pdf)"
        )
        if filename:
            self.output_path.setText(filename)

    def merge_pdfs(self):
        files = self.get_current_files()
        output = self.output_path.text().strip()
        if not files:
            self.status.setText("Please add at least two PDF files.")
            return
        if len(files) < 2:
            self.status.setText("Need at least two files to merge!")
            return
        if not output:
            self.status.setText("Please select an output file.")
            return
        try:
            merger = PdfMerger()
            for f in files:
                merger.append(f)
            merger.write(output)
            merger.close()
            self.status.setText(f"Successfully merged to:\n{output}")
        except Exception as e:
            self.status.setText(f"Failed to merge: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = PDFMergeUI()
    win.show()
    sys.exit(app.exec_())

