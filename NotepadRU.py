import tkinter as tk
from tkinter import filedialog
from cyrillic_keyboard import RU
from ttkthemes import ThemedTk
import sys
import os

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class NotepadRU_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("NotepadRU")
        self.set_window_icon()
        self.text_widget = tk.Text(root, wrap="word", undo=True)
        self.text_widget.pack(expand="yes", fill="both")
        self.create_menu()
        self.bind_shortcuts()
        self.text_widget.bind("<Return>", self.convert_to_RU)

    def set_window_icon(self):
        icon_path = resource_path("bin/NotepadRU_icon.ico")
        self.root.iconbitmap(icon_path)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        # Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.text_widget.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_widget.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)

    def new_file(self):
        self.text_widget.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, content)
            self.root.title(f"NotepadRU - {file_path}")

    def save_file(self, event = None):
        if hasattr(self, 'file_path'):
            content = self.text_widget.get(1.0, tk.END)
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(content)
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            content = self.text_widget.get(1.0, tk.END)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            self.file_path = file_path
            self.root.title(f"NotepadRU - {file_path}")

    def cut_text(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_widget.event_generate("<<Paste>>")

    def convert_to_RU(self, event):
        # Get the current cursor position
        cursor_position = self.text_widget.index(tk.INSERT)

        # Get the start and end indices of the current line
        line_start = cursor_position.split(".")[0] + ".0"
        line_end = cursor_position.split(".")[0] + ".end"

        # Get the text of the current line
        current_line = self.text_widget.get(line_start, line_end)

        # Convert the current line to uppercase
        current_line_RU = RU(current_line)

        # Replace the current line with the uppercase version
        self.text_widget.replace(line_start, line_end, current_line_RU)

    def bind_shortcuts(self):
        self.text_widget.bind("<Control-s>", self.save_file)

root = ThemedTk(themebg=True, theme='equilux')
app = NotepadRU_Window(root)
root.mainloop()