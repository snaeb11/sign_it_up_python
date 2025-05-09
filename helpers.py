username_helper = '''
MDTextField:
    id: usernameField
    hint_text: 'Enter username'
    mode: 'rectangle'
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    size_hint_x: None
    icon_right: "account"
    width: 300
'''

username_helper_register = '''
MDTextField:
    id: usernameField
    hint_text: 'Enter username'
    mode: 'rectangle'
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    size_hint_x: None
    icon_right: "account"
    width: 300
'''

password_helper = '''
MDTextField:
    id: passField
    hint_text: 'Enter password'
    mode: 'rectangle'
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    size_hint_x: None
    password: True
    icon_right: "account-key"
    width: 300
'''

loginButton_helper = '''
MDRaisedButton:
    text: 'Login'
    md_bg_color: 'gray'
'''

registerButton_helper = '''
MDRaisedButton:
    text: 'Register'
    md_bg_color: 'gray'
'''

introButton = '''
<ImageButton@ButtonBehavior+Image>:
    allow_stretch: True
    keep_ratio: True

BoxLayout:
    orientation: 'vertical'
    spacing: 20
    padding: 50

    ImageButton:
        source: 'assets/intro.png'
        size_hint: None, None
        size: 100, 100
        on_press: app.openVowelsMenu
'''

vowelsButton = '''
<ImageButton@ButtonBehavior+Image>:
    allow_stretch: True
    keep_ratio: True

BoxLayout:
    orientation: 'vertical'
    spacing: 20
    padding: 50

    ImageButton:
        source: 'assets/vowels.png'
        size_hint: None, None
        size: 100, 100
        on_press: app.openVowelsMenu
'''

##letter buttons
aButton = '''
<ImageButton@ButtonBehavior+Image>:
    allow_stretch: True
    keep_ratio: True

BoxLayout:
    orientation: 'vertical'
    spacing: 20
    padding: 50

    ImageButton:
        source: 'assets/aA.png'
        size_hint: None, None
        size: 100, 100
        on_press: app.openVowelsMenu
'''

##dialog
congrats = '''
BoxLayout:
    orientation: 'vertical'
    spacing: dp(20)
    padding: dp(40)

    MDRaisedButton:
        text: "Show Congratulations"
        pos_hint: {"center_x": 0.5}
        on_release: app.show_congratulations_dialog()
'''
