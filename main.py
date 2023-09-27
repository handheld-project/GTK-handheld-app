# main.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from views.page1 import Page1
from views.page2 import Page2
from views.page3 import CameraApp

class MultiPageApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Multi-Page Gtk App")
        self.set_default_size(400, 300)
        self.connect("destroy", Gtk.main_quit)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.page1 = Page1()
        self.page2 = Page2()
        self.page3 = CameraApp()

        self.notebook.append_page(self.page1, Gtk.Label("Page 1"))
        self.notebook.append_page(self.page2, Gtk.Label("Page 2"))
        self.notebook.append_page(self.page3, Gtk.Label("Page 3_CameraApp"))

    def run(self):
        self.show_all()

if __name__ == "__main__":
    app = MultiPageApp()
    app.run()
    Gtk.main()
