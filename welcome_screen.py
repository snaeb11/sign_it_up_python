# welcome_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
import pickle
import os

class WelcomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.welcome_text = "Welcome"
        Clock.schedule_once(self.check_account, 0)

    def check_account(self, dt):
        if os.path.exists("account_data.pkl"):
            try:
                with open("account_data.pkl", "rb") as file:
                    account = pickle.load(file)

                    if account.username == "User":
                        self.manager.current = "register"
                    else:
                        self.manager.current = "bottom_nav"

            except Exception as e:
                print(f"Failed to load account: {e}")

        self.label = MDLabel(
            text=self.welcome_text,
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.add_widget(self.label)
