import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from views.page1 import Page1
from views.page2 import Page2
from views.page3 import Page3
from views.loadingPage import LoadingPage
from views.splashPage import SplashPage

class MultiPageApp(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.processing_data = {}
        self.set_default_size(1080, 720)
        self.connect("destroy", Gtk.main_quit)
        self.set_resizable(False)
        self.stack = Gtk.Stack()
        self.page1 = None
        self.page2 = None
        self.page3 = None
        self.loadingPage = None
        self.splashPage = None

        self.init_stack()
        self.init_main_app_window()

    def init_stack(self):
        self.add(self.stack)
        self.page1 = Page1(self,self.stack)
        self.page2 = Page2(self,self.stack)
        self.page3 = Page3(self,self.stack)
        self.loadingPage = LoadingPage()
        self.splashPage = SplashPage(self.stack)
 
        self.stack.add_named(self.page1, "page1")
        self.stack.add_named(self.page2, "page2")
        self.stack.add_named(self.splashPage, "splashPage")
        self.stack.add_named(self.loadingPage, "loadingPage")
        self.stack.add_named(self.page3, "page3")

    def init_main_app_window(self):
        # Set the background color for the entire window
        background_color = Gdk.RGBA()
        background_color.parse("rgb(184, 184, 184)")  # Replace with your desired color
        self.override_background_color(Gtk.StateFlags.NORMAL, background_color)

        # Styling css 
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("./styles/main.style.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Schedule a callback to switch to Page1 after 3 seconds
        # GLib.timeout_add_seconds(3, self.show_page1)
        
  
    def reset_all_page(self):
        new_stack = Gtk.Stack()

        self.page1 = None
        self.page2 = None
        self.page3 = None
        self.loadingPage = None
        self.splashPage = None

        # Create new instances of pages
        self.page1 = Page1(self, new_stack)
        self.page2 = Page2(self, new_stack)
        self.page3 = Page3(self, new_stack)
        self.loadingPage = LoadingPage()
        self.splashPage = SplashPage(new_stack)
        
        print("update pageId", self.page1 ,  self.page2)

        # Add the new instances to the new stack
        new_stack.add_named(self.page1, "page1")
        new_stack.add_named(self.page2, "page2")
        new_stack.add_named(self.splashPage, "splashPage")
        new_stack.add_named(self.loadingPage, "loadingPage")
        new_stack.add_named(self.page3, "page3")
        
        # Replace the old stack with the new one
        self.replace_stack(new_stack)
        
        # Set the visible child to "page1"
        # new_stack.set_visible_child_name("page1")

    def replace_stack(self, new_stack):
        # Get the parent of the current stack
        parent = self.stack.get_parent()
        
        # Remove the old stack from its parent
        parent.remove(self.stack)
        
        # Set the new stack as the stack in the MainWindow
        self.stack = new_stack
        
        # Add the new stack to its parent
        parent.add(self.stack)
        
    def set_processing_data(self, processing_data):
        self.processing_data = processing_data

    def get_processing_data(self):
        return self.processing_data

    def show_page1(self):
        self.stack.set_visible_child_name("page1")
        return False  # Stop the timeout callback

    def run(self):
        self.show_all()