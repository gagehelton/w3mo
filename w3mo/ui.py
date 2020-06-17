import sys
sys.path.insert(0,'')
try:
    from w3mo import discover
except ImportError:
    from w3mo.w3mo import discover

import threading

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.button import Button
from kivymd.uix.spinner import MDSpinner
from kivymd.app import MDApp

## Global Variables #######################################

t = False
getting_devices = False
sm = ScreenManager()
kv = '''
ScreenManager:
    LoadingScreen:
    MainScreen:

<LoadingScreen>
    name: 'loading'

    Label:
        text: 'Searching for Devices'
        font_size: 40
        pos_hint: {'center_x': .5, 'center_y': .6}

    MDSpinner:
        id: spinner
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': .5, 'center_y': .4}
        active: True

<MainScreen>
    name: 'main'
    on_enter: root.add()
'''

## End Global Variables ###################################

class LoadingScreen(Screen):
    pass
    
class MainScreen(Screen):
    def add(self):
        self.add_widget(grid())
        
def callback(instance):
    d = devices[instance.text]
    o = d['obj']
    if(o.state):  
        d['obj'].set_state(0)
        instance.color = .5,.5,.5,.5
    elif(not o.state):
        d['obj'].set_state(1)
        instance.color = 1,1,1,1

class grid(GridLayout):
    def __init__(self, **kwargs):
        super(grid, self).__init__(**kwargs)
        self.cols = 1
        self.inside = GridLayout()
        for device,val in devices.items():
            if(val['obj'].state): 
                color = 1,1,1,1
            else:
                color = .5,.5,.5,.5
            b = Button(text=device, font_size=40, color=color)
            b.bind(on_press=callback)
            self.add_widget(b)

class w3mo_UI(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.root_widget = Builder.load_string(kv)
    
        t = threading.Thread(target=self.get_devices)
        t.daemon = True
        t.start()
        
        return self.root_widget
        
    def get_devices(self):
        global devices
        devices = discover()
        self.root_widget.current = 'main'
        
        
if __name__ == "__main__":
    w3mo_UI().run()