# pages/page2.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib,Pango
import datetime
from components.boBackButton import GoBackButton
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
        self.is_confirmed = None 
        self.child_combo_index = 0 

        # gridPage
        self.gridPage = Gtk.Grid() 
        self.gridPage.set_valign(Gtk.Align.CENTER)
        self.gridPage.set_halign(Gtk.Align.CENTER)
        self.gridPage.set_column_homogeneous(True)  # Make columns expand equall

        # function button
        self.goBackButton = Gtk.Button("ถ่ายรูปใหม่")
        self.goBackButton.set_size_request(60,30)
        

        self.goNextButton = Gtk.Button("ยืนยันข้อมูล")
        self.goBackButton.set_size_request(120,30)
        

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

        self.radio_button1 = Gtk.RadioButton.new_with_label_from_widget(None, "ข้อความเคลื่อนไหวได้")
        self.radio_button1.connect("toggled", self.on_radio_button_toggled)

        # Create a radio button with the label "Option 2"
        self.radio_button2 = Gtk.RadioButton.new_with_label_from_widget(self.radio_button1, "ข้อความเคลื่อนไหวไม่ได้")
        self.radio_button2.connect("toggled", self.on_radio_button_toggled)

        self.area = Gtk.Label(label="พื้นที่")
        self.area.set_size_request(80 , 40 )
        self.calculated_area = Gtk.Entry()
        self.calculated_area.set_size_request(205 , 40 )

        self.type = Gtk.Label(label="ชนิดป้าย") 
        self.type.set_size_request(80 , 80 )

        self.calculated_type_entry = Gtk.Entry()
        self.calculated_type_entry.set_size_request(205, 80)
        self.calculated_type_entry.set_sensitive(False)

        self.dropdown_list = Gtk.ListBox()
        self.dropdown_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        # Populate the ListBox with items
        for i, item_text in enumerate(["1. อักษรภาษาไทยทั้งหมด", "2. อักษรภาษาไทยปน กับ \nภาษาต่างประเทศ/ภาพ\n/เครื่องหมายอื่น", "3. อักษาไทยอยู่ต่ำกว่า\nอักษรต่างประเทศ/\nไม่มีอักษรไทยเลย"]):
            list_item = Gtk.Label(label=item_text)
            if i == 2:  # Adjust alignment for the third item
                list_item.set_alignment(0.3, 0.2)
            else:
                list_item.set_alignment(0.5, 0.5)
            list_box_row = Gtk.ListBoxRow()
            list_box_row.add(list_item)
            self.dropdown_list.add(list_box_row)
             
        self.dropdown_list.select_row(self.dropdown_list.get_row_at_index(0))


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
        self.goNextButton.get_style_context().add_class("goNextButton")

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

        # adding content to page 
        self.boxTopContent.add(self.gridTopContent)
        self.boxBottomContent.add(self.gridBottomContent)

        # align 
        self.gridContent.set_valign(Gtk.Align.CENTER)
        self.gridContent.set_halign(Gtk.Align.CENTER)
        
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
        self.gridTopContent.attach( self.dropdown_list, 1 , 5 , 1 , 1 )
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
        self.gridContent.attach( self.boxBottomContent , 0 , 1 , 1 , 1 )

        # content wrap all
        self.gridContentWrapper.attach(self.boxImage, 0 , 0 , 2 , 1 ) 
        self.gridContentWrapper.attach(self.gridContent, 2 , 0 , 2 , 1 ) 
        self.gridContentWrapper.attach( self.goBackButton ,2 ,1 ,1 ,1 )
        self.gridContentWrapper.attach( self.goNextButton ,3 ,1 ,1 ,1 )

        self.gridPage.attach( self.label , 0 , 0 , 4 , 1 )
        self.gridPage.attach( self.gridContentWrapper , 0 , 1 , 4, 1 )
        
        self.add(self.gridPage)

        self.set_can_focus(True) 
        self.connect("key-press-event", self.on_key_press)
        self.goBackButton.connect("clicked", self.on_go_back)
        self.goNextButton.connect("clicked", self.on_go_next)

    def on_key_press(self, widget, event):
        keyval = event.keyval
        print(keyval)
        if not self.is_confirmed :

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
                    122: self.confirm_combo,     # z
                }
                
        action_function = key_actions.get(keyval, None)
        action_function()
                
        self.calculated_width.queue_draw()
        self.calculated_height.queue_draw()
        self.calculated_type_entry.queue_draw()
        self.radio_button1.queue_draw()
        self.radio_button2.queue_draw()
        self.goBackButton.queue_draw()
        self.goNextButton.queue_draw()

    def chose_upper_child_combo(self):
        selected_row = self.dropdown_list.get_selected_row()
        if selected_row:
            all_rows = list(self.dropdown_list.get_children())
            index = all_rows.index(selected_row)
            if index > 0:
                prev_row = all_rows[index - 1]
                self.dropdown_list.select_row(prev_row)
            else : 
                index = 1 

    def chose_lower_child_combo(self):
        selected_row = self.dropdown_list.get_selected_row()
        if selected_row:
            all_rows = list(self.dropdown_list.get_children())
            index = all_rows.index(selected_row)
            if index < 3:
                prev_row = all_rows[index + 1]
                self.dropdown_list.select_row(prev_row)
            else : 
                index = 2

    def confirm_combo(self):
        selected_row = self.dropdown_list.get_selected_row()
        if(selected_row):
            text_value = selected_row.get_child().get_text()
            self.calculated_type_entry.set_text(text_value)
            self.calculated_type_entry.queue_draw()

            self.is_confirmed = False 
            self.dropdown_list.hide()

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

    def update_calculated_width(self):
        self.calculated_width.get_style_context().add_class("blue-border")
        self.calculated_height.get_style_context().remove_class("blue-border")

    def update_calculated_height(self):
        self.calculated_width.get_style_context().remove_class("blue-border")
        self.calculated_height.get_style_context().add_class("blue-border")
        self.radio_button1.get_style_context().remove_class("radioSelected")

    def update_radio_1(self):
        self.calculated_height.get_style_context().remove_class("blue-border")
        self.radio_button1.get_style_context().add_class("radioSelected")
        self.radio_button2.get_style_context().remove_class("radioSelected")

    def update_radio_2(self):

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
        self.current_entity = min(self.current_entity, 6)
        self.update_ui()

    def decrement_entity(self):
        self.current_entity -= 1
        self.current_entity = max(self.current_entity, 0)
        self.update_ui()

    def cancel_action(self):
        self.is_confirmed = False

    def confirm_action(self):
        if self.current_entity == 4 : 
            self.dropdown_list.show()
            self.is_confirmed = True
        elif self.current_entity == 2 : 
            self.radio_button1.set_active(True)
        elif self.current_entity == 3 :
            self.radio_button2.set_active(True)
        elif self.current_entity == 5 : 
            self.goBackButton.emit("clicked")
        elif self.current_entity == 6 : 
            self.goNextButton.emit("clicked")
        else : 
            self.is_confirmed = True

    # stack page change handler 
    def on_stack_visible_child_changed(self , stack, param_spec):
        visible_child_name = self.stack.get_visible_child_name()
        print("change child to page2")
        if visible_child_name == "page2":
            # Retrieve the filename from the main window
            self.grab_focus()
            exported_data = self.main_window.get_processing_data()
            self.dropdown_list.hide()
            if exported_data:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(exported_data['src_image'])
                scaled_pixbuf = pixbuf.scale_simple(720, 405, GdkPixbuf.InterpType.BILINEAR)
                self.image.set_from_pixbuf(scaled_pixbuf)
               
    def on_radio_button_toggled(self, button):
        if button.get_active():
            print(button.get_label() + " selected")

    def on_go_back(self,widget) :
        self.stack.set_visible_child_name("page1")

    def on_go_next(self,widget) :
        self.stack.set_visible_child_name("page3")

    