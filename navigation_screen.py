from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

class ImageButton(ButtonBehavior, Image):
    pass

class BottomNavScreen(MDScreen):

    ##button open
    def open_vowels_menu(self, *args):
        app = MDApp.get_running_app()
        app.openVowelsMenu()
    
    def open_intro(self, *args):
        app = MDApp.get_running_app()
        app.openIntro()
    ##button open

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        bottom_nav = MDBottomNavigation()

        ##home tab vv
        homeTab = MDBottomNavigationItem(name="homeScreen", text="Home", icon="home",)

        vowelsButton = ImageButton(source='assets/vowels.png',
                          size_hint=(None, None),
                          size=(150, 150))
        vowelsButton.bind(on_press=self.open_vowels_menu)

        introButton = ImageButton(source='assets/intro.png',
                          size_hint=(None, None),
                          size=(150, 150))
        introButton.bind(on_press=self.open_intro)

        home_layout = MDBoxLayout(orientation='horizontal',
                                    spacing=20,
                                    padding=[10, 10, 10, 10],
                                    size_hint=(None, None),
                                    size=(300, 150),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                )
        
        
        home_layout.add_widget(introButton)
        home_layout.add_widget(vowelsButton)
        homeTab.add_widget(home_layout)

        ##home tab ^^
        handTab = MDBottomNavigationItem(name="handScreen", text="Hand", icon="hand-back-left-outline",)
        menuTab = MDBottomNavigationItem(name="menuScreen", text="Menu", icon="menu",)

        handTab.add_widget(MDLabel(text='HAND', halign='center'))
        menuTab.add_widget(MDLabel(text='MENU', halign='center'))

        bottom_nav.add_widget(homeTab)
        bottom_nav.add_widget(handTab)
        bottom_nav.add_widget(menuTab)

        self.add_widget(bottom_nav)