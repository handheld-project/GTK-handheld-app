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
        # type price formular
        self.firstTypeAndPrice = { False:5 , True:10 }
        self.secondTypeAndPrice = { False:26 ,True:52 } 
        self.thridTypeAndPrice = { False:50 , True:52 }
        self.mapType = {1:"อักษรภาษาไทยทั้งหมด", 2:"อักษรภาษาไทยปนกับภาษาต่างประเทศ/ภาพ/เครื่องหมายอื่น", 3:"อักษาไทยอยู่ต่ำกว่าอักษรต่างประเทศ/ไม่มีอักษรไทยเลย"}
        self.is_moveable = None

        self.stack = stack
        self.main_window = main_window
        self.filename = ""
        self.stack.connect("notify::visible-child-name", self.on_stack_visible_child_changed)

        # control variable 
        self.current_entity = 0
        self.is_confirmed = False 
        self.child_combo_index = 0 
        self.is_popup = False 
        self.max_entity_index = 5

        # gridPage
        self.gridPage = Gtk.Grid() 
        self.gridPage.set_valign(Gtk.Align.CENTER)
        self.gridPage.set_halign(Gtk.Align.CENTER)
        self.gridPage.set_column_homogeneous(True)  # Make columns expand equall

        self.leftMainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6) 

        # function button
        self.buttonsBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6) 

        self.goBackButton = Gtk.Button("ถ่ายรูปใหม่")
        self.goBackButton.set_size_request(60,20)

        self.goNextButton = Gtk.Button("ยืนยันข้อมูล")
        self.goBackButton.set_size_request(120,20)
        
        self.buttonsBox.pack_start(self.goBackButton , False , False , 0 )
        self.buttonsBox.pack_start(self.goNextButton , False , False , 0 )

        #gridContents wrapper
        self.gridContentWrapper = Gtk.Grid() 

        # labelPage
        self.label = Gtk.Label(label="ผลลัพธ์การตรวจจับป้ายโฆษณา")

        # Image
            #Container
        self.boxImage = Gtk.Box() 
        self.image = Gtk.Image() 
        self.image.set_size_request(400, 350)

        # Calculated Content 
        self.gridContent = Gtk.Grid()
        
        # top
        self.boxTopContent = Gtk.Box() 
        self.gridTopContent = Gtk.Grid() 
        
        self.topContentLabel = Gtk.Label(label="ข้อมูลป้าย" ) 
        self.topContentLabel.set_size_request(180 , 20 )

        self.unit_label_w = Gtk.Label(label="ม.")
        self.unit_label_h = Gtk.Label(label="ม.")
        self.unit_area_label = Gtk.Label(label="ตร.ม")
        self.unit_tax = Gtk.Label(label="บาท")

        self.adjustment_width = Gtk.Adjustment(0, 0, 100, 0.01, 10, 0)

        self.width = Gtk.Label(label="ความกว้าง") 
        self.width.set_size_request(80 , 40 )

        self.calculated_width = Gtk.SpinButton()
        self.calculated_width.set_size_request(205 , 40 )
        self.calculated_width.set_adjustment(self.adjustment_width)
        self.calculated_width.set_digits(2)  
        
        self.adjustment_height = Gtk.Adjustment(0, 0, 100, 0.01, 10, 0)

        self.height = Gtk.Label(label="ความสูง") 
        self.height.set_size_request(80 , 40 )

        self.calculated_height = Gtk.SpinButton()
        self.calculated_height.set_size_request(205 , 40 )
        self.calculated_height.set_adjustment(self.adjustment_height)
        self.calculated_height.set_digits(2)  

        self.radio_group = Gtk.RadioButton.new(None)
        self.radio_button1 = Gtk.RadioButton.new_with_label_from_widget(self.radio_group, "ข้อความเคลื่อนไหวได้")
        self.radio_button1.connect("toggled", self.on_radio_button_toggled)

        # Create a radio button with the label "Option 2"
        self.radio_button2 = Gtk.RadioButton.new_with_label_from_widget(self.radio_group, "ข้อความเคลื่อนไหวไม่ได้")
        self.radio_button2.connect("toggled", self.on_radio_button_toggled)

        self.area = Gtk.Label(label="พื้นที่")
        self.area.set_size_request(80 , 20 )
        self.calculated_area = Gtk.Entry()
        self.calculated_area.set_size_request(205 , 20 )
        self.calculated_area.set_sensitive(False)

        self.type = Gtk.Label(label="ชนิดป้าย") 
        self.type.set_size_request(80 , 20 )

        self.calculated_type_entry = Gtk.Entry()
        self.calculated_type_entry.set_size_request(205, 20)
        self.calculated_type_entry.set_sensitive(False)

        self.dropdown_list = Gtk.ListBox()
        self.dropdown_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.dropdown_list.set_size_request(-1,50)

        # Populate the ListBox with items
        for i, item_text in enumerate(["1. อักษรภาษาไทยทั้งหมด", "2. อักษรภาษาไทยปนกับภาษาต่างประเทศ\n/ภาพ/เครื่องหมายอื่น", "3. อักษาไทยอยู่ต่ำกว่าอักษรต่างประเทศ\n/ไม่มีอักษรไทยเลย"]):
            list_item = Gtk.Label(label=item_text)
            list_box_row = Gtk.ListBoxRow()
            list_box_row.add(list_item)
            self.dropdown_list.add(list_box_row)
             
        self.dropdown_list.select_row(self.dropdown_list.get_row_at_index(0))


        self.taxPrice = Gtk.Label("ราคาภาษี") 
        self.taxPrice.set_size_request(80 , 20 )
        self.calculated_taxPrice = Gtk.Entry()
        self.calculated_taxPrice.set_size_request(205 , 20 )
        self.calculated_taxPrice.set_sensitive(False)
        

        # bottom 
        self.boxBottomContent = Gtk.Box() 
        self.gridBottomContent = Gtk.Grid()

        self.latitude = Gtk.Label(label="ละติจูด")
        self.latitude.set_size_request(80 , 20 ) 
        self.calculated_latitude = Gtk.Entry( ) 
        self.calculated_latitude.set_size_request(205 , 20 )
        self.calculated_latitude.set_sensitive(False)


        self.longitude = Gtk.Label(label="ลองจิจูด") 
        self.longitude.set_size_request(80 , 20 ) 
        self.calculated_longitude  = Gtk.Entry() 
        self.calculated_longitude.set_size_request(205 , 20 )
        self.calculated_longitude.set_sensitive(False)


        self.time = Gtk.Label(label="เวลา") 
        self.time.set_size_request(80 , 20 ) 
        self.calculated_time  = Gtk.Entry() 
        self.calculated_time.set_size_request(205 , 20 )
        self.calculated_time.set_text(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        self.calculated_time.set_sensitive(False)


        # adding content to page 
        self.boxTopContent.add(self.gridTopContent)
        self.boxBottomContent.add(self.gridBottomContent)

        # align 
        self.gridContent.set_valign(Gtk.Align.CENTER)
        self.gridContent.set_halign(Gtk.Align.CENTER)
        self.leftMainBox.set_valign(Gtk.Align.CENTER)
        self.leftMainBox.set_halign(Gtk.Align.CENTER)
        self.buttonsBox.set_halign(Gtk.Align.CENTER)
        
            # align top content
        self.width.set_halign(Gtk.Align.START)
        self.height.set_halign(Gtk.Align.START)
        self.radio_button1.set_halign(Gtk.Align.START)
        self.radio_button2.set_halign(Gtk.Align.START)
        self.area.set_halign(Gtk.Align.START)
        self.type.set_halign(Gtk.Align.START)
        self.taxPrice.set_halign(Gtk.Align.START)

        self.calculated_width.set_halign(Gtk.Align.END)
        self.calculated_height.set_halign(Gtk.Align.END)
        self.calculated_area.set_halign(Gtk.Align.END)
        self.calculated_type_entry .set_halign(Gtk.Align.END)
        self.calculated_taxPrice.set_halign(Gtk.Align.END)

            # align bottom content
        self.latitude.set_halign(Gtk.Align.START)
        self.longitude.set_halign(Gtk.Align.START)
        self.time.set_halign(Gtk.Align.START)

        self.calculated_latitude.set_halign(Gtk.Align.END)
        self.calculated_latitude.set_halign(Gtk.Align.END)
        self.calculated_time.set_halign(Gtk.Align.END)

        # #sizing 
        # self.gridTopContent.set_size_request(275,300)

        self.gridPage.set_column_homogeneous(True)
        
        self.gridPage.set_hexpand(True)
        self.gridContentWrapper.set_hexpand(True)
        self.gridTopContent.set_hexpand(True)        
        self.gridBottomContent.set_hexpand(True)

            # adding image box 
        self.boxImage.add(self.image)
        self.leftMainBox.pack_start(self.boxImage, False, False, 0)
        self.leftMainBox.pack_start(self.buttonsBox, False, False, 0)
            # adding top content 
            # left top width height 

        self.gridTopContent.attach( self.topContentLabel , 0 , 0 ,2 , 1 )
        self.gridTopContent.attach( self.width , 0 , 1 , 1 , 1)
        self.gridTopContent.attach( self.unit_label_w, 1 , 1 , 1 , 1 ) 
        self.gridTopContent.attach( self.calculated_width , 1 , 1 , 1 ,1 )
        self.gridTopContent.attach( self.height , 0 , 2 , 1 , 1)
        self.gridTopContent.attach( self.unit_label_h, 1 , 2 , 1 , 1 ) 
        self.gridTopContent.attach( self.calculated_height , 1 , 2 ,1 ,1 )
        self.gridTopContent.attach( self.radio_button1 , 1 , 3 ,1 ,1 )
        self.gridTopContent.attach( self.radio_button2 , 1 , 4 ,1 ,1 )
        self.gridTopContent.attach( self.area ,  0 , 6 , 1 , 1)
        self.gridTopContent.attach( self.unit_area_label,  1, 6, 1, 1) 
        self.gridTopContent.attach( self.calculated_area , 1 , 6 ,1 ,1)
        self.gridTopContent.attach( self.type ,0 ,5 ,1, 1)
        self.gridTopContent.attach( self.calculated_type_entry  ,1 , 5, 1 , 1)
        self.gridTopContent.attach( self.taxPrice ,0 ,7 ,1 ,1 )
        self.gridTopContent.attach( self.unit_tax ,1 ,7 ,1, 1)
        self.gridTopContent.attach( self.calculated_taxPrice ,1 ,7 ,1, 1)

        #  adding bottom conntent
            # left top width heigt 
        self.gridBottomContent.attach(self.latitude , 0 , 0 , 1, 1 ) 
        self.gridBottomContent.attach(self.calculated_latitude , 1 , 0 , 1 ,1 ) 
        self.gridBottomContent.attach(self.longitude , 0 , 1 , 1 , 1 ) 
        self.gridBottomContent.attach(self.calculated_longitude , 1, 1 , 1 , 1 ) 
        self.gridBottomContent.attach(self.time , 0, 2 , 1 , 1 ) 
        self.gridBottomContent.attach(self.calculated_time , 1 , 2 , 1 , 1 ) 

        # content in right side
        self.gridContent.attach( self.boxTopContent , 0 , 0 , 1 , 1 )
        self.gridContent.attach( self.dropdown_list, 0 , 0 , 2 , 1 )
        self.gridContent.attach( self.boxBottomContent , 0 , 1 , 1 , 1 )

        # content wrap all
        self.gridContentWrapper.attach(self.leftMainBox, 0 , 0 , 2 , 1 ) 
        self.gridContentWrapper.attach(self.gridContent, 2 , 0 , 2 , 1 ) 

        self.gridContentWrapper.attach( self.goBackButton ,2 ,1 ,1 ,1 )
        self.gridContentWrapper.attach( self.goNextButton ,3 ,1 ,1 ,1 )

        self.gridPage.attach( self.label , 0 , 0 , 4 , 1 )
        self.gridPage.attach( self.gridContentWrapper , 0 , 1 , 4, 1 )
        
        self.init_css_context()
        self.add(self.gridPage)

        self.set_can_focus(True) 
        self.connect("key-press-event", self.on_key_press)
        self.goBackButton.connect("clicked", self.on_go_back)
        self.goNextButton.connect("clicked", self.on_go_next)

    def init_css_context(self):
        # add styling
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_path("./styles/page2.style.css")

        self.contextGoBack = self.goBackButton.get_style_context()
        self.contextGoNext = self.goNextButton.get_style_context()

        self.contextLabel = self.label.get_style_context()
        self.contextUnitLabelW = self.unit_label_w.get_style_context()
        self.contextUnitLabelH = self.unit_label_h.get_style_context()
        self.contextUnitAreaLabel = self.unit_area_label.get_style_context()
        self.contextUnitTaxLabel = self.unit_tax.get_style_context()

        self.contextImage = self.image.get_style_context()
        self.contextBoxTopContent = self.boxTopContent.get_style_context()
        self.contextBoxBottomContent = self.boxBottomContent.get_style_context()
        self.contextGridContentWrapper = self.gridContentWrapper.get_style_context()

        self.contextWidth = self.width.get_style_context()
        self.contextHeight = self.height.get_style_context()
        self.contextArea = self.area.get_style_context()
        self.contextTaxPrice = self.taxPrice.get_style_context()
        self.contextType = self.type.get_style_context()
        self.contextRadio1 = self.radio_button1.get_style_context()
        self.contextRadio2 = self.radio_button2.get_style_context()
        self.contextDropdownList = self.dropdown_list.get_style_context()

        self.contextCalculated_width = self.calculated_width.get_style_context()
        self.contextCalculated_height= self.calculated_height.get_style_context()
        self.contextCalculated_area = self.calculated_area.get_style_context()
        self.contextCalculated_taxPrice = self.calculated_taxPrice.get_style_context()
        self.contextcalculated_type_entry = self.calculated_type_entry .get_style_context()

        self.contextLatitude = self.latitude.get_style_context()
        self.contextLongitude = self.longitude.get_style_context()
        self.contextTime = self.time.get_style_context()
        
        self.contextCalulated_latitude = self.calculated_latitude.get_style_context()
        self.contextCalulated_longitude = self.calculated_longitude.get_style_context()
        self.contextCalculated_time = self.calculated_time.get_style_context()
   
        self.goBackButton.get_style_context().add_class("goBackButton")
        self.goNextButton.get_style_context().add_class("goNextButtonDisable")

        self.label.get_style_context().add_class("labelName")
        self.unit_label_w.get_style_context().add_class("unitLabel")
        self.unit_label_h.get_style_context().add_class("unitLabel")
        self.unit_area_label.get_style_context().add_class("unitAreaLabel")
        self.unit_tax.get_style_context().add_class("unitAreaLabel")

        self.image.get_style_context().add_class("image")
        self.boxTopContent.get_style_context().add_class("boxTopContent")
        self.boxBottomContent.get_style_context().add_class("boxBottomContent")
        self.gridContentWrapper.get_style_context().add_class("gridContentWrapper")

        self.width.get_style_context().add_class("labelName")
        self.height.get_style_context().add_class("labelName")
        self.area.get_style_context().add_class("labelName")
        self.taxPrice.get_style_context().add_class("labelName")
        self.type.get_style_context().add_class("labelName")
        self.radio_button1.get_style_context().add_class("radio")
        self.radio_button2.get_style_context().add_class("radio")

        self.calculated_width.get_style_context().add_class("calculatedBox")
        self.calculated_height.get_style_context().add_class("calculatedBox")
        self.calculated_area.get_style_context().add_class("calculatedBox")
        self.calculated_taxPrice.get_style_context().add_class("calculatedBox")
        self.calculated_type_entry.get_style_context().add_class("calculatedBox")
        self.dropdown_list.get_style_context().add_class("dropdownList")

        self.latitude.get_style_context().add_class("labelName")
        self.longitude.get_style_context().add_class("labelName")
        self.time.get_style_context().add_class("labelName")

        self.calculated_latitude.get_style_context().add_class("calculatedBox")
        self.calculated_longitude.get_style_context().add_class("calculatedBox")
        self.calculated_time.get_style_context().add_class("calculatedBox")

        self.contextGoBack.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextGoNext.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.contextLabel.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextUnitLabelW.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextUnitLabelH.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextUnitAreaLabel.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextUnitTaxLabel.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.contextImage.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextBoxTopContent.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextBoxBottomContent.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextGridContentWrapper.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.contextWidth.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextHeight.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextArea.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextTaxPrice.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextType.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextRadio1.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextRadio2.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextDropdownList.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.contextCalculated_width.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalculated_height.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalculated_area.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalculated_taxPrice.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextcalculated_type_entry.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        self.contextLatitude.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextLongitude.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextTime.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.contextCalulated_latitude.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalulated_longitude.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalculated_time.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        

    def on_key_press(self, widget, event):
        keyval = event.keyval
        if  not self.is_confirmed :
            key_actions = {
                105: self.decrement_entity,  # i
                107: self.increment_entity,  # k
                122: self.confirm_action,     # z
                120: self.cancel_action       # x
            }
            self.update_ui()
    
        else :
            # handle editing value for GTK.comboBox() and GTK.spinButton()
            # type spinButton
            if (self.current_entity == 0) :
                key_actions = {
                    105: self.increase_width_value,  # i
                    107: self.decrease_width_value,  # k
                    120: self.cancel_action       # x
                }
            elif (self.current_entity == 1) :
                key_actions = {
                    105: self.increase_height_value,  # i
                    107: self.decrease_height_value,  # k
                    120: self.cancel_action       # x
                }
            #  type check box 
            elif self.current_entity == 4 :
                key_actions = {
                    105: self.chose_upper_child_combo,  # i
                    107: self.chose_lower_child_combo,  # k
                    120: self.cancel_action,       # x
                    122: self.confirm_combo,     # z
                }
            
        action_function = key_actions.get(keyval, None)
        action_function()

    def chose_upper_child_combo(self):
        if(self.is_confirmed is True and self.is_popup is True) :
            selected_row = self.dropdown_list.get_selected_row()
            if selected_row:
                all_rows = list(self.dropdown_list.get_children())
                index = all_rows.index(selected_row)
                if index > 0:
                    prev_row = all_rows[index - 1]
                    self.dropdown_list.select_row(prev_row)
                else : 
                    index = 1 
        else : 
            pass 
    def chose_lower_child_combo(self):
        if(self.is_confirmed is True and self.is_popup is True) :
            selected_row = self.dropdown_list.get_selected_row()
            if selected_row:
                all_rows = list(self.dropdown_list.get_children())
                index = all_rows.index(selected_row)
                if index < 2:
                    prev_row = all_rows[index + 1]
                    self.dropdown_list.select_row(prev_row)
                else : 
                    index = 2
        else : 
            pass


    def confirm_combo(self):

        if self.is_popup is False : 
            self.dropdown_list.show() 
            self.is_popup = True
        else :
            selected_row = self.dropdown_list.get_selected_row()
            if(selected_row):
                text_value = selected_row.get_child().get_text()
                self.calculated_type_entry.set_text(text_value)
                self.calculated_type_entry.queue_draw()
                self.dropdown_list.hide()
                self.calculate()
            self.is_popup = False
 


    def decrease_height_value(self) :
        self.calculated_height.set_value(self.calculated_height.get_value()-0.01)

    def increase_height_value(self) :
        self.calculated_height.set_value(self.calculated_height.get_value()+0.01)

    def decrease_width_value(self) :
        self.calculated_width.set_value(self.calculated_width.get_value()-0.01)

    def increase_width_value(self) :
        self.calculated_width.set_value(self.calculated_width.get_value()+0.01)

    def update_ui(self):
        update_functions = [
            self.update_calculated_width,
            self.update_calculated_height,
            self.update_radio_1,
            self.update_radio_2,
            self.update_calculated_type,
            self.update_goback,
            self.update_gonext
        ]

        for index, update_function in enumerate(update_functions):
            if index == self.current_entity:
                update_function()

    def update_confirmed_ui(self):
        update_functions = [
            self.update_confirmed_calculated_width,
            self.update_confirmed_calculated_height,
            self.do_not_thing,
            self.do_not_thing,
            self.update_confirmed_calculated_type
        ]

        for index, update_function in enumerate(update_functions):
            if index == self.current_entity:
                update_function()

    def update_cancle_ui(self):
        update_functions = [
            self.update_cancle_calculated_width,
            self.update_cancle_calculated_height,
            self.do_not_thing,
            self.do_not_thing,
            self.update_cancle_calculated_type
        ]

        for index, update_function in enumerate(update_functions):
            if index == self.current_entity:
                update_function()

    def update_confirmed_calculated_width(self):
        self.calculated_width.get_style_context().remove_class("blue-border")
        self.calculated_width.get_style_context().add_class("orange-border")

    def update_confirmed_calculated_height(self):
        self.calculated_height.get_style_context().remove_class("blue-border")
        self.calculated_height.get_style_context().add_class("orange-border") 

    def do_not_thing(self):
        print("do notinh work")
        # this method needed dont delet this !
        pass

    def update_confirmed_calculated_type(self): 
        self.calculated_type_entry.get_style_context().remove_class("blue-border")
        self.calculated_type_entry.get_style_context().add_class("orange-border")

    def update_cancle_calculated_width(self):
        self.calculated_width.get_style_context().add_class("blue-border")
        self.calculated_width.get_style_context().remove_class("orange-border")

    def update_cancle_calculated_height(self):
        self.calculated_height.get_style_context().add_class("blue-border")
        self.calculated_height.get_style_context().remove_class("orange-border") 

    def update_cancle_calculated_type(self): 
        self.calculated_type_entry.get_style_context().add_class("blue-border")
        self.calculated_type_entry.get_style_context().remove_class("orange-border")

    def update_calculated_width(self):
        self.calculated_width.get_style_context().add_class("blue-border")
        self.calculated_height.get_style_context().remove_class("blue-border")

    def update_calculated_height(self):
        self.calculated_width.get_style_context().remove_class("blue-border")
        self.calculated_height.get_style_context().add_class("blue-border")
        self.radio_button1.get_style_context().remove_class("radioSelected")

    def update_radio_1(self):
        print("update ui radio1")
        self.calculated_height.get_style_context().remove_class("blue-border")
        self.radio_button1.get_style_context().add_class("radioSelected")
        self.radio_button2.get_style_context().remove_class("radioSelected")

    def update_radio_2(self):
        print("update ui radio2")
        self.radio_button1.get_style_context().remove_class("radioSelected")
        self.radio_button2.get_style_context().add_class("radioSelected")        
        self.calculated_type_entry.get_style_context().remove_class("blue-border")

    def update_calculated_type(self):
        self.radio_button2.get_style_context().remove_class("radioSelected")        
        self.calculated_type_entry.get_style_context().add_class("blue-border")
        self.goBackButton.get_style_context().remove_class("goBackButtonSelect")        

    def update_goback(self):
        self.calculated_type_entry.get_style_context().remove_class("blue-border")     
        self.goBackButton.get_style_context().add_class("goBackButtonSelect")        
        self.goNextButton.get_style_context().remove_class("goNextButtonSelect")

    def update_gonext(self):
        self.goBackButton.get_style_context().remove_class("goBackButtonSelect")        
        self.goNextButton.get_style_context().add_class("goNextButtonSelect")

    def increment_entity(self):

        self.current_entity += 1
        self.current_entity = min(self.current_entity, self.max_entity_index)
        self.update_ui()

    def decrement_entity(self):

        self.current_entity -= 1
        self.current_entity = max(self.current_entity, 0)
        self.update_ui()

    def cancel_action(self):
        if self.current_entity == 4 and self.is_popup is True: 
            pass 
        else :   
            self.is_confirmed = False
            self.calculate()
            self.update_cancle_ui()

    def confirm_action(self):
        if self.current_entity == 4 : 
            self.is_confirmed = True
            self.is_popup = True
            self.dropdown_list.show()
        elif self.current_entity == 2 : 
            print("confirm radio1")
            self.radio_button1.set_active(True)
            self.calculate()
        elif self.current_entity == 3 :
            print("confirm radio2")
            self.radio_button2.set_active(True)
            self.calculate()
        elif self.current_entity == 5 : 
            self.goBackButton.emit("clicked")
        elif self.current_entity == 6 : 
            self.goNextButton.emit("clicked")
        else : 
            self.is_confirmed = True

        # for oragane border confirmed cursur 
        self.update_confirmed_ui()


    # stack page change handler 
    def on_stack_visible_child_changed(self , stack, param_spec):
        visible_child_name = self.stack.get_visible_child_name()
        if visible_child_name == "page2":
            self.main_window.page1.stop_update_Ui()
            # reseting data and UI
            self.dropdown_list.hide()
            self.grab_focus()
            self.reset_page()
            exported_data = self.main_window.get_processing_data()
            self.set_data()

            if exported_data:
                # setting data from processing process ! 
                self.filename = exported_data['src_image']
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(exported_data['src_image'])
                scaled_pixbuf = pixbuf.scale_simple(400, 225, GdkPixbuf.InterpType.BILINEAR)
                self.image.set_from_pixbuf(scaled_pixbuf)


    def on_radio_button_toggled(self, button):
        if button.get_active():
            if button.get_label() == "ข้อความเคลื่อนไหวไม่ได้" : 
                self.is_moveable = False
            elif button.get_label() == "ข้อความเคลื่อนไหวได้" : 
                self.is_moveable = True
            else :
                self.is_moveable = None

        self.max_entity_index = 6 
        
        self.goNextButton.get_style_context().remove_class("goNextButtonDisable")
        self.goNextButton.get_style_context().add_class("goNextButton")


    def on_go_back(self,widget) :
        try:
            current_path= self.filename
            os.remove(current_path)
            print(f"Directory '{current_path}' deleted successfully.")
            
            self.stack.set_visible_child_name("page1")

        except OSError as e:
            print(f"Error deleting {e}")

    def on_go_next(self,widget) :
        print(self.is_moveable)
        if self.is_moveable or self.is_moveable is False:
            typeNumber = int(self.calculated_type_entry.get_text()[0])
            document = {
                "width" : "{:.4f}".format(self.calculated_width.get_value())  ,
                "height" : self.calculated_height.get_value()  ,
                "is_movable" : self.is_moveable ,
                "type" : self.mapType[typeNumber] , 
                "area" : self.calculated_area.get_text() , 
                "price" : self.calculated_taxPrice.get_text() ,
                "latitude" : self.calculated_latitude.get_text() ,
                "longitude" : self.calculated_longitude.get_text()
            }
            print(document)
            self.main_window.set_document(document)

            self.stack.set_visible_child_name("page3")

            self.goNextButton.get_style_context().add_class("goNextButtonDisable")
            self.goNextButton.get_style_context().remove_class("goNextButton")

        else : 
            pass


    def set_data(self): 
        # from image model
        self.set_dropdown_data()
        # from hardware 
        self.set_data_from_hardware()
        # from calculate function 
        # pass 

    def set_dropdown_data(self) : 
        # check type from model then set value 
        # set dropdown to detected type
        all_rows = list(self.dropdown_list.get_children())
        self.dropdown_list.select_row(all_rows[1])
        self.calculated_type_entry.set_text(all_rows[1].get_child().get_text())
        self.dropdown_list.hide()
        self.calculated_type_entry.queue_draw()
      

    def set_data_from_hardware(self): 
        # w mock
        self.calculated_width.get_adjustment().set_value(1.00)
        # h mock
        self.calculated_height.get_adjustment().set_value(1.00)
        # latitude mock 
        self.calculated_latitude.set_text("40.7128° N")
        # longitude mock 
        self.calculated_longitude.set_text("-74.0060° W")


    def calculate(self): 
        if(self.is_moveable is not None):
            # set_area
            area = self.calculated_width.get_value() * self.calculated_height.get_value()
            area = "{:.4f}".format(area)
            self.calculated_area.set_text(area)

            # set_price
            selected_row = self.dropdown_list.get_selected_row()
            all_rows = list(self.dropdown_list.get_children())
            index = all_rows.index(selected_row)    
            areaCmUnit = (float(area) * (10**4) ) / 500
            areaCmUnit = float("{:.4f}".format(areaCmUnit))
            
            if index == 0 : 
                price = areaCmUnit * self.firstTypeAndPrice[self.is_moveable]
            elif index == 1 : 
                price = areaCmUnit * self.secondTypeAndPrice[self.is_moveable]
            elif index == 2 : 
                price = areaCmUnit * self.thridTypeAndPrice[self.is_moveable]

            price = "{:.4f}".format(price)
            self.calculated_taxPrice.set_text(price)
            
        else : 
            pass 

    def reset_page(self) : 

        self.radio_group.set_active(True)
        self.current_entity = 0
        self.is_confirmed = False 
        self.is_moveable = None
        self.child_combo_index = 0 
        self.is_popup = False 
        self.max_entity_index = 5
        self.calculated_area.set_text("")
        self.calculated_taxPrice.set_text("")

        print("move able is ",self.is_moveable)
        self.init_css_context()
        