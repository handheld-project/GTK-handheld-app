# pages/page3.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import cv2
import numpy as np
from PIL import Image

class Page3(Gtk.Grid):
    def __init__(self,main_window,stack):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.gridPage = Gtk.Grid() 
        self.gridPage.set_valign(Gtk.Align.CENTER)
        self.gridPage.set_halign(Gtk.Align.START)
        # self.gridPage.set_column_homogeneous(True)  # Make columns expand equall

        # function button
        self.goBackButton = Gtk.Button("กลับไปหน้าเเรก")
        self.goBackButton.set_size_request(45,30)

        self.goNextButton = Gtk.Button("ยืนยันข้อมูล")
        self.goBackButton.set_size_request(105,30)
        
        #gridContents wrapper
        self.gridContentWrapper = Gtk.Grid() 

        # labelPage
        self.label = Gtk.Label(label="ผลลัพธ์การตรวจจับป้ายโฆษณา")
        self.label.set_size_request(1080,50)

        self.excelLabel = Gtk.Label(label="the excel file name")
        self.excelLabel.set_size_request(80,50)

        self.excelLabel2 = Gtk.Label(label="บันทึกข้อมูลสำเร็จ")
        self.excelLabel2.set_size_request(80,50)

        # Image
            #Container
        self.boxImage = Gtk.Box() 
        self.image = Gtk.Image() 
        self.image.set_size_request(465, 270)

        self.excelImage = Gtk.Image() 
        self.excelImage.set_size_request(200, 200)
        self.init_excel_image()
        
        self.excelCorrect= Gtk.Image() 
        self.excelImage.set_size_request(200, 200)
        self.init_correct_image()

        self.boxExcel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.boxExcel.set_size_request(200, 200)

        # Calculated Content 
        self.gridContent = Gtk.Grid()
        
        # top
        self.boxTopContent = Gtk.Box() 
        self.gridTopContent = Gtk.Grid() 
        
        self.topContentLabel = Gtk.Label(label="ข้อมูลป้าย" ) 
        self.topContentLabel.set_size_request(165 , 40 )

        self.unit_label_w = Gtk.Label(label="ม.")
        self.unit_label_h = Gtk.Label(label="ม.")
        self.unit_area_label = Gtk.Label(label="ตร.ม")
        self.unit_tax = Gtk.Label(label="บาท")

        self.adjustment_width = Gtk.Adjustment(0, 0, 100, 0.01, 10, 0)

        self.width = Gtk.Label(label="ความกว้าง") 
        self.width.set_size_request(65 , 40 )

        self.calculated_width = Gtk.SpinButton()
        self.calculated_width.set_size_request(190 , 40 )
        self.calculated_width.set_adjustment(self.adjustment_width)
        self.calculated_width.set_sensitive(False) 
        self.calculated_width.set_digits(2)  
        
        self.adjustment_height = Gtk.Adjustment(0, 0, 100, 0.01, 10, 0)

        self.height = Gtk.Label(label="ความสูง") 
        self.height.set_size_request(65 , 40 )

        self.calculated_height = Gtk.SpinButton()
        self.calculated_height.set_size_request(190 , 40 )
        self.calculated_height.set_adjustment(self.adjustment_height)
        self.calculated_height.set_sensitive(False) 
        self.calculated_height.set_digits(2)  

        self.radio_group = Gtk.RadioButton.new(None)
        self.radio_button1 = Gtk.RadioButton.new_with_label_from_widget(self.radio_group, "ข้อความเคลื่อนไหวได้")
    
        # Create a radio button with the label "Option 2"
        self.radio_button2 = Gtk.RadioButton.new_with_label_from_widget(self.radio_group, "ข้อความเคลื่อนไหวไม่ได้")

        self.area = Gtk.Label(label="พื้นที่")
        self.area.set_size_request(65 , 40 )
        self.calculated_area = Gtk.Entry()
        self.calculated_area.set_size_request(190 , 40 )
        self.calculated_area.set_sensitive(False)

        self.type = Gtk.Label(label="ชนิดป้าย") 
        self.type.set_size_request(65 , 80 )

        self.calculated_type_entry = Gtk.Entry()
        self.calculated_type_entry.set_size_request(190, 80)
        self.calculated_type_entry.set_sensitive(False)

        self.taxPrice = Gtk.Label("ราคาภาษี") 
        self.taxPrice.set_size_request(65 , 40 )
        self.calculated_taxPrice = Gtk.Entry()
        self.calculated_taxPrice.set_size_request(190 , 40 )
        self.calculated_taxPrice.set_sensitive(False)
        
        # bottom 
        self.boxBottomContent = Gtk.Box() 
        self.gridBottomContent = Gtk.Grid()

        self.latitude = Gtk.Label(label="ละติจูด")
        self.latitude.set_size_request(65 , 40 ) 
        self.calculated_latitude = Gtk.Entry( ) 
        self.calculated_latitude.set_size_request(190 , 40 )
        self.calculated_latitude.set_sensitive(False)

        self.longitude = Gtk.Label(label="ลองจิจูด") 
        self.longitude.set_size_request(65 , 40 ) 
        self.calculated_longitude  = Gtk.Entry() 
        self.calculated_longitude.set_size_request(190 , 40 )
        self.calculated_longitude.set_sensitive(False)

        self.time = Gtk.Label(label="เวลา") 
        self.time.set_size_request(65 , 40 ) 
        self.calculated_time  = Gtk.Entry() 
        self.calculated_time.set_size_request(190 , 40 )
        self.calculated_time.set_text("time")
        self.calculated_time.set_sensitive(False)
         
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(30 , 700 )
        self.drawing_area.connect("draw", self.on_draw)
        
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

        self.gridPage.attach( self.label , 0 , 0 , 3 , 1 )
        self.gridPage.attach( self.excelCorrect , 2 , 1 , 1 , 1 ) 
        self.gridPage.attach( self.excelImage , 2 , 1 , 1 , 1 ) 
        self.gridPage.attach( self.excelLabel , 2 , 1 , 1 , 1 ) 
        self.gridPage.attach( self.excelLabel2 , 2 , 1 , 1 , 1 ) 
        self.gridPage.attach( self.boxExcel , 2 , 1 , 1 , 1 ) 

        self.gridPage.attach( self.drawing_area , 1 , 1 , 1 , 1 )
        self.gridPage.attach( self.gridContentWrapper , 0 , 1 , 1, 1 )

        self.init_css_context()
        self.add(self.gridPage)
        # self.add(self.drawing_area)


    def init_css_context(self):
        # add styling
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_path("./styles/page3.style.css")

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

        self.contextBoxExcel = self.boxExcel.get_style_context()
        self.contextExcelCorrect = self.excelCorrect.get_style_context()
        self.contextExcelImage = self.excelImage.get_style_context()
        self.contextExcelLabel = self.excelLabel.get_style_context() 
        self.contextExcelLabel2 = self.excelLabel2.get_style_context() 


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

        self.latitude.get_style_context().add_class("labelName")
        self.longitude.get_style_context().add_class("labelName")
        self.time.get_style_context().add_class("labelName")

        self.calculated_latitude.get_style_context().add_class("calculatedBox")
        self.calculated_longitude.get_style_context().add_class("calculatedBox")
        self.calculated_time.get_style_context().add_class("calculatedBox")

        self.boxExcel.get_style_context().add_class("boxExcel")
        self.excelImage.get_style_context().add_class("excelImage")
        self.excelLabel.get_style_context().add_class("excelLabel")
        self.excelLabel2.get_style_context().add_class("excelLabel2")
        self.excelCorrect.get_style_context().add_class("excelCorrect")

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

        self.contextBoxExcel.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextExcelImage.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextExcelLabel.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextExcelLabel2.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextExcelCorrect.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def init_excel_image(self): 
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("./assets/images/excel.png")
        scaled_pixbuf = pixbuf.scale_simple(100, 100, GdkPixbuf.InterpType.BILINEAR)
        self.excelImage.set_from_pixbuf(scaled_pixbuf)
    
    def init_correct_image(self): 
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("./assets/images/correct.png")
        scaled_pixbuf = pixbuf.scale_simple(50, 50, GdkPixbuf.InterpType.BILINEAR)
        self.excelCorrect.set_from_pixbuf(scaled_pixbuf)


    def on_draw(self, widget, cr):
        # Set line color
        cr.set_source_rgb(0.15, 0.55, 0.25)

        # Set line width
        cr.set_line_width(5)

        # Move to the starting point (x1, y1)
        x = 10  # X-coordinate of the top-left corner
        y = 0  # Y-coordinate of the top-left corner
        width = 5  # Width of the rectangle
        height = 800  # Height of the rectangle

        cr.rectangle(x, y, width, height)
        cr.stroke()
