import tkinter
import tkinter.filedialog
import tkinter.messagebox
import pygame
import os
import logging
import json
import webbrowser
from pynput import keyboard

import modules.utils as utils
from modules.audio import SoundMusic, BackgroundMusic
        
github = "https://github.com/ajwalkiewicz/sound-pad"

FONT = ('Helvetica', '10')
NUMBER_OF_BUTTONS = 9
sounds_list = [None for _ in range(NUMBER_OF_BUTTONS)]

open_img_path = "images/folder-2x.png"
stop_img_path = "images/media-stop-2x.png"
pause_img_path = "images/media-pause-2x.png"
play_img_path = "images/media-play-2x.png"


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
        self["command"] = self.play_stop
        self["text"] = str(nr)
        PadButton.buttons_list.append(self)
        # self._button_list_sort()

    def play_stop(self):
        if isinstance(sounds_list[self.nr], BackgroundMusic):
            if self.state:
                sounds_list[self.nr].play()
                self.state = False
            else:
                sounds_list[self.nr].stop()
                self.state = True

        if isinstance(sounds_list[self.nr], SoundMusic):
            sounds_list[self.nr].play()

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
    key_assigment = {
        1: "7", 2: "8", 3: "9",
        4: "4", 5: "5", 6: "6",
        7: "1", 8: "2", 9: "3"
    }

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
        initial_directory = os.path.join('sounds')
        title = "Select A File"
        file_types = [('wav files', '*.wav')]
        self.file_path = tkinter.filedialog.askopenfilename(
            initialdir=initial_directory, title=title, filetypes=file_types)
        if self.file_path:
            sounds_list[self.nr] = SoundMusic(self.file_path)
            hotkey = self.key_assigment.get(self.nr+1, "0")
            keyboard.GlobalHotKeys({hotkey: lambda: sounds_list[self.nr].play()}).start()
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
        if isinstance(sounds_list[self.nr], SoundMusic):
            sounds_list[self.nr].stop()


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
        if isinstance(sounds_list[self.nr], BackgroundMusic):
            sounds_list[self.nr].pause()


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
        logging.info(f"Play button used, id: {self.nr}")
        if isinstance(sounds_list[self.nr], BackgroundMusic) or isinstance(sounds_list[self.nr], SoundMusic):
            sounds_list[self.nr].play()


