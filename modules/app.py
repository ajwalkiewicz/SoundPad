import json
import logging
import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import webbrowser
from typing import Optional

import pygame
from pynput import keyboard

from modules import settings
from modules.audio import NoSound, Sound
from modules.player import Player
from modules.playlist import Playlist
from modules.settings import Image, PublicConfig, Text

playlist = Playlist(max_sounds=settings.NUMBER_OF_BUTTONS)
global_player = Player(playlist=playlist)


def _bind_key_to_sound(key: int, object_: tkinter.Tk) -> None:
    logging.debug(f"Bind key: {key}")
    hotkey = settings.KEY_MAPPING.get(key + 1)
    if PublicConfig.KEY_RANGE == "inside_app":
        object_.bind(hotkey, lambda event: _play_binded_sound(key))
    if PublicConfig.KEY_RANGE == "system_wide":
        keyboard.GlobalHotKeys({hotkey: lambda: _play_binded_sound(key)}).start()


def _play_binded_sound(key: int) -> None:
    try:
        return global_player.play(key)
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
        global_player.set_volume(self.nr, float(value))


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
        global_player.playlist[self.nr].isloop = self.var.get()


class Button(tkinter.Button):
    def __init__(self, master=None):
        super().__init__(master)
        self["width"] = 25
        self["height"] = 25
        self["font"] = PublicConfig.FONT


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
        global_player.play(self.nr)

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
        icon = tkinter.PhotoImage(file=Image.open)
        self["image"] = icon
        self.image = icon
        self.file_path = None
        OpenButton.buttons_list.append(self)

    def open_file(self):
        logging.info(f"OPEN FILE BUTTON pressed, id {self.nr}")
        initial_directory = os.path.join(PublicConfig.DEFAULT_DIRECTORY)
        title = "Select A File"
        file_types = [
            ("wav files", "*.wav"),
            ("mp3 files", "*.mp3"),
            ("all files", "*.*"),
        ]
        self.file_path = tkinter.filedialog.askopenfilename(
            initialdir=initial_directory, title=title, filetypes=file_types
        )
        if self.file_path:
            global_player.playlist[self.nr] = Sound(self.file_path, self.nr)
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
        icon = tkinter.PhotoImage(file=Image.stop)
        self["image"] = icon
        self.image = icon
        self.buttons_list.append(self)

    def stop_file(self):
        logging.info(f"STOP BUTTON pressed, id: {self.nr}")
        global_player.stop(self.nr)


class PauseButton(Button):
    buttons_list: list = []

    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self.nr = len(self.buttons_list)
        self["text"] = "Pause"
        self["command"] = self.pause
        icon = tkinter.PhotoImage(file=Image.pause)
        self["image"] = icon
        self.image = icon
        self.buttons_list.append(self)

    def pause(self) -> None:
        logging.info(f"PAUSE BUTTON pressed, id: {self.nr}")
        global_player.play_pause(self.nr)


