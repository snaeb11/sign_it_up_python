import pickle
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from register import Account


class ImageButton(ButtonBehavior, Image):
    pass


class BottomNavScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.welcome_label = None

    def on_pre_enter(self):
        """Updates account data before the screen is displayed."""
        self.update_account_data()

    def update_account_data(self):
        """Loads account data from file and updates the welcome label."""
        try:
            account = self.load_account_data()
            if account:
                self.update_welcome_label(account.username)
                self.create_gui(account.username)
        except Exception as e:
            print(f"Failed to load account in BottomNavScreen: {e}")

    def load_account_data(self):
        """Loads the account data from the pickle file."""
        try:
            with open('account_data.pkl', 'rb') as file:
                account: Account = pickle.load(file)
                print(f"Account loaded: {account.username}")
                return account
        except Exception as e:
            print(f"Error loading account data: {e}")
            return None

    def update_welcome_label(self, username):
        """Updates the text of the welcome label if it exists."""
        if self.welcome_label:
            self.welcome_label.text = f"Welcome, {username}!"
        else:
            self.create_account_label(username)

    def create_account_label(self, username):
        """Creates and adds a new welcome label."""
        self.welcome_label = MDLabel(
            text=f"Welcome, {username}!",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # White color for the text
            font_style="H5"
        )

    def create_gui(self, username):
        """Creates the GUI components after account data is loaded."""
        top_layout = MDBoxLayout(orientation="vertical", size_hint=(1, 1.7))
        top_layout.add_widget(self.welcome_label)

        bottom_nav = MDBottomNavigation()

        # Home Tab
        home_tab = self.create_home_tab()

        # Hand Tab
        hand_tab = MDBottomNavigationItem(name="handScreen", text="Hand", icon="hand-back-left-outline")
        hand_tab.add_widget(MDLabel(text='HAND', halign='center'))

        # Menu Tab
        menu_tab = MDBottomNavigationItem(name="menuScreen", text="Menu", icon="menu")
        menu_tab.add_widget(MDLabel(text='MENU', halign='center'))

        bottom_nav.add_widget(home_tab)
        bottom_nav.add_widget(hand_tab)
        bottom_nav.add_widget(menu_tab)

        self.add_widget(bottom_nav)
        self.add_widget(top_layout)

    def create_home_tab(self):
        """Creates the home tab with buttons and layout."""
        home_tab = MDBottomNavigationItem(name="homeScreen", text="Home", icon="home")

        vowels_button = self.create_image_button('assets/vowels.png', self.open_vowels_menu)
        intro_button = self.create_image_button('assets/intro.png', self.open_intro)

        home_layout = MDBoxLayout(
            orientation='horizontal', spacing=20, padding=[10, 10, 10, 10],
            size_hint=(None, None), size=(300, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        home_layout.add_widget(intro_button)
        home_layout.add_widget(vowels_button)
        home_tab.add_widget(home_layout)

        return home_tab

    def create_image_button(self, source, on_press_callback):
        """Creates a reusable image button."""
        button = ImageButton(source=source, size_hint=(None, None), size=(150, 150))
        button.bind(on_press=on_press_callback)
        return button

    def open_vowels_menu(self, *args):
        """Open the vowels menu."""
        app = MDApp.get_running_app()
        app.openVowelsMenu()

    def open_intro(self, *args):
        """Open the intro screen."""
        app = MDApp.get_running_app()
        app.openIntro()
