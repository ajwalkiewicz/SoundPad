import tkinter
import tkinter.filedialog
import pygame
import os
import keyboard
from modules.audio import SoundMusic, BackgroundMusic

NUMBER_OF_BUTTONS = 9
sounds_list = [None for _ in range(NUMBER_OF_BUTTONS)]

play_img = "images/play.png"
stop_img = "images/stop.png"
pause_img = "images/pause.png"


class Button(tkinter.Button):

    def __init__(self, master=None):
        super().__init__(master)


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
        self["command"] = self.open_file
        OpenButton.buttons_list.append(self)

    def open_file(self):
        initial_directory = os.path.join('sounds')
        title = "Select A File"
        file_types = [('wav files', '*.wav')]
        file_path = tkinter.filedialog.askopenfilename(
            initialdir=initial_directory, title=title, filetypes=file_types)
        if file_path:
            sounds_list[self.nr] = SoundMusic(file_path)
            hotkey = self.key_assigment.get(self.nr+1, "0")
            keyboard.add_hotkey(hotkey, lambda: sounds_list[self.nr].play())
            pad_button_text = os.path.split(file_path)[1]
            PadButton.buttons_list[self.nr].config(text=pad_button_text)


class StopButton(Button):
    buttons_list = []

    def __init__(self, frame=None):
        super().__init__(frame)
        self.frame = frame
        self.nr = len(self.buttons_list)
        self["text"] = "Stop"
        self["width"] = 10
        self["command"] = self.stop_file
        # self["image"] = tkinter.PhotoImage(file=stop_img)
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
        # self["image"] = tkinter.PhotoImage(file=pause_img)
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
        # self["image"] = tkinter.PhotoImage(file="images/play.png")
        self.buttons_list.append(self)

    def play(self):
        if isinstance(sounds_list[self.nr], BackgroundMusic) or isinstance(sounds_list[self.nr], SoundMusic):
            sounds_list[self.nr].play()


class SaveProjectButton(Button):
    pass


class OpenProjectButton(Button):
    pass


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


class AppWindow(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.settings_frame = SettingsFrame(self)
        self.settings_frame.grid(row=0, column=1, sticky=tkinter.NSEW)


if __name__ == "__main__":
    pygame.mixer.init()
    app = AppWindow()

    play_img = tkinter.PhotoImage(file="images/play.png")
    stop_img = tkinter.PhotoImage(file="images/stop.png")
    pause_img = tkinter.PhotoImage(file="images/pause.png")

    app.mainloop()
