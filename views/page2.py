# pages/page2.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib,Pango
import datetime
import os
# อักษรภาษาไทยทั้งหมด
# อักษรภาษาไทยปนกับภาษาต่างประเทศ/ภาพ/เครื่องหมายอื่น
# อักษาไทยอยู่ต่ำกว่าอักษรต่างประเทศ/ไม่มีอักษรไทยเลย

class Page2(Gtk.Grid):
    def __init__(self , main_window , stack):

        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.stack = stack
        self.main_window = main_window
        self.filename = ""
        self.stack.connect("notify::visible-child-name", self.on_stack_visible_child_changed)
        
        # control variable 
        self.current_entity = 0
        self.is_cancel = None 

        # type 
        self.list_store = Gtk.ListStore(str)
        self.list_store.append(["1.อักษรภาษาไทยทั้งหมด"])
        self.list_store.append(["2.อักษรภาษาไทยปน กับ \nภาษาต่างประเทศ/ภาพ\n/เครื่องหมายอื่น"])
        self.list_store.append(["3.อักษาไทยอยู่ต่ำกว่า\nอักษรต่างประเทศ/\nไม่มีอักษรไทยเลย"]) 

        # gridPage
        self.gridPage = Gtk.Grid() 
        self.gridPage.set_valign(Gtk.Align.CENTER)
        self.gridPage.set_halign(Gtk.Align.CENTER)
        self.gridPage.set_column_homogeneous(True)  # Make columns expand equall

        #gridContents wrapper
        self.gridContentWrapper = Gtk.Grid() 

        # labelPage
        self.label = Gtk.Label(label="ผลลัพธ์การตรวจจับป้ายโฆษณา")

        # Image
            #Container
        self.boxImage = Gtk.Box() 
        self.image = Gtk.Image() 
        self.image.set_size_request(720, 405)

        # Calculated Content 
        self.gridContent = Gtk.Grid()
        
        # top
        self.boxTopContent = Gtk.Box() 
        self.gridTopContent = Gtk.Grid() 
        
        self.topContentLabel = Gtk.Label(label="ข้อมูลป้าย" ) 
        self.topContentLabel.set_size_request(180 , 40 )

        self.adjustment = Gtk.Adjustment(0, 0, 100, 0.1, 10, 0)

        self.width = Gtk.Label(label="ความกว้าง") 
        self.width.set_size_request(80 , 40 )

        self.calculated_width = Gtk.SpinButton()
        self.calculated_width.set_size_request(205 , 40 )
        self.calculated_width.set_adjustment(self.adjustment)
        self.calculated_width.set_digits(2)  
        self.calculated_width.set_numeric(True)

        self.height = Gtk.Label(label="ความสูง") 
        self.height.set_size_request(80 , 40 )

        self.calculated_height = Gtk.SpinButton()
        self.calculated_height.set_size_request(205 , 40 )
        self.calculated_height.set_adjustment(self.adjustment)
        self.calculated_height.set_digits(2)  
        self.calculated_height.set_numeric(True)



        self.area = Gtk.Label(label="พื้นที่")
        self.area.set_size_request(80 , 40 )
        self.calculated_area = Gtk.Entry()
        self.calculated_area.set_size_request(205 , 40 )

        self.type = Gtk.Label(label="ชนิดป้าย") 
        self.type.set_size_request(80 , 80 )
        self.calculated_type = Gtk.ComboBox.new_with_model(self.list_store)
        self.calculated_type.set_size_request(180 , 80 )
        
        self.renderer_text = Gtk.CellRendererText()
        self.calculated_type.pack_start(self.renderer_text, True)
        self.calculated_type.add_attribute(self.renderer_text, "text", 0)

        self.taxPrice = Gtk.Label("ราคาภาษี") 
        self.taxPrice.set_size_request(80 , 40 )
        self.calculated_taxPrice = Gtk.Entry()
        self.calculated_taxPrice.set_size_request(205 , 40 )

        # bottom 
        self.boxBottomContent = Gtk.Box() 
        self.gridBottomContent = Gtk.Grid()

        self.latitude = Gtk.Label(label="ละติจูด")
        self.latitude.set_size_request(80 , 40 ) 
        self.calculated_latitude = Gtk.Entry()
        self.calculated_latitude.set_size_request(205 , 40 )

        self.longitude = Gtk.Label(label="ลองจิจูด") 
        self.longitude.set_size_request(80 , 40 ) 
        self.calculated_longitude  = Gtk.Entry()
        self.calculated_longitude.set_size_request(205 , 40 )

        self.time = Gtk.Label(label="เวลา") 
        self.time.set_size_request(80 , 40 ) 
        self.calculated_time  = Gtk.Label( label = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") ) 
        self.calculated_time.set_size_request(205 , 40 )
         
        # add styling
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_path("./styles/page2.style.css")

        self.contextLabel= self.label.get_style_context()

        self.contextImage = self.image.get_style_context()
        self.contextBoxTopContent = self.boxTopContent.get_style_context()
        self.contextBoxBottomContent = self.boxBottomContent.get_style_context()
        self.contextGridContentWrapper = self.gridContentWrapper.get_style_context()

        self.contextWidth = self.width.get_style_context()
        self.contextHeight = self.height.get_style_context()
        self.contextArea = self.area.get_style_context()
        self.contextTaxPrice = self.taxPrice.get_style_context()
        self.contextType = self.type.get_style_context()

        self.contextCalculated_width = self.calculated_width.get_style_context()
        self.contextCalculated_height= self.calculated_height.get_style_context()
        self.contextCalculated_area = self.calculated_area.get_style_context()
        self.contextCalculated_taxPrice = self.calculated_taxPrice.get_style_context()
        self.contextCalculated_type = self.calculated_type.get_style_context()

        self.contextLatitude = self.latitude.get_style_context()
        self.contextLongitude = self.longitude.get_style_context()
        self.contextTime = self.time.get_style_context()
        
        self.contextCalulated_latitude = self.calculated_latitude.get_style_context()
        self.contextCalulated_longitude = self.calculated_longitude.get_style_context()
        self.contextCalculated_time = self.calculated_time.get_style_context()
   
        self.label.get_style_context().add_class("labelName")

        self.image.get_style_context().add_class("image")
        self.boxTopContent.get_style_context().add_class("boxTopContent")
        self.boxBottomContent.get_style_context().add_class("boxBottomContent")
        self.gridContentWrapper.get_style_context().add_class("gridContentWrapper")

        self.width.get_style_context().add_class("labelName")
        self.height.get_style_context().add_class("labelName")
        self.area.get_style_context().add_class("labelName")
        self.taxPrice.get_style_context().add_class("labelName")
        self.type.get_style_context().add_class("labelName")

        self.calculated_width.get_style_context().add_class("calculatedBox")
        self.calculated_height.get_style_context().add_class("calculatedBox")
        self.calculated_area.get_style_context().add_class("calculatedBox")
        self.calculated_taxPrice.get_style_context().add_class("calculatedBox")
        self.calculated_type.get_style_context().add_class("combo-box")

        self.latitude.get_style_context().add_class("labelName")
        self.longitude.get_style_context().add_class("labelName")
        self.time.get_style_context().add_class("labelName")

        self.calculated_latitude.get_style_context().add_class("calculatedBox")
        self.calculated_longitude.get_style_context().add_class("calculatedBox")
        self.calculated_time.get_style_context().add_class("calculatedBox")

        self.contextLabel.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.contextImage.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextBoxTopContent.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextBoxBottomContent.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextGridContentWrapper.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.contextWidth.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextHeight.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextArea.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextTaxPrice.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextType.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.contextCalculated_width.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalculated_height.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalculated_area.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalculated_taxPrice.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalculated_type.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        self.contextLatitude.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextLongitude.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextTime.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.contextCalulated_latitude.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalulated_longitude.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalculated_time.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # adding content to page 
        self.boxTopContent.add(self.gridTopContent)
        self.boxBottomContent.add(self.gridBottomContent)

        # align 
        self.gridContent.set_valign(Gtk.Align.CENTER)
        self.gridContent.set_halign(Gtk.Align.CENTER)

            # align top content
        self.width.set_halign(Gtk.Align.START)
        self.height.set_halign(Gtk.Align.START)
        self.area.set_halign(Gtk.Align.START)
        self.type.set_halign(Gtk.Align.START)
        self.taxPrice.set_halign(Gtk.Align.START)

        # self.width.set_valign(Gtk.Align.START)
        # self.height.set_valign(Gtk.Align.START)
        # self.area.set_valign(Gtk.Align.START)
        # self.type.set_valign(Gtk.Align.START)
        # self.taxPrice.set_valign(Gtk.Align.START)

        self.calculated_width.set_halign(Gtk.Align.END)
        self.calculated_height.set_halign(Gtk.Align.END)
        self.calculated_area.set_halign(Gtk.Align.END)
        self.calculated_type.set_halign(Gtk.Align.END)
        self.calculated_taxPrice.set_halign(Gtk.Align.END)

        # self.calculated_width.set_valign(Gtk.Align.END)
        # self.calculated_height.set_valign(Gtk.Align.END)
        # self.calculated_area.set_valign(Gtk.Align.END)
        # self.calculated_type.set_valign(Gtk.Align.END)
        # self.calculated_taxPrice.set_valign(Gtk.Align.END)

            # align bottom content
        self.latitude.set_halign(Gtk.Align.START)
        self.longitude.set_halign(Gtk.Align.START)
        self.time.set_halign(Gtk.Align.START)

        self.calculated_latitude.set_halign(Gtk.Align.END)
        self.calculated_latitude.set_halign(Gtk.Align.END)
        self.calculated_time.set_halign(Gtk.Align.END)

        #sizing 
        self.gridTopContent.set_size_request(275,300)

        self.gridPage.set_column_homogeneous(True)
        # self.gridTopContent.set_column_homogeneous(True)
        # self.gridBottomContent.set_column_homogeneous(True)


        self.gridPage.set_hexpand(True)
        self.gridContentWrapper.set_hexpand(True)
        self.gridTopContent.set_hexpand(True)        
        self.gridBottomContent.set_hexpand(True)

            # adding image box 
        self.boxImage.add(self.image)

            # adding top content 
        self.gridTopContent.attach( self.topContentLabel , 0 , 0 ,2 , 1 )
        self.gridTopContent.attach( self.width , 0 , 1 , 1 , 1)
        self.gridTopContent.attach( self.calculated_width , 1 , 1 , 1 ,1 )
        self.gridTopContent.attach( self.height , 0 , 2 , 1 , 1)
        self.gridTopContent.attach( self.calculated_height , 1 , 2 ,1 ,1 )
        self.gridTopContent.attach( self.area , 0 ,3 ,1, 1)
        self.gridTopContent.attach( self.calculated_area , 1 , 3, 1 ,1)
        self.gridTopContent.attach( self.type , 0 , 4 , 1 , 1 )
        self.gridTopContent.attach( self.calculated_type ,1 , 4 ,1 ,1 )
        self.gridTopContent.attach( self.taxPrice ,0 ,5 ,1 ,1 )
        self.gridTopContent.attach( self.calculated_taxPrice ,1 ,5 ,1, 1)

        #  adding bottom conntent
            # left top width heigt 
        self.gridBottomContent.attach(self.latitude , 0 , 0 , 1, 1 ) 
        self.gridBottomContent.attach(self.calculated_latitude , 1 , 0 , 1 ,1 ) 
        self.gridBottomContent.attach(self.longitude , 0 , 1, 1 , 1 ) 
        self.gridBottomContent.attach(self.calculated_longitude , 1, 1 , 1 , 1 ) 
        self.gridBottomContent.attach(self.time , 0, 2 , 1 , 1 ) 
        self.gridBottomContent.attach(self.calculated_time , 1 , 2 , 1 , 1 ) 

        self.gridContent.attach( self.boxTopContent , 0 , 0 , 1 , 1 )
        self.gridContent.attach( self.boxBottomContent , 0 , 1 , 1 , 1 )

        self.gridContentWrapper.attach(self.boxImage, 0 , 0 , 1 , 1 ) 
        self.gridContentWrapper.attach(self.gridContent, 1 , 0 , 1 , 1 ) 

        self.gridPage.attach( self.label , 0 , 0 , 1 , 1 )
        self.gridPage.attach( self.gridContentWrapper , 0 , 1 , 1, 1 )
        
        self.add(self.gridPage)
        self.set_can_focus(True) 
        self.connect("key-press-event", self.on_key_press)

    def on_key_press(self, widget, event):
        keyval = event.keyval
        key_actions = {
            105: self.decrement_entity,  # i
            107: self.increment_entity,  # k
            122: self.confirm_action,     # z
            120: self.cancel_action       # x
        }

        action_function = key_actions.get(keyval, None)
        
        if action_function:
            action_function()
            print(self.current_entity)
            self.update_ui()
            self.calculated_width.queue_draw()
            self.calculated_height.queue_draw()
            self.calculated_type.queue_draw()
        else:
            pass


    def update_ui(self):
        update_functions = [
            self.update_calculated_width,
            self.update_calculated_height,
            self.update_calculated_type
        ]

        for index, update_function in enumerate(update_functions):
            if index == self.current_entity:
                update_function()


    def update_calculated_width(self):
        self.calculated_width.get_style_context().add_class("blue-border")
        self.calculated_height.get_style_context().remove_class("blue-border")
        self.calculated_type.get_style_context().remove_class("combo-box-selected")

    def update_calculated_height(self):
        self.calculated_width.get_style_context().remove_class("blue-border")
        self.calculated_height.get_style_context().add_class("blue-border")
        self.calculated_type.get_style_context().remove_class("combo-box-selected")

    def update_calculated_type(self):
        self.calculated_width.get_style_context().remove_class("blue-border")
        self.calculated_height.get_style_context().remove_class("blue-border")
        self.calculated_type.get_style_context().add_class("combo-box-selected")

    def increment_entity(self):
        print("i")
        self.current_entity += 1
        self.current_entity = min(self.current_entity, 2)
        self.update_ui()

    def decrement_entity(self):
        print("j")
        self.current_entity -= 1
        self.current_entity = max(self.current_entity, 0)
        self.update_ui()

    def confirm_action(self):
        self.is_cancel = False
        print("z")

    def cancel_action(self):
        self.is_cancel = True
        print("x")


    # stack page change handler 
    def on_stack_visible_child_changed(self , stack, param_spec):
        visible_child_name = self.stack.get_visible_child_name()
        print("change child to page2")
        if visible_child_name == "page2":
            # Retrieve the filename from the main window
            self.grab_focus()
            exported_data = self.main_window.get_processing_data()
            if exported_data:
                print("ei ei ,",exported_data['src_image'])
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(exported_data['src_image'])
                scaled_pixbuf = pixbuf.scale_simple(720, 405, GdkPixbuf.InterpType.BILINEAR)
                self.image.set_from_pixbuf(scaled_pixbuf)
               
                