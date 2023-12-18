import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import cv2
import datetime
import threading
import time
import os 

class CircularButton(Gtk.EventBox):
    def __init__(self , stack , main_window , capture ):
        super().__init__()

        self.stack = stack
        self.main_window = main_window
        self.export_data={}
        self.stop_event = threading.Event() 
        self.clicked = False
        
        self.grid = Gtk.Grid()

        self.circular_area = Gtk.DrawingArea() 
        self.circular_area.set_size_request(70, 70)
        self.circular_area.connect("draw", self.on_draw)
        self.circular_area.set_valign(Gtk.Align.CENTER)
        self.circular_area.set_halign(Gtk.Align.CENTER)

        self.inner_circular_area = Gtk.DrawingArea() 
        self.inner_circular_area.set_size_request(55, 55)
        self.inner_circular_area.connect("draw", self.on_draw_inner)
        self.inner_circular_area.set_valign(Gtk.Align.CENTER)
        self.inner_circular_area.set_halign(Gtk.Align.CENTER)

        self.grid.attach(self.inner_circular_area, 0, 1, 1, 1)    
        self.grid.attach(self.circular_area, 0, 1, 1, 1)    

        # video 
        self.capture = capture      
        # set to make page1 update its self.video from this circulabutton captured data

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
    

    def on_button_press(self, widget, event ):
        print("button",self.capture)

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.clicked = True 
   
        ret, frame = self.capture.read()

        if os.path.exists("./temp") and os.path.isdir("./temp") : 
            pass 
        else :
            os.makedirs("./temp")

        if ret:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            temp_filename = f"./temp/{current_datetime}.png"
            self.export_data['src_image'] = temp_filename
            cv2.imwrite(temp_filename, frame)
            print(f"Image saved to: {temp_filename}")
        
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
        time.sleep(0.5)  # Simulate 3 seconds of processing
        # Switch to Page 2 after processing is complete
        print("process_image_stop")
        GLib.idle_add(self.update_export_data) 
        GLib.idle_add(self.switch_to_page) 

        self.stop_event.set()
        
    def update_export_data(self):
        self.main_window.set_processing_data(self.export_data)

    def switch_to_page(self):
        self.stack.set_visible_child_name("page2")

    def set_capture(self,capture): 
        self.capture = capture
  
  