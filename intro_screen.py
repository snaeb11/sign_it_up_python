from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton


class IntroScreen (MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = MDBoxLayout(orientation='vertical',
                                    spacing=20,
                                    padding=[0, 0, 0, 0],
                                    size_hint=(None, None),
                                    size=(300, 150),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            )
        
        testButton = MDRaisedButton(
            text='INTRO!'
        )

        self.add_widget(layout)