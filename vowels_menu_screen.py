from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.metrics import dp
from helpers import *

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
        app.openLetteru()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Scrollable container
        scroll_view = MDScrollView(size_hint=(1, 1))

        # Grid layout: 2 buttons per row, vertical scrolling
        layout = GridLayout(
            cols=2,
            spacing=dp(10),
            padding=[dp(10), dp(10)],
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))

        # Add all vowel buttons
        vowels = {
            'aA': self.open_letter_a,
            'eE': self.open_letter_e,
            'iI': self.open_letter_i,
            'oO': self.open_letter_o,
            'uU': self.open_letter_u,
        }

        for key, callback in vowels.items():
            btn = ImageButton(
                source=f'assets/{key}.png',
                size_hint=(None, None),
                size=(dp(150), dp(150))
            )
            btn.bind(on_press=callback)
            layout.add_widget(btn)

        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)
