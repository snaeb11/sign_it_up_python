import pickle
import cv2
import mediapipe as mp
import numpy as np
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp

# --- Load model and MediaPipe once ---
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# --- IntroScreen class ---
class IntroScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.capture = None
        self.event = None
        self.gesture_timer_event = None
        self.gesture_hold_time = 0

        scroll = MDScrollView(size_hint=(1, 1))

        self.layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(20),
            size_hint_y=None,
        )
        self.layout.bind(minimum_height=self.layout.setter('height'))

        # Title
        self.layout.add_widget(MDLabel(
            text="Sing-it-Up: Learn Filipino Sign Language Through Play",
            theme_text_color="Primary",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        ))

        # Introduction paragraph
        self.layout.add_widget(MDLabel(
            text="Sing-it-Up is a fun and interactive mobile game designed to help users learn Filipino Sign Language (FSL) in an exciting and engaging way! "
                 "Using your phone’s camera, the game detects and evaluates your hand gestures in real time. Your goal? Match the correct sign for letters and basic words to move through each level and improve your skills.",
            theme_text_color="Secondary",
            halign="left",
            size_hint_y=None,
            height=dp(120),
            text_size=(dp(300), None),
        ))

        # Section: What You’ll Learn
        self.layout.add_widget(MDLabel(
            text="What You’ll Learn and Experience",
            theme_text_color="Primary",
            font_style="H6",
            halign="left",
            size_hint_y=None,
            height=dp(30),
        ))
        self.layout.add_widget(MDLabel(
            text="- Sign language basics using hand gesture recognition\n"
                 "- Real-time feedback as you play and learn\n"
                 "- A progress tracker to keep you motivated\n"
                 "- Visual and animated guides for each sign",
            theme_text_color="Secondary",
            halign="left",
            size_hint_y=None,
            height=dp(100),
            text_size=(dp(300), None),
        ))

        # Section: How It Works
        self.layout.add_widget(MDLabel(
            text="How It Works",
            theme_text_color="Primary",
            font_style="H6",
            halign="left",
            size_hint_y=None,
            height=dp(30),
        ))
        self.layout.add_widget(MDLabel(
            text="1. Look at the screen and mimic the hand gesture shown below the camera view.\n"
                 "2. Hold the gesture steady for 3 seconds.\n"
                 "3. That’s it—your gesture will be detected and confirmed automatically!",
            theme_text_color="Secondary",
            halign="left",
            size_hint_y=None,
            height=dp(100),
            text_size=(dp(300), None),
        ))

        # Section: Technologies Used
        self.layout.add_widget(MDLabel(
            text="Technologies Used",
            theme_text_color="Primary",
            font_style="H6",
            halign="left",
            size_hint_y=None,
            height=dp(30),
        ))
        self.layout.add_widget(MDLabel(
            text="- Python\n- OpenCV and MediaPipe for hand tracking\n- NumPy for efficient data handling",
            theme_text_color="Secondary",
            halign="left",
            size_hint_y=None,
            height=dp(80),
            text_size=(dp(300), None),
        ))

        # Section: Why Sing-it-Up?
        self.layout.add_widget(MDLabel(
            text="Why Sing-it-Up?",
            theme_text_color="Primary",
            font_style="H6",
            halign="left",
            size_hint_y=None,
            height=dp(30),
        ))
        self.layout.add_widget(MDLabel(
            text="We created this game to make learning sign language more inclusive, accessible, and fun—especially for the deaf and hard-of-hearing community, and anyone who wants to communicate better using FSL. It's a modern take on language learning that turns education into a game.",
            theme_text_color="Secondary",
            halign="left",
            size_hint_y=None,
            height=dp(120),
            text_size=(dp(300), None),
        ))

        # Camera preview
        self.image = Image(size_hint_y=None, height=300)
        self.layout.add_widget(self.image)

        # Prediction label
        self.label = MDLabel(
            text="Waiting for input...",
            theme_text_color="Secondary",
            halign="center",
            size_hint_y=None,
            height=dp(30),
        )
        self.layout.add_widget(self.label)

        # Start button
        self.layout.add_widget(MDRaisedButton(
            text='Start Playing!',
            pos_hint={'center_x': 0.5}
        ))

        scroll.add_widget(self.layout)
        self.add_widget(scroll)

    def on_enter(self):
        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.update, 1.0 / 30.0)

    def on_leave(self):
        if self.capture:
            self.capture.release()
            self.capture = None
        if self.event:
            Clock.unschedule(self.event)
            self.event = None
        self.reset_gesture_timer()

    def update(self, dt):
        if not self.capture:
            return

        ret, frame = self.capture.read()
        if not ret:
            return

        data_aux = []
        x_, y_ = [], []
        H, W, _ = frame.shape

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

                    if idx == 5 and confidence >= 0.7:
                        prediction_text = "OKKKKKKKKKKKKKKK"
                        if not self.gesture_timer_event:
                            self.gesture_hold_time = 0
                            self.gesture_timer_event = Clock.schedule_interval(self.update_gesture_timer, 0.1)
                    else:
                        prediction_text = "Gesture incorrect"
                        self.reset_gesture_timer()
                except:
                    prediction_text = "Prediction error"
                    self.reset_gesture_timer()

        if prediction_text == "No hand detected":
            self.reset_gesture_timer()

        self.label.text = prediction_text

        frame = cv2.flip(frame, 0)
        buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = texture

    def update_gesture_timer(self, dt):
        self.gesture_hold_time += dt
        if self.gesture_hold_time >= 3:
            self.label.text = "Gesture confirmed! 🎉"
            self.reset_gesture_timer()
            # You can add screen change or dialog here

    def reset_gesture_timer(self):
        self.gesture_hold_time = 0
        if self.gesture_timer_event:
            Clock.unschedule(self.gesture_timer_event)
            self.gesture_timer_event = None
