import pickle

from flatbuffers import Builder
from kivy.uix.image import Image, AsyncImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.app import MDApp

from helpers import vowels_easy_input


# --- class ---
class VowelsEasyChallengeScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        app.sm.current = 'first_screen'

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openChallenges()

class FirstScreen(MDScreen):
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

        self.answerInput = Builder.load_string(vowels_easy_input)

        self.gif_image = AsyncImage(
            source='assets/hands/letterE.PNG',
            allow_stretch=True,
            size_hint=(None, None),
            width=200,
            height=200,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            anim_delay=0.05
        )

        self.submitButton = MDRaisedButton(
            text='Submit answer',
            md_bg_color='gray',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_release=self.submit_first
        )

        layout.add_widget(self.gif_image)
        layout.add_widget(self.answerInput)
        layout.add_widget(self.submitButton)

        self.add_widget(layout)


    def submit_first(self, obj):
        answer = self.answerInput.text.strip()
        if answer.lower() == 'e':
            print("korek")

            def go_to_next_screen(*args):
                correct_dialog.dismiss()
                app = MDApp.get_running_app()
                app.sm.current = 'second_screen'

            correct_dialog = MDDialog(
                title="Correct!",
                text="Great job! You got it right.",
                buttons=[
                    MDRaisedButton(
                        text="Continue",
                        on_release=go_to_next_screen
                    )
                ]
            )
            correct_dialog.open()
        else:
            print("wrong")

            def dismiss_wrong_dialog(*args):
                wrong_dialog.dismiss()

            wrong_dialog = MDDialog(
                title="❌ Incorrect",
                text="Oops! Try again.",
                buttons=[
                    MDRaisedButton(
                        text="Try Again",
                        on_release=dismiss_wrong_dialog
                    )
                ]
            )
            wrong_dialog.open()

class SecondScreen(MDScreen):
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

        self.answerInput = Builder.load_string(vowels_easy_input)

        self.gif_image = AsyncImage(
            source='assets/hands/letterU.png',
            allow_stretch=True,
            size_hint=(None, None),
            width=200,
            height=200,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            anim_delay=0.05
        )

        self.submitButton = MDRaisedButton(
            text='Second Screen',
            md_bg_color='gray',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_release=self.submit_first
        )

        layout.add_widget(self.gif_image)
        layout.add_widget(self.answerInput)
        layout.add_widget(self.submitButton)

        self.add_widget(layout)


    def submit_first(self, obj):
        answer = self.answerInput.text.strip()
        if answer.lower() == 'u':
            print("korek")

            def go_to_next_screen(*args):
                correct_dialog.dismiss()
                app = MDApp.get_running_app()
                app.sm.current = 'third_screen'

            correct_dialog = MDDialog(
                title="Correct!",
                text="Great job! You got it right.",
                buttons=[
                    MDRaisedButton(
                        text="Continue",
                        on_release=go_to_next_screen
                    )
                ]
            )
            correct_dialog.open()
        else:
            print("wrong")

            def dismiss_wrong_dialog(*args):
                wrong_dialog.dismiss()

            wrong_dialog = MDDialog(
                title="❌ Incorrect",
                text="Oops! Try again.",
                buttons=[
                    MDRaisedButton(
                        text="Try Again",
                        on_release=dismiss_wrong_dialog
                    )
                ]
            )
            wrong_dialog.open()

