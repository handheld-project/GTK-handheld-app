import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib ,Gdk
from PIL import Image
from components.circularButton import CircularButton
from picamera2 import Picamera2
from libcamera import controls
import time
import RPi.GPIO as GPIO
import numpy as np
import cv2
import subprocess

class Page1(Gtk.Grid):

    def __init__(self,main_window,stack ) :
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        #software init

        self.stop_event = threading.Event()


        self.stack = stack
        self.openTimes = 0
        self.main_window = main_window
        self.capture = None
        self.video = None
        self.timer = None
        self.gridPage = None
        self.boxLabelConainter = None
        self.pageLabel = None
        self.boxButtonContainer = None
        self.button = None
        self.grid = None
        self.style_provider = None
        self.capture = Picamera2()
        self.capture.configure(self.capture.create_preview_configuration(main={"format": 'XRGB8888', "size": (1280, 720)}))
        self.capture.start()


        self.generate_interface()
        self.set_up_event()

    def set_up_event(self):
        self.set_can_focus(True)
        self.video.connect("draw", self.on_draw)
        self.stack.connect("notify::visible-child-name", self.on_stack_visible_child_changed)
        self.connect("key-press-event", self.on_key_press)
        self.connect("key-release-event", self.on_key_release )
        self.timer = GLib.timeout_add(100, self.update_image, self.video)

    def generate_interface(self):

        # grid page container
        self.gridPage = Gtk.Grid()
        self.gridPage.set_valign(Gtk.Align.CENTER)
        self.gridPage.set_halign(Gtk.Align.CENTER)
        self.gridPage.set_column_homogeneous(True)  # Make columns expand equall

        # Video/Image Init

        self.video = Gtk.DrawingArea()
        # self.timer = GLib.timeout_add(100, self.update_image)
        self.video.set_size_request(600, 450)
        self.reset_capture()

        # label init
            #container
        self.boxLabelConainter = Gtk.Box()
        self.boxLabelConainter.set_valign(Gtk.Align.CENTER)
        self.boxLabelConainter.set_halign(Gtk.Align.CENTER)

        self.pageLabel = Gtk.Label(label="ถ่ายรูปป้ายโฆษณา ")
        self.pageLabel.get_style_context().add_class("label")
        self.pageLabel.set_valign(Gtk.Align.CENTER)
        self.pageLabel.set_halign(Gtk.Align.CENTER)

        self.boxLabelConainter.add(self.pageLabel)

        # button init
            #Container
        self.boxButtonContainer = Gtk.Box()
        self.boxButtonContainer.set_valign(Gtk.Align.CENTER)
        self.boxButtonContainer.set_halign(Gtk.Align.CENTER)
        self.button = CircularButton( self.stack , self.main_window , self.capture )

        self.boxButtonContainer.add(self.button)

        # Grid init
        self.grid = Gtk.Grid()
        self.grid.set_valign(Gtk.Align.CENTER)
        self.grid.set_halign(Gtk.Align.CENTER)


        self.grid.attach(self.video, 0, 0, 1, 1)
        self.grid.attach(self.boxButtonContainer, 1, 0, 1, 1)

        self.gridPage.attach(self.boxLabelConainter,0,0,1,1)
        self.gridPage.attach(self.grid,0,1,1,1)

        self.init_css_context()

        self.add(self.gridPage)


    def init_css_context(self):
        # style setting
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_path("./styles/page1.style.css")

        contextGridPage = self.gridPage.get_style_context()
        contextpageLabel = self.pageLabel.get_style_context()
        contextGrid = self.grid.get_style_context()
        contextBoxButtonContainer = self.boxButtonContainer.get_style_context()
        contextBoxLabelContainer = self.boxLabelConainter.get_style_context()

        self.gridPage.get_style_context().add_class("gridPage")
        self.pageLabel.get_style_context().add_class("label")
        self.grid.get_style_context().add_class("grid")  # Add a CSS class to the grid for styling
        contextVideo = self.video.get_style_context()
        self.video.get_style_context().add_class("video")  # Add a CSS class to the grid for styling
        contextVideo.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.boxButtonContainer.get_style_context().add_class("BoxCantainer")  # Add a CSS class to the grid for styling
        self.boxLabelConainter.get_style_context().add_class("labelCantainer")  # Add a CSS class to the grid for styling

        contextGridPage.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextpageLabel.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextGrid.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextBoxButtonContainer.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        contextBoxLabelContainer.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def stop_update_Ui(self):
        if self.timer is not None:
            GLib.source_remove(self.timer)
            self.timer = None

    def reset_capture (self) :
        if self.capture:
            #self.capture.close()
            pass
        #self.capture.start()
        pass

    def reset_timer(self):
        self.timer = GLib.timeout_add(100, self.update_image, self.video)

    def on_draw(self, widget, context):

        frame = self.capture.capture_array()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized_frame = cv2.resize(frame_rgb, (800, 450))

        # Convert to a format suitable for GdkPixbuf
        image_data = resized_frame.tobytes()
        gdk_pixbuf = GdkPixbuf.Pixbuf.new_from_data(
                image_data,
                GdkPixbuf.Colorspace.RGB,
                False,
                8,
                resized_frame.shape[1],  # width
                resized_frame.shape[0],  # height
                resized_frame.shape[1] * 3,  # rowstride
        )

            # Draw the GdkPixbuf onto the drawing area
        Gdk.cairo_set_source_pixbuf(context, gdk_pixbuf, 0, 0)
        context.paint()

        return False  # Return False to stop the default draw handler

    def on_key_press(self, widget, event):
        keyval = event.keyval
        print(f"Key pressed: {keyval}")
        if(keyval == 122) :
            self.button.emit("button-press-event", None)

        return True

    def on_key_release(self, widget , event) :

        keyval = event.keyval
        if(keyval == 122) :
            self.button.emit("button-release-event", None)
        print("the key is release" , keyval)

    def release_capture(self) :
        self.capture.close()
        time.sleep(1)

    def update_image(self, widget):
        self.video.queue_draw()
        return True



    def on_stack_visible_child_changed(self , stack, param_spec):
        visible_child_name = self.stack.get_visible_child_name()

        if visible_child_name == "page1":
            # software re-init

            # powersave / ondemand
            self.main_window.set_cpu_governor("powersave")
            self.main_window.set_brightness(0)
            self.grab_focus()
            self.openTimes += 1

            if (self.openTimes > 1 ) :
                #self.release_capture()
                #self.capture = Picamera2()
                #self.capture.configure(self.capture.create_preview_configuration(main={"format": 'XRGB8888', "size": (1280, 720)}))
                #self.capture.start()
                self.reset_timer()
                self.button.set_capture(self.capture)
                self.video.queue_draw()

