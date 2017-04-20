from firebase import firebase
import random
import time
import threading
from threading import Thread
import zmq
import RPi.GPIO as GPIO

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
ind_sensor = 26 #12 
motor_pin = 19
micro_sw = 23 #17

#GPIO Pins Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(ind_sensor,GPIO.IN,GPIO.PUD_DOWN)
GPIO.setup(micro_sw,GPIO.IN,GPIO.PUD_DOWN)
GPIO.setup(motor_pin, GPIO.OUT)

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
        self.nocache = True

class LogoutButton(Button):
    def __init__(self,**kwargs):
        Button.__init__(self, **kwargs)
        self.font_size = 20
        self.font_name = 'Pixeled'
        self.markup = True 
        self.background_normal = '2nd page/log off text.png'
        self.background_down = '2nd page/log off text_pressed.png'  
        self.nocache = True

#Thread to run RFID reader
class ZmqThread(Thread):
    def __init__(self, screen):
        super(ZmqThread, self).__init__()
        self.screen = screen
        #entire python program exits when only daemon threads are left
        self.daemon = True 

    #runs when thread starts
    def run(self):
        screen = self.screen
        #connects to zmq server to retrieve id data send by RFID reader
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PAIR)
        self._socket.connect('tcp://localhost:5555')
        #gets the ids of existing users from firebase
        idlist = firebase.get('/idlist')
        while True:
            print 'getting data....'
            #stores id received in a variable
            data = self._socket.recv()
            print data
            if data in idlist.values():
                #checks the user for the respective id detected
                self.user = idlist.keys()[idlist.values().index(data)]
                print self.user
                screen.profileUpdate()
            #if new id is registered, it will add a new child node under the idlist 
            else:
                new_user_no = int(len(idlist.keys())) + 1
                firebase.put('/','/idlist', 'user'+ str(new_user_no), data)
                screen.profileUpdate()

