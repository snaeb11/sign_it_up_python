import os
import pickle

import cv2
import mediapipe as mp
import numpy as np
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.core.audio import SoundLoader
from status import status_tracker
from kivymd.uix.progressbar import MDProgressBar

# Load model once
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Setup MediaPipe once
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

#LetterA --------------------------------------------------------------------
class LetterAScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

        # Load user's volume setting from account data
        self.load_volume_setting()

        # Consolidate all SFX into a dictionary
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'success': SoundLoader.load('assets/sounds/levelwin2.mp3'),
            'achievement': SoundLoader.load("assets/sounds/achievementunlock2.mp3"),
            'instruction': SoundLoader.load('assets/sounds/copyinstruction.mp3')
        }

        # Set volumes according to user setting (excluding instruction)
        self.update_sound_volumes()
        # Set instruction sound to full volume
        if self.sfx.get('instruction'):
            self.sfx['instruction'].volume = 1.0

        self.gesture_hold_time = 0
        self.gesture_target_time = 3
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

        self.image = Image(
            size_hint=(None, None),
            width=200,
            height=200
        )

        self.gif_image = AsyncImage(
            source='assets/hands/letterA.PNG',
            allow_stretch=True,
            size_hint=(None, None),
            width=200,
            height=200,
            anim_delay=0.05
        )

        self.label = Label(text="Detecting...", font_size=20)
        self.progress_bar = MDProgressBar(value=0, max=100)

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
        self.layout.add_widget(self.progress_bar)

        # Add sound to back button
        back_button = MDRaisedButton(
            text='Back to Menu',
            md_bg_color='gray',
            on_release=self.go_back_with_sound
        )
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def on_enter(self, *args):
        # Start camera capture immediately
        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.update, 1.0 / 30.0)

        # Set up sound control
        self.sound_allowed = True
        Clock.schedule_once(self._delayed_instruction, 1.5)

    def on_leave(self, *args):
        # Immediately block any pending sounds
        self.sound_allowed = False

        # Force stop any currently playing instruction sound
        if 'instruction' in self.sfx and self.sfx['instruction']:
            self.sfx['instruction'].stop()

        # Cleanup camera and events
        if self.capture:
            self.capture.release()
        if self.event:
            Clock.unschedule(self.event)

    def load_volume_setting(self):
        """Load the user's saved volume setting"""
        try:
            if os.path.exists("account_data.pkl"):
                with open("account_data.pkl", "rb") as file:
                    account = pickle.load(file)
                    self.sfx_volume = getattr(account, 'sfx_volume', 0.5)
            else:
                self.sfx_volume = 0.5  # Default if no account exists yet
        except Exception as e:
            print(f"Error loading volume setting: {e}")

    def update_sound_volumes(self):
        """Update all sound volumes to current setting (except instruction sound)"""
        for key, sound in self.sfx.items():
            if sound and key != 'instruction':  # Skip the instruction sound
                sound.volume = self.sfx_volume

    def play_sound(self, sound_name):
        """Play a sound effect with current volume (instruction always at full volume)"""
        if sound_name in self.sfx and self.sfx[sound_name]:
            # Instruction sound always plays at full volume
            volume = 1.0 if sound_name == 'instruction' else self.sfx_volume
            self.sfx[sound_name].volume = volume
            self.sfx[sound_name].stop()
            self.sfx[sound_name].play()

    def _delayed_instruction(self, dt):
        if getattr(self, 'sound_allowed', False):
            self.play_sound('instruction')

    def go_back_with_sound(self, *args):
        """Wrapper for go_back that plays button sound"""
        self.play_sound('button_click')
        self.go_back(*args)

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
                    self.reset_gesture_timer()

        if prediction_text == "No hand detected":
            self.reset_gesture_timer()

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

    ##timer
    def update_gesture_timer(self, dt):
        self.gesture_hold_time += dt
        # Update progress bar value based on the gesture hold time
        progress = (self.gesture_hold_time / self.gesture_target_time) * 100
        self.progress_bar.value = progress  # Update progress bar

        if self.gesture_hold_time >= self.gesture_target_time:
            self.reset_gesture_timer()
            self.show_success_dialog()

    def reset_gesture_timer(self):
        if self.gesture_timer_event:
            self.gesture_timer_event.cancel()
            self.gesture_timer_event = None
        self.gesture_hold_time = 0
        self.progress_bar.value = 0  # Reset progress bar when timer is reset

    def show_success_dialog(self):
        if not self.dialog_shown:
            # Update SFX volume from app settings
            self.sfx_volume = self.app.sfx_volume
            self.update_sound_volumes()

            # Play success sound with current volume
            if self.sfx.get('success'):
                self.sfx['success'].stop()
                self.sfx['success'].play()

            self.dialog_shown = True

            # Load account data
            with open("account_data.pkl", "rb") as file:
                account = pickle.load(file)

            # Check if this is the first completion
            show_achievement = not getattr(account, "aStatus", False)

            # Mark aStatus as complete
            account.aStatus = True

            with open("account_data.pkl", "wb") as file:
                pickle.dump(account, file)

            # Define the button behavior
            def on_thank_you(instance_btn):
                self.dialog.dismiss()
                self.dialog_shown = False  # Reset flag when dialog is dismissed
                if show_achievement:
                    self.show_achievement_popup()
                else:
                    self.go_back()

            # Build the success dialog
            self.dialog = MDDialog(
                title="Congratulations!",
                text="You did an amazing job!",
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Thank you!",
                        on_release=on_thank_you
                    )
                ],
            )

            self.dialog.open()

    def show_achievement_popup(self):
        # Update SFX volume from app settings
        self.sfx_volume = self.app.sfx_volume
        self.update_sound_volumes()

        # Play achievement sound with current volume
        if self.sfx.get('achievement'):
            self.sfx['achievement'].stop()
            self.sfx['achievement'].play()

        # Build and show achievement dialog
        achievement_dialog = MDDialog(
            title="Achievement Unlocked!",
            text="You've successfully learned the Letter A! Keep going!",
            radius=[20, 7, 20, 7],
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="Awesome!",
                    on_release=lambda x: (achievement_dialog.dismiss(), self.go_back())
                )
            ],
        )
        achievement_dialog.open()

    def reset_dialog_flag(self):
        self.dialog_shown = False

class LetterEScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

        # Load user's volume setting from account data
        self.load_volume_setting()

        # Consolidate all SFX into a dictionary
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'success': SoundLoader.load('assets/sounds/levelwin2.mp3'),
            'achievement': SoundLoader.load("assets/sounds/achievementunlock2.mp3"),
            'instruction': SoundLoader.load('assets/sounds/copyinstruction.mp3')
        }

        # Set volumes according to user setting (excluding instruction)
        self.update_sound_volumes()
        # Set instruction sound to full volume
        if self.sfx.get('instruction'):
            self.sfx['instruction'].volume = 1.0

        self.gesture_hold_time = 0
        self.gesture_target_time = 3
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

        self.image = Image(
            size_hint=(None, None),
            width=200,
            height=200
        )

        self.gif_image = AsyncImage(
            source='assets/hands/letterE.PNG',
            allow_stretch=True,
            size_hint=(None, None),
            width=200,
            height=200,
            anim_delay=0.05
        )

        self.label = Label(text="Detecting...", font_size=20)
        self.progress_bar = MDProgressBar(value=0, max=100)

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
        self.layout.add_widget(self.progress_bar)

        # Add sound to back button
        back_button = MDRaisedButton(
            text='Back to Menu',
            md_bg_color='gray',
            on_release=self.go_back_with_sound
        )
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def on_enter(self, *args):
        # Start camera capture immediately
        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.update, 1.0/30.0)

        # Set up sound control
        self.sound_allowed = True
        Clock.schedule_once(self._delayed_instruction, 1.5)

    def on_leave(self, *args):
        # Immediately block any pending sounds
        self.sound_allowed = False

        # Force stop any currently playing instruction sound
        if 'instruction' in self.sfx and self.sfx['instruction']:
            self.sfx['instruction'].stop()

        # Cleanup camera and events
        if self.capture:
            self.capture.release()
        if self.event:
            Clock.unschedule(self.event)

    def load_volume_setting(self):
        """Load the user's saved volume setting"""
        try:
            if os.path.exists("account_data.pkl"):
                with open("account_data.pkl", "rb") as file:
                    account = pickle.load(file)
                    self.sfx_volume = getattr(account, 'sfx_volume', 0.5)
            else:
                self.sfx_volume = 0.5  # Default if no account exists yet
        except Exception as e:
            print(f"Error loading volume setting: {e}")

    def update_sound_volumes(self):
        """Update all sound volumes to current setting (except instruction sound)"""
        for key, sound in self.sfx.items():
            if sound and key != 'instruction':  # Skip the instruction sound
                sound.volume = self.sfx_volume

    def play_sound(self, sound_name):
        """Play a sound effect with current volume (instruction always at full volume)"""
        if sound_name in self.sfx and self.sfx[sound_name]:
            # Instruction sound always plays at full volume
            volume = 1.0 if sound_name == 'instruction' else self.sfx_volume
            self.sfx[sound_name].volume = volume
            self.sfx[sound_name].stop()
            self.sfx[sound_name].play()

    def _delayed_instruction(self, dt):
        if getattr(self, 'sound_allowed', False):
            self.play_sound('instruction')

    def go_back_with_sound(self, *args):
        """Wrapper for go_back that plays button sound"""
        self.play_sound('button_click')
        self.go_back(*args)

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

                    if idx == 1 and confidence >= 0.7:  # Index 1 for Letter E
                        prediction_text = "You have successfully done the Letter E -- hold for 3 seconds"
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
        # Update progress bar value based on the gesture hold time
        progress = (self.gesture_hold_time / self.gesture_target_time) * 100
        self.progress_bar.value = progress  # Update progress bar

        if self.gesture_hold_time >= self.gesture_target_time:
            self.reset_gesture_timer()
            self.show_success_dialog()

    def reset_gesture_timer(self):
        if self.gesture_timer_event:
            self.gesture_timer_event.cancel()
            self.gesture_timer_event = None
        self.gesture_hold_time = 0
        self.progress_bar.value = 0  # Reset progress bar when timer is reset

    def show_success_dialog(self):
        if not self.dialog_shown:
            # Update SFX volume from app settings
            self.sfx_volume = self.app.sfx_volume
            self.update_sound_volumes()

            # Play success sound with current volume
            if self.sfx.get('success'):
                self.sfx['success'].stop()
                self.sfx['success'].play()

            self.dialog_shown = True

            # Load account data
            with open("account_data.pkl", "rb") as file:
                account = pickle.load(file)

            # Check if this is the first completion
            show_achievement = not getattr(account, "eStatus", False)

            # Mark eStatus as complete
            account.eStatus = True

            with open("account_data.pkl", "wb") as file:
                pickle.dump(account, file)

            # Define the button behavior
            def on_thank_you(instance_btn):
                self.dialog.dismiss()
                self.dialog_shown = False  # Reset flag when dialog is dismissed
                if show_achievement:
                    self.show_achievement_popup()
                else:
                    self.go_back()

            # Build the success dialog
            self.dialog = MDDialog(
                title="Congratulations!",
                text="You did an amazing job with Letter E!",
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Thank you!",
                        on_release=on_thank_you
                    )
                ],
            )

            self.dialog.open()

    def show_achievement_popup(self):
        # Update SFX volume from app settings
        self.sfx_volume = self.app.sfx_volume
        self.update_sound_volumes()

        # Play achievement sound with current volume
        if self.sfx.get('achievement'):
            self.sfx['achievement'].stop()
            self.sfx['achievement'].play()

        # Build and show achievement dialog
        achievement_dialog = MDDialog(
            title="Achievement Unlocked!",
            text="You've successfully learned the Letter E! Keep going!",
            radius=[20, 7, 20, 7],
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="Awesome!",
                    on_release=lambda x: (achievement_dialog.dismiss(), self.go_back())
                )
            ],
        )
        achievement_dialog.open()

    def reset_dialog_flag(self):
        self.dialog_shown = False