class PlayButton(Button):
    buttons_list: list = []

    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self.nr = len(self.buttons_list)
        self["text"] = "Play"
        self["command"] = self.play
        icon = tkinter.PhotoImage(file=Image.play)
        self["image"] = icon
        self.image = icon
        self.buttons_list.append(self)

    def play(self) -> None:
        logging.info(f"PLAY BUTTON pressed, id: {self.nr}")
        global_player.play(self.nr)


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
                sounds_path = global_player.playlist.get_paths()
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
                message="You do not have permission to save files in this location",
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
                try:
                    settings: dict = json.loads(f.read())
                except json.JSONDecodeError:
                    message = (
                        f"SoundPad is not able to read file: {file_path}\n"
                        "Possible reasons:\n"
                        "  - file is not a json file\n"
                        "  - file is incorrectly formated\n"
                        "  - file is empty\n"
                    )
                    tkinter.messagebox.showerror(
                        title="Invalid project file format", message=message
                    )
                    return

                files_not_found_list: list = []

                for index, sound_details in settings.items():
                    index: int = int(index)
                    path: str = sound_details["path"]
                    volume: float = sound_details["volume"]
                    isloop: int = sound_details["isloop"]

                    if path:
                        try:
                            global_player.playlist[index] = Sound(
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
                            files_not_found_list.append(path)
                            logging.exception(f"File not found: {path}")
                    else:
                        global_player.playlist[index] = NoSound()

            global_player.stop_all()

            if files_not_found_list:
                message = "The following files could not be found: \n"
                for nr, text in enumerate(files_not_found_list):
                    message += f"\n{nr+1}. {text}"
                tkinter.messagebox.showerror(title="Missing Files", message=message)


class StopAll(Button):
    def __init__(self, frame=None, pause_unpause_all: "PauseUnpauseAll" = None):
        super().__init__(frame)
        self.frame = frame
        self["width"] = 20
        self["height"] = 2
        self["text"] = "STOP ALL"
        if pause_unpause_all:
            self["command"] = lambda: self.stop_all(pause_unpause_all)
        else:
            self["command"] = self.stop_all

    @staticmethod
    def stop_all(button: "PauseUnpauseAll" = None) -> None:
        logging.info("STOP ALL BUTTON pressed")
        global_player.stop_all()

        if button:
            button["text"] = "PAUSE ALL"
            button.state = True


class PauseUnpauseAll(Button):
    state = True

    state = True

    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["width"] = 20
        self["height"] = 2
        self["text"] = "PAUSE ALL"
        self["command"] = self.pause_unpause_all

    def pause_unpause_all(self) -> None:
        self._pause_unpause_all(self)

    @staticmethod
    def _pause_unpause_all(button: "PauseUnpauseAll") -> bool:
        logging.info("PAUSE ALL BUTTON pressed")

        if not pygame.mixer.get_busy():
            logging.debug("Nothing is playing")
            return PauseUnpauseAll.state

        if PauseUnpauseAll.state:
            logging.debug("PAUSE ALL")
            pygame.mixer.pause()
        else:
            logging.debug("UNPAUSE ALL")
            pygame.mixer.unpause()

        PauseUnpauseAll._change_text(button)
        PauseUnpauseAll._change_state()

        return PauseUnpauseAll.state

    @staticmethod
    def _change_state():
        PauseUnpauseAll.state = not PauseUnpauseAll.state

    @staticmethod
    def _change_text(button: "PauseUnpauseAll"):
        button["text"] = "UNPAUSE ALL" if PauseUnpauseAll.state else "PAUSE ALL"


class FadeoutAll(Button):
    def __init__(self, frame=None, value: Optional[int] = None):
        super().__init__(frame)
        self.frame = frame
        self.value = value or PublicConfig.FADEOUT_LENGTH
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
        self.add_command(
            label="Open Project (Ctrl+o)", command=OpenProjectButton.open_project
        )
        self.add_command(
            label="Save Project (Ctrl+s)", command=SaveProjectButton.save_project
        )
        # self.add_command(label="Settings", command=SettingsWindow)
        self.add_command(label="Settings (Ctrl+/)", command=settings.open_settings)
        self.add_separator()


class View(MenuBar):
    """View menu bar
    Currently not used. Waiting for more options to be put here.
    """

    def __init__(self):
        tkinter.Menu.__init__(self, tearoff=0)
        self.settings_state = PublicConfig.SHOW_SETTINGS
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
            label="More info", command=lambda: webbrowser.open_new_tab(Text.github)
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

        self.pause_unpause_all_btn = PauseUnpauseAll(self)
        self.pause_unpause_all_btn.grid(
            row=7, column=6, columnspan=5, sticky=tkinter.NSEW
        )

        self.stop_all_btn = StopAll(self, self.pause_unpause_all_btn)
        self.stop_all_btn.grid(row=7, column=1, columnspan=5, sticky=tkinter.NSEW)

        self.fadeout_all_btn = FadeoutAll(self)
        self.fadeout_all_btn.grid(row=7, column=11, columnspan=5, sticky=tkinter.NSEW)
        self.fadeout_all_btn = FadeoutAll(self)
        self.fadeout_all_btn.grid(row=7, column=11, columnspan=5, sticky=tkinter.NSEW)


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
            self, text=Text.help_message, justify=tkinter.LEFT
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

        if PublicConfig.SHOW_SETTINGS:
            self.settings_frame.show_frame()

        self.key_mapping = settings.KEY_MAPPING

        # General keybindings
        self.bind("<Control-Key-o>", lambda event: OpenProjectButton.open_project())
        self.bind("<Control-Key-s>", lambda event: SaveProjectButton.save_project())
        self.bind("<Control-Key-slash>", lambda event: settings.open_settings())

        # Bind "0" key
        self.bind_key_0(PublicConfig.KEY_RANGE, PublicConfig.KEY_0_BEHAVIOR)

        # To change
        File.file_list[0].add_command(label="Exit", command=self.destroy)
        self.config(menu=self.filemenu)

    def bind_key_0(self, key_range, kp_0_behavior):
        hotkey = self.key_mapping.get(0)

        action = {
            "inside_app": {
                "pause": self._inside_app_pause,
                "stop": self._inside_app_stop,
            },
            "system_wide": {
                "pause": self._system_wide_pause,
                "stop": self._system_wide_stop,
            },
        }

        action[key_range][kp_0_behavior](hotkey)

    def _system_wide_pause(self, hotkey):
        keyboard.GlobalHotKeys(
            {
                hotkey: lambda: PauseUnpauseAll._pause_unpause_all(
                    self.button_frame.pause_unpause_all_btn
                )
            }
        ).start()

    def _inside_app_pause(self, hotkey):
        self.bind(
            hotkey,
            lambda event: PauseUnpauseAll._pause_unpause_all(
                self.button_frame.pause_unpause_all_btn
            ),
        )

    def _system_wide_stop(self, hotkey):
        keyboard.GlobalHotKeys(
            {hotkey: lambda: StopAll.stop_all(self.button_frame.pause_unpause_all_btn)}
        ).start()

    def _inside_app_stop(self, hotkey):
        self.bind(
            hotkey,
            lambda event: StopAll.stop_all(self.button_frame.pause_unpause_all_btn),
        )


def run() -> None:
    """Main Program Function"""
    pygame.mixer.init()
    pygame.mixer.set_num_channels(settings.NUMBER_OF_CHANNELS)
    app = AppWindow()
    # app.lift()
    app.attributes("-topmost", PublicConfig.IS_ON_TOP)
    app.mainloop()


if __name__ == "__main__":
    run()
