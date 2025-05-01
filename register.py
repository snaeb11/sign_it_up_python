from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from helpers import *
from kivy.core.window import Window
import pickle


class Account:
    def __init__(self, username: str):
        self.username = username

class RegisterScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        Window.bind(on_key_down=self.on_key_down)

        layout = MDBoxLayout(orientation='vertical',
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

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 9:  # Tab key
            self.switch_focus()
            return True
        elif key == 13:  # Enter key
            self.register(None)
            return True

    def switch_focus(self):
        self.current_field_index = (self.current_field_index + 1) % len(self.fields)
        self.fields[self.current_field_index].focus = True

    def save_account(self):
        account = Account(self.userName.text)
        with open("account_data.pkl", "wb") as file:
            pickle.dump(account, file)
        print(f"Account saved: {account.username}")

    # if correct
    def register(self, obj):
        self.dialog = MDDialog(
            text="Username cannot be empty.",
            padding=50,
            size_hint=(0.5, 1),
            buttons=[
                MDRaisedButton(text="DISCARD", padding=10, on_release=self.close_dialog),
            ]
        )
        if self.userName.text.strip() != "":
            print("Account registered with username:", self.userName.text)
            self.save_account()
            print('pickle rick')
            self.parent.current = "bottom_nav"
        else:
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()