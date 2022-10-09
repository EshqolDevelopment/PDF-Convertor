
from kivy.uix.boxlayout import BoxLayout


KivyString = '''
<Content>
    orientation: "vertical"
    size_hint_y: None
    height: "70dp"

    MyMDTextField:
        id: get_path
        hint_text: "Select a path to save your converted file"
        size_hint_x: 0.85
        icon_right: "folder-outline"

'''


class Content(BoxLayout):
    pass


