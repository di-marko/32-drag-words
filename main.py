# Created by Dmitri Markélov

import sys, os
from fpdf import FPDF
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QMenuBar,
    QMenu,
    QAction,
    QFileDialog,
    QAbstractItemView,
    QTextEdit,
    QPushButton,
    QDialog,
    QHBoxLayout,
    QMessageBox,
    QLabel,
)
from PyQt5.QtGui import QKeySequence, QIcon, QPainter
from PyQt5.QtCore import Qt, QRect


class CustomTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder_text = "Drag the selected word in here to add it to the list."

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.rowCount() == 0:
            painter = QPainter(self.viewport())
            painter.setPen(Qt.lightGray)

            # Set the font size
            font = painter.font()
            font.setPointSize(14)
            painter.setFont(font)

            # Wrap the text
            rect = self.rect()

            # Add padding
            padding = 20
            padded_rect = QRect(
                rect.left() + padding,
                rect.top() + padding,
                rect.width() - 2 * padding,
                rect.height() - 2 * padding,
            )
            painter.drawText(
                padded_rect, Qt.AlignCenter | Qt.TextWordWrap, self.placeholder_text
            )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word List")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon("images/logo_bl.png"))

        central_widget = QWidget(self)
        layout = QVBoxLayout()

        self.table_widget = CustomTableWidget(0, 2)
        self.table_widget.setHorizontalHeaderLabels(["Word", "Meaning"])
        self.table_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.verticalHeader().sectionClicked.connect(self.select_row)
        self.table_widget.cellChanged.connect(self.check_cell_length)
        layout.addWidget(self.table_widget)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.create_menu()

        self.setAcceptDrops(True)

    def create_menu(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        file_menu = QMenu("File", self)
        menubar.addMenu(file_menu)

        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_list)
        file_menu.addAction(new_action)

        """ open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action) """

        save_action = QAction("Save As", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = QMenu("Edit", self)
        menubar.addMenu(edit_menu)

        add_action = QAction("Add Row", self)
        add_action.setShortcut(QKeySequence(Qt.Key_Plus))
        add_action.triggered.connect(self.add_row)
        edit_menu.addAction(add_action)

        delete_action = QAction("Delete Row(s)", self)
        delete_action.setShortcut(QKeySequence(Qt.Key_Delete))
        delete_action.triggered.connect(self.delete_selected_rows)
        edit_menu.addAction(delete_action)

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about)
        menubar.addAction(self.about_action)

    def show_about(self):
        about_window = QDialog(self)
        about_window.setWindowTitle("About")
        about_window.setFixedSize(300, 200)
        about_window.setWindowFlags(
            about_window.windowFlags() & ~Qt.WindowContextHelpButtonHint
        )

        layout = QVBoxLayout()

        description = "A simple and intuitive application to create word lists from any text source. Whether you're a language learner, a teacher, or simply someone who loves words, the Word List application provides an easy-to-use interface to drag, drop, and manage words and their meanings."
        label = QLabel(description, about_window)
        label.setWordWrap(True)
        label.setMaximumWidth(350)
        layout.addWidget(label)

        author_label = QLabel("Author: Dmitri Markélov", about_window)
        layout.addWidget(author_label)

        button_layout = QHBoxLayout()
        github_button = QPushButton("GitHub", about_window)
        github_button.clicked.connect(
            lambda: self.open_link("https://github.com/di-marko")
        )
        github_button.setFocusPolicy(Qt.NoFocus)
        button_layout.addWidget(github_button)

        linkedin_button = QPushButton("LinkedIn", about_window)
        linkedin_button.clicked.connect(
            lambda: self.open_link("https://www.linkedin.com/in/dmitri-mark%C3%A9lov/")
        )
        linkedin_button.setFocusPolicy(Qt.NoFocus)
        button_layout.addWidget(linkedin_button)

        layout.addLayout(button_layout)
        about_window.setLayout(layout)
        about_window.exec_()

    def open_link(self, link):
        os.system(f'start "" "{link}"')

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def new_list(self):
        reply = QMessageBox.question(
            self,
            "New List",
            "Are you sure you want to create a new list?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.table_widget.setRowCount(0)

    """ def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Word List",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )
        if file_name:
            with open(file_name, "r") as file:
                self.table_widget.setRowCount(0)
                for line in file.readlines():
                    parts = line.strip().split("\t")
                    if len(parts) == 2:
                        word, translation = parts
                        row = self.table_widget.rowCount()
                        self.table_widget.insertRow(row)
                        self.table_widget.setItem(row, 0, QTableWidgetItem(word))
                        self.table_widget.setItem(row, 1, QTableWidgetItem(translation)) """

    def save_file(self):
        options = QFileDialog.Options()
        file_name, file_type = QFileDialog.getSaveFileName(
            self,
            "Save Word List",
            "",
            "Text Files (*.txt);;PDF Files (*.pdf);;All Files (*)",
            options=options,
        )
        if file_name:
            if file_type == "Text Files (*.txt)":
                with open(file_name, "w") as file:
                    for row in range(self.table_widget.rowCount()):
                        word_item = self.table_widget.item(row, 0)
                        translation_item = self.table_widget.item(row, 1)
                        if word_item and translation_item:
                            word = word_item.text()
                            translation = translation_item.text()
                            file.write(f"{word} - {translation}\n")
            elif file_type == "PDF Files (*.pdf)":
                self.generate_pdf(file_name)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def generate_pdf(self, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        col1_width = 60
        col2_width = 120
        for row in range(self.table_widget.rowCount()):
            word_item = self.table_widget.item(row, 0)
            translation_item = self.table_widget.item(row, 1)
            if word_item and translation_item:
                word = word_item.text()
                translation = translation_item.text()
                pdf.set_font("Arial", size=12)
                pdf.cell(col1_width, 10, word, border=1)
                pdf.multi_cell(col2_width, 10, translation, border=1)
        pdf.output(file_name)

    def dropEvent(self, event):
        word = event.mimeData().text().strip()
        if word:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(word))
            self.table_widget.setItem(row, 1, QTableWidgetItem(""))

    def add_row(self):
        selected_rows = sorted(
            set(
                index.row()
                for index in self.table_widget.selectionModel().selectedRows()
            )
        )
        if selected_rows:
            self.table_widget.insertRow(selected_rows[-1] + 1)
        else:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)

    def delete_selected_rows(self):
        reply = QMessageBox.question(
            self,
            "Delete Row(s)",
            "Are you sure you want to delete the selected row(s)?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            selected_rows = sorted(
                set(
                    index.row()
                    for index in self.table_widget.selectionModel().selectedRows()
                )
            )
            for row in reversed(selected_rows):
                self.table_widget.removeRow(row)

    def select_row(self, row):
        self.table_widget.selectRow(row)

    def check_cell_length(self, row, column):
        max_length = 50
        item = self.table_widget.item(row, column)
        if item and len(item.text()) > max_length:
            item.setText(item.text()[:max_length])
            QMessageBox.warning(
                self, "Warning", f"Maximum allowed length is {max_length} characters."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
