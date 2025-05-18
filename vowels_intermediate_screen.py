
from kivymd.uix.label import MDLabel
import pickle
import cv2
import numpy as np
import mediapipe as mp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.progressbar import MDProgressBar

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.app import MDApp

# Load model once
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
            font_style="H4",  # You can change to "H3" or "H5" depending on size preference
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

    def go_to_next_screen(*args):
        app = MDApp.get_running_app()
        app.sm.current = 'vowel_first_intermediate_screen'

class FirstScreenVowelIntermediate(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dialog_shown = False
        self.failed = False
        self.countdown = 5
        self.countdown_event = None

        self.capture = None
        self.event = None

        self.layout = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=[0, 0, 0, 0],
            size_hint=(None, None),
            size=(400, 550),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.image = Image(size_hint=(None, None), width=200, height=200)
        self.gif_image = AsyncImage(
            source='assets/hands/letterI.PNG',
            allow_stretch=True,
            size_hint=(None, None),
            width=200,
            height=200
        )

        self.label = Label(text="Detecting...", font_size=20)
        self.countdown_label = Label(text="Time left: 5s", font_size=16)
        self.progress_bar = MDProgressBar(value=100, max=100)

        side_by_side_layout = BoxLayout(
            orientation='horizontal',
            spacing=5,
            size_hint=(1, None),
            height=200
        )
        side_by_side_layout.add_widget(self.image)
        side_by_side_layout.add_widget(self.gif_image)

        self.layout.add_widget(side_by_side_layout)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.countdown_label)
        self.layout.add_widget(self.progress_bar)
        self.layout.add_widget(MDRaisedButton(
            text='Back to Menu',
            md_bg_color='gray',
            on_release=self.go_back
        ))

        self.add_widget(self.layout)

    def on_enter(self, *args):
        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.update, 1.0 / 30.0)

        self.countdown = 5
        self.failed = False
        self.dialog_shown = False
        self.countdown_event = Clock.schedule_interval(self.update_countdown, 1)

    def on_leave(self, *args):
        if self.capture:
            self.capture.release()
            self.capture = None
        if self.event:
            Clock.unschedule(self.event)
            self.event = None
        if self.countdown_event:
            Clock.unschedule(self.countdown_event)
            self.countdown_event = None

    def update(self, dt):
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

                    if idx == 2 and confidence >= 0.7:
                        prediction_text = "Correct gesture detected!"
                        if self.countdown_event:
                            Clock.unschedule(self.countdown_event)
                            self.countdown_event = None
                        self.show_success_dialog()
                        return
                    else:
                        prediction_text = "Gesture incorrect"
                except:
                    prediction_text = "Prediction error"

        self.label.text = prediction_text

        frame = cv2.flip(frame, 0)
        buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = img_texture

    def update_countdown(self, dt):
        if self.countdown <= 0:
            Clock.unschedule(self.countdown_event)
            self.countdown_event = None
            self.progress_bar.value = 0
            self.countdown_label.text = "Time left: 0s"
            if not self.dialog_shown and not self.failed:
                self.failed = True
                self.show_failure_dialog()
            return

        self.countdown_label.text = f"Time left: {self.countdown}s"
        self.progress_bar.value = (self.countdown / 5) * 100
        self.countdown -= 1

    def show_success_dialog(self):
        if self.dialog_shown:
            return

        self.dialog_shown = True
        if not hasattr(self, 'dialog') or not self.dialog:
            self.dialog = MDDialog(
                title="🎉 Congratulations! 🎉",
                text="You did an amazing job!",
                radius=[20, 7, 20, 7],
                buttons=[
                    MDRaisedButton(
                        text="Thank you!",
                        on_release=lambda x: (self.dialog.dismiss(), self.go_back())
                    )
                ],
            )
        with open("account_data.pkl", "rb") as file:
            account = pickle.load(file)
        # account.iStatus = True  # Optional status flag
        with open("account_data.pkl", "wb") as file:
            pickle.dump(account, file)

        self.dialog.open()

    def show_failure_dialog(self):
        self.dialog_shown = True
        self.dialog = MDDialog(
            title="❌ You Failed",
            text="Time's up and the correct gesture wasn't detected.",
            radius=[20, 7, 20, 7],
            buttons=[
                MDRaisedButton(
                    text="Try Again",
                    on_release=lambda x: (self.dialog.dismiss(), self.go_back())
                )
            ],
        )
        self.dialog.open()

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openChallenges()
