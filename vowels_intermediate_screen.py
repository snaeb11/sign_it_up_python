import pickle
import cv2
import numpy as np
import mediapipe as mp
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
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.progressbar import MDProgressBar

# Load model once (moved to top level)
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Setup MediaPipe once
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)


class VowelsIntermediateChallengeScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        app.sm.current = 'vowels_intermediate_instruction'

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openChallenges()


class VowelsIntermediateInstructionScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3')
        }

        layout = MDBoxLayout(
            orientation='vertical',
            padding=40,
            spacing=20,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(None, None),
            size=("500dp", "300dp")
        )

        self.title_label = MDLabel(
            text="Intermediate Challenge",
            halign="center",
            theme_text_color="Primary",
            font_style="H4",
            size_hint_y=None,
            height="50dp"
        )

        self.instruction_label = MDLabel(
            text="One must do the proper hand sign of the displayed object within 5 seconds, if not all is lost.",
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

    def play_sfx(self, sound_name):
        """Helper method to play SFX with current volume"""
        app = MDApp.get_running_app()
        if sound_name in self.sfx and self.sfx[sound_name]:
            self.sfx[sound_name].volume = app.sfx_volume
            self.sfx[sound_name].play()

    def go_to_next_screen(self, *args):
        self.play_sfx('button_click')
        app = MDApp.get_running_app()
        app.sm.current = 'vowel_first_intermediate_screen'


class BaseIntermediateScreen(MDScreen):
    """Base class for all intermediate challenge screens with common functionality"""

    def __init__(self, target_letter_idx, image_source, next_screen, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_letter_idx = target_letter_idx
        self.image_source = image_source
        self.next_screen = next_screen
        self.countdown_duration = 5  # seconds
        self.countdown = self.countdown_duration

        # State variables
        self.dialog_shown = False
        self.failed = False
        self.countdown = 5
        self.countdown_event = None
        self.capture = None
        self.event = None

        # Sound effects
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'correct_answer': SoundLoader.load('assets/sounds/correct.mp3'),
            'wrong_answer': SoundLoader.load('assets/sounds/wrong.mp3'),
            'countdown_tick': SoundLoader.load('assets/sounds/counter.mp3')
        }

        self.setup_ui()

    def setup_ui(self):
        """Setup the common UI elements for all intermediate screens"""
        # Main container for vertical centering
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint=(1, 1)
        )

        # Content container (centered)
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[0, 0, 0, 0],
            size_hint=(None, None),
            size=(dp(400), dp(550)),  # Adjusted size to fit all elements
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Side-by-side layout for camera and example image
        side_by_side_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            size_hint=(1, None),
            height=dp(200)
        )

        # Camera feed
        self.camera_image = Image(
            size_hint=(None, None),
            width=dp(200),
            height=dp(200),
            allow_stretch=True
        )

        # Example image
        self.example_image = AsyncImage(
            source=self.image_source,
            allow_stretch=True,
            size_hint=(None, None),
            width=dp(200),
            height=dp(200),
            anim_delay=0.05
        )

        # Detection label
        self.detection_label = MDLabel(
            text="Detecting...",
            halign="center",
            theme_text_color="Primary",
            font_style="Body1"
        )

        # Countdown label
        self.countdown_label = MDLabel(
            text=f"Time left: {self.countdown}s",
            halign="center",
            theme_text_color="Primary"
        )

        # Progress bar
        self.progress_bar = MDProgressBar(
            value=100,
            max=100
        )

        # Back button
        self.back_button = MDRaisedButton(
            text='Back to Menu',
            md_bg_color='gray',
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            on_release=self.go_back
        )

        # Assemble the layout
        side_by_side_layout.add_widget(self.camera_image)
        side_by_side_layout.add_widget(self.example_image)

        content_layout.add_widget(side_by_side_layout)
        content_layout.add_widget(self.detection_label)
        content_layout.add_widget(self.countdown_label)
        content_layout.add_widget(self.progress_bar)
        content_layout.add_widget(self.back_button)

        # Add spacers for vertical centering
        top_spacer = MDBoxLayout(size_hint_y=None, height=0)
        bottom_spacer = MDBoxLayout(size_hint_y=None, height=0)

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

    def on_enter(self, *args):
        """Start camera and timers when screen becomes active"""
        app = MDApp.get_running_app()
        self.reset_state()
        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.update, 1.0 / 30.0)
        self.countdown_event = Clock.schedule_interval(self.update_countdown, 1)

        # Update sound volumes
        for sound in self.sfx.values():
            if sound:
                sound.volume = app.sfx_volume

    def on_leave(self, *args):
        """Ensure all resources are cleaned up when leaving screen"""
        self.go_back()  # This will handle all cleanup

    def reset_state(self):
        """Reset all state variables"""
        self.dialog_shown = False
        self.failed = False
        self.countdown = 5

        # Reset UI elements
        self.progress_bar.value = 100
        self.countdown_label.text = f"Time left: {self.countdown}s"
        self.detection_label.text = "Detecting..."

        # Dismiss any existing dialog
        if hasattr(self, 'dialog') and self.dialog and self.dialog.open:
            self.dialog.dismiss()
            self.dialog = None

    def play_sfx(self, sound_name):
        """Enhanced SFX playback with volume control and error handling"""
        app = MDApp.get_running_app()
        try:
            if sound_name in self.sfx and self.sfx[sound_name]:
                # Stop sound if already playing
                self.sfx[sound_name].stop()
                # Set current volume
                self.sfx[sound_name].volume = app.sfx_volume
                # Play sound
                self.sfx[sound_name].play()
        except Exception as e:
            print(f"Error playing sound {sound_name}: {e}")

    def update(self, dt):
        """Process camera frame and detect gestures"""
        if not self.capture:
            return

        ret, frame = self.capture.read()
        if not ret:
            return

        data_aux = []
        x_, y_ = [], []
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        prediction_text = "No hand detected"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                for lm in hand_landmarks.landmark:
                    x_.append(lm.x)
                    y_.append(lm.y)

                for lm in hand_landmarks.landmark:
                    data_aux.append(lm.x - min(x_))
                    data_aux.append(lm.y - min(y_))

                try:
                    proba = model.predict_proba([np.asarray(data_aux)])
                    confidence = np.max(proba)
                    idx = np.argmax(proba)

                    if idx == self.target_letter_idx and confidence >= 0.7:
                        prediction_text = "Correct gesture detected!"
                        if not self.dialog_shown:
                            self.play_sfx('correct_answer')
                            if self.countdown_event:
                                Clock.unschedule(self.countdown_event)
                                self.countdown_event = None
                            self.show_success_dialog()
                    else:
                        prediction_text = "Gesture incorrect"
                except Exception as e:
                    prediction_text = "Prediction error"

        self.detection_label.text = prediction_text

        # Update camera texture
        frame = cv2.flip(frame, 0)
        buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.camera_image.texture = img_texture

    def stop_all_sounds(self):
        """Stop all currently playing sound effects"""
        for sound in self.sfx.values():
            if sound:
                sound.stop()

    def update_countdown(self, dt):
        """Update the countdown timer with immediate SFX feedback"""
        if self.countdown <= 0:
            if self.countdown_event:
                Clock.unschedule(self.countdown_event)
                self.countdown_event = None
            self.progress_bar.value = 0
            self.countdown_label.text = "Time left: 0s"
            if not self.dialog_shown and not self.failed:
                self.failed = True
                self.play_sfx('wrong_answer')
                self.show_failure_dialog()
            return

        # Play tick sound for each countdown update
        if self.countdown <= 5:
            self.play_sfx('countdown_tick')

        self.countdown_label.text = f"Time left: {self.countdown}s"
        self.progress_bar.value = (self.countdown / self.countdown_duration) * 100
        self.countdown -= 1

    def show_success_dialog(self):
        """Show success dialog with proper countdown stopping"""
        if self.dialog_shown:
            return

        # Stop countdown immediately
        if self.countdown_event:
            Clock.unschedule(self.countdown_event)
            self.countdown_event = None

        self.dialog_shown = True
        self.play_sfx('correct_answer')

        def go_to_next_screen(*args):
            self.dialog.dismiss()
            app = MDApp.get_running_app()
            app.sm.current = self.next_screen

        self.dialog = MDDialog(
            title="Correct!",
            text="Great job! You got it right.",
            radius=[20, 7, 20, 7],
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="Continue",
                    on_release=lambda x: (self.play_sfx('button_click'), go_to_next_screen())
                )
            ],
        )
        self.dialog.open()

    def show_failure_dialog(self):
        """Show failure dialog with proper countdown stopping"""
        self.dialog_shown = True

        # Stop countdown if it wasn't already stopped
        if self.countdown_event:
            Clock.unschedule(self.countdown_event)
            self.countdown_event = None

        self.play_sfx('wrong_answer')

        def try_again(*args):
            self.dialog.dismiss()
            self.go_back()

        self.dialog = MDDialog(
            title="Time's Up!",
            text="You didn't make the gesture in time.",
            radius=[20, 7, 20, 7],
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="Try Again",
                    on_release=lambda x: (self.play_sfx('button_click'), try_again())
                )
            ],
        )
        self.dialog.open()

    def go_back(self, *args):
        """Return to challenges menu with sound and cleanup"""
        self.play_sfx('button_click')
        self.stop_all_sounds()

        # Schedule actual navigation after sound plays
        Clock.schedule_once(lambda dt: self._actual_go_back(), 0.1)

    def _actual_go_back(self):
        """Perform the actual cleanup and navigation"""
        if self.countdown_event:
            Clock.unschedule(self.countdown_event)
            self.countdown_event = None
        if self.capture:
            self.capture.release()
            self.capture = None
        if self.event:
            Clock.unschedule(self.event)
            self.event = None

        app = MDApp.get_running_app()
        app.openChallenges()


