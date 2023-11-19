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

class Page1(Gtk.Grid):

    def __init__(self,main_window,stack ):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        
        self.stack = stack
        self.main_window = main_window

        # mainbox 

        # grid page container
        self.gridPage = Gtk.Grid()
        self.gridPage.set_valign(Gtk.Align.CENTER)
        self.gridPage.set_halign(Gtk.Align.CENTER)
        self.gridPage.set_column_homogeneous(True)  # Make columns expand equall

        # Video/Image Init 
        self.capture = cv2.VideoCapture(0) 
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set width to 640 pixels
        # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set height to 480 pixels
        self.video = Gtk.Image()
        self.timer = GLib.timeout_add(100, self.update_image)
        self.video.set_size_request(800, 600)

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

        self.button = CircularButton(self.capture , self.stack , self.main_window)
        
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

        self.add(self.gridPage)

        # connect event listen
        self.set_can_focus(True) 
        self.connect("key-press-event", self.on_key_press)

    def on_key_press(self, widget, event):
        # Check the keyval attribute of the event to get the key code
        keyval = event.keyval

        # Print the key value
        print(f"Key pressed: {keyval}")
        
        # press enter / confrim button 
        if(keyval == 65293) : 
            self.button.emit("button-press-event", None)
        return True

    def update_image(self):
        
        ret, frame = self.capture.read()
    
        if ret:
            # Convert the OpenCV image (BGR format) to RGB using NumPy
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Calculate the height to maintain 4:3 aspect ratio with width close to 850 pixels

            # Resize the image while maintaining the aspect ratio
            resized_frame = cv2.resize(frame_rgb, (728, 546))

            # Convert to a format suitable for GdkPixbuf
            image = Image.fromarray(resized_frame)
            

            # Create the GdkPixbuf from the PIL image with the desired size
            image_bytes = bytes(image.tobytes())
            gdk_pixbuf = GdkPixbuf.Pixbuf.new_from_data(
                image_bytes, GdkPixbuf.Colorspace.RGB, False, 8, image.width, image.height, image.width * 3
            )

            # Update the GTK Image widget with the new image
            self.video.set_from_pixbuf(gdk_pixbuf)

        return True
    
    def release_capture(self) :
        self.set_can_focus(False) 
        self.capture.release()

class CircularButton(Gtk.EventBox):
    def __init__(self, capture , stack , main_window):
        super().__init__()

        self.stack = stack
        self.main_window = main_window
        self.export_data={}
        self.stop_event = threading.Event() 
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
        # self.stack.get_child_by_name("page1").release_capture()

        print(f"Setting capture resolution to 1280x720")
        # self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        print(f"Capture width: {self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)}") 
        print(f"Capture height: {self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)}")

        self.clicked = True 

        ret, frame = self.capture.read()
        if ret:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            temp_filename = f"./temp/{current_datetime}.png"
            self.export_data['src_image'] = temp_filename
            cv2.imwrite(temp_filename, frame)

            print(f"Image saved to: {temp_filename}")
            print(current_datetime)

        self.capture.release()
        widget.queue_draw()

        # Continue with other processing or thread creation as needed
        processing_thread = threading.Thread(target=self.process_image)
        processing_thread.start()

    def on_button_release(self, widget , event )  :
        self.clicked = False
        widget.queue_draw()
        # Set the loading page visible after the processing thread completes
        GLib.idle_add(self.show_loading_page)
    
    def show_loading_page(self):
        self.stack.set_visible_child_name("loadingPage")
        return False  # Stop the idle callback

    # image processing flow 

    def process_image(self):
        # Simulate image processing (replace this with your actual processing logic)
        print("process_image_start")
        time.sleep(1)  # Simulate 3 seconds of processing
        # Switch to Page 2 after processing is complete
        GLib.idle_add(self.switch_to_page) 
        print("process_image_stop")
        
        self.main_window.set_processing_data(self.export_data)
        self.stop_event.set()
        

    def switch_to_page(self):
        self.stack.set_visible_child_name("page2")