import tkinter
import tkinter.filedialog
import tkinter.messagebox
import pygame
import os
import sys
import logging
import json
from typing import List, Union

import webbrowser

import modules.utils as utils
from modules.audio import SoundMusic

_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

FONT = ("Helvetica", "10")
NUMBER_OF_BUTTONS = 9
SOUNDS_LIST: List[Union[SoundMusic, None]] = [None for _ in range(NUMBER_OF_BUTTONS)]

SYSTEM_WIDE_KEY_MAPPING = {
    1: "7",
    2: "8",
    3: "9",
    4: "4",
    5: "5",
    6: "6",
    7: "1",
    8: "2",
    9: "3",
}

INSIDE_APP_KEY_MAPPING = {
    1: "<KP_7>",
    2: "<KP_8>",
    3: "<KP_9>",
    4: "<KP_4>",
    5: "<KP_5>",
    6: "<KP_6>",
    7: "<KP_1>",
    8: "<KP_2>",
    9: "<KP_3>",
}

github = "https://github.com/ajwalkiewicz/sound-pad"

open_img_path = "images/folder-2x.png"
stop_img_path = "images/media-stop-2x.png"
pause_img_path = "images/media-pause-2x.png"
play_img_path = "images/media-play-2x.png"

SETTINGS = os.path.join(_THIS_FOLDER, "data", "settings.json")

with open(SETTINGS, "r") as json_file:
    settings: dict = json.load(json_file)
    DEFAULT_DIRECTORY: str = settings["default_directory"]
    NUM_CHANNELS: int = settings["num_channels"]
    KEY_RANGE: str = settings["key_range"]
    FONT: tuple = (settings["font_type"], settings["font_size"])
    SHOW_SETTINGS: bool = settings["show_settings"]

system = sys.platform
if system == "win32":
    logging.info(f"System detected: {system}. Use Windows configuration")
    import keyboard

    def _keyboard_add_hotkey(hotkey: str, key: int):
        return keyboard.add_hotkey(hotkey, lambda: SOUNDS_LIST[key].play())

    def _open_settings():
        os.system(f"notepad.exe {SETTINGS}")

else:
    logging.info(f"System detected: {system}. Use UNIX configuration")
    from pynput import keyboard

    def _keyboard_add_hotkey(hotkey: str, key: int):
        return keyboard.GlobalHotKeys({hotkey: lambda: SOUNDS_LIST[key].play()}).start()

    def _open_settings():
        os.system(f"xdg-open {SETTINGS}")


def bind_key(key: int, object: tkinter.Tk):
    logging.debug(f"Bind key: {key}")
    if KEY_RANGE == "inside_app":
        hotkey = INSIDE_APP_KEY_MAPPING.get(key + 1, "0")
        object.bind(hotkey, lambda event: SOUNDS_LIST[key].play())
    if KEY_RANGE == "system_wide":
        hotkey = SYSTEM_WIDE_KEY_MAPPING.get(key + 1, "0")
        _keyboard_add_hotkey(hotkey, key)


class VolumeBar(tkinter.Scale):
    volume_bar_list = []

    def __init__(self, master=None):
        super().__init__(master)
        self.nr = len(self.volume_bar_list)
        self["width"] = 15
        self["orient"] = tkinter.VERTICAL
        self["from_"] = 1
        self["to"] = 0
        self["resolution"] = 0.01
        self["showvalue"] = 0
        self["sliderlength"] = 30
        self["command"] = self.set_sound_volume
        # self.set(0.50)
        self.volume_bar_list.append(self)

    def set_sound_volume(self, value):
        logging.debug(f"Volume set to: {value}")
        sound = SOUNDS_LIST[self.nr]
        if isinstance(sound, SoundMusic):
            sound.set_volume(float(value))
            logging.debug(f"VOLUMEBAR: volume set to: {value}")
        else:
            logging.debug(f"VOLUMEBAR: no sound")


class LoopCheckBox(tkinter.Checkbutton):
    loop_check_box_list = []

    def __init__(self, master=None):
        super().__init__(master)
        self.nr = len(self.loop_check_box_list)
        self.var = tkinter.IntVar()
        self["width"] = 1
        self["command"] = self.check
        self["variable"] = self.var
        self["onvalue"] = -1
        self["offvalue"] = 0
        fake_icon = tkinter.PhotoImage(width=6, height=15)
        self["image"] = fake_icon
        self.image = fake_icon
        self.loop_check_box_list.append(self)

    def check(self):
        logging.debug(f"CHECKBOX checked, id: {self.nr}")
        sound = SOUNDS_LIST[self.nr]
        if isinstance(sound, SoundMusic):
            sound.is_looped = self.var.get()
            logging.info(f"CHECKBOX value: {self.var.get()}")
        else:
            logging.debug(f"CHECKBOX: Empty button")


