import gi
gi.require_version("Gtk", "3.0")
import RPi.GPIO as GPIO
from business.hardware import MyButton
from gi.repository import Gtk, Gdk, GLib
from views.page1 import Page1
from views.page2 import Page2
from views.page3 import Page3
from views.loadingPage import LoadingPage
from views.splashPage import SplashPage
from libcamera import controls
import time
import screen_brightness_control as sbc
import subprocess


class MultiPageApp(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        #hardware init
        GPIO.setmode(GPIO.BCM)

        self.ondemandState = False

        self.laserPin = 22
        self.laserModule = GPIO.setup( self.laserPin  , GPIO.OUT )

        self.confirmButton = MyButton( 16 );
        self.cancelButton = MyButton( 17 );
        self.upButton = MyButton( 23 );
        self.downButton = MyButton( 24 );

        self.aimTriggerButton = MyButton( 25 );
        self.captureTriggerButton = MyButton( 27 );

        #software init
        self.processing_data = {}
        self.set_default_size(800, 480)
        self.connect("destroy", Gtk.main_quit)
        self.set_resizable(False)
        self.stack = Gtk.Stack()
        self.page1 = None
        self.page2 = None
        self.page3 = None
        self.loadingPage = None
        self.splashPage = None

        self.processing_data = {
            "src_image" : "" ,
            "top_left" : None ,
            "top_right" : None ,
            "bottom_left": None ,
            "bottom_right": None ,
            "detected_type":  0

        }
        self.commited_document = {
               "width" :  "" ,
                "height" : ""  ,
                "is_movable" : False ,
                "type" : "" ,
                "area" : "" ,
                "price" : "" ,
                "latitude" : "" ,
                "longitude" : "" ,
                "time" : ""
        }
        self.mapType = {1:"อักษรภาษาไทยทั้งหมด", 2:"อักษรภาษาไทยปนกับภาษาต่างประเทศ/ภาพ/เครื่องหมายอื่น", 3:"อักษาไทยอยู่ต่ำกว่าอักษรต่างประเทศ/ไม่มีอักษรไทยเลย"}

        self.init_stack()
        self.init_main_app_window()
        self.set_all_callback()
        self.set_brightness(0)

    def init_stack(self):
        self.add(self.stack)
        self.page1 = Page1(self,self.stack )
        self.page2 = Page2(self,self.stack )
        self.page3 = Page3(self,self.stack )
        self.loadingPage = LoadingPage()
        self.splashPage = SplashPage(self.stack)

        self.stack.add_named(self.page1, "page1")
        self.stack.add_named(self.page2, "page2")
        self.stack.add_named(self.page3, "page3")

        # self.stack.add_named(self.splashPage, "splashPage")
        self.stack.add_named(self.loadingPage, "loadingPage")

        #self.stack.connect("notify::visible-child-name", self.on_stack_visible_child_changed)

    def init_main_app_window(self):
        # Set the background color for the entire window
        background_color = Gdk.RGBA()
        background_color.parse("rgb(184, 184, 184)")  # Replace with your desired color
        self.override_background_color(Gtk.StateFlags.NORMAL, background_color)

        # Styling css
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("./styles/main.style.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # self.fullscreen()

        # Schedule a callback to switch to Page1 after 3 seconds
        # GLib.timeout_add_seconds(3, self.show_page1)

    def get_mapType(self):
        return self.mapType

    def set_document(self, document):
        self.commited_document = document

    def get_document(self):
        return self.commited_document

    def set_processing_data(self, processing_data):
        self.processing_data = processing_data

    def get_processing_data(self):
        return self.processing_data

    def show_page1(self):
        self.stack.set_visible_child_name("page1")

        return False  # Stop the timeout callback

    def run(self):
        self.show_all()

    def reset_all_callback (self) :
        list_pin = [16 ,17 , 23, 24 ,25 ,27 ]
        for pin in list_pin :
             GPIO.remove_event_detect(pin)

    def set_all_callback(self) :

        self.aimTriggerButton.set_callback(self.aim_button_callback)
        self.captureTriggerButton.set_callback(self.capture_button_callback)

        self.confirmButton.set_callback(self.confirm_button_callback)
        self.cancelButton.set_callback(self.cancel_button_callback)

        self.upButton.set_callback(self.up_button_callback)
        self.downButton.set_callback(self.down_button_callback)

    # button's callback function manager
    def aim_button_callback(self, _) :
        visible_child_name = self.stack.get_visible_child_name()
        if visible_child_name == "page1":
            self.aim_callback_page1()
        else :
            pass
        print(visible_child_name)

    def capture_button_callback(self, _):
        visible_child_name = self.stack.get_visible_child_name()
        if visible_child_name == "page1":
            self.capture_callback_page1()
        else :
            pass
        print(visible_child_name)

    def up_button_callback(self, _):
        visible_child_name = self.stack.get_visible_child_name()
        if visible_child_name == "page2":
            self.up_callback_page2()
        else :
            pass
        print(visible_child_name)

    def down_button_callback(self, _):
        visible_child_name = self.stack.get_visible_child_name()
        if visible_child_name == "page2":
            self.down_callback_page2()
        else :
            pass
        print(visible_child_name)

    def confirm_button_callback(self, _):
        visible_child_name = self.stack.get_visible_child_name()
        if visible_child_name == "page2":
            self.confirm_callback_page2()
        elif visible_child_name == "page3" :
            self.confirm_callback_page3()
        print(visible_child_name)


    def cancel_button_callback(self, _):
        visible_child_name = self.stack.get_visible_child_name()
        if visible_child_name == "page2":
            self.cancel_callback_page2()
        else :
            pass
        print(visible_child_name)

    def set_brightness(self , n) :
        sbc.fade_brightness(n, increment=4 , interval=0.1)
    # physical button callback function
         # page1

    def capture_callback_page1(self) :
        # set cpu governor
        while GPIO.input(self.captureTriggerButton.pin) == GPIO.LOW :
            self.page1.button.emit("button-press-event", None)

        self.set_brightness(20)
        self.set_cpu_governor("ondemand")


        self.page1.button.emit("button-release-event", None)

    def aim_callback_page1(self) :

        self.set_brightness(20)
        # camera auto focus
        self.page1.capture.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        # set cpu governor

        if not self.ondemandState :
            self.set_cpu_governor("ondemand")
            self.ondemandState = True

        # power the laser module
        while GPIO.input(self.aimTriggerButton.pin) == GPIO.LOW :
            GPIO.output(self.laserPin ,GPIO.HIGH)
        GPIO.output(self.laserPin ,GPIO.LOW)

        # page2
    def confirm_callback_page2(self) :
        event = Gdk.Event()
        event.type = Gdk.EventType.KEY_PRESS
        event.keyval = Gdk.keyval_from_name("z")
        self.page2.emit("key-press-event", event)

    def cancel_callback_page2(self) :
        event = Gdk.Event()
        event.type = Gdk.EventType.KEY_PRESS
        event.keyval = Gdk.keyval_from_name("x")
        self.page2.emit("key-press-event", event)

    def up_callback_page2(self) :
        while GPIO.input(self.upButton.pin) == GPIO.LOW :
            event = Gdk.Event()
            event.type = Gdk.EventType.KEY_PRESS
            event.keyval = Gdk.keyval_from_name("i")
            self.page2.emit("key-press-event", event)
            time.sleep(0.2)
        print(self.upButton.pin)

    def down_callback_page2(self) :
        while GPIO.input(self.downButton.pin) == GPIO.LOW :
            event = Gdk.Event()
            event.type = Gdk.EventType.KEY_PRESS
            event.keyval = Gdk.keyval_from_name("k")
            self.page2.emit("key-press-event", event)
            time.sleep(0.2)
        print(self.downButton.pin)

        # page3

    def confirm_callback_page3 (self ) :
        event = Gdk.Event()
        event.type = Gdk.EventType.KEY_PRESS
        event.keyval = Gdk.keyval_from_name("z")
        self.page3.emit("key-press-event", event)
        self.page3.goBackButton.emit("clicked")

    def set_cpu_governor(self,governor):
        try :
            subprocess.run(['sudo','cpufreq-set','-g',governor] , check = True )
            print("gorvernor set to :",governor)
        except subprocess.CalledProcessError as e :
            print(f"Error:{e}")



