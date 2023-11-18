# pages/page3.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import cv2
import numpy as np
from PIL import Image

class Page3(Gtk.Grid):
    def __init__(self,main_window,stack):
        super().__init__()
        

        
