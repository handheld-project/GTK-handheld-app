import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import cv2
import numpy as np
from PIL import Image

class Page1(Gtk.Box):

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.capture = cv2.VideoCapture(0) 
        self.image = Gtk.Image()
        self.timer = GLib.timeout_add(60, self.update_image)
        
        # label init
        self.label1 = Gtk.Label(label="ถ่ายรูปป้ายโฆษณา ภายในระยะห่างจากป้าย xx เมตร ")
        self.label1.get_style_context().add_class("label")

        # button init
        self.button = CircularButton()
    
        self.load_css("./styles/page1.style.css")
      
        self.add(self.label1)
        self.add(self.image)
        self.add(self.button)

    def load_css(self, filename):
        # Create a CSS provider
        provider = Gtk.CssProvider()

        # Load CSS styles from the file
        try:
            provider.load_from_path(filename)
        except Exception as e:
            print(f"Error loading CSS from '{filename}': {e}")
            return

        # Apply the CSS style to the label
        context = self.label1.get_style_context()
        context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
  

    def update_image(self):
        ret, frame = self.capture.read()
        if ret:
            # Convert the OpenCV image (BGR format) to RGB using NumPy
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to a format suitable for GdkPixbuf
            image = Image.fromarray(frame_rgb)
            image = image.transpose(Image.FLIP_LEFT_RIGHT)  # Optionally flip the image horizontally

            # Create the GdkPixbuf from the PIL image
            image_bytes = bytes(image.tobytes())
            gdk_pixbuf = GdkPixbuf.Pixbuf.new_from_data(
                image_bytes, GdkPixbuf.Colorspace.RGB, False, 8, image.width, image.height, image.width * 3
            )

            # Update the GTK Image widget with the new image
            self.image.set_from_pixbuf(gdk_pixbuf)

        return True
    
    def on_button_click(self,widget):
        print("clicked")
    



class CircularButton(Gtk.EventBox):
    def __init__(self):
        super().__init__()

        # Create a circular area
        circular_area = Gtk.DrawingArea()
        circular_area.set_size_request(100, 100)
        circular_area.connect("draw", self.on_draw)
        self.connect("button-press-event", self.on_button_press)
        self.add(circular_area)

    def on_draw(self, widget, context):
        # Draw a circle on the button
        allocation = widget.get_allocation()
        radius = min(allocation.width, allocation.height) / 2
        center_x = allocation.width / 2
        center_y = allocation.height / 2

        context.set_source_rgb(0.8, 0.8, 0.8)  

        context.arc(center_x, center_y, radius, 0, 2 * 3.141592)
        context.fill()

    def on_button_press(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            # Handle left mouse button click here
            print("Button clicked")