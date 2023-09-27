# pages/page3.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import cv2
import numpy as np
from PIL import Image

class CameraApp(Gtk.Box):
    def __init__(self):
        super().__init__()

        self.image = Gtk.Image()
        self.pack_start(self.image, True, True, 0)

        self.capture = cv2.VideoCapture(0)  # Open the default camera (0)

        # Set up a timer to periodically update the image
        self.timer = GLib.timeout_add(75, self.update_image)

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
