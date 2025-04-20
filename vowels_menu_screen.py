from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from helpers import *
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

class ImageButton(ButtonBehavior, Image):
    pass

class VowelMenuScreen (MDScreen):
    ##button open
    def open_letter_a(self, *args):
        app = MDApp.get_running_app()
        app.openLetterA()
    ##button open

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = MDBoxLayout(orientation='vertical',
                                    spacing=20,
                                    padding=[0, 0, 0, 0],
                                    size_hint=(None, None),
                                    size=(300, 150),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            )
        
        testButton = MDRaisedButton(
            text='hallo vowels menu'
        )

        aButton = ImageButton(source='assets/aA.png',
                          size_hint=(None, None),
                          size=(150, 150))
        aButton.bind(on_press=self.open_letter_a)

        layout.add_widget(aButton)
        layout.add_widget(testButton)

        self.add_widget(layout)
