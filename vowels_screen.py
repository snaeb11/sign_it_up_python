import pickle
import cv2
import mediapipe as mp
import numpy as np
from kivymd.uix.dialog import MDDialog

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

# Setup MediaPipe once
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)


class LetterAScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.gesture_hold_time = 0
        self.gesture_target_time = 3  # seconds to hold
        self.gesture_timer_event = None

        self.dialog_shown = False

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

                    if idx == 0 and confidence >= 0.7:
                        prediction_text = "You have successfully done the Letter A -- hold for 3 seconds"
                        if not self.gesture_timer_event:
                            self.gesture_hold_time = 0
                            self.gesture_timer_event = Clock.schedule_interval(self.update_gesture_timer, 0.1)
                    else:
                        prediction_text = "Gesture incorrect"
                        self.reset_gesture_timer()
                except:
                    prediction_text = "Prediction error"

        self.label.text = prediction_text

        # Display camera feed
        frame = cv2.flip(frame, 0)
        buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = img_texture

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openVowelsMenu()

    ##timer shii
    def update_gesture_timer(self, dt):
        self.gesture_hold_time += dt
        if self.gesture_hold_time >= self.gesture_target_time:
            self.reset_gesture_timer()
            self.show_success_dialog()

    def reset_gesture_timer(self):
        if self.gesture_timer_event:
            self.gesture_timer_event.cancel()
            self.gesture_timer_event = None
        self.gesture_hold_time = 0

     ##suckseas
    def show_success_dialog(self):
        if not self.dialog_shown:
            prediction_text = "You have successfully done the letter!"
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
            self.dialog.open()
            self.dialog_shown = True

    def reset_dialog_flag(self):
        self.dialog_shown = False  # Reset the flag when the user goes back

class LetterEScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.gesture_hold_time = 0
        self.gesture_target_time = 3  # seconds to hold
        self.gesture_timer_event = None

        self.dialog_shown = False

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

                    if idx == 1 and confidence >= 0.7:  # Assuming idx 1 corresponds to Letter E
                        prediction_text = "You have successfully done the Letter E -- hold for 3 seconds"
                        if not self.gesture_timer_event:
                            self.gesture_hold_time = 0
                            self.gesture_timer_event = Clock.schedule_interval(self.update_gesture_timer, 0.1)
                    else:
                        prediction_text = "Gesture incorrect"
                        self.reset_gesture_timer()
                except:
                    prediction_text = "Prediction error"

        self.label.text = prediction_text

        # Display camera feed
        frame = cv2.flip(frame, 0)
        buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = img_texture

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openVowelsMenu()

    def update_gesture_timer(self, dt):
        self.gesture_hold_time += dt
        if self.gesture_hold_time >= self.gesture_target_time:
            self.reset_gesture_timer()
            self.show_success_dialog()

    def reset_gesture_timer(self):
        if self.gesture_timer_event:
            self.gesture_timer_event.cancel()
            self.gesture_timer_event = None
        self.gesture_hold_time = 0

    def show_success_dialog(self):
        if not self.dialog_shown:
            prediction_text = "You have successfully done the letter!"
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
            self.dialog.open()
            self.dialog_shown = True

    def reset_dialog_flag(self):
        self.dialog_shown = False  # Reset the flag when the user goes back


class LetterIScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.gesture_hold_time = 0
        self.gesture_target_time = 3  # seconds to hold
        self.gesture_timer_event = None

        self.dialog_shown = False

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

                    if idx == 2 and confidence >= 0.7:  # Assuming idx 2 corresponds to Letter I
                        prediction_text = "You have successfully done the Letter I -- hold for 3 seconds"
                        if not self.gesture_timer_event:
                            self.gesture_hold_time = 0
                            self.gesture_timer_event = Clock.schedule_interval(self.update_gesture_timer, 0.1)
                    else:
                        prediction_text = "Gesture incorrect"
                        self.reset_gesture_timer()
                except:
                    prediction_text = "Prediction error"

        self.label.text = prediction_text

        # Display camera feed
        frame = cv2.flip(frame, 0)
        buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = img_texture

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openVowelsMenu()

    def update_gesture_timer(self, dt):
        self.gesture_hold_time += dt
        if self.gesture_hold_time >= self.gesture_target_time:
            self.reset_gesture_timer()
            self.show_success_dialog()

    def reset_gesture_timer(self):
        if self.gesture_timer_event:
            self.gesture_timer_event.cancel()
            self.gesture_timer_event = None
        self.gesture_hold_time = 0

    def show_success_dialog(self):
        if not self.dialog_shown:
            prediction_text = "You have successfully done the letter!"
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
            self.dialog.open()
            self.dialog_shown = True

    def reset_dialog_flag(self):
        self.dialog_shown = False  # Reset the flag when the user goes back


class LetterOScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.gesture_hold_time = 0
        self.gesture_target_time = 3  # seconds to hold
        self.gesture_timer_event = None

        self.dialog_shown = False

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

                    if idx == 3 and confidence >= 0.7:  # Assuming idx 3 corresponds to Letter O
                        prediction_text = "You have successfully done the Letter O -- hold for 3 seconds"
                        if not self.gesture_timer_event:
                            self.gesture_hold_time = 0
                            self.gesture_timer_event = Clock.schedule_interval(self.update_gesture_timer, 0.1)
                    else:
                        prediction_text = "Gesture incorrect"
                        self.reset_gesture_timer()
                except:
                    prediction_text = "Prediction error"

        self.label.text = prediction_text

        # Display camera feed
        frame = cv2.flip(frame, 0)
        buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = img_texture

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openVowelsMenu()

    def update_gesture_timer(self, dt):
        self.gesture_hold_time += dt
        if self.gesture_hold_time >= self.gesture_target_time:
            self.reset_gesture_timer()
            self.show_success_dialog()

    def reset_gesture_timer(self):
        if self.gesture_timer_event:
            self.gesture_timer_event.cancel()
            self.gesture_timer_event = None
        self.gesture_hold_time = 0

    def show_success_dialog(self):
        if not self.dialog_shown:
            prediction_text = "You have successfully done the letter!"
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
            self.dialog.open()
            self.dialog_shown = True

    def reset_dialog_flag(self):
        self.dialog_shown = False  # Reset the flag when the user goes back


class LetterUScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.gesture_hold_time = 0
        self.gesture_target_time = 3  # seconds to hold
        self.gesture_timer_event = None

        self.dialog_shown = False

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

                    if idx == 4 and confidence >= 0.7:  # Assuming idx 4 corresponds to Letter U
                        prediction_text = "You have successfully done the Letter U -- hold for 3 seconds"
                        if not self.gesture_timer_event:
                            self.gesture_hold_time = 0
                            self.gesture_timer_event = Clock.schedule_interval(self.update_gesture_timer, 0.1)
                    else:
                        prediction_text = "Gesture incorrect"
                        self.reset_gesture_timer()
                except:
                    prediction_text = "Prediction error"

        self.label.text = prediction_text

        # Display camera feed
        frame = cv2.flip(frame, 0)
        buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = img_texture

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openVowelsMenu()

    def update_gesture_timer(self, dt):
        self.gesture_hold_time += dt
        if self.gesture_hold_time >= self.gesture_target_time:
            self.reset_gesture_timer()
            self.show_success_dialog()

    def reset_gesture_timer(self):
        if self.gesture_timer_event:
            self.gesture_timer_event.cancel()
            self.gesture_timer_event = None
        self.gesture_hold_time = 0

    def show_success_dialog(self):
        if not self.dialog_shown:
            prediction_text = "You have successfully done the letter!"
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
            self.dialog.open()
            self.dialog_shown = True

    def reset_dialog_flag(self):
        self.dialog_shown = False  # Reset the flag when the user goes back