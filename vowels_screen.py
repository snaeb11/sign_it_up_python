from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from kivymd.app import MDApp

class LetterAScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.capture = None  # delay starting it until screen is active
        self.event = None

        layout = MDBoxLayout(orientation='vertical',
                             spacing=20,
                             padding=[0, 0, 0, 0],
                             size_hint=(None, None),
                             size=(400, 400),
                             pos_hint={'center_x': 0.5, 'center_y': 0.5},
                             )

        layout.add_widget(MDRaisedButton(
            text='Back to Menu',
            md_bg_color='gray',
            on_release=self.go_back
        ))

        self.image = Image()
        layout.add_widget(self.image)

        self.add_widget(layout)

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
        if self.capture:
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.flip(frame, 0)
                buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
                img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                self.image.texture = img_texture

    def go_back(self, *args):
        app = MDApp.get_running_app()
        app.openVowelsMenu()