class Button(tkinter.Button):
    def __init__(self, master=None):
        super().__init__(master)
        self["width"] = 25
        self["height"] = 25
        self["font"] = FONT


class PadButton(Button):
    buttons_list = []

    def __init__(self, master=None, nr=None):
        super().__init__(master)
        self.master = master
        self.nr = len(self.buttons_list)
        self.state = True
        self["width"] = 20
        self["height"] = 10
        self["command"] = self.play
        self["text"] = str(nr)
        PadButton.buttons_list.append(self)
        # self._button_list_sort()

    def play(self):
        logging.debug(f"PAD BUTTON pressed, id: {self.nr}")
        sound = SOUNDS_LIST[self.nr]
        if isinstance(sound, SoundMusic):
            sound.play()
            logging.info(f"PLAY: {sound.path}")
        else:
            logging.debug(f"Empty PAD BUTTON pressed.")

    # def _button_list_sort(self):
    #     """Setting buttons in a right order.
    #     From this order: [0,1,2,3,4,5,6,7,8]
    #     To this order:   [6,7,8,3,4,5,0,1,2]"""
    #     if len(self.buttons_list) == NUMBER_OF_BUTTONS:
    #         self.buttons_list[0], self.buttons_list[6] = self.buttons_list[6], self.buttons_list[0]
    #         self.buttons_list[1], self.buttons_list[7] = self.buttons_list[7], self.buttons_list[1]
    #         self.buttons_list[2], self.buttons_list[8] = self.buttons_list[8], self.buttons_list[2]


class OpenButton(Button):
    buttons_list = []

    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self.nr = len(self.buttons_list)
        self["text"] = "Open"
        self["width"] = 25
        self["command"] = self.open_file
        icon = tkinter.PhotoImage(file=open_img_path)
        self["image"] = icon
        self.image = icon
        self.file_path = None
        OpenButton.buttons_list.append(self)

    def open_file(self):
        logging.info(f"OPEN FILE BUTTON pressed, id {self.nr}")
        initial_directory = os.path.join(DEFAULT_DIRECTORY)
        title = "Select A File"
        file_types = [("wav files", "*.wav")]
        self.file_path = tkinter.filedialog.askopenfilename(
            initialdir=initial_directory, title=title, filetypes=file_types
        )
        if self.file_path:
            SOUNDS_LIST[self.nr] = SoundMusic(self.file_path, self.nr)
            bind_key(self.nr, self.master.master)
            pad_button_text = os.path.split(self.file_path)[1]
            PadButton.buttons_list[self.nr].config(text=pad_button_text)


class StopButton(Button):
    buttons_list = []

    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self.nr = len(self.buttons_list)
        self["text"] = "Stop"
        # self["width"] = 10
        self["command"] = self.stop_file
        icon = tkinter.PhotoImage(file=stop_img_path)
        self["image"] = icon
        self.image = icon
        self.buttons_list.append(self)

    def stop_file(self):
        logging.info(f"STOP BUTTON pressed, id: {self.nr}")
        if isinstance(SOUNDS_LIST[self.nr], SoundMusic):
            SOUNDS_LIST[self.nr].stop()


class PauseButton(Button):
    buttons_list = []

    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self.nr = len(self.buttons_list)
        self["text"] = "Pause"
        self["command"] = self.pause
        icon = tkinter.PhotoImage(file=pause_img_path)
        self["image"] = icon
        self.image = icon
        self.buttons_list.append(self)

    def pause(self):
        logging.info(f"PAUSE BUTTON pressed, id: {self.nr}")
        if isinstance(SOUNDS_LIST[self.nr], SoundMusic):
            SOUNDS_LIST[self.nr].play_pause()


class PlayButton(Button):
    buttons_list = []

    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self.nr = len(self.buttons_list)
        self["text"] = "Play"
        self["command"] = self.play
        icon = tkinter.PhotoImage(file=play_img_path)
        self["image"] = icon
        self.image = icon
        self.buttons_list.append(self)

    def play(self):
        logging.info(f"PLAY BUTTON pressed, id: {self.nr}")
        if isinstance(SOUNDS_LIST[self.nr], SoundMusic):
            SOUNDS_LIST[self.nr].play()


