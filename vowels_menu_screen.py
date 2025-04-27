from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.metrics import dp
from helpers import *
from status import status_tracker

class ImageButton(ButtonBehavior, Image):
    pass

class VowelMenuScreen(MDScreen):
    def open_letter_a(self, *args):
        app = MDApp.get_running_app()
        app.openLetterA()

    def open_letter_e(self, *args):
        app = MDApp.get_running_app()
        app.openLetterE()

    def open_letter_i(self, *args):
        app = MDApp.get_running_app()
        app.openLetterI()

    def open_letter_o(self, *args):
        app = MDApp.get_running_app()
        app.openLetterO()

    def open_letter_u(self, *args):
        app = MDApp.get_running_app()
        app.openLetterU()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Scrollable container
        scroll_view = MDScrollView(size_hint=(1, 1))

        # Grid layout: 2 buttons per row, vertical scrolling
        self.layout = GridLayout(
            cols=2,
            spacing=dp(10),
            padding=[dp(10), dp(10)],
            size_hint_y=None
        )
        self.layout.bind(minimum_height=self.layout.setter('height'))

        # Add all vowel buttons
        self.add_vowel_buttons()

        scroll_view.add_widget(self.layout)
        self.add_widget(scroll_view)

    def add_vowel_buttons(self):
        # Clear existing widgets first
        self.layout.clear_widgets()

        # Add 'a' button depending on status_tracker.aStatus
        if status_tracker.aStatus:
            aBtn = ImageButton(
                source=f'assets/checkAa.png',
                size_hint=(None, None),
                size=(dp(150), dp(150)),
                disabled=True
            )
        else:
            aBtn = ImageButton(
                source=f'assets/aA.png',
                size_hint=(None, None),
                size=(dp(150), dp(150)),
            )

        if status_tracker.eStatus:
            eBtn = ImageButton(
                source=f'assets/checkEe.png',
                size_hint=(None, None),
                size=(dp(150), dp(150)),
                disabled=True
            )
        else:
            eBtn = ImageButton(
                source=f'assets/eE.png',
                size_hint=(None, None),
                size=(dp(150), dp(150)),
            )


        aBtn.bind(on_press=self.open_letter_a)
        eBtn.bind(on_press=self.open_letter_e)

        self.layout.add_widget(aBtn)
        self.layout.add_widget(eBtn)

    def on_enter(self):
        # Ensure this method is called when returning to the screen
        print(status_tracker.aStatus, "<-- vowels_menu_screen")
        self.add_vowel_buttons()  # Update the button based on the status
