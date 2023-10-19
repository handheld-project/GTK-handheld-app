import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from views.page1 import Page1
from views.page2 import Page2
from views.page3 import CameraApp
from views.loadingPage import LoadingPage

class MultiPageApp(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.set_default_size(1080, 720)
        self.connect("destroy", Gtk.main_quit)

        self.stack = Gtk.Stack()
        self.add(self.stack)

        self.page1 = Page1(self.stack)
        self.page2 = Page2(self.stack)
        self.page3 = CameraApp()
        self.loadingPage = LoadingPage()

        self.stack.add_named(self.page1, "page1")
        self.stack.add_named(self.page2, "page2")
        self.stack.add_named(self.page3, "page3")
        self.stack.add_named(self.loadingPage, "loadingPage")

        # Set the background color for the entire window
        background_color = Gdk.RGBA()
        background_color.parse("rgb(184, 184, 184)")  # Replace with your desired color
        self.override_background_color(Gtk.StateFlags.NORMAL, background_color)

        #styling css 
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("./styles/main.style.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


    def run(self):
        self.show_all()

if __name__ == "__main__":
    app = Gtk.Application(application_id="com.example.myapp")
    app_window = MultiPageApp(app)
    app.add_window(app_window)
    app_window.run()
    Gtk.main()
