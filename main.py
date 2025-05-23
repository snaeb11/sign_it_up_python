import os
import subprocess
import sys

from kivy.uix.screenmanager import ScreenManager
from challenges_screen import ChallengesScreen
from helpers import *
from intro_screen import IntroScreen
from navigation_screen import BottomNavScreen
from register import RegisterScreen
from vowels_easy_screen import *
from vowels_hard_screen import *
from vowels_intermediate_screen import *
from vowels_menu_screen import VowelMenuScreen
from vowels_screen import *

# List of required packages
required_packages = ['kivy', 'kivymd', 'mediapipe', 'opencv-python', 'numpy', 'scikit-learn', 'cycler', 'matplotlib']

# Try to import each package and install if missing
for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("All required packages are installed.")

#main--------------------------------------------------------------------
class SignItUp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._button_sound_callback = self._make_click_callback()

        # Initialize with defaults (will be overwritten by load)
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self.load_volume_settings()  # Load saved settings immediately

        # Initialize audio objects as None
        self.click_sfx = None
        self.idle_music = None

    def load_volume_settings(self):
        """Load and immediately apply volume settings"""
        try:
            if os.path.exists("account_data.pkl"):
                with open("account_data.pkl", "rb") as f:
                    account = pickle.load(f)

                self.music_volume = getattr(account, 'music_volume', 0.5)
                self.sfx_volume = getattr(account, 'sfx_volume', 0.5)

        except Exception as e:
            print(f"Error loading volume settings: {e}")

    def save_volume_settings(self):
        """Save current volume settings to account data"""
        try:
            if os.path.exists("account_data.pkl"):
                with open("account_data.pkl", "rb") as f:
                    account = pickle.load(f)

                account.music_volume = self.music_volume
                account.sfx_volume = self.sfx_volume

                with open("account_data.pkl", "wb") as f:
                    pickle.dump(account, f)

        except Exception as e:
            print(f"Error saving volume settings: {e}")

    def _make_click_callback(self):
        def callback(instance):
            self.play_click_sound()

        return callback

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
        self.bottom_nav_screen = BottomNavScreen(name='bottom_nav')
        self.vowels_menu_screen = VowelMenuScreen(name='vowels_menu')
        self.intro_screen = IntroScreen(name='intro')
        self.challenges_screen = ChallengesScreen(name='challenges_menu')

        ##vowels easy challenges
        self.vowels_easy_screen = VowelsEasyChallengeScreen(name='vowels_easy')
        self.vowels_easy_instruction = EasyInstructionScreen(name='vowels_easy_instruction')
        self.first_screen = FirstScreen(name='first_screen_easy')
        self.second_screen = SecondScreen(name='second_screen_easy')
        self.third_screen = ThirdScreen(name='third_screen_easy')
        self.fourth_screen = FourthScreen(name='fourth_screen_easy')
        self.fifth_screen = FifthScreen(name='fifth_screen_easy')

        ##vowels intermediate challenges
        self.vowels_intermediate_screen = VowelsIntermediateChallengeScreen(name='vowels_intermediate')
        self.vowels_intermediate_instruction = VowelsIntermediateInstructionScreen(name='vowels_intermediate_instruction')
        self.vowels_intermediate_first_screen = FirstScreenVowelIntermediate(name='vowel_first_intermediate_screen')
        self.vowels_intermediate_second_screen = SecondScreenVowelIntermediate(name='vowel_second_intermediate_screen')
        self.vowels_intermediate_third_screen = ThirdScreenVowelIntermediate(name='vowel_third_intermediate_screen')
        self.vowels_intermediate_fourth_screen = FourthScreenVowelIntermediate(name='vowel_fourth_intermediate_screen')
        self.vowels_intermediate_fifth_screen = FifthScreenVowelIntermediate(name='vowel_fifth_intermediate_screen')

        ## vowels hard challenges
        self.vowels_hard_screen = VowelsHardChallengeScreen(name='vowels_hard')
        self.vowels_hard_instruction = VowelsHardInstructionScreen(name='vowels_hard_instruction')
        self.vowels_hard_first_screen = FirstScreenVowelHard(name='vowel_first_hard_screen')
        self.vowels_hard_second_screen = SecondScreenVowelHard(name='vowel_second_hard_screen')
        self.vowels_hard_third_screen = ThirdScreenVowelHard(name='vowel_third_hard_screen')
        self.vowels_hard_fourth_screen = FourthScreenVowelHard(name='vowel_fourth_hard_screen')
        self.vowels_hard_fifth_screen = FifthScreenVowelHard(name='vowel_fifth_hard_screen')

        #vowels screen
        self.letter_a_screen = LetterAScreen(name='a_screen')
        self.letter_e_screen = LetterEScreen(name='e_screen')
        self.letter_i_screen = LetterIScreen(name='i_screen')
        self.letter_o_screen = LetterOScreen(name='o_screen')
        self.letter_u_screen = LetterUScreen(name='u_screen')

        self.sm.add_widget(self.register_screen)
        self.sm.add_widget(self.bottom_nav_screen)
        self.sm.add_widget(self.vowels_menu_screen)
        self.sm.add_widget(self.intro_screen)
        self.sm.add_widget(self.challenges_screen)

        ### vowel easy chal
        self.sm.add_widget(self.vowels_easy_screen)
        self.sm.add_widget(self.vowels_easy_instruction)
        self.sm.add_widget(self.first_screen)
        self.sm.add_widget(self.second_screen)
        self.sm.add_widget(self.third_screen)
        self.sm.add_widget(self.fourth_screen)
        self.sm.add_widget(self.fifth_screen)

        ### vowel inter chal
        self.sm.add_widget(self.vowels_intermediate_screen)
        self.sm.add_widget(self.vowels_intermediate_instruction)
        self.sm.add_widget(self.vowels_intermediate_first_screen)
        self.sm.add_widget(self.vowels_intermediate_second_screen)
        self.sm.add_widget(self.vowels_intermediate_third_screen)
        self.sm.add_widget(self.vowels_intermediate_fourth_screen)
        self.sm.add_widget(self.vowels_intermediate_fifth_screen)

        ### vowel hard chal
        self.sm.add_widget(self.vowels_hard_screen)
        self.sm.add_widget(self.vowels_hard_instruction)
        self.sm.add_widget(self.vowels_hard_first_screen)
        self.sm.add_widget(self.vowels_hard_second_screen)
        self.sm.add_widget(self.vowels_hard_third_screen)
        self.sm.add_widget(self.vowels_hard_fourth_screen)
        self.sm.add_widget(self.vowels_hard_fifth_screen)
        #
        self.sm.add_widget(self.letter_a_screen)
        self.sm.add_widget(self.letter_e_screen)
        self.sm.add_widget(self.letter_i_screen)
        self.sm.add_widget(self.letter_o_screen)
        self.sm.add_widget(self.letter_u_screen)

        self.sm.current = "bottom_nav"
        self.sm.bind(current=self.on_screen_change)
        self.bind_sfx_to_all_buttons(self.sm.get_screen("bottom_nav"))

        # Load button SFX & BGM with correct volumes
        self.click_sfx = SoundLoader.load('assets/sounds/select2.mp3')
        if self.click_sfx:
            self.click_sfx.volume = self.sfx_volume  # Apply loaded volume

        self.idle_music = SoundLoader.load('assets/sounds/idlemusic1.mp3')
        if self.idle_music:
            self.idle_music.loop = True
            self.idle_music.volume = self.music_volume  # Apply loaded volume
            self.idle_music.play()

        return self.sm

    def openVowelChallenges (self):
        self.sm.current = 'challenges_menu'
        self.stop_idle_music()

    def openVowelsMenu (self):
     self.stop_idle_music()
     self.sm.current = 'vowels_menu'

    def openMain(self):
        self.sm.current = 'bottom_nav'
        if self.idle_music:
            self.idle_music.play()

    def openChallenges (self):
        self.sm.current = 'challenges_menu'

    def openIntro (self):
     self.stop_idle_music()
     self.sm.current = 'intro'

    def openLetterA (self):
     self.sm.current = 'a_screen'

    def openLetterE (self):
     self.sm.current = 'e_screen'

    def openLetterI (self):
     self.sm.current = 'i_screen'

    def openLetterO (self):
     self.sm.current = 'o_screen'

    def openLetterU (self):
     self.sm.current = 'u_screen'

    def openVowelEasy (self):
     self.sm.current = 'vowels_easy'

    def openVowelIntermediate (self):
     self.sm.current = 'vowels_intermediate'

    def openVowelHard (self):
     self.sm.current = 'vowels_hard'

    def validate_vowel_input(self, instance):
        text = instance.text

        if len(text) > 1 or not text.isalpha():
            instance.text = text[:1] if text[:1].isalpha() else ''

    def play_click_sound(self):
        if self.click_sfx:
            self.click_sfx.volume = self.sfx_volume
            self.click_sfx.play()

    def stop_idle_music(self):
        if hasattr(self, 'idle_music') and self.idle_music:
            self.idle_music.stop()

    def bind_sfx_to_all_buttons(self, root_widget):
        for child in root_widget.walk():
            if hasattr(child, 'on_press') and hasattr(child, 'bind'):
                child.bind(on_press=self._button_sound_callback)

    def unbind_sfx_from_all_buttons(self, root_widget):
        for child in root_widget.walk():
            if hasattr(child, 'on_press') and hasattr(child, 'unbind'):
                child.unbind(on_press=self._button_sound_callback)

    def on_screen_change(self, instance, value):
        # Unbind from all screens first (clean slate)
        for screen in self.sm.screens:
            self.unbind_sfx_from_all_buttons(screen)

        # Bind only on the current screen if not 'register'
        if value != 'register':
            current_screen = self.sm.get_screen(value)
            self.bind_sfx_to_all_buttons(current_screen)

    def set_music_volume(self, volume):
        """Set music volume and ensure it's applied immediately"""
        self.music_volume = volume
        if hasattr(self, 'idle_music') and self.idle_music:
            self.idle_music.volume = volume
        self.save_volume_settings()

    def set_sfx_volume(self, volume):
        """Set SFX volume and ensure it's applied immediately"""
        self.sfx_volume = volume
        if hasattr(self, 'click_sfx') and self.click_sfx:
            self.click_sfx.volume = volume
        self.save_volume_settings()

#main-run---------------------------------------------------------
if __name__ == '__main__':
    SignItUp().run()