class SaveProjectButton(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["text"] = "Save Project"
        self["command"] = self.save_project

    @staticmethod
    def save_project():
        logging.info(f"SAVE PROJECT selected")
        initial_directory = os.path.join(".")
        title = "Save Project"
        file_types = [("json files", "*.json"), ("All Files", "*.*")]
        try:
            save_file = tkinter.filedialog.asksaveasfile(
                mode="w",
                initialdir=initial_directory,
                title=title,
                filetypes=file_types,
                defaultextension=".json",
            )
            if hasattr(save_file, "write"):
                config = {
                    key: button.file_path
                    for key, button in enumerate(OpenButton.buttons_list)
                }
                json.dump(config, save_file)
                save_file.close()
        except PermissionError:
            logging.debug(f"PERMISSION ERROR while trying to save project")
            tkinter.messagebox.showerror(
                title="Permission Error",
                message="You do not have perrmision to save files in this loaction",
            )


class OpenProjectButton(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["text"] = "Open Project"
        self["command"] = self.open_project

    @staticmethod
    def open_project():
        logging.info(f"OPEN PROJECT selected")
        initial_directory = os.path.join(".")
        title = "Select Project"
        file_types = [("json files", "*.json"), ("All Files", "*.*")]
        file_path = tkinter.filedialog.askopenfilename(
            initialdir=initial_directory, title=title, filetypes=file_types
        )

        if file_path:
            # if keyboard._hotkeys:
            # keyboard.remove_all_hotkeys()

            for position, text in enumerate([7, 8, 9, 4, 5, 6, 1, 2, 3]):
                PadButton.buttons_list[position].config(text=str(text))
                SOUNDS_LIST[position] = None

            with open(file_path, "r") as read_file:
                data = json.loads(read_file.read())
                files_not_found_list = []
                for key, item in data.items():
                    if item is not None:
                        try:
                            SOUNDS_LIST[int(key)] = SoundMusic(item, int(key))
                            pad_button_text = os.path.split(item)[1]
                            # OpenButton.buttons_list[int(key)].bind_key(int(key))
                            bind_key(
                                int(key),
                                OpenButton.buttons_list[int(key)].master.master,
                            )
                            PadButton.buttons_list[int(key)].config(
                                text=pad_button_text
                            )
                        except FileNotFoundError:
                            files_not_found_list.append(item)

            if files_not_found_list:
                message = "The following files could not be found: \n"
                for nr, text in enumerate(files_not_found_list):
                    message += f"\n{nr+1}. {text}"
                tkinter.messagebox.showerror(title="Missing Files", message=message)


class StopAll(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["width"] = 20
        self["height"] = 2
        self["text"] = "STOP ALL"
        self["command"] = self.stop_all

    def stop_all(self) -> None:
        logging.info(f"STOP ALL BUTTON pressed")
        pygame.mixer.stop()


class PauseUnpauseAll(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["width"] = 20
        self["height"] = 2
        self["text"] = "PAUSE ALL"
        self["command"] = self.pause_unpause_all
        self.state = True

    def pause_unpause_all(self) -> None:
        if self.state:
            logging.info(f"PAUSE ALL")
            pygame.mixer.pause()
            self.state = False
        else:
            logging.info(f"UNPAUSE ALL")
            pygame.mixer.unpause()
            self.state = True


class FadeoutAll(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["width"] = 20
        self["height"] = 2
        self["text"] = "FADEOUT ALL"
        self["command"] = self.fadeout_all

    def fadeout_all(self) -> None:
        logging.info(f"FADEOUT ALL BUTTON pressed")
        pygame.mixer.fadeout(2000)


# Get rid of Menu classes, and put them in a AppWindow
# To much unnecessary code


class MenuBar(tkinter.Menu):
    def __init__(self):
        tkinter.Menu.__init__(self)
        self.create_file_menu()

    def create_file_menu(self):
        self.add_cascade(label="File", menu=File())
        self.add_cascade(label="View", menu=View())
        self.add_cascade(label="Help", menu=Help())


class File(MenuBar):
    file_list = []

    def __init__(self):
        tkinter.Menu.__init__(self, tearoff=0)
        self.file_menu()
        self.file_list.append(self)

    def file_menu(self):
        self.add_command(label="Open Project", command=OpenProjectButton.open_project)
        self.add_command(label="Save Project", command=SaveProjectButton.save_project)
        # self.add_command(label="Settigns", command=SettingsWindow)
        self.add_command(label="Settigns", command=_open_settings)
        self.add_separator()


class View(MenuBar):
    def __init__(self):
        tkinter.Menu.__init__(self, tearoff=0)
        self.settings_state = SHOW_SETTINGS
        self.view_menu()

    def view_menu(self):
        if self.settings_state:
            settings_label = "✓ Show settings"
        else:
            settings_label = "  Show settings"
        self.add_command(label=settings_label, command=self.toggle_settings_frame)

    def toggle_settings_frame(self):
        logging.debug(f"settings state: {self.settings_state}")
        if self.settings_state:
            self.settings_state = False
            self.entryconfigure(1, label="  Show settings")
        else:
            self.settings_state = True
            self.entryconfigure(1, label="✓ Show settings")

        settings_frame = SettingsFrame.settings_frame_list[0]

        return (
            settings_frame.show_frame()
            if self.settings_state
            else settings_frame.hide_frame()
        )


class Help(MenuBar):
    def __init__(self):
        tkinter.Menu.__init__(self, tearoff=0)
        self.help_menu()

    def help_menu(self):
        self.add_command(label="Help", command=HelpWindow)
        self.add_command(
            label="More info", command=lambda: webbrowser.open_new_tab(github)
        )


class ButtonFrame(tkinter.Frame):
    BUTTONS_VALUES = [
        (1, [(1, 7), (6, 8), (11, 9)]),
        (3, [(1, 4), (6, 5), (11, 6)]),
        (5, [(1, 1), (6, 2), (11, 3)]),
    ]

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.create_buttons()

    def create_buttons(self):
        for row, values in self.BUTTONS_VALUES:
            for col, val in values:
                pad_btn = PadButton(self, val)
                pad_btn.grid(row=row, column=col, columnspan=4, sticky=tkinter.NSEW)

                volume_bar = VolumeBar(self)
                volume_bar.grid(row=row, column=col + 4, sticky=tkinter.NSEW)

                open_btn = OpenButton(self)
                open_btn.grid(row=row + 1, column=col, sticky=tkinter.NSEW)

                stop_btn = StopButton(self)
                stop_btn.grid(row=row + 1, column=col + 1, sticky=tkinter.NSEW)

                pause_btn = PauseButton(self)
                pause_btn.grid(row=row + 1, column=col + 2, sticky=tkinter.NSEW)

                play_btn = PlayButton(self)
                play_btn.grid(row=row + 1, column=col + 3, sticky=tkinter.NSEW)

                loop_check_box = LoopCheckBox(self)
                loop_check_box.grid(row=row + 1, column=col + 4, sticky=tkinter.NSEW)

        stop_all_btn = StopAll(self)
        stop_all_btn.grid(row=7, column=1, columnspan=5, sticky=tkinter.NSEW)

        pause_unpause_all_btn = PauseUnpauseAll(self)
        pause_unpause_all_btn.grid(row=7, column=6, columnspan=5, sticky=tkinter.NSEW)

        fadeout_all_btn = FadeoutAll(self)
        fadeout_all_btn.grid(row=7, column=11, columnspan=5, sticky=tkinter.NSEW)


class SettingsFrame(tkinter.Frame):
    settings_frame_list = []

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.create_buttons()
        self.settings_frame_list.append(self)

    def create_buttons(self):
        StopAll(self).grid(row=0)
        PauseUnpauseAll(self).grid(row=1)
        FadeoutAll(self).grid(row=2)

    def show_frame(self):
        logging.debug(f"Show settings frame")
        return self.grid(row=0, column=1, sticky=tkinter.NSEW)

    def hide_frame(self):
        logging.debug(f"Hide settings frame")
        return self.grid_forget()


class HelpWindow(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title("Help")
        self.resizable(width=False, height=False)
        self.help_label = tkinter.Label(
            self, text=utils.help_message, justify=tkinter.LEFT
        )
        self.help_label.pack()


class SettingsWindow(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title("Settings")
        self.resizable(width=False, height=False)
        self.help_label = tkinter.Label(
            self, text="TODO: Settings here", justify=tkinter.LEFT
        )
        self.help_label.pack()


class AppWindow(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title("Sound Pad")
        self.resizable(width=False, height=False)
        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.settings_frame = SettingsFrame(self)
        self.filemenu = MenuBar()
        if SHOW_SETTINGS:
            self.settings_frame.show_frame()
        # General keybindings
        self.bind("<Control-Key-o>", lambda event: OpenProjectButton.open_project())
        self.bind("<Control-Key-s>", lambda event: SaveProjectButton.save_project())
        # To change
        File.file_list[0].add_command(label="Exit", command=self.destroy)
        self.config(menu=self.filemenu)


def run() -> None:
    """Main Program Function"""
    pygame.mixer.init()
    pygame.mixer.set_num_channels(NUM_CHANNELS)
    app = AppWindow()
    app.mainloop()


if __name__ == "__main__":
    run()
