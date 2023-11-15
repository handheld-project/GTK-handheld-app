# pages/page2.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import datetime

class Page2(Gtk.Grid):
    def __init__(self , stack ):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        
        self.stack = stack
        
        # mainbox 
        self.main_box = Gtk.Box()
        
        # gridPage
        self.gridPage = Gtk.Grid() 
        self.gridPage.set_valign(Gtk.Align.CENTER)
        self.gridPage.set_halign(Gtk.Align.CENTER)
        self.gridPage.set_column_homogeneous(True)  # Make columns expand equall

        #gridContents wrapper
        self.gridContentWrapper = Gtk.Grid() 

        # labelPage
        self.pageLabel = Gtk.Label(label="ถ่ายรูปป้ายโฆษณา ภายในระยะห่างจากป้าย xx เมตร ")

        self.label = Gtk.Label(label="ผลลัพธ์การตรวจจับป้ายโฆษณา")
        # Image
            #Container
        self.boxImage = Gtk.Box() 
        self.image = Gtk.Image() 
        self.image.set_size_request(700, 600)

        # Calculated Content 
        self.gridContent = Gtk.Grid()
        
        # top
        self.boxTopContent = Gtk.Box() 
        self.gridTopContent = Gtk.Grid() 
        
        self.topContentLabel = Gtk.Label(label="ข้อมูลป้าย") 

        self.width = Gtk.Label(label="ความกว้าง" ) 
        self.calculated_width = Gtk.Label(label="ความกว้าง asdasdasd" ) 

        self.height = Gtk.Label(label="ความสูง") 
        self.calculated_height = Gtk.Label()

        self.area = Gtk.Label(label="พื้นที่")
        self.calculated_area = Gtk.Label()

        self.type = Gtk.Label(label="ชนิดป้าย") 
        self.calculated_type = Gtk.Label()

        self.taxPrice = Gtk.Label("ราคาภาษี") 
        self.calculated_taxPrice = Gtk.Label()


        # bottom 
        self.boxBottomContent = Gtk.Box() 
        self.gridBottomContent = Gtk.Grid()
        self.latitude = Gtk.Label(label="ละติจูด") 
        self.calculated_latitude = Gtk.Label() 

        self.longitude = Gtk.Label(label="ลองจิจูด") 
        self.calculated_longitude  = Gtk.Label() 

        self.time = Gtk.Label(label="เวลา") 
        self.calculated_time  = Gtk.Label( label = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") ) 
         
        # add styling
        
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_path("./styles/page2.style.css")
        
        self.contextImage = self.image.get_style_context()
        self.contextBoxTopContent = self.boxTopContent.get_style_context()
        self.contextBoxBottomContent = self.boxBottomContent.get_style_context()
        self.contextGridContentWrapper = self.gridContentWrapper.get_style_context()
        self.contextCalculated_width = self.calculated_width.get_style_context()
   
        self.image.get_style_context().add_class("image")
        self.boxTopContent.get_style_context().add_class("boxTopContent")
        self.boxBottomContent.get_style_context().add_class("boxBottomContent")
        self.gridContentWrapper.get_style_context().add_class("gridContentWrapper")
        self.calculated_width.get_style_context().add_class("calculatedWidth")


        self.contextImage.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextBoxTopContent.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextBoxBottomContent.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextGridContentWrapper.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.contextCalculated_width.add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # adding content to page 
        self.boxTopContent.add(self.gridTopContent)
        self.boxBottomContent.add(self.gridBottomContent)

        # align 
        self.gridContent.set_valign(Gtk.Align.CENTER)
        self.gridContent.set_halign(Gtk.Align.CENTER)

        self.width.set_halign(Gtk.Align.END)
        self.width.set_valign(Gtk.Align.END)
        self.calculated_width.set_halign(Gtk.Align.START)
        self.calculated_width.set_valign(Gtk.Align.START)
        
        self.height.set_halign(Gtk.Align.END)
        self.height.set_valign(Gtk.Align.END)
        self.calculated_height.set_halign(Gtk.Align.START)
        self.calculated_height.set_valign(Gtk.Align.START)

        #sizing 
        self.gridTopContent.set_size_request(275,300)

        self.gridPage.set_column_homogeneous(True)
        self.gridTopContent.set_column_homogeneous(True)




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
        self.gridBottomContent.attach(self.calculated_latitude , 0 , 1 , 1 ,1 ) 
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