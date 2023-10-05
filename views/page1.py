import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
import datetime

class Page1(Gtk.Box):

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Video/Image Init 
        self.capture = cv2.VideoCapture(0) 
        self.video = Gtk.Image()
        self.timer = GLib.timeout_add(60, self.update_image)
        self.video.set_size_request(900, 700)

        # label init
        self.label1 = Gtk.Label(label="ถ่ายรูปป้ายโฆษณา ภายในระยะห่างจากป้าย xx เมตร ")
        self.label1.get_style_context().add_class("label")
        self.label1.set_valign(Gtk.Align.CENTER)
        self.label1.set_halign(Gtk.Align.CENTER)

        # button init
            #Container 
        self.boxButtonContainer = Gtk.Box() 
        self.boxButtonContainer.set_valign(Gtk.Align.CENTER)
        self.boxButtonContainer.set_halign(Gtk.Align.CENTER)

            #Container inner 
        self.innerBoxButtonContainer = Gtk.Box() 
        self.innerBoxButtonContainer.set_valign(Gtk.Align.CENTER)
        self.innerBoxButtonContainer.set_halign(Gtk.Align.CENTER)

        self.button = CircularButton(self.capture)
        self.innerButton = InnerCircularButton(self.capture)

        self.boxButtonContainer.add(self.button)        
        self.innerBoxButtonContainer.add(self.innerButton)        

        # Grid init
        self.grid = Gtk.Grid()
        self.grid.set_valign(Gtk.Align.CENTER)
        self.grid.set_halign(Gtk.Align.CENTER)

        self.grid.attach(self.label1, 0, 0, 2, 1)
        self.grid.attach(self.video, 0, 1, 1, 1)
        self.grid.attach(self.innerBoxButtonContainer, 1, 0, 1, 2)      
        self.grid.attach(self.boxButtonContainer, 1, 0, 1, 2)      

        
        # style setting 
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_path("./styles/page1.style.css")

        contextLabel1 = self.label1.get_style_context()
        contextGrid = self.grid.get_style_context()
        contextVideo = self.video.get_style_context()        
        contextBoxButtonContainer = self.boxButtonContainer.get_style_context()      
        contextInnerBoxButtonContainer = self.innerBoxButtonContainer.get_style_context()      

        self.label1.get_style_context().add_class("label")
        self.grid.get_style_context().add_class("grid")  # Add a CSS class to the grid for styling
        self.video.get_style_context().add_class("video")  # Add a CSS class to the grid for styling
        self.boxButtonContainer.get_style_context().add_class("BoxCantainer")  # Add a CSS class to the grid for styling
        self.innerBoxButtonContainer.get_style_context().add_class("innerBoxButtonContainer")  # Add a CSS class to the grid for styling
        
        contextLabel1.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextGrid.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextVideo.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextBoxButtonContainer.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextInnerBoxButtonContainer.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.add(self.grid)
        
  
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
            self.video.set_from_pixbuf(gdk_pixbuf)

        return True


class CircularButton(Gtk.EventBox):
    def __init__(self,capture):
        super().__init__()
        self.capture = capture
        
        # Create a circular area
        circular_area = Gtk.DrawingArea()
        circular_area.set_size_request(100, 100)

        circular_area.connect("draw", self.on_draw)

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

class InnerCircularButton(Gtk.EventBox):
    def __init__(self,capture):
        super().__init__()
        self.capture = capture

        inner_circular_area = Gtk.DrawingArea() 
        inner_circular_area.set_size_request(80, 80)

        inner_circular_area.connect("draw", self.on_draw_inner)
        inner_circular_area.set_valign(Gtk.Align.CENTER)
        inner_circular_area.set_halign(Gtk.Align.CENTER)

        self.connect("button-press-event", self.on_button_press)
        self.add(inner_circular_area)


    def on_draw_inner(self, widget, context):
        # Draw a circle on the button
        allocation = widget.get_allocation()
        radius = min(allocation.width, allocation.height) / 2
        center_x = allocation.width / 2
        center_y = allocation.height / 2

        context.set_source_rgb(0.7, 0.7, 0.7)  

        context.arc(center_x, center_y, radius, 0, 2 * 3.141592)
        context.fill()

    def on_button_press(self, widget, event):
        print("method from innter button")
        ret, frame = self.capture.read()
        if ret:
            # Generate a filename based on the current date and time
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            temp_filename = f"./temp/{current_datetime}.png"  # Specify the path to the 'temp' folder

            # Save the captured frame as a PNG image
            cv2.imwrite(temp_filename, frame)

            print(f"Image saved to: {temp_filename}")
            print(current_datetime)