class SaveProjectButton(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["text"] = "Save Project"
        self["command"] = self.save_project

    @staticmethod
    def save_project():
        initial_directory = os.path.join('.')
        title = "Save Project"
        file_types = [('json files', '*.json'), ("All Files", "*.*")]
        try:
            save_file = tkinter.filedialog.asksaveasfile(
                mode="w", initialdir=initial_directory, title=title, filetypes=file_types, defaultextension=".json")
            if hasattr(save_file, 'write'):
                config = {key: button.file_path for key,
                          button in enumerate(OpenButton.buttons_list)}
                json.dump(config, save_file)
                save_file.close()
        except PermissionError:
            tkinter.messagebox.showerror(
                title="Permission Error", message="You do not have perrmision to save files in this loaction")


class OpenProjectButton(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["text"] = "Open Project"
        self["command"] = self.open_project

    @staticmethod
    def open_project():
        initial_directory = os.path.join('.')
        title = "Select Project"
        file_types = [('json files', '*.json'), ("All Files", "*.*")]
        file_path = tkinter.filedialog.askopenfilename(
            initialdir=initial_directory, title=title, filetypes=file_types)

        if file_path:
            # if keyboard._hotkeys:
                # keyboard.remove_all_hotkeys()

            for position, text in enumerate([7, 8, 9, 4, 5, 6, 1, 2, 3]):
                PadButton.buttons_list[position].config(text=str(text))
                sounds_list[position] = None

            with open(file_path, "r") as read_file:
                data = json.loads(read_file.read())
                files_not_found_list = []
                for key, item in data.items():
                    if item is not None:
                        try:
                            sounds_list[int(key)] = SoundMusic(item)
                            pad_button_text = os.path.split(item)[1]
                            hotkey = OpenButton.key_assigment.get(
                                int(key)+1, "0")
                            keyboard.GlobalHotKeys({
                                hotkey: lambda key=int(key): sounds_list[key].play()
                                }).start()
                            PadButton.buttons_list[int(key)].config(
                                text=pad_button_text)
                        except FileNotFoundError:
                            files_not_found_list.append(item)

            if files_not_found_list:
                message = "The following files could not be found: \n"
                for nr, text in enumerate(files_not_found_list):
                    message += f"\n{nr+1}. {text}"
                tkinter.messagebox.showerror(
                    title="Missing Files", message=message)


class StopAll(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["height"] = 2
        self["text"] = "Stop All"
        self["command"] = self.stop_all

    def stop_all(self) -> None:
        pygame.mixer.stop()


class PauseAll(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["height"] = 2
        self["text"] = "Pause All"
        self["command"] = self.pause_all

    def pause_all(self) -> None:
        pygame.mixer.pause()


class UnpauseAll(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["height"] = 2
        self["text"] = "Unpause All"
        self["command"] = self.unpause_all

    def unpause_all(self) -> None:
        pygame.mixer.unpause()


class FadeoutAll(Button):
    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self["height"] = 2
        self["text"] = "Fadeout All"
        self["command"] = self.fadeout_all

    def fadeout_all(self) -> None:
        pygame.mixer.fadeout(2000)


# Get rid of Menu classes, and put them in a AppWindow
# To much unnecessary code


class MenuBar(tkinter.Menu):
    def __init__(self):
        tkinter.Menu.__init__(self)
        self.create_file_menu()

    def create_file_menu(self):
        self.add_cascade(label="File", menu=File())
        self.add_cascade(label="Help", menu=Help())


class File(MenuBar):
    file_list = []

    def __init__(self):
        tkinter.Menu.__init__(self, tearoff=0)
        self.file_menu()
        self.file_list.append(self)

    def file_menu(self):
        self.add_command(label="Open Project",
                         command=OpenProjectButton.open_project)
        self.add_command(label="Save Project",
                         command=SaveProjectButton.save_project)
        self.add_separator()


class Help(MenuBar):
    def __init__(self):
        tkinter.Menu.__init__(self, tearoff=0)
        self.help_menu()

    def help_menu(self):
        self.add_command(label="Help", command=HelpWindow)
        self.add_command(label="More info",
                         command=lambda: webbrowser.open_new_tab(github))


class ButtonFrame(tkinter.Frame):
    BUTTONS_VALUES = [
        (1, [(1, 7), (6, 8), (10, 9)]),
        (3, [(1, 4), (6, 5), (10, 6)]),
        (5, [(1, 1), (6, 2), (10, 3)])
    ]

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.create_buttons()

    def create_buttons(self):
        for row, values in self.BUTTONS_VALUES:
            for col, val in values:
                button = PadButton(self, val)
                button.grid(row=row, column=col,
                            columnspan=4, sticky=tkinter.NSEW)

                btn = OpenButton(self)
                btn.grid(row=row+1, column=col, sticky=tkinter.NSEW)

                stop_btn = StopButton(self)
                stop_btn.grid(row=row+1, column=col+1, sticky=tkinter.NSEW)

                pause_btn = PauseButton(self)
                pause_btn.grid(row=row+1, column=col+2, sticky=tkinter.NSEW)

                play_btn = PlayButton(self)
                play_btn.grid(row=row+1, column=col+3, sticky=tkinter.NSEW)


class SettingsFrame(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master = master
        # self.create_buttons()

    def create_buttons(self):
        # SaveProjectButton(self).grid(row=0)
        # OpenProjectButton(self).grid(row=1)
        StopAll(self).grid(row=0)
        PauseAll(self).grid(row=1)
        UnpauseAll(self).grid(row=2)
        FadeoutAll(self).grid(row=3)
        pass

class HelpWindow(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title("Help")
        self.resizable(width=False, height=False)
        self.help_label = tkinter.Label(
            self, text=utils.help_message, justify=tkinter.LEFT)
        self.help_label.pack()


class AppWindow(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title("Sound Pad")
        self.resizable(width=False, height=False)
        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.settings_frame = SettingsFrame(self)
        self.settings_frame.grid(row=0, column=1, sticky=tkinter.NSEW)
        self.filemenu = MenuBar()
        # To change
        File.file_list[0].add_command(label="Exit", command=self.destroy)
        self.config(menu=self.filemenu)


def run() -> None:
    """Main Program Function"""
    pygame.mixer.init()
    app = AppWindow()
    app.mainloop()

if __name__ == "__main__":
    run()
