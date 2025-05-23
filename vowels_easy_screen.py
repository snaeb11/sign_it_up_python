import pickle

from flatbuffers import Builder
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.uix.image import Image, AsyncImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
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
        app.sm.current = 'vowels_easy_instruction'

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openChallenges()

#Instruction--------------------------------------------------------------------
class EasyInstructionScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = MDBoxLayout(
            orientation='vertical',
            padding=40,
            spacing=20,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(None, None),
            size=("500dp", "300dp")
        )

        self.title_label = MDLabel(
            text="Easy Challenge",
            halign="center",
            theme_text_color="Primary",
            font_style="H4",
            size_hint_y=None,
            height="50dp"
        )

        self.instruction_label = MDLabel(
            text="In order to complete this challenge, you must enter the correct letter of the displayed hand gesture. This must be done to all the letters — one wrong answer and all is lost.",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height="120dp",
        )

        self.button = MDRaisedButton(
            text="Start Challenge",
            pos_hint={'center_x': 0.5},
            on_release=self.go_to_next_screen
        )

        layout.add_widget(self.title_label)
        layout.add_widget(self.instruction_label)
        layout.add_widget(self.button)

        self.add_widget(layout)

    def go_to_next_screen(*args):
        app = MDApp.get_running_app()
        app.sm.current = 'first_screen_easy'

#First Screen --------------------------------------------------------------------
class FirstScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

        # Initialize sound effects
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'correct_answer': SoundLoader.load('assets/sounds/correct.mp3'),
            'wrong_answer': SoundLoader.load('assets/sounds/wrong.mp3')
        }

        # Main container for vertical centering
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint=(1, 1)
        )

        # Top spacer to help with centering
        top_spacer = MDBoxLayout(size_hint_y=None, height=0)

        # Content container (this will be centered)
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[0, 0, 0, 0],
            size_hint=(None, None),
            size=(dp(300), dp(400)),  # Increased height to accommodate all elements
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Bottom spacer to help with centering
        bottom_spacer = MDBoxLayout(size_hint_y=None, height=0)

        self.answerInput = Builder.load_string(vowels_easy_input)

        self.gif_image = AsyncImage(
            source='assets/hands/letterE.PNG',
            allow_stretch=True,
            size_hint=(None, None),
            width=dp(200),
            height=dp(200),
            pos_hint={'center_x': 0.5},
            anim_delay=0.05
        )

        self.submitButton = MDRaisedButton(
            text='Submit answer',
            md_bg_color='gray',
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.submitButton.bind(on_release=self.submit_first)

        # Add widgets to content layout
        content_layout.add_widget(self.gif_image)
        content_layout.add_widget(self.answerInput)
        content_layout.add_widget(self.submitButton)

        # Add to main layout
        main_layout.add_widget(top_spacer)
        main_layout.add_widget(content_layout)
        main_layout.add_widget(bottom_spacer)

        # Function to maintain centering when screen size changes
        def update_spacers(*args):
            screen_height = self.height
            content_height = content_layout.height
            remaining_space = max(0, (screen_height - content_height) / 2)
            top_spacer.height = remaining_space
            bottom_spacer.height = remaining_space

        self.bind(height=update_spacers)
        update_spacers()  # Initial call

        self.add_widget(main_layout)

    def on_enter(self):
        """Update sound volumes when screen becomes active"""
        for sound in self.sfx.values():
            if sound:
                sound.volume = self.app.sfx_volume

    def play_sfx(self, sound_name):
        """Helper method to play SFX with current volume"""
        if sound_name in self.sfx and self.sfx[sound_name]:
            self.sfx[sound_name].volume = self.app.sfx_volume
            self.sfx[sound_name].play()

    def submit_first(self, obj):
        # Play button click sound
        self.play_sfx('button_click')

        answer = self.answerInput.text.strip()
        self.answerInput.text = ''

        if answer.lower() == 'e':
            # Play correct answer sound
            self.play_sfx('correct_answer')

            def go_to_next_screen(*args):
                correct_dialog.dismiss()
                self.app.sm.current = 'second_screen_easy'

            correct_dialog = MDDialog(
                title="Correct!",
                text="Great job! You got it right.",
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Continue",
                        on_release=lambda x: (self.play_sfx('button_click'), go_to_next_screen())
                    )
                ]
            )
            correct_dialog.open()
        else:
            # Play wrong answer sound
            self.play_sfx('wrong_answer')

            def dismiss_wrong_dialog(*args):
                wrong_dialog.dismiss()
                self.app.sm.current = 'challenges_menu'

            wrong_dialog = MDDialog(
                title="Incorrect",
                text="Oops! Try again.",
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Try Again",
                        on_release=lambda x: (self.play_sfx('button_click'), dismiss_wrong_dialog())
                    )
                ]
            )
            wrong_dialog.open()

