import pickle
import cv2
import mediapipe as mp
import numpy as np


from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.app import MDApp

# Load model once
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']
labels_dict = {0: 'A', 1: 'E', 2: 'I', 3: 'O', 4: 'U'}

# Setup MediaPipe once
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

class LetterAScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capture = None
        self.event = None

        self.layout = MDBoxLayout(orientation='vertical',
                                  spacing=20,
                                  padding=[0, 0, 0, 0],
                                  size_hint=(None, None),
                                  size=(400, 500),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.image = Image()
        self.label = Label(text="Detecting...", font_size=20)

        self.layout.add_widget(self.image)
        self.layout.add_widget(self.label)
        self.layout.add_widget(MDRaisedButton(
            text='Back to Menu',
            md_bg_color='gray',
            on_release=self.go_back
        ))

        self.add_widget(self.layout)

    def on_enter(self, *args):
        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.update, 1.0 / 30.0)

    def on_leave(self, *args):
        if self.capture:
            self.capture.release()
            self.capture = None
        if self.event:
            Clock.unschedule(self.event)
            self.event = None

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

        predicted_character = "No hand detected"

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

                    if confidence >= 0.7:
                        predicted_character = labels_dict.get(idx, "Gesture incorrect")
                    else:
                        predicted_character = "Gesture incorrect"
                except:
                    predicted_character = "Prediction error"

        self.label.text = f"Prediction: {predicted_character}"

        # Display camera feed
        frame = cv2.flip(frame, 0)
        buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = img_texture

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openVowelsMenu()