#LetterI --------------------------------------------------------------------
class LetterIScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

        # Load user's volume setting from account data
        self.load_volume_setting()

        # Consolidate all SFX into a dictionary
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'success': SoundLoader.load('assets/sounds/levelwin2.mp3'),
            'achievement': SoundLoader.load("assets/sounds/achievementunlock2.mp3"),
            'instruction': SoundLoader.load('assets/sounds/copyinstruction.mp3')
        }

        # Set volumes according to user setting (excluding instruction)
        self.update_sound_volumes()
        # Set instruction sound to full volume
        if self.sfx.get('instruction'):
            self.sfx['instruction'].volume = 1.0

        self.gesture_hold_time = 0
        self.gesture_target_time = 3
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

        self.image = Image(
            size_hint=(None, None),
            width=200,
            height=200
        )

        self.gif_image = AsyncImage(
            source='assets/hands/letterI.PNG',
            allow_stretch=True,
            size_hint=(None, None),
            width=200,
            height=200,
            anim_delay=0.05
        )

        self.label = Label(text="Detecting...", font_size=20)
        self.progress_bar = MDProgressBar(value=0, max=100)

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
        self.layout.add_widget(self.progress_bar)

        # Add sound to back button
        back_button = MDRaisedButton(
            text='Back to Menu',
            md_bg_color='gray',
            on_release=self.go_back_with_sound
        )
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def on_enter(self, *args):
        # Start camera capture immediately
        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.update, 1.0/30.0)

        # Set up sound control
        self.sound_allowed = True
        Clock.schedule_once(self._delayed_instruction, 1.5)

    def on_leave(self, *args):
        # Immediately block any pending sounds
        self.sound_allowed = False

        # Force stop any currently playing instruction sound
        if 'instruction' in self.sfx and self.sfx['instruction']:
            self.sfx['instruction'].stop()

        # Cleanup camera and events
        if self.capture:
            self.capture.release()
        if self.event:
            Clock.unschedule(self.event)

    def load_volume_setting(self):
        """Load the user's saved volume setting"""
        try:
            if os.path.exists("account_data.pkl"):
                with open("account_data.pkl", "rb") as file:
                    account = pickle.load(file)
                    self.sfx_volume = getattr(account, 'sfx_volume', 0.5)
            else:
                self.sfx_volume = 0.5  # Default if no account exists yet
        except Exception as e:
            print(f"Error loading volume setting: {e}")

    def update_sound_volumes(self):
        """Update all sound volumes to current setting (except instruction sound)"""
        for key, sound in self.sfx.items():
            if sound and key != 'instruction':  # Skip the instruction sound
                sound.volume = self.sfx_volume

    def play_sound(self, sound_name):
        """Play a sound effect with current volume (instruction always at full volume)"""
        if sound_name in self.sfx and self.sfx[sound_name]:
            # Instruction sound always plays at full volume
            volume = 1.0 if sound_name == 'instruction' else self.sfx_volume
            self.sfx[sound_name].volume = volume
            self.sfx[sound_name].stop()
            self.sfx[sound_name].play()

    def _delayed_instruction(self, dt):
        if getattr(self, 'sound_allowed', False):
            self.play_sound('instruction')

    def go_back_with_sound(self, *args):
        """Wrapper for go_back that plays button sound"""
        self.play_sound('button_click')
        self.go_back(*args)

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

                    if idx == 2 and confidence >= 0.7:  # Index 2 for Letter I
                        prediction_text = "You have successfully done the Letter I -- hold for 3 seconds"
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
        # Update progress bar value based on the gesture hold time
        progress = (self.gesture_hold_time / self.gesture_target_time) * 100
        self.progress_bar.value = progress  # Update progress bar

        if self.gesture_hold_time >= self.gesture_target_time:
            self.reset_gesture_timer()
            self.show_success_dialog()

    def reset_gesture_timer(self):
        if self.gesture_timer_event:
            self.gesture_timer_event.cancel()
            self.gesture_timer_event = None
        self.gesture_hold_time = 0
        self.progress_bar.value = 0  # Reset progress bar when timer is reset

    def show_success_dialog(self):
        if not self.dialog_shown:
            # Update SFX volume from app settings
            self.sfx_volume = self.app.sfx_volume
            self.update_sound_volumes()

            # Play success sound with current volume
            if self.sfx.get('success'):
                self.sfx['success'].stop()
                self.sfx['success'].play()

            self.dialog_shown = True

            # Load account data
            with open("account_data.pkl", "rb") as file:
                account = pickle.load(file)

            # Check if this is the first completion
            show_achievement = not getattr(account, "iStatus", False)

            # Mark iStatus as complete
            account.iStatus = True

            with open("account_data.pkl", "wb") as file:
                pickle.dump(account, file)

            # Define the button behavior
            def on_thank_you(instance_btn):
                self.dialog.dismiss()
                self.dialog_shown = False  # Reset flag when dialog is dismissed
                if show_achievement:
                    self.show_achievement_popup()
                else:
                    self.go_back()

            # Build the success dialog
            self.dialog = MDDialog(
                title="Congratulations!",
                text="You did an amazing job with Letter I!",
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Thank you!",
                        on_release=on_thank_you
                    )
                ],
            )

            self.dialog.open()

    def show_achievement_popup(self):
        # Update SFX volume from app settings
        self.sfx_volume = self.app.sfx_volume
        self.update_sound_volumes()

        # Play achievement sound with current volume
        if self.sfx.get('achievement'):
            self.sfx['achievement'].stop()
            self.sfx['achievement'].play()

        # Build and show achievement dialog
        achievement_dialog = MDDialog(
            title="Achievement Unlocked!",
            text="You've successfully learned the Letter I! Keep going!",
            radius=[20, 7, 20, 7],
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="Awesome!",
                    on_release=lambda x: (achievement_dialog.dismiss(), self.go_back())
                )
            ],
        )
        achievement_dialog.open()

    def reset_dialog_flag(self):
        self.dialog_shown = False

