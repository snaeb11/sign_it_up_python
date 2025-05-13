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
            print("No account_data.pkl found. Creating new account.")
            self.create_default_account()
        else:
            with open("account_data.pkl", "rb") as file:
                account = pickle.load(file)

            # a button
            if account.aStatus:
                aBtn = ImageButton(
                    source=f'assets/checkAa.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                aBtn = ImageButton(
                    source=f'assets/aA.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )

            # e button
            if not account.aStatus:
                eBtn = ImageButton(
                    source=f'assets/lockEe.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                    disabled = True
                )
            elif account.eStatus:
                eBtn = ImageButton(
                    source=f'assets/checkEe.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                eBtn = ImageButton(
                    source=f'assets/eE.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )

            # i button
            if not account.eStatus:
                iBtn = ImageButton(
                    source=f'assets/lockIi.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                    disabled=True
                )
            elif account.iStatus:
                iBtn = ImageButton(
                    source=f'assets/checkIi.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                iBtn = ImageButton(
                    source=f'assets/Ii.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )

            # o button
            if not account.iStatus:
                oBtn = ImageButton(
                    source=f'assets/lockOo.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                    disabled=True
                )
            elif account.oStatus:
                oBtn = ImageButton(
                    source=f'assets/checkOo.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                oBtn = ImageButton(
                    source=f'assets/Oo.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )

            # u button
            if not account.oStatus:
                uBtn = ImageButton(
                    source=f'assets/lockUu.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                    disabled=True
                )
            elif account.uStatus:
                uBtn = ImageButton(
                    source=f'assets/checkUu.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150))
                )
            else:
                uBtn = ImageButton(
                    source=f'assets/Uu.png',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),
                )

            aBtn.bind(on_press=self.open_letter_a)
            eBtn.bind(on_press=self.open_letter_e)
            iBtn.bind(on_press=self.open_letter_i)
            oBtn.bind(on_press=self.open_letter_o)
            uBtn.bind(on_press=self.open_letter_u)

            self.layout.add_widget(aBtn)
            self.layout.add_widget(eBtn)
            self.layout.add_widget(iBtn)
            self.layout.add_widget(oBtn)
            self.layout.add_widget(uBtn)

            self.add_widget(MDRaisedButton(
                text='Back to Menu',
                md_bg_color='gray',
                on_release=self.go_back,
                size_hint=(0.5, None),
                pos_hint={'center_x': 0.5,
                          'center_y': 0.3}
            ))

    def create_default_account(self):
        print('yawa')

    def on_enter(self):
        # Ensure this method is called when returning to the screen
        print(status_tracker.aStatus, "<-- vowels_menu_screen")
        self.add_vowel_buttons()  # Update the button based on the status

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openMain()