class ThirdScreen(MDScreen):
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

        self.answerInput = Builder.load_string(vowels_easy_input)

        self.gif_image = AsyncImage(
            source='assets/hands/letterA.png',
            allow_stretch=True,
            size_hint=(None, None),
            width=200,
            height=200,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            anim_delay=0.05
        )

        self.submitButton = MDRaisedButton(
            text='Second Screen',
            md_bg_color='gray',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_release=self.submit_first
        )

        layout.add_widget(self.gif_image)
        layout.add_widget(self.answerInput)
        layout.add_widget(self.submitButton)

        self.add_widget(layout)


    def submit_first(self, obj):
        answer = self.answerInput.text.strip()
        if answer.lower() == 'a':
            print("korek")

            def go_to_next_screen(*args):
                correct_dialog.dismiss()
                app = MDApp.get_running_app()
                app.sm.current = 'fourth_screen'

            correct_dialog = MDDialog(
                title="Correct!",
                text="Great job! You got it right.",
                buttons=[
                    MDRaisedButton(
                        text="Continue",
                        on_release=go_to_next_screen
                    )
                ]
            )
            correct_dialog.open()
        else:
            print("wrong")

            def dismiss_wrong_dialog(*args):
                wrong_dialog.dismiss()

            wrong_dialog = MDDialog(
                title="❌ Incorrect",
                text="Oops! Try again.",
                buttons=[
                    MDRaisedButton(
                        text="Try Again",
                        on_release=dismiss_wrong_dialog
                    )
                ]
            )
            wrong_dialog.open()

class FourthScreen(MDScreen):
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

        self.answerInput = Builder.load_string(vowels_easy_input)

        self.gif_image = AsyncImage(
            source='assets/hands/letterI.png',
            allow_stretch=True,
            size_hint=(None, None),
            width=200,
            height=200,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            anim_delay=0.05
        )

        self.submitButton = MDRaisedButton(
            text='Second Screen',
            md_bg_color='gray',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_release=self.submit_first
        )

        layout.add_widget(self.gif_image)
        layout.add_widget(self.answerInput)
        layout.add_widget(self.submitButton)

        self.add_widget(layout)


    def submit_first(self, obj):
        answer = self.answerInput.text.strip()
        if answer.lower() == 'i':
            print("korek")

            def go_to_next_screen(*args):
                correct_dialog.dismiss()
                app = MDApp.get_running_app()
                app.sm.current = 'fifth_screen'

            correct_dialog = MDDialog(
                title="Correct!",
                text="Great job! You got it right.",
                buttons=[
                    MDRaisedButton(
                        text="Continue",
                        on_release=go_to_next_screen
                    )
                ]
            )
            correct_dialog.open()
        else:
            print("wrong")

            def dismiss_wrong_dialog(*args):
                wrong_dialog.dismiss()

            wrong_dialog = MDDialog(
                title="❌ Incorrect",
                text="Oops! Try again.",
                buttons=[
                    MDRaisedButton(
                        text="Try Again",
                        on_release=dismiss_wrong_dialog
                    )
                ]
            )
            wrong_dialog.open()

class FifthScreen(MDScreen):
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

        self.answerInput = Builder.load_string(vowels_easy_input)

        self.gif_image = AsyncImage(
            source='assets/hands/letterO.png',
            allow_stretch=True,
            size_hint=(None, None),
            width=200,
            height=200,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            anim_delay=0.05
        )

        self.submitButton = MDRaisedButton(
            text='Second Screen',
            md_bg_color='gray',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_release=self.submit_first
        )

        layout.add_widget(self.gif_image)
        layout.add_widget(self.answerInput)
        layout.add_widget(self.submitButton)

        self.add_widget(layout)


    def submit_first(self, obj):
        answer = self.answerInput.text.strip()
        if answer.lower() == 'o':
            print("korek")

            def go_to_next_screen(*args):
                correct_dialog.dismiss()
                app = MDApp.get_running_app()
                app.sm.current = 'challenges_menu'

            correct_dialog = MDDialog(
                title="Correct!",
                text="Great job! You got it right.",
                buttons=[
                    MDRaisedButton(
                        text="Continue",
                        on_release=go_to_next_screen
                    )
                ]
            )
            correct_dialog.open()
            with open("account_data.pkl", "rb") as file:
                account = pickle.load(file)

            account.easyChallenge = True

            with open("account_data.pkl", "wb") as file:
                pickle.dump(account, file)
        else:
            print("wrong")

            def dismiss_wrong_dialog(*args):
                wrong_dialog.dismiss()

            wrong_dialog = MDDialog(
                title="❌ Incorrect",
                text="Oops! Try again.",
                buttons=[
                    MDRaisedButton(
                        text="Try Again",
                        on_release=dismiss_wrong_dialog
                    )
                ]
            )
            wrong_dialog.open()