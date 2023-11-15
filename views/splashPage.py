import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf


class SplashPage(Gtk.Box):
    def __init__(self,stack):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.stack = stack
        self.gridPageLayout = Gtk.Grid()

        # background img
        self.image_file = "./assets/images/SplashPage.png"  
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.image_file)
        self.image_widget = Gtk.Image.new_from_pixbuf(self.pixbuf)

        self.image_widget.set_halign(Gtk.Align.FILL)
        self.image_widget.set_valign(Gtk.Align.FILL)

        # spinner 
        self.spinner = Gtk.Spinner()
        self.spinner.start()
        
        # left top width height 
        self.gridPageLayout.attach( self.spinner,1,1,1,1)
        self.gridPageLayout.attach( self.image_widget,0,0,3,3)


        # styles
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_path("./styles/spinner.style.css")
        self.spinner.get_style_context().add_class("spinner")
        self.spinner.get_style_context().add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


        self.add(self.gridPageLayout)

    