#LetterO --------------------------------------------------------------------
class LetterOScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

        # Load user's volume setting from account data
        self.load_volume_setting()

        # Consolidate all SFX into a dictionary
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'success': SoundLoader.load('assets/sounds/levelwin2.mp3'),
            'achievement': SoundLoader.load("assets/sounds/achievementunlock2.mp3"),
            'instruction': SoundLoader.load('assets/sounds/copyinstruction.mp3')
        }

        # Set volumes according to user setting (excluding instruction)
        self.update_sound_volumes()
        # Set instruction sound to full volume
        if self.sfx.get('instruction'):
            self.sfx['instruction'].volume = 1.0

        self.gesture_hold_time = 0
        self.gesture_target_time = 3
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

        self.image = Image(
            size_hint=(None, None),
            width=200,
            height=200
        )

        self.gif_image = AsyncImage(
            source='assets/hands/letterO.PNG',
            allow_stretch=True,
            size_hint=(None, None),
            width=200,
            height=200,
            anim_delay=0.05
        )

        self.label = Label(text="Detecting...", font_size=20)
        self.progress_bar = MDProgressBar(value=0, max=100)

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
        self.layout.add_widget(self.progress_bar)

        # Add sound to back button
        back_button = MDRaisedButton(
            text='Back to Menu',
            md_bg_color='gray',
            on_release=self.go_back_with_sound
        )
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def on_enter(self, *args):
        # Start camera capture immediately
        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.update, 1.0/30.0)

        # Set up sound control
        self.sound_allowed = True
        Clock.schedule_once(self._delayed_instruction, 1.5)

    def on_leave(self, *args):
        # Immediately block any pending sounds
        self.sound_allowed = False

        # Force stop any currently playing instruction sound
        if 'instruction' in self.sfx and self.sfx['instruction']:
            self.sfx['instruction'].stop()

        # Cleanup camera and events
        if self.capture:
            self.capture.release()
        if self.event:
            Clock.unschedule(self.event)

    def load_volume_setting(self):
        """Load the user's saved volume setting"""
        try:
            if os.path.exists("account_data.pkl"):
                with open("account_data.pkl", "rb") as file:
                    account = pickle.load(file)
                    self.sfx_volume = getattr(account, 'sfx_volume', 0.5)
            else:
                self.sfx_volume = 0.5  # Default if no account exists yet
        except Exception as e:
            print(f"Error loading volume setting: {e}")

    def update_sound_volumes(self):
        """Update all sound volumes to current setting (except instruction sound)"""
        for key, sound in self.sfx.items():
            if sound and key != 'instruction':  # Skip the instruction sound
                sound.volume = self.sfx_volume

    def play_sound(self, sound_name):
        """Play a sound effect with current volume (instruction always at full volume)"""
        if sound_name in self.sfx and self.sfx[sound_name]:
            # Instruction sound always plays at full volume
            volume = 1.0 if sound_name == 'instruction' else self.sfx_volume
            self.sfx[sound_name].volume = volume
            self.sfx[sound_name].stop()
            self.sfx[sound_name].play()

    def _delayed_instruction(self, dt):
        if getattr(self, 'sound_allowed', False):
            self.play_sound('instruction')

    def go_back_with_sound(self, *args):
        """Wrapper for go_back that plays button sound"""
        self.play_sound('button_click')
        self.go_back(*args)

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

                    if idx == 3 and confidence >= 0.7:  # Index 3 for Letter O
                        prediction_text = "You have successfully done the Letter O -- hold for 3 seconds"
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
        # Update progress bar value based on the gesture hold time
        progress = (self.gesture_hold_time / self.gesture_target_time) * 100
        self.progress_bar.value = progress  # Update progress bar

        if self.gesture_hold_time >= self.gesture_target_time:
            self.reset_gesture_timer()
            self.show_success_dialog()

    def reset_gesture_timer(self):
        if self.gesture_timer_event:
            self.gesture_timer_event.cancel()
            self.gesture_timer_event = None
        self.gesture_hold_time = 0
        self.progress_bar.value = 0  # Reset progress bar when timer is reset

    def show_success_dialog(self):
        if not self.dialog_shown:
            # Update SFX volume from app settings
            self.sfx_volume = self.app.sfx_volume
            self.update_sound_volumes()

            # Play success sound with current volume
            if self.sfx.get('success'):
                self.sfx['success'].stop()
                self.sfx['success'].play()

            self.dialog_shown = True

            # Load account data
            with open("account_data.pkl", "rb") as file:
                account = pickle.load(file)

            # Check if this is the first completion
            show_achievement = not getattr(account, "oStatus", False)

            # Mark oStatus as complete
            account.oStatus = True

            with open("account_data.pkl", "wb") as file:
                pickle.dump(account, file)

            # Define the button behavior
            def on_thank_you(instance_btn):
                self.dialog.dismiss()
                self.dialog_shown = False  # Reset flag when dialog is dismissed
                if show_achievement:
                    self.show_achievement_popup()
                else:
                    self.go_back()

            # Build the success dialog
            self.dialog = MDDialog(
                title="Congratulations!",
                text="You did an amazing job with Letter O!",
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Thank you!",
                        on_release=on_thank_you
                    )
                ],
            )

            self.dialog.open()

    def show_achievement_popup(self):
        # Update SFX volume from app settings
        self.sfx_volume = self.app.sfx_volume
        self.update_sound_volumes()

        # Play achievement sound with current volume
        if self.sfx.get('achievement'):
            self.sfx['achievement'].stop()
            self.sfx['achievement'].play()

        # Build and show achievement dialog
        achievement_dialog = MDDialog(
            title="Achievement Unlocked!",
            text="You've successfully learned the Letter O! Keep going!",
            radius=[20, 7, 20, 7],
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="Awesome!",
                    on_release=lambda x: (achievement_dialog.dismiss(), self.go_back())
                )
            ],
        )
        achievement_dialog.open()

    def reset_dialog_flag(self):
        self.dialog_shown = False

