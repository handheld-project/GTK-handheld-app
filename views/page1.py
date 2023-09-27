# pages/page1.py
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Page1(Gtk.Box):
    def __init__(self):
        super().__init__()

        label = Gtk.Label("Page 1")
        self.pack_start(label, True, True, 0)

    def show_page(self):
        # Logic to display page 1
        pass
