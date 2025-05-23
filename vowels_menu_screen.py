import os
import pickle

from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

        # Initialize sounds
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'vowel_select': SoundLoader.load('assets/sounds/select2.mp3')
        }

        # Main container to center content vertically
        main_box = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            padding=dp(10),
            spacing=dp(10)
        )

        # Add an empty box to push content to vertical center
        top_spacer = MDBoxLayout(size_hint_y=None, height=0)
        content_box = MDBoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(180),
            pos_hint={'center_y': 0.5}
        )

        # Scrollable container with horizontal scrolling
        scroll_view = MDScrollView(
            do_scroll_x=True,
            do_scroll_y=False,
            size_hint=(1, None),
            height=dp(180),
            bar_width = 0
        )

        # Grid layout: 1 row, horizontally scrollable
        self.layout = GridLayout(
            rows=1,
            spacing=dp(10),
            padding=[dp(10), dp(10)],
            size_hint_x=None,
            height=dp(150)
        )
        self.layout.bind(minimum_width=self.layout.setter('width'))
        self.add_vowel_buttons()

        scroll_view.add_widget(self.layout)
        content_box.add_widget(scroll_view)

        # Spacer at bottom for centering effect
        bottom_spacer = MDBoxLayout(size_hint_y=None, height=0)

        main_box.add_widget(top_spacer)
        main_box.add_widget(content_box)
        main_box.add_widget(bottom_spacer)

        # Adjust spacers dynamically to center content vertically
        def update_spacers(*args):
            screen_height = self.height
            content_height = content_box.height
            remaining = max(0, (screen_height - content_height) / 2)
            top_spacer.height = remaining
            bottom_spacer.height = remaining

        self.bind(height=update_spacers)
        update_spacers()

        self.add_widget(main_box)

    def on_enter(self):
        """Update volumes when screen becomes active"""
        for sound in self.sfx.values():
            if sound:
                sound.volume = self.app.sfx_volume
        self.add_vowel_buttons()

    def play_sfx(self, sound_name):
        """Helper method to play SFX with current volume"""
        if sound_name in self.sfx and self.sfx[sound_name]:
            self.sfx[sound_name].volume = self.app.sfx_volume
            self.sfx[sound_name].play()

    def open_letter_a(self, *args):
        self.play_sfx('vowel_select')
        app = MDApp.get_running_app()
        app.openLetterA()

    def open_letter_e(self, *args):
        self.play_sfx('vowel_select')
        app = MDApp.get_running_app()
        app.openLetterE()

    def open_letter_i(self, *args):
        self.play_sfx('vowel_select')
        app = MDApp.get_running_app()
        app.openLetterI()

    def open_letter_o(self, *args):
        self.play_sfx('vowel_select')
        app = MDApp.get_running_app()
        app.openLetterO()

    def open_letter_u(self, *args):
        self.play_sfx('vowel_select')
        app = MDApp.get_running_app()
        app.openLetterU()

    def add_vowel_buttons(self):
        # Clear existing widgets first
        self.layout.clear_widgets()

        if not os.path.exists("account_data.pkl"):
            print("No account_data.pkl found. Creating new account.")
            self.create_default_account()
        else:
            with open("account_data.pkl", "rb") as file:
                account = pickle.load(file)

            # Create buttons
            buttons = []

            # a button
            if account.aStatus:
                aBtn = ImageButton(
                    source='assets/checkAa.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                aBtn = ImageButton(
                    source='assets/aA.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )
            buttons.append(aBtn)

            # e button
            if not account.aStatus:
                eBtn = ImageButton(
                    source='assets/lockEe.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                    disabled=True
                )
            elif account.eStatus:
                eBtn = ImageButton(
                    source='assets/checkEe.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                eBtn = ImageButton(
                    source='assets/eE.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )
            buttons.append(eBtn)

            # i button
            if not account.eStatus:
                iBtn = ImageButton(
                    source='assets/lockIi.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                    disabled=True
                )
            elif account.iStatus:
                iBtn = ImageButton(
                    source='assets/checkIi.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                iBtn = ImageButton(
                    source='assets/Ii.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )
            buttons.append(iBtn)

            # o button
            if not account.iStatus:
                oBtn = ImageButton(
                    source='assets/lockOo.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                    disabled=True
                )
            elif account.oStatus:
                oBtn = ImageButton(
                    source='assets/checkOo.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                oBtn = ImageButton(
                    source='assets/Oo.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )
            buttons.append(oBtn)

            # u button
            if not account.oStatus:
                uBtn = ImageButton(
                    source='assets/lockUu.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                    disabled=True
                )
            elif account.uStatus:
                uBtn = ImageButton(
                    source='assets/checkUu.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                uBtn = ImageButton(
                    source='assets/Uu.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )
            buttons.append(uBtn)

            # Bind buttons with sound effects
            buttons[0].bind(on_press=lambda x: (self.play_sfx('button_click'), self.open_letter_a()))
            buttons[1].bind(on_press=lambda x: (self.play_sfx('button_click'), self.open_letter_e()))
            buttons[2].bind(on_press=lambda x: (self.play_sfx('button_click'), self.open_letter_i()))
            buttons[3].bind(on_press=lambda x: (self.play_sfx('button_click'), self.open_letter_o()))
            buttons[4].bind(on_press=lambda x: (self.play_sfx('button_click'), self.open_letter_u()))

            # Calculate required space and adjust button sizes if needed
            button_width = dp(150)
            num_buttons = len(buttons)
            screen_width = Window.width
            total_button_width = num_buttons * button_width
            min_spacing = dp(5)  # Minimum spacing between buttons

            # Check if buttons fit with minimum spacing
            if total_button_width + (num_buttons - 1) * min_spacing > screen_width:
                # Calculate maximum possible button width that fits
                max_button_width = (screen_width - (num_buttons - 1) * min_spacing) / num_buttons
                button_width = min(button_width, max_button_width)
                # Update all button sizes
                for btn in buttons:
                    btn.size = (button_width, button_width)

            # Calculate total width including spacing
            total_width = num_buttons * button_width + (num_buttons - 1) * min_spacing
            # Calculate side padding
            side_padding = max(0, (screen_width - total_width) / 2)

            # Create a horizontal box layout for the buttons
            button_layout = BoxLayout(
                size_hint=(None, None),
                size=(total_width, button_width),
                spacing=min_spacing,
                pos_hint={'center_x': 0.5, 'top': 0.9}
            )

            # Add buttons to the button layout
            for btn in buttons:
                button_layout.add_widget(btn)

            # Add the button layout to the main layout
            self.layout.add_widget(button_layout)

            # Back button
            back_button = MDRaisedButton(
                text='Back to Menu',
                md_bg_color='gray',
                on_release=lambda x: (self.play_sfx('button_click'), self.go_back()),
                size_hint=(0.5, None),
                height=dp(50),
                pos_hint={'center_x': 0.5, 'center_y': 0.3}
            )
            self.add_widget(back_button)

    def create_default_account(self):
        print('Creating default account')

    def go_back(self, *args):
        self.play_sfx('button_click')
        app = MDApp.get_running_app()
        app.openMain()