#LetterU --------------------------------------------------------------------
class LetterUScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

        # Load user's volume setting from account data
        self.load_volume_setting()

        # Consolidate all SFX into a dictionary
        self.sfx = {
            'button_click': SoundLoader.load('assets/sounds/select2.mp3'),
            'success': SoundLoader.load('assets/sounds/levelwin2.mp3'),
            'achievement': SoundLoader.load("assets/sounds/achievementunlock2.mp3"),
            'instruction': SoundLoader.load('assets/sounds/copyinstruction.mp3')
        }

        # Set volumes according to user setting (excluding instruction)
        self.update_sound_volumes()
        # Set instruction sound to full volume
        if self.sfx.get('instruction'):
            self.sfx['instruction'].volume = 1.0

        self.gesture_hold_time = 0
        self.gesture_target_time = 3
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

        self.image = Image(
            size_hint=(None, None),
            width=200,
            height=200
        )

        self.gif_image = AsyncImage(
            source='assets/hands/letterU.PNG',
            allow_stretch=True,
            size_hint=(None, None),
            width=200,
            height=200,
            anim_delay=0.05
        )

        self.label = Label(text="Detecting...", font_size=20)
        self.progress_bar = MDProgressBar(value=0, max=100)

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
        self.layout.add_widget(self.progress_bar)

        # Add sound to back button
        back_button = MDRaisedButton(
            text='Back to Menu',
            md_bg_color='gray',
            on_release=self.go_back_with_sound
        )
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def on_enter(self, *args):
        # Start camera capture immediately
        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.update, 1.0/30.0)

        # Set up sound control
        self.sound_allowed = True
        Clock.schedule_once(self._delayed_instruction, 1.5)

    def on_leave(self, *args):
        # Immediately block any pending sounds
        self.sound_allowed = False

        # Force stop any currently playing instruction sound
        if 'instruction' in self.sfx and self.sfx['instruction']:
            self.sfx['instruction'].stop()

        # Cleanup camera and events
        if self.capture:
            self.capture.release()
        if self.event:
            Clock.unschedule(self.event)

    def load_volume_setting(self):
        """Load the user's saved volume setting"""
        try:
            if os.path.exists("account_data.pkl"):
                with open("account_data.pkl", "rb") as file:
                    account = pickle.load(file)
                    self.sfx_volume = getattr(account, 'sfx_volume', 0.5)
            else:
                self.sfx_volume = 0.5  # Default if no account exists yet
        except Exception as e:
            print(f"Error loading volume setting: {e}")

    def update_sound_volumes(self):
        """Update all sound volumes to current setting (except instruction sound)"""
        for key, sound in self.sfx.items():
            if sound and key != 'instruction':  # Skip the instruction sound
                sound.volume = self.sfx_volume

    def play_sound(self, sound_name):
        """Play a sound effect with current volume (instruction always at full volume)"""
        if sound_name in self.sfx and self.sfx[sound_name]:
            # Instruction sound always plays at full volume
            volume = 1.0 if sound_name == 'instruction' else self.sfx_volume
            self.sfx[sound_name].volume = volume
            self.sfx[sound_name].stop()
            self.sfx[sound_name].play()

    def _delayed_instruction(self, dt):
        if getattr(self, 'sound_allowed', False):
            self.play_sound('instruction')

    def go_back_with_sound(self, *args):
        """Wrapper for go_back that plays button sound"""
        self.play_sound('button_click')
        self.go_back(*args)

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

                    if idx == 4 and confidence >= 0.7:  # Index 4 for Letter U
                        prediction_text = "You have successfully done the Letter U -- hold for 3 seconds"
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
        # Update progress bar value based on the gesture hold time
        progress = (self.gesture_hold_time / self.gesture_target_time) * 100
        self.progress_bar.value = progress  # Update progress bar

        if self.gesture_hold_time >= self.gesture_target_time:
            self.reset_gesture_timer()
            self.show_success_dialog()

    def reset_gesture_timer(self):
        if self.gesture_timer_event:
            self.gesture_timer_event.cancel()
            self.gesture_timer_event = None
        self.gesture_hold_time = 0
        self.progress_bar.value = 0  # Reset progress bar when timer is reset

    def show_success_dialog(self):
        if not self.dialog_shown:
            # Update SFX volume from app settings
            self.sfx_volume = self.app.sfx_volume
            self.update_sound_volumes()

            # Play success sound with current volume
            if self.sfx.get('success'):
                self.sfx['success'].stop()
                self.sfx['success'].play()

            self.dialog_shown = True

            # Load account data
            with open("account_data.pkl", "rb") as file:
                account = pickle.load(file)

            # Check if this is the first completion
            show_achievement = not getattr(account, "uStatus", False)

            # Mark uStatus as complete and unlock vowel challenges
            account.uStatus = True
            account.vowelScreen = True  # Unlock vowel challenges

            with open("account_data.pkl", "wb") as file:
                pickle.dump(account, file)

            # Define the button behavior
            def on_thank_you(instance_btn):
                self.dialog.dismiss()
                self.dialog_shown = False  # Reset flag when dialog is dismissed
                if show_achievement:
                    self.show_achievement_popup()
                else:
                    self.go_back()

            # Build the success dialog
            self.dialog = MDDialog(
                title="Congratulations!",
                text="You did an amazing job with Letter U! Vowel challenges unlocked!",
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="Thank you!",
                        on_release=on_thank_you
                    )
                ],
            )

            self.dialog.open()

    def show_achievement_popup(self):
        # Update SFX volume from app settings
        self.sfx_volume = self.app.sfx_volume
        self.update_sound_volumes()

        # Play achievement sound with current volume
        if self.sfx.get('achievement'):
            self.sfx['achievement'].stop()
            self.sfx['achievement'].play()

        # Build and show achievement dialog
        achievement_dialog = MDDialog(
            title="Achievement Unlocked!",
            text="You've completed all vowels! Vowel challenges are now available!",
            radius=[20, 7, 20, 7],
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="Awesome!",
                    on_release=lambda x: (achievement_dialog.dismiss(), self.go_back())
                )
            ],
        )
        achievement_dialog.open()

    def reset_dialog_flag(self):
        self.dialog_shown = False