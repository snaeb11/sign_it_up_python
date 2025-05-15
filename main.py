import subprocess
import sys

from challenges_screen import ChallengesScreen

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

from kivy.lang import Builder
from helpers import *
from kivy.uix.screenmanager import ScreenManager, Screen
from vowels_screen import *
from intro_screen import IntroScreen
from vowels_menu_screen import VowelMenuScreen
from navigation_screen import BottomNavScreen
from register import RegisterScreen


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
        self.register_screen = RegisterScreen(name='register')
        ##self.welcome_screen = WelcomeScreen(name='welcome')
        self.bottom_nav_screen = BottomNavScreen(name='bottom_nav')
        self.vowels_menu_screen = VowelMenuScreen(name='vowels_menu')
        self.intro_screen = IntroScreen(name='intro')
        self.challenges_screen = ChallengesScreen(name='challenges_menu')

        #vowels screen
        self.letter_a_screen = LetterAScreen(name='a_screen')
        self.letter_e_screen = LetterEScreen(name='e_screen')
        self.letter_i_screen = LetterIScreen(name='i_screen')
        self.letter_o_screen = LetterOScreen(name='o_screen')
        self.letter_u_screen = LetterUScreen(name='u_screen')

        ##self.sm.add_widget(self.welcome_screen)
        self.sm.add_widget(self.register_screen)
        self.sm.add_widget(self.bottom_nav_screen)
        self.sm.add_widget(self.vowels_menu_screen)
        self.sm.add_widget(self.intro_screen)
        self.sm.add_widget(self.challenges_screen)
        #bullied class

        #
        self.sm.add_widget(self.letter_a_screen)
        self.sm.add_widget(self.letter_e_screen)
        self.sm.add_widget(self.letter_i_screen)
        self.sm.add_widget(self.letter_o_screen)
        self.sm.add_widget(self.letter_u_screen)

        self.sm.current = "bottom_nav"
        return self.sm
    
    def openVowelsMenu (self):
     print('vowels menu')
     self.sm.current = 'vowels_menu'

    def openMain (self):
     print('open menu')
     self.sm.current = 'bottom_nav'

    def openChallenges (self):
        print('shallenge time')
        self.sm.current = 'challenges_menu'

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