# Concrete screen implementations
class FirstScreenVowelIntermediate(BaseIntermediateScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(
            target_letter_idx=2,  # Letter I
            image_source='assets/challenges/inter/igloo.jpg',
            next_screen='vowel_second_intermediate_screen',
            *args, **kwargs
        )


class SecondScreenVowelIntermediate(BaseIntermediateScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(
            target_letter_idx=4,  # Letter U
            image_source='assets/challenges/inter/umbrella.jpg',
            next_screen='vowel_third_intermediate_screen',
            *args, **kwargs
        )


class ThirdScreenVowelIntermediate(BaseIntermediateScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(
            target_letter_idx=0,  # Letter A
            image_source='assets/challenges/inter/apple.jpg',
            next_screen='vowel_fourth_intermediate_screen',
            *args, **kwargs
        )


class FourthScreenVowelIntermediate(BaseIntermediateScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(
            target_letter_idx=3,  # Letter O
            image_source='assets/challenges/inter/ostrich.jpg',
            next_screen='vowel_fifth_intermediate_screen',
            *args, **kwargs
        )


class FifthScreenVowelIntermediate(BaseIntermediateScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(
            target_letter_idx=1,  # Letter E
            image_source='assets/challenges/inter/elephant.jpg',
            next_screen='challenges_menu',
            *args, **kwargs
        )

        # Add completion sound effects
        self.sfx['completion'] = SoundLoader.load('assets/sounds/levelwin2.mp3')
        self.sfx['achievement'] = SoundLoader.load('assets/sounds/achievementunlock2.mp3')

    def show_success_dialog(self):
        """Override to show completion dialog and handle achievements"""
        if self.dialog_shown:
            return

        self.dialog_shown = True

        def show_challenge_complete(*args):
            self.dialog.dismiss()

            # Load account data and check if first completion
            with open("account_data.pkl", "rb") as file:
                account = pickle.load(file)
            first_completion = not account.intermediateChallenge
            account.intermediateChallenge = True

            # Save updated account data
            with open("account_data.pkl", "wb") as file:
                pickle.dump(account, file)

            # Play completion sound
            self.play_sfx('completion')

            # Show challenge complete dialog
            complete_dialog = MDDialog(
                title="Challenge Complete!",
                text="You've mastered all the vowels in the Intermediate Challenge!",
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

        self.dialog = MDDialog(
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
        self.dialog.open()

    def show_achievement(self, first_completion):
        """Show achievement unlocked dialog if first completion"""
        if first_completion:
            self.play_sfx('achievement')
            achievement_dialog = MDDialog(
                title="Achievement Unlocked!",
                text="First Time Completion: Intermediate Vowels Challenge!",
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
        """Navigate back to challenges menu"""
        app = MDApp.get_running_app()
        app.openChallenges()