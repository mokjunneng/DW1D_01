from firebase import firebase
from Read import ReadRFID
import random
import time
import thread 

# import RPi.GPIO as GPIO
#import kivy APIs
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image, AsyncImage
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window 
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.clock import Clock


#Assign Pins
ind_sensor = 12

#GPIO Pins Setup
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(ind_sensor,GPIO.IN,GPIO.PUD_DOWN)


#Set up firebase database
url = 'https://dw1d-recycling.firebaseio.com/'
token = 'ZTY8ja6uJyD3uM2Fjz98ejSJhxwJSORy9ppz7xMS'
firebase = firebase.FirebaseApplication(url,token)

#Widget Styles
class HomeLabel(Label):
    def __init__(self, **kwargs):
        Label.__init__(self, **kwargs)
        self.font_size = 15
        self.font_name = "Pixeled"

class SpinButton(Button):
    def __init__(self, **kwargs):
        Button.__init__(self, **kwargs)
        self.font_size = 30
        self.font_name = 'Pixeled'
        self.markup = True
        self.background_normal = '2nd page/spin text box.png'
        self.background_down = '2nd page/spin text box_pressed.png'

class LogoutButton(Button):
    def __init__(self,**kwargs):
        Button.__init__(self, **kwargs)
        self.font_size = 20
        self.font_name = 'Pixeled'
        self.markup = True 
        self.background_normal = '2nd page/log off text.png'
        self.background_down = '2nd page/log off text_pressed.png'  

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        Screen.__init__(self,**kwargs)
        try:
            thread.start_new_thread(ReadRFID())
        except:
            print "Error: unable to start thread"
        #Layouts
        mainlayout = BoxLayout( orientation = "vertical" )
        titlelayout = BoxLayout(size = (800,73), size_hint = (None,None))
        imgboxlayout = BoxLayout(orientation = 'horizontal', size = (800,407), size_hint = (None,None))
        imgboxcol1background = BoxLayout(orientation = 'vertical', size = (400,407))
        imgboxcol2background = BoxLayout(orientation = 'vertical', size = (400,407))
        img1box = AnchorLayout(size = (400,320), size_hint = (None,None))
        img2box = AnchorLayout(size = (400,320), size_hint = (None,None))
        label1box = AnchorLayout(size = (400,87), size_hint = (None,None))
        label2box = AnchorLayout(size = (400,87), size_hint = (None,None))

        #Background images/color
        titlelayout.canvas.add(Rectangle(size = (800,73), source = 'final project/top.jpg', pos = (0,407)))
        imgboxcol1background.canvas.add(Rectangle(size = (400,407), source = 'final project/left.jpg', pos = (0,0)))
        imgboxcol2background.canvas.add(Rectangle(size = (400,407), source = 'final project/right.jpg', pos = (400,0)))
        
        #creating sub-widgets
        image1 = Image(source = 'final project/instruction_left.png')
        image2 = Image(source = 'final project/instruction_right.png')
        hometitle = Label(text = "[color=fff8df]Recycle to Win![/color]", font_name = "Pixeled", font_size = 30,markup=True)
        label1 = HomeLabel(text = '[color=ff0000]Please Scan your ID[/color]', on_touch_down = self.change_to_profile, size_hint = (None,None), markup=True)
        label2 = HomeLabel(text = '[color=056011]Wait for the green light[/color]', size_hint = (None,None), markup=True)

        #adding widgets to layout
        img1box.add_widget(image1)
        img2box.add_widget(image2)
        label1box.add_widget(label1)
        label2box.add_widget(label2)
        titlelayout.add_widget(hometitle)

        imgboxcol1background.add_widget(img1box)
        imgboxcol1background.add_widget(label1box)

        imgboxcol2background.add_widget(img2box)
        imgboxcol2background.add_widget(label2box)

        imgboxlayout.add_widget(imgboxcol1background)
        imgboxlayout.add_widget(imgboxcol2background)

        mainlayout.add_widget(titlelayout)
        mainlayout.add_widget(imgboxlayout)

        self.add_widget(mainlayout)

        #Read RFID reader
        self.readRFID()
    
    def change_to_profile(self, touch, value):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Profile'

    def readRFID(self):
        While True:




class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        #inductive sensor initialization
        # self.indState = GPIO.LOW
        # Clock.schedule_interval(self.inductiveSense, 0.1)
        #Layouts
        mainlayout = BoxLayout(orientation = 'horizontal')
        column1 = BoxLayout(orientation = 'vertical', size = (420,480), size_hint = (None,None))
        column2 = BoxLayout(orientation = 'vertical', size = (380,480), size_hint = (None,None))

        #userlayout 
        userlayout = GridLayout(cols = 2, size = (420,213))
        usercol1 = BoxLayout(orientation = 'vertical', size = (160,213), size_hint = (None,None))
        usercol2 = BoxLayout(orientation = 'vertical', size = (260,213), size_hint = (None,None))
        profilePicBg = AnchorLayout(size = (160,160), size_hint = (None,None))
        profilePicAnchor = AnchorLayout(size = (140,140), size_hint = (None,None))
        crownLayout = AnchorLayout(size = (260,60), size_hint = (None,None))
        namelayout = AnchorLayout(size = (160,53), size_hint = (None,None))
        rankTitleLayout = AnchorLayout(size = (260,153), size_hint = (None,None))
        
        #counterlayout
        counterlayout = BoxLayout(orientation = 'horizontal', size = (420,89), size_hint = (None,None))
        canImgAnchor = AnchorLayout(size = (92,89), size_hint = (None,None))
        cansCounterAnchor = AnchorLayout(size = (328,89), size_hint = (None,None))

        #ButtonLayout
        btnlayoutBg = AnchorLayout(size = (420,178), size_hint = (None,None))
        btnAnchor = AnchorLayout(size = (314,91), size_hint = (None,None))

        #col2 of mainlyout
        logoffbox = BoxLayout(orientataion = 'horizontal', size = (380,74), size_hint = (None,None), padding = (155,9,0,9))
        spinwheelbox = AnchorLayout(size = (380,268), size_hint = (None,None))
        spinwheelneedlebox = BoxLayout(size = (380,26), size_hint = (None,None))
        resultbox = AnchorLayout(size = (380,112), size_hint = (None,None))


        #Background images/color
        profilePicBg.canvas.add(Color(247/255.0, 1, 237/255.0, 1))
        profilePicBg.canvas.add(Rectangle(size = (160,160), pos = (0,320)))

        namelayout.canvas.add(Color(199/255.0, 239/255.0, 246/255.0, 1))
        namelayout.canvas.add(Rectangle(size = (160,53), pos = (0,267)))

        rankTitleLayout.canvas.add(Color(164/255.0, 1, 216/255.0, 1))
        rankTitleLayout.canvas.add(Rectangle(size = (260,153), pos = (160,267)))

        cansCounterAnchor.canvas.add(Color(212/255.0, 1, 216/255.0, 1))
        cansCounterAnchor.canvas.add(Rectangle(size = (328,89), pos = (92,178)))

        btnlayoutBg.canvas.add(Color(209/255.0, 170/255.0, 136/255.0, 1))
        btnlayoutBg.canvas.add(Rectangle(size = (420,178), pos = (0,0)))

        canImgAnchor.canvas.add(Color(1,1,1,1))
        canImgAnchor.canvas.add(Rectangle(size = (92,89), pos = (0,178)))

        logoffbox.canvas.add(Color(161/255.0 ,230/255.0 ,1 ,1))
        logoffbox.canvas.add(Rectangle(size = (380,74), pos = (420,406)))

        spinwheelbox.canvas.add(Color(1,1,1,1))
        spinwheelbox.canvas.add(Rectangle(size = (380,268), pos = (420,112)))

        resultbox.canvas.add(Color(1, 237/255.0, 188/255.0, 1))
        resultbox.canvas.add(Rectangle(size = (380,112), pos = (420,0)))

        spinwheelneedlebox.canvas.add(Color(1,1,1,1))
        spinwheelneedlebox.canvas.add(Rectangle(size = (380,26), pos = (420,380)))

        #creating and adding widgets under userlayout
        profilePic = Image(source = '2nd page/profilePic.jpg')
        crownPic = Image(source = '2nd page/lvl2.png')
        profileName = Label(text = '[color=95989a]Shawn[/color]', markup = True, font_size = 8, font_name = 'Pixeled', size_hint = (None,None))
        profileRank = Label(text = '[color=7a7a7a]Recycling \n Master[/color]', markup = True, font_size = 30, font_name = 'Pixeled', size_hint = (None,None))
        
        profilePicAnchor.add_widget(profilePic)
        profilePicBg.add_widget(profilePicAnchor)
        crownLayout.add_widget(crownPic)
        namelayout.add_widget(profileName)
        rankTitleLayout.add_widget(profileRank)
        
        usercol1.add_widget(profilePicBg)
        usercol1.add_widget(namelayout)
        usercol2.add_widget(crownLayout)
        usercol2.add_widget(rankTitleLayout)
        userlayout.add_widget(usercol1)
        userlayout.add_widget(usercol2)

        #creating and adding widgets under counterlayout
        canImage = Image(source = '2nd page/can.png')
        self.cansCounter = ProgressBar(max = 20)
        canImgAnchor.add_widget(canImage)
        cansCounterAnchor.add_widget(self.cansCounter)
        counterlayout.add_widget(canImgAnchor)
        counterlayout.add_widget(cansCounterAnchor)

        #Button to run jackpot machine
        self.spin_button = SpinButton(text = '[color=ff67a4]SPIN[/color]', on_touch_up = self.SpinningWheel, on_press = self.refresh_result)
        btnAnchor.add_widget(self.spin_button)
        btnlayoutBg.add_widget(btnAnchor)

        #creating and adding widgets under col2 of mainlayout
        logoutBtn = LogoutButton(text = '[color=95989a]Log Off[/color]', on_press = self.change_to_home)
        logoffbox.add_widget(logoutBtn)
        spinwheelneedle = Image(source = '2nd page/wheelneedle.png')
        spinwheelneedlebox.add_widget(spinwheelneedle)
        self.spinwheel = Image(source="2nd page/start_wheel.jpg", nocache=True, allow_stretch=True, anim_loop=5, anim_delay=0.05)
        spinwheelbox.add_widget(self.spinwheel)
        self.resultLabel = Label(text = '', markup = True, font_size = 20, font_name = 'Pixeled')
        resultbox.add_widget(self.resultLabel)
        column2.add_widget(logoffbox)
        column2.add_widget(spinwheelneedlebox)
        column2.add_widget(spinwheelbox)
        column2.add_widget(resultbox)

        #Layout orientation
        column1.add_widget(userlayout)
        column1.add_widget(counterlayout)
        column1.add_widget(btnlayoutBg)
        mainlayout.add_widget(column1)
        mainlayout.add_widget(column2)


        self.add_widget(mainlayout)

    def SpinningWheel(self,instance,touch):
        token = random.randint(1,3)
        self.resultLabel.text = ''
        if token == 3:
            self.spinwheel.source = '2nd page/win_wheel.gif'
            Clock.schedule_once(self.Win, 10)
            self.spinwheel.reload()
           
        else:
            self.spinwheel.source = '2nd page/wheel.gif'
            Clock.schedule_once(self.Lose, 10)
            self.spinwheel.reload()

    def Win(self, instance):
        self.resultLabel.text = '[color=ff6409]You Win! \n Congratulations![/color]'
    
    def Lose(self, instance):
        self.resultLabel.text = '[color=ff6409]You Lose. \n Try Again Next Time![/color]'
        
        
              
    def refresh_result(self,instance):
        # self.spinwheel.reload()
        self.resultLabel.text = ''

    # def inductiveSense(self,*args):
    #     if GPIO.input(ind_sensor) == GPIO.LOW and self.indState == GPIO.LOW:
    #         self.cansCounter.value += 1
    #         self.indState = GPIO.HIGH
    #     if GPIO.input(ind_sensor) == GPIO.HIGH:
    #         self.indState = GPIO.LOW
        
    
    def change_to_home(self,value):
        self.manager.transition.direction = 'right'
        self.manager.current = 'Home'

class RecyclingGUIApp(App):
    def build(self):
        Window.size = (800,480)
        sm = ScreenManager()
        hs = HomeScreen(name = 'Home')
        ps = ProfileScreen(name = 'Profile')
        sm.add_widget(hs)
        sm.add_widget(ps)
        sm.current = 'Home'
        return sm

if __name__=='__main__':
    RecyclingGUIApp().run()