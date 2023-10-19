# pages/page2.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class LoadingPage(Gtk.Box):
    def __init__(self):
        super().__init__()

        self.spinner = Gtk.Spinner()
        self.spinner.start()

        self.pack_start(self.spinner, True, True, 0)