from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
import os
import pickle
from helpers import *

class Account:
    def __init__(self, username: str = "user"):
        self.username = username

        # Vowels status
        self.aStatus = False
        self.eStatus = False
        self.iStatus = False
        self.oStatus = False
        self.uStatus = False

        # Intro screen status
        self.introStatus = False

        ## vowels screen, if true all vowels are cleared
        self.vowelScreen = False

        # challenge
        self.easyChallenge = False
        self.intermediateChallenge = False
        self.hardChallenge = False

        self.finalAchievement = False

        # User Preference Settings
        self.music_volume = 0.5
        self.sfx_volume = 0.5


class RegisterScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=[0, 0, 0, 0],
            size_hint=(None, None),
            size=(300, 150),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )

        self.userName = Builder.load_string(username_helper)

        registerButton = MDRaisedButton(
            text='Login',
            md_bg_color='gray',
            on_release=self.register
        )

        layout.add_widget(self.userName)
        layout.add_widget(registerButton)
        self.add_widget(layout)
        self.current_field_index = 0

    def on_enter(self):
        """Check for existing account after screen is loaded into manager."""
        # Bind keyboard when screen is entered
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_key_down)
        Clock.schedule_once(self.check_existing_account, 0)

    def on_leave(self):
        """Unbind keyboard when leaving the screen."""
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self.on_key_down)
            self._keyboard = None

    def check_existing_account(self, dt):
        """Load existing account and redirect if valid."""
        if os.path.exists("account_data.pkl"):
            try:
                with open("account_data.pkl", "rb") as file:
                    account = pickle.load(file)

                if isinstance(account, Account):  # Ensure it's an Account object
                    # Case-insensitive check for 'user' username
                    if account.username.lower() == 'user':
                        self.parent.current = 'register'
                        self.create_default_account()
                    else:
                        # Redirect to bottom_nav screen
                        if self.manager and "bottom_nav" in self.manager.screen_names:
                            self.manager.current = "bottom_nav"
                        else:
                            print("Error: 'bottom_nav' screen not found.")
                else:
                    print("Invalid account data. Creating a new default account.")
                    self.create_default_account()
            except (pickle.UnpicklingError, EOFError):
                print("Corrupted account file. Creating a new default account.")
                self.create_default_account()
        else:
            print("No account_data.pkl found. Creating new account file.")
            self.create_default_account()

    def create_default_account(self):
        """Create a default account and save it."""
        default_account = Account()
        with open("account_data.pkl", "wb") as file:
            pickle.dump(default_account, file)

        self.parent.current = 'register'

    def _keyboard_closed(self):
        """Handle keyboard being closed."""
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self.on_key_down)
            self._keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        key, scancode = keycode
        if key == 9:  # Tab
            self.switch_focus()
            return True
        elif key == 13:  # Enter
            self.register(None)
            return True
        return False

    def switch_focus(self):
        self.current_field_index = (self.current_field_index + 1) % len(self.fields)
        self.fields[self.current_field_index].focus = True

    def save_account(self):
        self.account = Account(self.userName.text)
        with open("account_data.pkl", "wb") as file:
            pickle.dump(self.account, file)

    def register(self, obj):
        """Triggered when user presses 'Login'."""
        username_input = self.userName.text.strip()

        # Check if the username is 'user' (case-insensitive)
        if username_input.lower() == 'user':
            self.dialog = MDDialog(
                text="Username cannot be 'user'. Please choose a different one.",
                padding=50,
                size_hint=(0.5, 1),
                buttons=[
                    MDRaisedButton(text="DISCARD", padding=10, on_release=self.close_dialog),
                ]
            )
            self.dialog.open()
            return  # Prevent further execution

        # Proceed if the username is not 'user'
        if username_input != "":
            self.save_account()
            if self.manager and "bottom_nav" in self.manager.screen_names:
                self.manager.current = "bottom_nav"
            else:
                print("Error: 'bottom_nav' screen not found in ScreenManager.")
        else:
            self.dialog = MDDialog(
                text="Username cannot be empty.",
                padding=50,
                size_hint=(0.5, 1),
                buttons=[
                    MDRaisedButton(text="DISCARD", padding=10, on_release=self.close_dialog),
                ]
            )
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