#Second Screen --------------------------------------------------------------------
class SecondScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

        # Initialize sound effects
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'correct_answer': SoundLoader.load('assets/sounds/correct.mp3'),
            'wrong_answer': SoundLoader.load('assets/sounds/wrong.mp3')
        }

        # Main container for vertical centering
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint=(1, 1)
        )

        # Top spacer to help with centering
        top_spacer = MDBoxLayout(size_hint_y=None, height=0)

        # Content container (this will be centered)
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[0, 0, 0, 0],
            size_hint=(None, None),
            size=(dp(300), dp(400)),  # Increased height to accommodate all elements
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Bottom spacer to help with centering
        bottom_spacer = MDBoxLayout(size_hint_y=None, height=0)

        self.answerInput = Builder.load_string(vowels_easy_input)

        self.gif_image = AsyncImage(
            source='assets/hands/letterU.png',
            allow_stretch=True,
            size_hint=(None, None),
            width=dp(200),
            height=dp(200),
            pos_hint={'center_x': 0.5},
            anim_delay=0.05
        )

        self.submitButton = MDRaisedButton(
            text='Submit Answer',
            md_bg_color='gray',
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.submitButton.bind(on_release=self.submit_first)

        # Add widgets to content layout
        content_layout.add_widget(self.gif_image)
        content_layout.add_widget(self.answerInput)
        content_layout.add_widget(self.submitButton)

        # Add to main layout
        main_layout.add_widget(top_spacer)
        main_layout.add_widget(content_layout)
        main_layout.add_widget(bottom_spacer)

        # Function to maintain centering when screen size changes
        def update_spacers(*args):
            screen_height = self.height
            content_height = content_layout.height
            remaining_space = max(0, (screen_height - content_height) / 2)
            top_spacer.height = remaining_space
            bottom_spacer.height = remaining_space

        self.bind(height=update_spacers)
        update_spacers()  # Initial call

        self.add_widget(main_layout)

    def on_enter(self):
        """Update sound volumes when screen becomes active"""
        for sound in self.sfx.values():
            if sound:
                sound.volume = self.app.sfx_volume

    def play_sfx(self, sound_name):
        """Helper method to play SFX with current volume"""
        if sound_name in self.sfx and self.sfx[sound_name]:
            self.sfx[sound_name].volume = self.app.sfx_volume
            self.sfx[sound_name].play()

    def submit_first(self, obj):
        # Play button click sound
        self.play_sfx('button_click')

        answer = self.answerInput.text.strip()
        self.answerInput.text = ''

        if answer.lower() == 'u':
            # Play correct answer sound
            self.play_sfx('correct_answer')

            def go_to_next_screen(*args):
                correct_dialog.dismiss()
                self.app.sm.current = 'third_screen_easy'

            correct_dialog = MDDialog(
                title="Correct!",
                text="Great job! You got it right.",
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Continue",
                        on_release=lambda x: (self.play_sfx('button_click'), go_to_next_screen())
                    )
                ]
            )
            correct_dialog.open()
        else:
            # Play wrong answer sound
            self.play_sfx('wrong_answer')

            def dismiss_wrong_dialog(*args):
                wrong_dialog.dismiss()
                self.app.sm.current = 'challenges_menu'

            wrong_dialog = MDDialog(
                title="Incorrect",
                text="Oops! Try again.",
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Try Again",
                        on_release=lambda x: (self.play_sfx('button_click'), dismiss_wrong_dialog())
                    )
                ]
            )
            wrong_dialog.open()

