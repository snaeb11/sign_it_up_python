import os
import pickle

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

class ChallengesScreen(MDScreen):
    def open_vowel_easy(self, *args):
        app = MDApp.get_running_app()
        app.openVowelEasy()

    def open_vowel_intermediate(self, *args):
        app = MDApp.get_running_app()
        app.openVowelIntermediate()

    def open_vowel_hard(self, *args):
        app = MDApp.get_running_app()
        app.openVowelHard()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def add_vowel_buttons(self):
        # Clear existing widgets first
        self.layout.clear_widgets()

        if not os.path.exists("account_data.pkl"):
            self.create_default_account()
        else:
            with open("account_data.pkl", "rb") as file:
                account = pickle.load(file)

            # easy button
            if account.easyChallenge:
                easyBtn = ImageButton(
                    source=f'assets/vowelsEasyCheck.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                easyBtn = ImageButton(
                    source=f'assets/vowelsEasyClick.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )

            # intermediate button
            if not account.easyChallenge:
                intermediateBtn = ImageButton(
                    source=f'assets/vowelsInterLocked.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                    disabled = True
                )
            elif account.intermediateChallenge:
                intermediateBtn = ImageButton(
                    source=f'assets/vowelsInterCheck.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                intermediateBtn = ImageButton(
                    source=f'assets/vowelsInterClick.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )

            # hard button
            if not account.intermediateChallenge:
                hardBtn = ImageButton(
                    source=f'assets/vowelsHardLocked.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                    disabled=True
                )
            elif account.hardChallenge:
                hardBtn = ImageButton(
                    source=f'assets/vowelsHardCheck.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                hardBtn = ImageButton(
                    source=f'assets/vowelsHardClick.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )


            easyBtn.bind(on_press=self.open_vowel_easy)
            intermediateBtn.bind(on_press=self.open_vowel_intermediate)
            hardBtn.bind(on_press=self.open_vowel_hard)

            self.layout.add_widget(easyBtn)
            self.layout.add_widget(intermediateBtn)
            self.layout.add_widget(hardBtn)

            self.add_widget(MDRaisedButton(
                text='Back to Menu',
                md_bg_color='gray',
                on_release=self.go_back,
                size_hint=(0.5, None),
                pos_hint={'center_x': 0.5,
                          'center_y': 0.3}
            ))

    def create_default_account(self):
        print('Creating account...')

    def on_enter(self):
        self.add_vowel_buttons()  # Update the button based on the status

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openMain()
