import os
import threading
from tkinter import Tk, filedialog
from kivy.config import Config
from kivy.uix.settings import SettingsPanel
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField

from a2 import convert_hic
from a4 import Content, KivyString
from os import getenv
from photos import create_photos
from pathlib import Path


app_data_path = getenv('APPDATA')
path1 = f"{app_data_path}/PDF_Convertor".replace("\\", "/")

root = Tk()
root.withdraw()

lst = ['word', 'img', 'html', 'txt']
y1, y2 = 0.55, 0.25
pos = [[0.3, y1], [0.7, y1], [0.3, y2], [0.7, y2]]


create_photos()


kind = ""

to_add = ''
for x in range(len(lst)):
    to_add += f"""
    Image:
        id: {lst[x]}
        source: '{path1}/{lst[x]}.png'
        pos_hint: """ + '{"center_x": ' + str(pos[x][0]) + ', "center_y": ' + str(pos[x][1]) + '''}
        size_hint_x: 0.15   
    Button:
        text: "''' + lst[x] + '''"
        font_size: 80
        pos_hint: ''' + '{"center_x": ' + str(pos[x][0]) + ', "center_y": ' + str(pos[x][1]) + '''}
        size_hint_y: 0.23
        size_hint_x: 0.16
        on_press: app.click(self.text)
        opacity: 0'''

Window.size = (1080, 720)

Window.minimum_width, Window.minimum_height = 800, 600

Config.set('graphics', 'resizable', True)
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', '0')
Config.write()

Main = KivyString + """
Screen:
    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        height: 180
        elevation: 10
        md_bg_color: 255/256, 196/256, 0/256, 1
        title: ""

    Screen:
        MDLabel:
            text: "Welcome to PDF converter tools"
            halign: "center"
            font_size: 34
            pos_hint: {"center_x": 0.5, "center_y": 0.9}
            bold: True
            # color: 1,1,1,1

        MDLabel:
            text: "Easy-to-use But Professional converter tools."
            halign: "center"
            font_size: 22
            pos_hint: {"center_x": 0.5, "center_y": 0.84}
            bold: True
            # color: 1,1,1,1
    """ + to_add + """
    """


class Heic(MDApp):
    dialog = None
    path_to_convert = ""

    def build(self):
        self.use_kivy_settings = False
        self.settings_cls = SettingsPanel
        self.title = "PDF Converter Advanced"
        return Builder.load_string(Main)

    def click(self, a):
        global kind
        kind = a

        files = [('PDF Document', '*.pdf')]
        self.path_to_convert = filedialog.askopenfilename(filetypes=files, defaultextension=".pdf")

        if self.path_to_convert is not None and self.path_to_convert != "":
            try:
                self.open_pop_up()

            except Exception:
                Snackbar(text="An unexpected error accrued").open()




    def open_pop_up(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Address:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=lambda s: self.dis()
                    ),
                    MDFlatButton(
                        text="CONVERT",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=lambda s: self.convert()
                    ), ], )
        self.dialog.open()


        try:
            downloads_path = str(Path.home() / "Downloads")
            if kind == "word":
                path = downloads_path + "\\" + self.path_to_convert.split("/")[-1].replace(".pdf", ".docx")
            elif kind == "html":
                path = downloads_path + "\\" + self.path_to_convert.split("/")[-1].replace(".pdf", ".html")
            elif kind == "txt":
                path = downloads_path + "\\" + self.path_to_convert.split("/")[-1].replace(".pdf", ".txt")
            else:
                try:
                    os.mkdir(downloads_path + "\\" + self.path_to_convert.split("/")[-1].replace(".pdf", "_photos"))
                except Exception:
                    pass
                path = downloads_path + "\\" + self.path_to_convert.split("/")[-1].replace(".pdf", "_photos")

            self.dialog.content_cls.ids.get_path.text = path
        except Exception:
            self.dialog.content_cls.ids.get_path.text = ""


    def dis(self):
        try:
            self.dialog.dismiss()
        except Exception:
            pass


    def convert(self):
        global kind
        path_to_dave = self.dialog.content_cls.ids.get_path.text
        self.dis()

        snack = Snackbar(
            text="Converting your file..."
        )
        snack.duration = 1000
        snack.open()

        threading.Thread(target=lambda: convert_hic(self.path_to_convert, path_to_dave, kind, snack), daemon=True).start()


class MyMDTextField(MDTextField):
    def on_touch_down(self, touch):
        x1, _ = touch.pos
        if self.collide_point(*touch.pos) and 680 < x1 < 750:
            if self.icon_right:

                global kind
                direc = False

                if kind == "txt":
                    files = [('Text Document', '*.txt')]
                elif kind == "word":
                    files = [('Text Document', '*.docx')]
                elif kind == "html":
                    files = [('HTML Document', '*.html')]
                else:
                    direc = True
                    files = [('PNG Format', '*.png')]

                if not direc:
                    path1 = filedialog.asksaveasfile(filetypes=files, defaultextension=f".{kind}")
                    if path1 is not None:
                        self.text = path1.name
                else:
                    path1 = filedialog.askdirectory()
                    if path1 is not None:
                        self.text = path1

        return super(MyMDTextField, self).on_touch_down(touch)



if __name__ == '__main__':
    Heic().run()

    