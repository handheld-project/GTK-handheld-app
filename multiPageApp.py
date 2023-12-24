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
        self.set_default_size(800, 480)
        self.connect("destroy", Gtk.main_quit)
        self.set_resizable(False)
        self.stack = Gtk.Stack()
        self.page1 = None
        self.page2 = None
        self.page3 = None
        self.loadingPage = None
        self.splashPage = None

        self.processing_data = {
            "src_image" : "" ,
            "top_left" : None ,
            "top_right" : None ,
            "bottom_left": None ,
            "bottom_right": None , 
            "detected_type":  0 

        }
        self.commited_document = {
               "width" :  "" ,
                "height" : ""  ,
                "is_movable" : False ,
                "type" : "" , 
                "area" : "" , 
                "price" : "" ,
                "latitude" : "" ,
                "longitude" : "" ,
                "time" : ""
        } 
        self.mapType = {1:"อักษรภาษาไทยทั้งหมด", 2:"อักษรภาษาไทยปนกับภาษาต่างประเทศ/ภาพ/เครื่องหมายอื่น", 3:"อักษาไทยอยู่ต่ำกว่าอักษรต่างประเทศ/ไม่มีอักษรไทยเลย"}

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
        self.stack.add_named(self.page3, "page3")

        # self.stack.add_named(self.splashPage, "splashPage")
        self.stack.add_named(self.loadingPage, "loadingPage")

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

        # self.fullscreen()

        # Schedule a callback to switch to Page1 after 3 seconds
        # GLib.timeout_add_seconds(3, self.show_page1)
    
    def get_mapType(self): 
        return self.mapType 

    def set_document(self, document):
        self.commited_document = document

    def get_document(self):
        return self.commited_document

    def set_processing_data(self, processing_data):
        self.processing_data = processing_data

    def get_processing_data(self):
        return self.processing_data

    def show_page1(self):
        self.stack.set_visible_child_name("page1")
        
        return False  # Stop the timeout callback

    def run(self):
        self.show_all()