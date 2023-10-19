import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
import datetime
import threading
import time

class Page1(Gtk.Box):

    def __init__(self,stack):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        
        self.stack = stack
        # mainbox 
        self.main_box = Gtk.Box()

        # grid page container
        self.gridPage = Gtk.Grid()
        self.gridPage.set_valign(Gtk.Align.CENTER)
        self.gridPage.set_halign(Gtk.Align.CENTER)
        self.gridPage.set_column_homogeneous(True)  # Make columns expand equall

        # Video/Image Init 
        self.capture = cv2.VideoCapture(0) 
        self.video = Gtk.Image()
        self.timer = GLib.timeout_add(60, self.update_image)
        self.video.set_size_request(900, 700)

        # label init
            #container 
        self.boxLabelConainter = Gtk.Box() 
        self.boxLabelConainter.set_valign(Gtk.Align.CENTER)
        self.boxLabelConainter.set_halign(Gtk.Align.CENTER)

        self.pageLabel = Gtk.Label(label="ถ่ายรูปป้ายโฆษณา ภายในระยะห่างจากป้าย xx เมตร ")
        self.pageLabel.get_style_context().add_class("label")
        self.pageLabel.set_valign(Gtk.Align.CENTER)
        self.pageLabel.set_halign(Gtk.Align.CENTER)

        self.boxLabelConainter.add(self.pageLabel)

        # button init
            #Container 
        self.boxButtonContainer = Gtk.Box() 
        self.boxButtonContainer.set_valign(Gtk.Align.CENTER)
        self.boxButtonContainer.set_halign(Gtk.Align.CENTER)

        self.button = CircularButton(self.capture , self.stack)
        
        self.boxButtonContainer.add(self.button)         

        # Grid init
        self.grid = Gtk.Grid()
        self.grid.set_valign(Gtk.Align.CENTER)
        self.grid.set_halign(Gtk.Align.CENTER)

        self.grid.attach(self.video, 0, 0, 1, 1)    
        self.grid.attach(self.boxButtonContainer, 1, 0, 1, 1)      

        # style setting 
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_path("./styles/page1.style.css")

        contextGridPage = self.gridPage.get_style_context()
        contextpageLabel = self.pageLabel.get_style_context()
        contextGrid = self.grid.get_style_context()
        contextVideo = self.video.get_style_context()        
        contextBoxButtonContainer = self.boxButtonContainer.get_style_context()       
        contextBoxLabelContainer = self.boxLabelConainter.get_style_context()    
        
        self.gridPage.get_style_context().add_class("gridPage")
        self.pageLabel.get_style_context().add_class("label")
        self.grid.get_style_context().add_class("grid")  # Add a CSS class to the grid for styling
        self.video.get_style_context().add_class("video")  # Add a CSS class to the grid for styling
        self.boxButtonContainer.get_style_context().add_class("BoxCantainer")  # Add a CSS class to the grid for styling
        self.boxLabelConainter.get_style_context().add_class("labelCantainer")  # Add a CSS class to the grid for styling
                
        contextGridPage.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextpageLabel.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextGrid.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextVideo.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextBoxButtonContainer.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextBoxLabelContainer.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.gridPage.attach(self.boxLabelConainter,0,0,1,1)
        self.gridPage.attach(self.grid,0,1,1,1)

        self.main_box.pack_start( self.gridPage, True, True, 0)
        self.add(self.main_box)
        
  
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
    def __init__(self,capture , stack):
        super().__init__()
        self.stack = stack
        self.capture = capture
        self.clicked = False

        self.grid = Gtk.Grid()

        self.circular_area = Gtk.DrawingArea() 
        self.circular_area.set_size_request(100, 100)
        self.circular_area.connect("draw", self.on_draw)
        self.circular_area.set_valign(Gtk.Align.CENTER)
        self.circular_area.set_halign(Gtk.Align.CENTER)

        self.inner_circular_area = Gtk.DrawingArea() 
        self.inner_circular_area.set_size_request(80, 80)
        self.inner_circular_area.connect("draw", self.on_draw_inner)
        self.inner_circular_area.set_valign(Gtk.Align.CENTER)
        self.inner_circular_area.set_halign(Gtk.Align.CENTER)

        self.grid.attach(self.inner_circular_area, 0, 1, 1, 1)    
        self.grid.attach(self.circular_area, 0, 1, 1, 1)    

        self.connect("button-press-event", self.on_button_press)
        self.connect("button_release_event", self.on_button_release)

        self.add(self.grid)

    def on_draw_inner(self, widget, context):
        # Draw a circle on the button
        allocation = widget.get_allocation()
        radius = min(allocation.width, allocation.height) / 2
        center_x = allocation.width / 2
        center_y = allocation.height / 2

        if self.clicked:
            context.set_source_rgb(0.5, 0.5, 0.5)  # Change to a darker color when clicked
        else:
            context.set_source_rgb(0.7, 0.7, 0.7)  # Original color


        context.arc(center_x, center_y, radius, 0, 2 * 3.141592)
        context.fill()


    def on_draw(self, widget, context):
        # Draw a circle on the button
        allocation = widget.get_allocation()
        radius = min(allocation.width, allocation.height) / 2
        center_x = allocation.width / 2
        center_y = allocation.height / 2

        if self.clicked:
            context.set_source_rgb(0.4, 0.4, 0.4)  # Change to a darker color when clicked
        else:
            context.set_source_rgb(0.6, 0.6, 0.6)  # Original color


        context.arc(center_x, center_y, radius, 0, 2 * 3.141592)
        context.fill()

    def on_button_press(self, widget, event):

        self.clicked = True 
        
        ret, frame = self.capture.read()
        if ret:
            # Generate a filename based on the current date and time
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            temp_filename = f"./temp/{current_datetime}.png"  # Specify the path to the 'temp' folder

            # Save the captured frame as a PNG image
            cv2.imwrite(temp_filename, frame)

            print(f"Image saved to: {temp_filename}")
            print(current_datetime)
    
        widget.queue_draw()
    
    def on_button_release(self, widget , event )  :
        
        self.clicked = False
        
        print("button released")
        print(self.clicked)

        widget.queue_draw()

        self.stack.set_visible_child_name("loadingPage")
        # Start the image processing in a separate thread
        processing_thread = threading.Thread(target = self.process_image )
        processing_thread.start()

    # image processing flow 

    def process_image(self):
        # Simulate image processing (replace this with your actual processing logic)
        time.sleep(3)  # Simulate 3 seconds of processing
        # Switch to Page 2 after processing is complete
        GLib.idle_add(self.switch_to_page) 
        
    def switch_to_page(self):
        self.stack.set_visible_child_name("page2")