#Third Screen--------------------------------------------------------------------
class ThirdScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

        # Initialize sound effects
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'correct_answer': SoundLoader.load('assets/sounds/correct.mp3'),
            'wrong_answer': SoundLoader.load('assets/sounds/wrong.mp3')
        }

        # Main container for vertical centering
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint=(1, 1)
        )

        # Top spacer to help with centering
        top_spacer = MDBoxLayout(size_hint_y=None, height=0)

        # Content container (this will be centered)
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[0, 0, 0, 0],
            size_hint=(None, None),
            size=(dp(300), dp(400)),  # Increased height to accommodate all elements
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Bottom spacer to help with centering
        bottom_spacer = MDBoxLayout(size_hint_y=None, height=0)

        self.answerInput = Builder.load_string(vowels_easy_input)

        self.gif_image = AsyncImage(
            source='assets/hands/letterA.png',
            allow_stretch=True,
            size_hint=(None, None),
            width=dp(200),
            height=dp(200),
            pos_hint={'center_x': 0.5},
            anim_delay=0.05
        )

        self.submitButton = MDRaisedButton(
            text='Submit Answer',
            md_bg_color='gray',
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.submitButton.bind(on_release=self.submit_first)

        # Add widgets to content layout
        content_layout.add_widget(self.gif_image)
        content_layout.add_widget(self.answerInput)
        content_layout.add_widget(self.submitButton)

        # Add to main layout
        main_layout.add_widget(top_spacer)
        main_layout.add_widget(content_layout)
        main_layout.add_widget(bottom_spacer)

        # Function to maintain centering when screen size changes
        def update_spacers(*args):
            screen_height = self.height
            content_height = content_layout.height
            remaining_space = max(0, (screen_height - content_height) / 2)
            top_spacer.height = remaining_space
            bottom_spacer.height = remaining_space

        self.bind(height=update_spacers)
        update_spacers()  # Initial call

        self.add_widget(main_layout)

    def on_enter(self):
        """Update sound volumes when screen becomes active"""
        for sound in self.sfx.values():
            if sound:
                sound.volume = self.app.sfx_volume

    def play_sfx(self, sound_name):
        """Helper method to play SFX with current volume"""
        if sound_name in self.sfx and self.sfx[sound_name]:
            self.sfx[sound_name].volume = self.app.sfx_volume
            self.sfx[sound_name].play()

    def submit_first(self, obj):
        # Play button click sound
        self.play_sfx('button_click')

        answer = self.answerInput.text.strip()
        self.answerInput.text = ''

        if answer.lower() == 'a':
            # Play correct answer sound
            self.play_sfx('correct_answer')

            def go_to_next_screen(*args):
                correct_dialog.dismiss()
                self.app.sm.current = 'fourth_screen_easy'

            correct_dialog = MDDialog(
                title="Correct!",
                text="Great job! You got it right.",
                auto_dismiss=False,  # Prevent closing by clicking outside
                buttons=[
                    MDRaisedButton(
                        text="Continue",
                        on_release=lambda x: (self.play_sfx('button_click'), go_to_next_screen())
                    )
                ]
            )
            correct_dialog.open()
        else:
            # Play wrong answer sound
            self.play_sfx('wrong_answer')

            def dismiss_wrong_dialog(*args):
                wrong_dialog.dismiss()
                self.app.sm.current = 'challenges_menu'

            wrong_dialog = MDDialog(
                title="Incorrect",
                text="Oops! Try again.",
                auto_dismiss=False,  # Prevent closing by clicking outside
                buttons=[
                    MDRaisedButton(
                        text="Try Again",
                        on_release=lambda x: (self.play_sfx('button_click'), dismiss_wrong_dialog())
                    )
                ]
            )
            wrong_dialog.open()

#Fourth Screen --------------------------------------------------------------------
class FourthScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

        # Initialize sound effects
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'correct_answer': SoundLoader.load('assets/sounds/correct.mp3'),
            'wrong_answer': SoundLoader.load('assets/sounds/wrong.mp3')
        }

        # Main container for vertical centering
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint=(1, 1)
        )

        # Top spacer to help with centering
        top_spacer = MDBoxLayout(size_hint_y=None, height=0)

        # Content container (this will be centered)
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[0, 0, 0, 0],
            size_hint=(None, None),
            size=(dp(300), dp(400)),  # Increased height to accommodate all elements
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Bottom spacer to help with centering
        bottom_spacer = MDBoxLayout(size_hint_y=None, height=0)

        self.answerInput = Builder.load_string(vowels_easy_input)

        self.gif_image = AsyncImage(
            source='assets/hands/letterI.png',
            allow_stretch=True,
            size_hint=(None, None),
            width=dp(200),
            height=dp(200),
            pos_hint={'center_x': 0.5},
            anim_delay=0.05
        )

        self.submitButton = MDRaisedButton(
            text='Submit Answer',  # Changed for consistency
            md_bg_color='gray',
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.submitButton.bind(on_release=self.submit_first)

        # Add widgets to content layout
        content_layout.add_widget(self.gif_image)
        content_layout.add_widget(self.answerInput)
        content_layout.add_widget(self.submitButton)

        # Add to main layout
        main_layout.add_widget(top_spacer)
        main_layout.add_widget(content_layout)
        main_layout.add_widget(bottom_spacer)

        # Function to maintain centering when screen size changes
        def update_spacers(*args):
            screen_height = self.height
            content_height = content_layout.height
            remaining_space = max(0, (screen_height - content_height) / 2)
            top_spacer.height = remaining_space
            bottom_spacer.height = remaining_space

        self.bind(height=update_spacers)
        update_spacers()  # Initial call

        self.add_widget(main_layout)

    def on_enter(self):
        """Update sound volumes when screen becomes active"""
        for sound in self.sfx.values():
            if sound:
                sound.volume = self.app.sfx_volume

    def play_sfx(self, sound_name):
        """Helper method to play SFX with current volume"""
        if sound_name in self.sfx and self.sfx[sound_name]:
            self.sfx[sound_name].volume = self.app.sfx_volume
            self.sfx[sound_name].play()

    def submit_first(self, obj):
        # Play button click sound
        self.play_sfx('button_click')

        answer = self.answerInput.text.strip()
        self.answerInput.text = ''

        if answer.lower() == 'i':
            # Play correct answer sound
            self.play_sfx('correct_answer')

            def go_to_next_screen(*args):
                correct_dialog.dismiss()
                self.app.sm.current = 'fifth_screen_easy'

            correct_dialog = MDDialog(
                title="Correct!",
                text="Great job! You got it right.",
                auto_dismiss=False,  # Prevent closing by clicking outside
                buttons=[
                    MDRaisedButton(
                        text="Continue",
                        on_release=lambda x: (self.play_sfx('button_click'), go_to_next_screen())
                    )
                ]
            )
            correct_dialog.open()
        else:
            # Play wrong answer sound
            self.play_sfx('wrong_answer')

            def dismiss_wrong_dialog(*args):
                wrong_dialog.dismiss()
                self.app.sm.current = 'challenges_menu'

            wrong_dialog = MDDialog(
                title="Incorrect",
                text="Oops! Try again.",
                auto_dismiss=False,  # Prevent closing by clicking outside
                buttons=[
                    MDRaisedButton(
                        text="Try Again",
                        on_release=lambda x: (self.play_sfx('button_click'), dismiss_wrong_dialog())
                    )
                ]
            )
            wrong_dialog.open()

#Fifth Screen --------------------------------------------------------------------
class FifthScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

        # Initialize sound effects
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'correct_answer': SoundLoader.load('assets/sounds/correct.mp3'),
            'wrong_answer': SoundLoader.load('assets/sounds/wrong.mp3'),
            'completion': SoundLoader.load('assets/sounds/levelwin2.mp3'),
            'achievement': SoundLoader.load('assets/sounds/achievementunlock2.mp3')
        }

        # Main container for vertical centering
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint=(1, 1)
        )

        # Content container
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[0, 0, 0, 0],
            size_hint=(None, None),
            size=(dp(300), dp(400)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Add spacers for vertical centering
        top_spacer = MDBoxLayout(size_hint_y=None, height=0)
        bottom_spacer = MDBoxLayout(size_hint_y=None, height=0)

        self.answerInput = Builder.load_string(vowels_easy_input)

        self.gif_image = AsyncImage(
            source='assets/hands/letterO.png',
            allow_stretch=True,
            size_hint=(None, None),
            width=dp(200),
            height=dp(200),
            pos_hint={'center_x': 0.5},
            anim_delay=0.05
        )

        self.submitButton = MDRaisedButton(
            text='Submit Answer',
            md_bg_color='gray',
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.submitButton.bind(on_release=self.submit_first)

        # Add widgets to content layout
        content_layout.add_widget(self.gif_image)
        content_layout.add_widget(self.answerInput)
        content_layout.add_widget(self.submitButton)

        # Add to main layout
        main_layout.add_widget(top_spacer)
        main_layout.add_widget(content_layout)
        main_layout.add_widget(bottom_spacer)

        # Function to maintain centering when screen size changes
        def update_spacers(*args):
            remaining = max(0, (self.height - content_layout.height) / 2)
            top_spacer.height = remaining
            bottom_spacer.height = remaining

        self.bind(height=update_spacers)
        update_spacers()

        self.add_widget(main_layout)

    def on_enter(self):
        """Update sound volumes when screen becomes active"""
        for sound in self.sfx.values():
            if sound:
                sound.volume = self.app.sfx_volume

    def play_sfx(self, sound_name):
        """Helper method to play SFX with current volume"""
        if sound_name in self.sfx and self.sfx[sound_name]:
            self.sfx[sound_name].volume = self.app.sfx_volume
            self.sfx[sound_name].play()

    def submit_first(self, obj):
        # Play button click sound
        self.play_sfx('button_click')

        answer = self.answerInput.text.strip()
        self.answerInput.text = ''

        if answer.lower() == 'o':
            self.play_sfx('correct_answer')

            # First show the correct answer dialog
            def show_challenge_complete(*args):
                correct_dialog.dismiss()

                # Load account data and check if first completion
                with open("account_data.pkl", "rb") as file:
                    account = pickle.load(file)
                first_completion = not account.easyChallenge
                account.easyChallenge = True

                # Save updated account data
                with open("account_data.pkl", "wb") as file:
                    pickle.dump(account, file)

                # Play completion sound
                self.play_sfx('completion')

                # Show challenge complete dialog
                complete_dialog = MDDialog(
                    title="Challenge Complete!",
                    text="You've mastered all the vowels in the Easy Challenge!",
                    radius=[20, 7, 20, 7],
                    auto_dismiss=False,
                    buttons=[
                        MDRaisedButton(
                            text="Continue",
                            on_release=lambda x: (
                                self.play_sfx('button_click'),
                                complete_dialog.dismiss(),
                                self.show_achievement(first_completion) if first_completion else
                                self.go_to_challenges_menu()
                            )
                        )
                    ]
                )
                complete_dialog.open()

            correct_dialog = MDDialog(
                title="Correct!",
                text="Great job! You got the last vowel right!",
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Continue",
                        on_release=lambda x: (
                            self.play_sfx('button_click'),
                            show_challenge_complete()
                        )
                    )
                ]
            )
            correct_dialog.open()
        else:
            self.play_sfx('wrong_answer')
            wrong_dialog = MDDialog(
                title="Incorrect",
                text="Oops! That's not the right letter. Try again!",
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Try Again",
                        on_release=lambda x: (
                            self.play_sfx('button_click'),
                            wrong_dialog.dismiss()
                        )
                    )
                ]
            )
            wrong_dialog.open()

    def show_achievement(self, first_completion):
        if first_completion:
            self.play_sfx('achievement')
            achievement_dialog = MDDialog(
                title="Achievement Unlocked!",
                text="First Time Completion: Easy Vowels Challenge!",
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Awesome!",
                        on_release=lambda x: (
                            self.play_sfx('button_click'),
                            achievement_dialog.dismiss(),
                            self.go_to_challenges_menu()
                        )
                    )
                ]
            )
            achievement_dialog.open()

    def go_to_challenges_menu(self):
        self.app.sm.current = 'challenges_menu'