from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from helpers import *
from kivy.core.window import Window

userNameSample = "username"
passwordSample = "password"

class LoginScreen (MDScreen):
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
        self.password = Builder.load_string(password_helper)
        self.fields = [self.userName, self.password]

        loginButton = MDRaisedButton(
            text= 'Login',
            md_bg_color= 'gray',
            on_release=self.login
        )

        layout.add_widget(self.userName)
        layout.add_widget(self.password)
        layout.add_widget(loginButton)

        self.add_widget(layout)
        self.current_field_index = 0

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 9:  # Tab key
            self.switch_focus()
            return True
        elif key == 13:  # Enter key
            self.login(None)
            return True

    def switch_focus(self):
        self.current_field_index = (self.current_field_index + 1) % len(self.fields)
        self.fields[self.current_field_index].focus = True


    #if correct
    def login(self, obj):
        self.dialog = MDDialog(
            text="Incorrect username or password",
            padding=50,
            size_hint=(0.5, 1),
            buttons=[
                 MDRaisedButton(text="DISCARD", padding=10, on_release=self.close_dialog),
            ]
        )
        if self.userName.text == userNameSample and self.password.text == passwordSample:
            print("korak")
            self.parent.current = "bottom_nav"
        else:
            self.dialog.open()
    
    def close_dialog(self, obj):
        self.dialog.dismiss()