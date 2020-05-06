import tkinter
import tkinter.filedialog
import os
import pygame
import keyboard
from modules.audio import SoundMusic, BackgroundMusic


FONT = ('Helvetica', '10')
# BTN_FONT = ('Helvetica', '15')
LENGTH = 30

BUTTONS_NR = 9


sounds_lst = [None for _ in range(BUTTONS_NR)]


def open_file(num):
    initial_directory = os.path.join('sounds')
    title = "Select A File"
    file_types = [('wav files', '*.wav'), ('All files', '*.*')]
    file_path = tkinter.filedialog.askopenfilename(
        initialdir=initial_directory, title=title, filetypes=file_types)
    if file_path:
        sounds_lst[num] = SoundMusic(file_path)
        _lbl_update(num, file_path)
        _btn_update(num, file_path)
        hotkey = f"{num+1}"
        keyboard.add_hotkey(hotkey, lambda: play_file(num))


def play_file(num):
    sound_file = sounds_lst[num]
    if isinstance(sound_file, SoundMusic):
        sound_file.play()


def stop_file(num):
    sound_file = sounds_lst[num]
    if isinstance(sound_file, SoundMusic):
        sound_file.stop()


def _lbl_update(num, text):
    global file_names
    global right_middle_frame
    lbl_text = os.path.split(text)[1][:LENGTH]
    file_names[num].set(lbl_text)
    right_middle_frame.update_idletasks()


def _btn_update(num, text):
    global buttons_values_list
    global left_frame
    btn_text = os.path.split(text)[1][:LENGTH]
    buttons_values_list[num].set(btn_text)
    left_frame.update_idletasks()


def pause_file(num):
    pass


def open_project():
    pass


def save_project():
    pass


def apply_changes():
    pass


