import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from multiPageApp import MultiPageApp

if __name__ == "__main__":
    app = Gtk.Application(application_id="com.example.myapp")
    app_window = MultiPageApp(app)
    app.add_window(app_window)
    app_window.run()
    Gtk.main()