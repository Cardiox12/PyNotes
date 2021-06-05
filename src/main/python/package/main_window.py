from PySide2 import QtWidgets, QtGui

from package.api.note import Note, get_notes


class MainWindow(QtWidgets.QWidget):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("PyNotes")
        self.setup_ui()
        self.populate_notes()

    # UI

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.create_note_button = QtWidgets.QPushButton("Create Note")
        self.notes_list_widget = QtWidgets.QListWidget()
        self.content_text_edit = QtWidgets.QTextEdit()

        self.setObjectName("main_window")
        self.create_note_button.setObjectName("create_note_button")
        self.notes_list_widget.setObjectName("notes_list_widget")
        self.content_text_edit.setObjectName("content_text_edit")

    def modify_widgets(self):
        self.notes_list_widget.setFixedWidth(300)
        style = self.ctx.get_resource("style.css")

        with open(style, "r") as f:
            self.setStyleSheet(f.read())

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.create_note_button, 1, 0, 1, 1)
        self.main_layout.addWidget(self.notes_list_widget, 0, 0, 1, 1)
        self.main_layout.addWidget(self.content_text_edit, 0, 1, 2, 1)

    def setup_connections(self):
        self.create_note_button.clicked.connect(self.create_note)
        self.content_text_edit.textChanged.connect(self.save_note)
        self.notes_list_widget.itemSelectionChanged.connect(self.populate_note_content)
        QtWidgets.QShortcut(QtGui.QKeySequence("Backspace"), self.notes_list_widget, self.delete_selected_note)

    # API

    def create_note(self):
        title, result = QtWidgets.QInputDialog.getText(self, "Add note", "Title: ")

        if result and title:
            note = Note(title)
            note.save()
            self.add_note_to_list_widget(note)

    def show_delete_confirmation_message_box(self, title):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setText(f"Are you sure you want to delete {title} ?")
        messageBox.setWindowTitle("Confirmation")
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        messageBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        ret = messageBox.exec_()

        if ret == QtWidgets.QMessageBox.Cancel:
            return False
        return True

    def delete_selected_note(self):
        selected_items = self.notes_list_widget.selectedItems()

        if not selected_items:
            return False
        select_item = selected_items[0]
        confirm = self.show_delete_confirmation_message_box(select_item.note.title)

        if confirm:
            if select_item.note.delete():
                row = self.notes_list_widget.row(select_item)
                self.notes_list_widget.takeItem(row)

    def populate_notes(self):
        notes = get_notes()

        for note in notes:
            self.add_note_to_list_widget(note)

    def populate_note_content(self):
        selected_items = self.notes_list_widget.selectedItems()

        if selected_items:
            content = selected_items[0].note.content
            self.content_text_edit.setText(content)

    def save_note(self):
        selected_items = self.notes_list_widget.selectedItems()

        if selected_items:
            selected_note = selected_items[0].note
            selected_note.content = self.content_text_edit.toPlainText()
            selected_note.save()

    def add_note_to_list_widget(self, note):
        item = QtWidgets.QListWidgetItem(note.title)
        item.note = note
        self.notes_list_widget.addItem(item)
