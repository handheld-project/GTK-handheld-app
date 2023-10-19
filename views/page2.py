# pages/page2.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Page2(Gtk.Box):
    def __init__(self , stack ):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        
        self.stack = stack
        # mainbox 
        self.main_box = Gtk.Box()
        # gridPage
        self.gridPage = Gtk.Grid() 
        # grid
        self.grid = Gtk.grid() 
        # Image
            #Container
        self.boxImage = Gtk.Box() 
        self.image = Gtk.Image() 
        # Calculated Content 
        self 
        # Time Content 