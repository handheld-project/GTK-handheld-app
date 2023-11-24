import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib
import cv2
from PIL import Image
from components.circularButton import CircularButton

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