class StartScreen(Screen):

    def __init__(self,**kwargs):
        Screen.__init__(self,**kwargs)
        layout = AnchorLayout()
        ss_img = Image(source = '2nd page/start_screen_01.png', on_touch_down = self.change_to_home, nocache = True)
        layout.add_widget(ss_img)
        self.add_widget(layout)
    
    #creates the RFID thread
    def zmq_connect(self):
        self._zthread = ZmqThread(self)
        self._zthread.start()

    #after ID detected, checks corresponding user data from firebase,
    #then updates the details on the next screen accordingly
    def profileUpdate(self):
        user = self._zthread.user
        print user
        profile = firebase.get('/'+ str(user))
        sc_profile=self.manager.get_screen('Profile')
        sc_profile.profileName.text = profile['name']
        sc_profile.profilePic.source = profile['profilePic']
        sc_profile.profileRank.text = profile['title']
        sc_profile.crownPic.source = profile['rank']
        self.change_to_profile()

    #switch to home screen
    def change_to_home(self, touch, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Home'
        self.zmq_connect()

    #switch to profile screen
    def change_to_profile(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Profile'
        
class HomeScreen(Screen):

    def __init__(self, **kwargs):
        Screen.__init__(self,**kwargs)
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
        image1 = Image(source = 'final project/instruction_left.png', nocache = True)
        image2 = Image(source = 'final project/instruction_right.png', nocache = True)
        hometitle = Label(text = "[color=fff8df]Recycle to Win![/color]", font_name = "Pixeled", font_size = 30,markup=True)
        label1 = HomeLabel(text = '[color=ff0000]Please Scan your ID[/color]',size_hint = (None,None), markup=True)
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
    
    def change_to_profile(self,instance,touch):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Profile'


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.fallEdge = False
        #starts servo motor      
        self.myservo = GPIO.PWM(19,50)
        self.myservo.start(0)

        #starts running inductive sensor 
        self.indState = GPIO.LOW
        Clock.schedule_interval(self.inductiveSense, 0.1)

        Clock.schedule_interval(self.dispense, 0.1)
        

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

        #col2 of mainlayout
        logoffbox = BoxLayout(orientataion = 'horizontal', size = (380,74), size_hint = (None,None), padding = (155,9,0,9))
        spinwheelbox = AnchorLayout(size = (380,268), size_hint = (None,None))
        spinwheelAnchor = AnchorLayout(size = (268,268), size_hint=(None,None))
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
        self.profilePic = Image(source = '', nocache = True, allow_stretch = True)
        self.crownPic = Image(source = '', nocache = True)
        self.profileName = Label(text = '' , markup = True, font_size = 8, font_name = 'Pixeled', size_hint = (None,None))
        self.profileRank = Label(text = '', markup = True, font_size = 30, font_name = 'Pixeled', size_hint = (None,None))
        
        profilePicAnchor.add_widget(self.profilePic)
        profilePicBg.add_widget(profilePicAnchor)
        crownLayout.add_widget(self.crownPic)
        namelayout.add_widget(self.profileName)
        rankTitleLayout.add_widget(self.profileRank)
        
        usercol1.add_widget(profilePicBg)
        usercol1.add_widget(namelayout)
        usercol2.add_widget(crownLayout)
        usercol2.add_widget(rankTitleLayout)
        userlayout.add_widget(usercol1)
        userlayout.add_widget(usercol2)

        #creating and adding widgets under counterlayout
        canImage = Image(source = '2nd page/can.png', nocache = True)
        self.cansCounter = ProgressBar(max = 10, value = 0)
        canImgAnchor.add_widget(canImage)
        cansCounterAnchor.add_widget(self.cansCounter)
        counterlayout.add_widget(canImgAnchor)
        counterlayout.add_widget(cansCounterAnchor)

        #Button to run jackpot machine
        self.spin_button = SpinButton(text = '[color=ff67a4]SPIN[/color]', on_touch_up = self.testWheel, on_press = self.refresh_result)
        btnAnchor.add_widget(self.spin_button)
        btnlayoutBg.add_widget(btnAnchor)

        #creating and adding widgets under col2 of mainlayout
        logoutBtn = LogoutButton(text = '[color=95989a]Log Off[/color]', on_press = self.change_to_home)
        logoffbox.add_widget(logoutBtn)
        spinwheelneedle = Image(source = '2nd page/wheelneedle.png', nocache = True)
        spinwheelneedlebox.add_widget(spinwheelneedle)
        self.spinwheel = Image(source="2nd page/start_wheel.jpg", anim_loop=5, anim_delay=0.05, nocache = True, mipmap = True)
        spinwheelAnchor.add_widget(self.spinwheel)
        spinwheelbox.add_widget(spinwheelAnchor)
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
    
    def testWheel(self,instance,touch):
        if self.cansCounter.value != 0:
            self.SpinningWheel()
        
    def SpinningWheel(self):

        #algorithm to calculate the chance of winning a can based on
        #the number of cans recycled (for demo purpose, algo is rather simple)
        cansRecycled = self.cansCounter.value
        token = random.randint(cansRecycled,10)

        #uploads cans recycled data to firebase
        firebase.put('/','/totalcans',self.cansCounter.value)

        #refreshes the cans counter progress bar
        self.cansCounter.value = 0

        if token == 10:
            self.spinwheel.source = '2nd page/wheel_winner.zip'
            self.spinwheel.reload()
            #runs after 3 seconds
            Clock.schedule_once(self.Win, 3)

        else:
            self.spinwheel.source = '2nd page/wheel_loser.zip'
            self.spinwheel.reload()
            Clock.schedule_once(self.Lose, 3)

    def Win(self, instance):
        self.resultLabel.text = '[color=ff6409]You Win! \n Congratulations![/color]'
        #overrides the micro switch and rotate the motor
        self.myservo.ChangeDutyCycle(6.69)
    
    def Lose(self, instance):
        self.resultLabel.text = '[color=ff6409]You Lose. \n Try Again Next Time![/color]'
    
    #refresh the result display when button is pressed
    def refresh_result(self,instance):
        self.resultLabel.text = ''
    
    #function to detect falling cans
    def inductiveSense(self,*args):
        if GPIO.input(ind_sensor) == GPIO.LOW and self.indState == GPIO.LOW:
            self.cansCounter.value += 1
            self.indState = GPIO.HIGH
        if GPIO.input(ind_sensor) == GPIO.HIGH:
            self.indState = GPIO.LOW
    
    #implements micro switch to stops the motor from running after it rotates for a quarter cycle
    def dispense(self,*args):
        if GPIO.input(micro_sw)==GPIO.HIGH and self.fallEdge == True:
            self.myservo.ChangeDutyCycle(0)
            self.fallEdge = False
        elif GPIO.input(micro_sw)==GPIO.LOW and self.fallEdge == False:
            self.myservo.ChangeDutyCycle(6.69)
            self.fallEdge = True
    
    def change_to_home(self,value):
        self.resultLabel.text = ''
        self.manager.transition.direction = 'right'
        self.manager.current = 'Home'

class RecyclingGUIApp(App):

    def build(self):
        Window.size = (800,480)
        sm = ScreenManager()
        ss = StartScreen(name = 'Start')
        hs = HomeScreen(name = 'Home')
        ps = ProfileScreen(name = 'Profile')
        sm.add_widget(ss)
        sm.add_widget(hs)
        sm.add_widget(ps)
        sm.current = 'Start'
        return sm
                
if __name__=='__main__':
    try:
        RecyclingGUIApp().run()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print 'cleaning....'