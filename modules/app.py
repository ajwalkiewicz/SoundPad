import tkinter
import tkinter.filedialog
import tkinter.messagebox
import pygame
import os
import sys
import logging
import json
from typing import List, Tuple, Dict, Union

import webbrowser
from pynput import keyboard

import modules.utils as utils
from modules.audio import SoundMusic

_THIS_FOLDER: str = os.path.dirname(os.path.abspath(__file__))

FONT: Tuple[str, str] = ("Helvetica", "10")
NUMBER_OF_BUTTONS: int = 9
NUMBER_CHANNELS: int = 9


SYSTEM_WIDE_KEY_MAPPING: Dict[int, str] = {
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

INSIDE_APP_KEY_MAPPING: Dict[int, str] = {
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

global_list_of_sounds: List[Union[SoundMusic, None]] = [
    None for _ in range(NUMBER_OF_BUTTONS)
]

github: str = "https://github.com/ajwalkiewicz/SoundPad"

open_img_path: str = "images/folder-2x.png"
stop_img_path: str = "images/media-stop-2x.png"
pause_img_path: str = "images/media-pause-2x.png"
play_img_path: str = "images/media-play-2x.png"

SETTINGS: str = os.path.join(_THIS_FOLDER, "data", "settings.json")

with open(SETTINGS, "r") as json_file:
    settings: dict = json.load(json_file)
    DEFAULT_DIRECTORY: str = settings["default_directory"]
    KEY_RANGE: str = settings["key_range"]
    FONT: Tuple[str, str] = (settings["font_type"], settings["font_size"])
    SHOW_SETTINGS: bool = settings["show_settings"]
    FADEOUT_LENGTH: int = settings["fadeout_length"]

SYSTEM: str = sys.platform
if SYSTEM == "win32":
    logging.info(f"Detected system: {SYSTEM}. Use Windows configuration")
else:
    logging.info(f"Detected system: {SYSTEM}. Use UNIX configuration")


def open_settings(system: str = SYSTEM) -> int:
    if system == "win32":
        command = SETTINGS
    else:
        command = f"xdg-open {SETTINGS}"
    return os.system(command)


def _bind_key_to_sound(key: int, object: tkinter.Tk) -> None:
    logging.debug(f"Bind key: {key}")
    if KEY_RANGE == "inside_app":
        hotkey = INSIDE_APP_KEY_MAPPING.get(key + 1, "0")
        object.bind(hotkey, lambda event: _play_binded_sound(key))
    if KEY_RANGE == "system_wide":
        hotkey = SYSTEM_WIDE_KEY_MAPPING.get(key + 1, "0")
        keyboard.GlobalHotKeys({hotkey: lambda: _play_binded_sound(key)}).start()


def _play_binded_sound(key: int) -> None:
    try:
        return global_list_of_sounds[key].play()
    except AttributeError:
        logging.debug(f"KEY INACTIVE: {key}")


class VolumeBar(tkinter.Scale):
    volume_bar_list: list = []

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
        # self.set(0.50) # If you want to have default value
        self.volume_bar_list.append(self)

    def set_sound_volume(self, value):
        logging.debug(f"VOLUMEBAR moved. Current value: {value}")
        sound = global_list_of_sounds[self.nr]
        if isinstance(sound, SoundMusic):
            sound.set_volume(float(value))
            logging.info(f"VOLUME set to: {value}")
        else:
            logging.info(f"EMPTY BUTTON")


class LoopCheckBox(tkinter.Checkbutton):
    loop_check_box_list: list = []

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
        sound = global_list_of_sounds[self.nr]
        if isinstance(sound, SoundMusic):
            sound.isloop = self.var.get()
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
    buttons_list: list = []

    def __init__(self, master=None, nr=None):
        super().__init__(master)
        self.master = master
        self.nr = len(self.buttons_list)
        self.state = True
        self["width"] = 20
        self["height"] = 10
        self["command"] = self.play
        self["text"] = str(nr)
        self["wraplength"] = self["width"] * 10
        PadButton.buttons_list.append(self)
        # self._button_list_sort()

    def play(self):
        logging.debug(f"PAD BUTTON pressed, id: {self.nr}")
        sound = global_list_of_sounds[self.nr]
        if isinstance(sound, SoundMusic):
            sound.play()
            logging.info(f"PLAY: {sound.path}")
        else:
            logging.info(f"EMPTY BUTTON")

    # I'm keeping this in case one day I'd like to sort button list
    # def _button_list_sort(self):
    #     """Setting buttons in a right order.
    #     From this order: [0,1,2,3,4,5,6,7,8]
    #     To this order:   [6,7,8,3,4,5,0,1,2]"""
    #     if len(self.buttons_list) == NUMBER_OF_BUTTONS:
    #         self.buttons_list[0], self.buttons_list[6] = self.buttons_list[6], self.buttons_list[0]
    #         self.buttons_list[1], self.buttons_list[7] = self.buttons_list[7], self.buttons_list[1]
    #         self.buttons_list[2], self.buttons_list[8] = self.buttons_list[8], self.buttons_list[2]


class OpenButton(Button):
    buttons_list: list = []

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
            global_list_of_sounds[self.nr] = SoundMusic(self.file_path, self.nr)
            _bind_key_to_sound(self.nr, self.master.master)
            pad_button_text = os.path.split(self.file_path)[1]
            PadButton.buttons_list[self.nr].config(text=pad_button_text)


class StopButton(Button):
    buttons_list: list = []

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
        if isinstance(global_list_of_sounds[self.nr], SoundMusic):
            global_list_of_sounds[self.nr].stop()


class PauseButton(Button):
    buttons_list: list = []

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

    def pause(self) -> None:
        logging.info(f"PAUSE BUTTON pressed, id: {self.nr}")
        if isinstance(global_list_of_sounds[self.nr], SoundMusic):
            global_list_of_sounds[self.nr].play_pause()


class PlayButton(Button):
    buttons_list: list = []

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

    def play(self) -> None:
        logging.info(f"PLAY BUTTON pressed, id: {self.nr}")
        if isinstance(global_list_of_sounds[self.nr], SoundMusic):
            global_list_of_sounds[self.nr].play()


class SaveProjectButton(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["text"] = "Save Project"
        self["command"] = self.save_project

    @staticmethod
    def save_project() -> None:
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
                # sounds_path = [sound.path for sound in global_list_of_sounds]
                sounds_path = list(map(lambda x: x.path if isinstance(x, SoundMusic) else "", global_list_of_sounds))
                sounds_volume = [
                    volume_bar.get() for volume_bar in VolumeBar.volume_bar_list
                ]
                sounds_isloop = [
                    loop_checkbox.var.get()
                    for loop_checkbox in LoopCheckBox.loop_check_box_list
                ]

                sounds_state = {
                    key: {
                        "path": options[0],
                        "volume": options[1],
                        "isloop": options[2],
                    }
                    for key, options in enumerate(
                        zip(sounds_path, sounds_volume, sounds_isloop)
                    )
                }
                logging.debug(sounds_state)
                json.dump(sounds_state, save_file, indent=True)
        except PermissionError:
            logging.debug(f"PERMISSION ERROR. Cannot save file in this directory")
            tkinter.messagebox.showerror(
                title="Permission Error",
                message="You do not have perrmision to save files in this loaction",
            )
        finally:
            save_file.close()


class OpenProjectButton(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["text"] = "Open Project"
        self["command"] = self.open_project

    @staticmethod
    def open_project() -> None:
        logging.info(f"OPEN PROJECT selected")
        initial_directory = os.path.join(".")
        title = "Select Project"
        file_types = [("json files", "*.json"), ("All Files", "*.*")]
        file_path = tkinter.filedialog.askopenfilename(
            initialdir=initial_directory, title=title, filetypes=file_types
        )

        for checkbox in LoopCheckBox.loop_check_box_list:
            checkbox.deselect()

        for volumebar in VolumeBar.volume_bar_list:
            volumebar.set(1)

        if file_path:
            for index, text in enumerate([7, 8, 9, 4, 5, 6, 1, 2, 3]):
                PadButton.buttons_list[index].config(text=str(text))

            with open(file_path, "r") as f:
                settings: dict = json.loads(f.read())
                files_not_found_list: list = []

                for index, sound_details in settings.items():
                    index: int = int(index)
                    path: str = sound_details["path"]
                    volume: float = sound_details["volume"]
                    isloop: int = sound_details["isloop"]

                    if path:
                        try:
                            global_list_of_sounds[index] = SoundMusic(
                                path, index, isloop, volume
                            )
                            _bind_key_to_sound(
                                index,
                                OpenButton.buttons_list[index].master.master,
                            )
                            pad_button_text = os.path.split(path)[1]
                            PadButton.buttons_list[index].config(text=pad_button_text)
                            VolumeBar.volume_bar_list[index].set_sound_volume(volume)
                            VolumeBar.volume_bar_list[index].set(volume)
                            if isloop < 0:
                                LoopCheckBox.loop_check_box_list[index].toggle()
                        except FileNotFoundError:
                            files_not_found_list.append(file_path)
                            logging.exception(f"File not found: {file_path}")
                    else:
                        global_list_of_sounds[index] = None

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
    def __init__(self, frame=None, value=FADEOUT_LENGTH):
        super().__init__(frame)
        self.frame = frame
        self.value = value  # milisecond
        self["width"] = 20
        self["height"] = 2
        self["text"] = "FADEOUT ALL"
        self["command"] = self.fadeout_all

    def fadeout_all(self) -> None:
        logging.info(f"FADEOUT ALL BUTTON pressed, value: {self.value}")
        pygame.mixer.fadeout(self.value)


# Get rid of Menu classes, and put them in a AppWindow
# To much unnecessary code


class MenuBar(tkinter.Menu):
    def __init__(self):
        tkinter.Menu.__init__(self)
        self.create_file_menu()

    def create_file_menu(self) -> None:
        self.add_cascade(label="File", menu=File())
        # Waiting for more options to put in menu bar
        # self.add_cascade(label="View", menu=View())
        self.add_cascade(label="Help", menu=Help())


class File(MenuBar):
    file_list: list = []

    def __init__(self):
        tkinter.Menu.__init__(self, tearoff=0)
        self.file_menu()
        self.file_list.append(self)

    def file_menu(self) -> None:
        self.add_command(label="Open Project", command=OpenProjectButton.open_project)
        self.add_command(label="Save Project", command=SaveProjectButton.save_project)
        # self.add_command(label="Settigns", command=SettingsWindow)
        self.add_command(label="Settigns", command=open_settings)
        self.add_separator()


class View(MenuBar):
    """View menu bar
    Currently not used. Waiting for more options to be put here.
    """

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
    settings_frame_list: list = []

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
    pygame.mixer.set_num_channels(NUMBER_CHANNELS)
    app = AppWindow()
    app.mainloop()


if __name__ == "__main__":
    run()