def main():
    global file_names
    global buttons_values_list
    global right_middle_frame
    global left_frame
    global buttons_list

    pygame.mixer.init()
    # Tkinter
    root = tkinter.Tk()
    root.title('Sound Pad')
    root.resizable(width=0, height=0)

    # Images
    play_img = tkinter.PhotoImage(file="images/play.png")
    stop_img = tkinter.PhotoImage(file="images/stop.png")
    pause_img = tkinter.PhotoImage(file="images/pause.png")

    # Creating frames
    left_frame = tkinter.LabelFrame(root)
    right_frame = tkinter.LabelFrame(root)
    # frm_right_up = tkinter.LabelFrame(right_frame)
    right_middle_frame = tkinter.LabelFrame(right_frame)
    right_down_frame = tkinter.LabelFrame(right_frame)

    left_frame.grid(row=0, column=0, sticky=tkinter.NSEW)
    right_frame.grid(row=0, column=1, sticky=tkinter.NSEW)
    # frm_right_up.grid(row=0, column=0, sticky=tkinter.NSEW)
    right_middle_frame.grid(row=1, column=0, sticky=tkinter.NSEW)
    right_down_frame.grid(row=2, column=0, sticky=tkinter.NSEW)

    # Initializiny 9 buttons in given panel (frame object)
    BUTTONS_VALUES = [
        [(tkinter.StringVar(), 7), (tkinter.StringVar(), 8), (tkinter.StringVar(), 9)],
        [(tkinter.StringVar(), 4), (tkinter.StringVar(), 5), (tkinter.StringVar(), 6)],
        [(tkinter.StringVar(), 1), (tkinter.StringVar(), 2), (tkinter.StringVar(), 3)]
    ]

    buttons_values_list = [
        BUTTONS_VALUES[2][0][0],
        BUTTONS_VALUES[2][1][0],
        BUTTONS_VALUES[2][2][0],
        BUTTONS_VALUES[1][0][0],
        BUTTONS_VALUES[1][1][0],
        BUTTONS_VALUES[1][2][0],
        BUTTONS_VALUES[0][0][0],
        BUTTONS_VALUES[0][1][0],
        BUTTONS_VALUES[0][2][0],
    ]

    BUTTONS_VALUES[0][0][0].set(7),
    BUTTONS_VALUES[0][1][0].set(8),
    BUTTONS_VALUES[0][2][0].set(9),
    BUTTONS_VALUES[1][0][0].set(4),
    BUTTONS_VALUES[1][1][0].set(5),
    BUTTONS_VALUES[1][2][0].set(6),
    BUTTONS_VALUES[2][0][0].set(1),
    BUTTONS_VALUES[2][1][0].set(2),
    BUTTONS_VALUES[2][2][0].set(3)

    buttons_list = []
    for row, values in enumerate(BUTTONS_VALUES):
        for col, val in enumerate(values):
            button = tkinter.Button(left_frame, width=20, height=10, textvariable=val[0],
                                    command=lambda i=val[1]-1: play_file(i))
            button.grid(row=row, column=col, sticky=tkinter.NSEW)
            buttons_list.append(button)

    # Create No. lables
    for no in range(BUTTONS_NR):
        lbl = tkinter.Label(right_middle_frame, text=f"{no+1}. ", font=FONT)
        lbl.grid(row=no+1, column=0, sticky=tkinter.NSEW)

    # Create file names lables
    file_names = [tkinter.StringVar() for _ in range(BUTTONS_NR)]
    for var in file_names:
        var.set("  "*LENGTH)

    for row, text in enumerate(file_names):
        tkinter.Label(right_middle_frame, textvariable=text, background='white', anchor=tkinter.W, font=FONT).grid(
            row=row+1, column=1, sticky=tkinter.NSEW)

    # Create Radio buttons
    values = [tkinter.StringVar() for _ in range(BUTTONS_NR)]
    for _ in values:
        _.set(0)
    modes = ['sound', 'music']

    for row, var in enumerate(values):
        for val, mode in enumerate(modes):
            tkinter.Radiobutton(right_middle_frame, variable=var,
                                value=val, text=mode).grid(row=row+1, column=val+2)

    # Create Check Buttons
    cbtns = [
        tkinter.Checkbutton(right_middle_frame) for i in range(BUTTONS_NR)
    ]
    for row, btn in enumerate(cbtns):
        btn.grid(row=row+1, column=4, sticky=tkinter.NSEW)

    # Create Open File Buttons
    btns_open_file = [
        tkinter.Button(right_middle_frame, text="Open File", font=FONT, command=lambda i=i: open_file(i)) for i in range(BUTTONS_NR)
    ]
    for row, btn in enumerate(btns_open_file):
        btn.grid(row=row+1, column=5, sticky=tkinter.NSEW)

     # Create Play Buttons
    btns_play = [
        tkinter.Button(right_middle_frame, text="Play", image=play_img, width=25, font=FONT, command=lambda i=i: play_file(i)) for i in range(BUTTONS_NR)
    ]
    for row, btn in enumerate(btns_play):
        btn.grid(row=row+1, column=8, sticky=tkinter.NSEW)

    # Create Stop Buttons
    btns_stop = [
        tkinter.Button(right_middle_frame, text="Stop", image=stop_img, font=FONT, width=25, command=lambda i=i: stop_file(i)) for i in range(BUTTONS_NR)
    ]
    for row, btn in enumerate(btns_stop):
        btn.grid(row=row+1, column=6, sticky=tkinter.NSEW)

     # Create Pause Buttons
    btns_pause = [
        tkinter.Button(right_middle_frame, text="Pause", image=pause_img, width=25, font=FONT, command=lambda i=i: pause_file(i)) for i in range(BUTTONS_NR)
    ]
    for row, btn in enumerate(btns_pause):
        btn.grid(row=row+1, column=7, sticky=tkinter.NSEW)

    # lbl_info = tkinter.Label(
    #     frm_right_up, text="Informaciones", width=50, height=4)
    # lbl_info.grid(row=0, column=0, sticky=tkinter.NSEW)

    # Settings
    btn_apply = tkinter.Button(
        right_down_frame, text="Apply", font=FONT)
    btn_open_project = tkinter.Button(
        right_down_frame, text="Open Project", font=FONT)
    btn_save_project = tkinter.Button(
        right_down_frame, text="Save Project", font=FONT)

    btn_apply.grid(row=0, column=2, sticky=tkinter.NSEW)
    btn_open_project.grid(row=0, column=0, sticky=tkinter.NSEW)
    btn_save_project.grid(row=0, column=1, sticky=tkinter.NSEW)

    root.mainloop()
    pygame.QUIT


if __name__ == "__main__":
    main()
