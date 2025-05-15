import os
import pickle

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.screen import MDScreen
from kivymd.uix.slider import MDSlider
from kivy.app import App


from register import Account


class ImageButton(ButtonBehavior, Image):
    pass


class BottomNavScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.welcome_label = None
        self.home_tab = None
        self.home_layout = None

    def on_pre_enter(self):
        """Updates account data before the screen is displayed."""
        self.update_account_data()
        if self.home_layout:
            self.refresh_home_tab()

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
            text_color=(1, 1, 1, 1),
            font_style="H5"
        )

    def create_gui(self, username):
        """Creates the GUI components after account data is loaded."""

        bottom_nav = MDBottomNavigation()

        # Home Tab
        home_tab = self.create_home_tab(username)

        # Account Tab (Profile)
        account_tab = MDBottomNavigationItem(name="accountScreen", text="Profile", icon="account")
        account_tab.add_widget(self.create_profile_section(username))

        # Settings Tab
        settings_tab = MDBottomNavigationItem(name="settingsScreen", text="Settings", icon="tools")
        settings_tab.add_widget(self.create_settings_ui())

        bottom_nav.add_widget(home_tab)
        bottom_nav.add_widget(account_tab)
        bottom_nav.add_widget(settings_tab)

        self.add_widget(bottom_nav)

    def create_home_tab(self, username):
        """Creates the home tab with centered welcome message and buttons."""
        home_tab = MDBottomNavigationItem(name="homeScreen", text="Home", icon="home")

        # Create welcome label if not already created
        if not self.welcome_label:
            self.create_account_label(username)

        # Ensure welcome label has fixed height
        self.welcome_label.size_hint_y = None
        self.welcome_label.height = 50

        # Vertical layout to hold welcome label and buttons, centered
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint=(None, None),
            size=(400, 250),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Buttons
        vowels_button = self.create_image_button('assets/vowels.png', self.open_vowels_menu)
        intro_button = self.create_image_button('assets/intro.png', self.open_intro)
        vowels_challenge_button = self.create_image_button('assets/vowelsChallengeClick.png', self.open_vowels_challenge)


        # Button row centered horizontally
        self.home_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=20,
            size_hint=(None, None),
            size=(490, 150),  # 3 buttons * 150 + 2 gaps * 20
            pos_hint={'center_x': 0.5}
        )

        self.home_layout.add_widget(intro_button)
        self.home_layout.add_widget(vowels_button)
        self.home_layout.add_widget(vowels_challenge_button)

        # Remove from previous parent if needed
        if self.welcome_label.parent:
            self.welcome_label.parent.remove_widget(self.welcome_label)

        # Add widgets to content layout
        content_layout.add_widget(self.welcome_label)
        content_layout.add_widget(self.home_layout)

        # Refresh actual buttons with logic (check progress)
        self.refresh_home_tab()

        # Add content to tab
        home_tab.add_widget(content_layout)
        return home_tab

    def refresh_home_tab(self):
        """Refreshes the button icons and states in the home tab."""
        self.home_layout.clear_widgets()

        if not os.path.exists("account_data.pkl"):
            print("No account_data.pkl found. Creating new account.")
            return

        with open("account_data.pkl", "rb") as file:
            account: Account = pickle.load(file)

        # Vowels Button
        if not account.introStatus:
            vowels_button = self.create_image_button('assets/lockVowels.png', self.open_vowels_menu)
            vowels_button.disabled = True
        elif account.aStatus and account.eStatus and account.iStatus and account.oStatus and account.uStatus:
            vowels_button = self.create_image_button('assets/checkVowels.png', self.open_vowels_menu)
        else:
            vowels_button = self.create_image_button('assets/vowels.png', self.open_vowels_menu)

        # Intro Button
        if account.introStatus:
            intro_button = self.create_image_button('assets/checkIntro.png', self.open_intro)
        else:
            intro_button = self.create_image_button('assets/intro.png', self.open_intro)

        ##vowels chalneghes butotn
        if not account.vowelScreen:
            vowels_challenge_button = self.create_image_button('assets/vowelsChallengeLocked.png', self.open_vowels_challenge)
            vowels_challenge_button.disabled = True
        elif account.easyChallenge and account.intermediateChallenge and account.hardChallenge:
            vowels_challenge_button = self.create_image_button('assets/vowelsChallengeCheck.png', self.open_vowels_challenge)
        else:
            vowels_challenge_button = self.create_image_button('assets/vowelsChallengeClick.png', self.open_vowels_challenge)

        self.home_layout.add_widget(intro_button)
        self.home_layout.add_widget(vowels_button)
        self.home_layout.add_widget(vowels_challenge_button)

    def create_profile_section(self, username):
        try:
            with open("account_data.pkl", "rb") as file:
                account = pickle.load(file)

            # ✅ Lesson Progress (5 lessons only: A, E, I, O, U)
            lesson_flags = [
                account.aStatus,
                account.eStatus,
                account.iStatus,
                account.oStatus,
                account.uStatus
            ]
            lesson_progress = sum(lesson_flags)
            progress_percent = int((lesson_progress / len(lesson_flags)) * 100)

            # ✅ Achievement Progress (now includes introStatus too)
            achievement_flags = [
                account.introStatus,
                account.aStatus,
                account.eStatus,
                account.iStatus,
                account.oStatus,
                account.uStatus,
                account.achievementOne,
                account.achievementTwo,
                account.achievementThree,
                account.achievementFour
            ]
            achievement_progress = sum(achievement_flags)
            achievement_percent = int((achievement_progress / len(achievement_flags)) * 100)

        except Exception as e:
            print(f"Failed to load account data: {e}")

        # Outer layout with top padding
        outer_layout = MDBoxLayout(
            orientation="vertical",
            padding=(50, 10, 50, 10),  # left, top, right, bottom
            spacing=10,
            size_hint=(1, 1),
        )

        # Inner layout with actual content
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None,
        )

        # Header
        header = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=40
        )
        user_label = MDLabel(
            text=f"Hello, {username}",
            font_style='H5',
            valign='middle'
        )
        header.add_widget(user_label)
        layout.add_widget(header)

        # Progression Tracker Label
        tracker_label = MDLabel(
            text="Progression Tracker:",
            font_style='H6',
            size_hint_y=None,
            height=20
        )
        layout.add_widget(tracker_label)

        # Progress: Lesson
        lesson_box = MDBoxLayout(orientation='vertical', size_hint_y=None, height=45, spacing=3)
        lesson_box.add_widget(MDLabel(
            text=f"Lesson Progress - {progress_percent}%",
            theme_text_color="Primary",
            size_hint_y=None,
            height=20
        ))
        lesson_box.add_widget(MDProgressBar(value=progress_percent, size_hint_y=None, height=15))
        layout.add_widget(lesson_box)

        # Progress: Achievement
        achievement_box = MDBoxLayout(orientation='vertical', size_hint_y=None, height=45, spacing=3)
        achievement_box.add_widget(MDLabel(
            text=f"Achievement Progress - {achievement_percent}%",
            theme_text_color="Primary",
            size_hint_y=None,
            height=20
        ))
        achievement_box.add_widget(MDProgressBar(value=achievement_percent, size_hint_y=None, height=15))
        layout.add_widget(achievement_box)

        # Spacer before Achievement Badges
        layout.add_widget(Widget(size_hint_y=None, height=5))

        # Achievement Badges Section
        layout.add_widget(MDLabel(
            text="ACHIEVEMENT BADGES",
            font_style='H6',
            halign='center',
            size_hint_y=None,
            height=30
        ))

        # Grid of Badges
        badges_grid = GridLayout(
            cols=5,
            spacing=[30, 12],
            padding=[40, 2, 0, 10],
            size_hint=(None, None),
            row_force_default=True,
            row_default_height=100,
        )
        badges_grid.bind(minimum_height=badges_grid.setter('height'),
                         minimum_width=badges_grid.setter('width'))

        badge_icons = [
            'star', 'fire', 'gesture', 'book', 'brain',
            'lock', 'lightbulb', 'trophy', 'medal', 'rocket'
        ]

        # Achievement badge descriptions
        badge_descriptions = [
            "Start of a Journey!",
            "A-mazing!",
            "E-xcellent!",
            "I-ncredible!",
            "O-utstanding!",
            "U-nstoppable!",
            "Mastered the Basics!",
            "Stepping Up the Game!",
            "Conquered the Challenge!",
            "The Completionist"
        ]

        for i, icon in enumerate(badge_icons):
            unlocked = achievement_flags[i]
            description = badge_descriptions[i] if unlocked else "Locked"

            # Create the icon button for the badge
            badge_button = MDIconButton(
                icon=icon,
                icon_size="60sp",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                pos_hint={"center_x": 0.5},
            )

            # Create a label for the badge description
            badge_label = MDLabel(
                text=description,
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_style="Caption",
                size_hint_y=None,
                height=20
            )

            # Add the badge button and label to a container layout
            badge_layout = MDBoxLayout(
                orientation='vertical',
                spacing=5,
                size_hint=(None, None),
                width=100,
                height=100,
                padding=[0, 10, 0, 0],
                pos_hint={'center_x': 0.5}
            )
            badge_layout.add_widget(badge_button)
            badge_layout.add_widget(badge_label)

            # Add the badge layout to the grid
            badges_grid.add_widget(badge_layout)

        layout.add_widget(badges_grid)

        # Add inner layout to outer layout
        outer_layout.add_widget(layout)

        return outer_layout

    def create_settings_ui(self):
        from kivy.metrics import dp

        # Outer vertical layout for spacing
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(30), size_hint=(1, 1))

        # Main Music Volume
        layout.add_widget(MDLabel(text="Main Music Volume", font_style="H6", size_hint_y=None, height=30))
        self.main_music_slider = MDSlider(min=0, max=100, value=50)
        self.main_music_slider.bind(value=self.on_music_slider_value_change)
        layout.add_widget(self.main_music_slider)

        # SFX Volume
        layout.add_widget(MDLabel(text="SFX Volume", font_style="H6", size_hint_y=None, height=30))
        self.sfx_slider = MDSlider(min=0, max=100, value=50)
        self.sfx_slider.bind(value=self.on_sfx_slider_value_change)
        layout.add_widget(self.sfx_slider)

        # Reset Progress Button
        reset_button = MDRaisedButton(
            text="Reset Progress",
            md_bg_color=(1, 0, 0, 1),
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={'center_x': 0.5}
        )
        reset_button.bind(on_press=self.confirm_reset_progress)
        layout.add_widget(reset_button)

        return layout

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

    def open_vowels_challenge(self, *args):
        """Open the intro screen."""
        app = MDApp.get_running_app()
        app.openVowelChallenges()

    def on_music_slider_value_change(self, instance, value):
        App.get_running_app().set_music_volume(value / 100.0)  # Assuming slider range is 0–100

    def on_sfx_slider_value_change(self, instance, value):
        App.get_running_app().set_sfx_volume(value / 100.0)

    def confirm_reset_progress(self, *args):
        """Ask the user to confirm before resetting progress."""
        self.dialog = MDDialog(
            title="Confirm Reset",
            text="Are you sure you want to reset your progress? This action cannot be undone.",
            buttons=[
                MDRaisedButton(text="Cancel", on_press=self.dismiss_dialog),
                MDRaisedButton(text="Reset", on_press=self.reset_progress)
            ]
        )
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()

    def reset_progress(self, *args):
        """Reset the account progress and save."""
        self.dialog.dismiss()
        try:
            account = self.load_account_data()
            if account:
                # Reset progress flags
                account.introStatus = False
                account.aStatus = False
                account.eStatus = False
                account.iStatus = False
                account.oStatus = False
                account.uStatus = False

                account.achievementOne = False
                account.achievementTwo = False
                account.achievementThree = False
                account.achievementFour = False

                account.vowelScreen = False
                account.easyChallenge = False
                account.intermediateChallenge = False
                account.hardChallenge = False

                # Save back to file
                with open('account_data.pkl', 'wb') as file:
                    pickle.dump(account, file)

                print("Progress reset successfully.")

                # Refresh UI to reflect changes
                self.refresh_home_tab()
                # If profile tab is visible, you may want to refresh it too (depends on your app flow)
        except Exception as e:
            print(f"Failed to reset progress: {e}")
