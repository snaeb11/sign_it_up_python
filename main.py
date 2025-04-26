import subprocess
import sys

# List of required packages
required_packages = ['kivy', 'kivymd', 'mediapipe', 'opencv-python', 'numpy', 'scikit-learn', 'cycler', 'matplotlib']

# Try to import each package and install if missing
for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("✅ All required packages are installed.")

from kivymd.app import MDApp
from kivy.lang import Builder
from helpers import *
from kivy.uix.screenmanager import ScreenManager, Screen
from vowels_screen import *
from intro_screen import IntroScreen
from vowels_menu_screen import VowelMenuScreen
from login_screen import LoginScreen
from navigation_screen import BottomNavScreen



#main--------------------------------------------------------------------
class SignItUp(MDApp):
    def build(self):

        ##button loads
        Builder.load_string(introButton)
        Builder.load_string(vowelsButton)
        Builder.load_string(aButton)
        Builder.load_string(congrats)
        #####

        self.theme_cls.primary_palette="Gray"
        self.theme_cls.theme_style="Dark"

        self.sm = ScreenManager()
        self.login_scren = LoginScreen(name='login')
        self.bottom_nav_screen = BottomNavScreen(name='bottom_nav')
        self.vowels_menu_screen = VowelMenuScreen(name='vowels_menu')
        self.intro_screen = IntroScreen(name='intro')

        #vowels screen
        self.letter_a_screen = LetterAScreen(name='a_screen')
        self.letter_e_screen = LetterEScreen(name='e_screen')
        self.letter_i_screen = LetterIScreen(name='i_screen')
        self.letter_o_screen = LetterOScreen(name='o_screen')
        self.letter_u_screen = LetterUScreen(name='u_screen')

        self.sm.add_widget(self.login_scren)
        self.sm.add_widget(self.bottom_nav_screen)
        self.sm.add_widget(self.vowels_menu_screen)
        self.sm.add_widget(self.intro_screen)

        #
        self.sm.add_widget(self.letter_a_screen)
        self.sm.add_widget(self.letter_e_screen)
        self.sm.add_widget(self.letter_i_screen)
        self.sm.add_widget(self.letter_o_screen)
        self.sm.add_widget(self.letter_u_screen)

        return self.sm
    
    def openVowelsMenu (self):
     print('vowels menu')
     self.sm.current = 'vowels_menu'

    def openIntro (self):
     print('intro')
     self.sm.current = 'intro'

    def openLetterA (self):
     print('letter a')
     self.sm.current = 'a_screen'

    def openLetterE (self):
     print('letter e')
     self.sm.current = 'e_screen'

    def openLetterI (self):
     print('letter i')
     self.sm.current = 'i_screen'

    def openLetterO (self):
     print('letter o')
     self.sm.current = 'o_screen'

    def openLetterU (self):
     print('letter u')
     self.sm.current = 'u_screen'



#main-run---------------------------------------------------------
if __name__ == '__main__':
    SignItUp().run()
