# import playsound
import tkinter
import tkinter.filedialog
import os
import pygame
from modules.audio import SoundMusic

FONT = ('Helvetica', '10')
# BTN_FONT = ('Helvetica', '15')
LENGTH = 30

BUTTONS_NR = 9

BUTTONS = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3]
]

sounds = [None for _ in range(9)]


def set_pad_btns(panel):
    """Initializiny 9 buttons in given panel (frame object)
    """
    btns = [[tkinter.Button(panel, width=20, height=10)
             for i in range(3)] for i in range(3)]

    for i in range(1, len(btns) + 1):
        for j in range(len(btns[i - 1])):
            btns[i-1][j].grid(row=i, column=j, sticky=tkinter.NSEW)


def open_file(num):
    initial_directory = os.path.join('.')
    title = "Select A File"
    file_types = (('wav files', '*.wav'), ('All files', '*.*'))
    file_path = tkinter.filedialog.askopenfilename(
        initialdir=initial_directory, title=title, filetype=file_types)
    if file_path:
        sounds[num] = SoundMusic(file_path)
        _lbl_update(num, file_path)


def play_file(num):
    sound_file = sounds[num]
    if isinstance(sound_file, SoundMusic):
        sound_file.play()


def stop_file(num):
    sound_file = sounds[num]
    if isinstance(sound_file, SoundMusic):
        sound_file.stop()


def pause_file(num):
    pass


def _lbl_update(num, text):
    global file_names
    global frm_right_middle
    sound_name = os.path.split(text)[1][:LENGTH]+"..."
    file_names[num].set(sound_name)
    frm_right_middle.update_idletasks()


def main():
    global file_names
    global frm_right_middle

    pygame.init()
    # Tkinter
    root = tkinter.Tk()
    root.title('Sound Pad')
    root.resizable(width=0, height=0)

    # Images
    play = tkinter.PhotoImage(file="images/play.png")
    stop = tkinter.PhotoImage(file="images/stop.png")
    pause = tkinter.PhotoImage(file="images/pause.png")

    # Creating frames
    frm_left = tkinter.LabelFrame(root)
    frm_right = tkinter.LabelFrame(root)
    # frm_right_up = tkinter.LabelFrame(frm_right)
    frm_right_middle = tkinter.LabelFrame(frm_right)
    frm_right_down = tkinter.LabelFrame(frm_right)

    frm_left.grid(row=0, column=0, sticky=tkinter.NSEW)
    frm_right.grid(row=0, column=1, sticky=tkinter.NSEW)
    # frm_right_up.grid(row=0, column=0, sticky=tkinter.NSEW)
    frm_right_middle.grid(row=1, column=0, sticky=tkinter.NSEW)
    frm_right_down.grid(row=2, column=0, sticky=tkinter.NSEW)

    # initializing buttons
    set_pad_btns(frm_left)

    # Legend:

    # Create No. Lables
    for no in range(1, 10):
        lbl = tkinter.Label(frm_right_middle, text=f"{no}. ", font=FONT)
        lbl.grid(row=no, column=0, sticky=tkinter.NSEW)

    # Create Title File Labels
    file_names = [tkinter.StringVar() for _ in range(9)]
    for var in file_names:
        var.set("  "*LENGTH)

    for row, text in enumerate(file_names):
        tkinter.Label(frm_right_middle, textvariable=text, background='white', anchor=tkinter.W, font=FONT).grid(
            row=row+1, column=1, sticky=tkinter.NSEW)

    # lbl_title = [
    #     tkinter.Label(frm_right_middle, text=' '*25, background='white', font=FONT) for i in range(9)
    # ]
    # for row, btn in enumerate(lbl_title):
    #     btn.grid(row=row+1, column=1, sticky=tkinter.NSEW)

    # Create Radio buttons

    values = [tkinter.StringVar() for _ in range(9)]
    for _ in values:
        _.set(0)
    modes = ['sound', 'music']

    for row, var in enumerate(values):
        for val, mode in enumerate(modes):
            tkinter.Radiobutton(frm_right_middle, variable=var,
                                value=val, text=mode).grid(row=row+1, column=val+2)

    # Create Check Buttons
    cbtns = [
        tkinter.Checkbutton(frm_right_middle) for i in range(9)
    ]
    for row, btn in enumerate(cbtns):
        btn.grid(row=row+1, column=4, sticky=tkinter.NSEW)

    # Create Open File Buttons
    btns_open_file = [
        tkinter.Button(frm_right_middle, text="Open File", font=FONT, command=lambda i=i: open_file(i)) for i in range(9)
    ]
    for row, btn in enumerate(btns_open_file):
        btn.grid(row=row+1, column=5, sticky=tkinter.NSEW)

     # Create Play Buttons
    btns_play = [
        tkinter.Button(frm_right_middle, text="Play", image=play, width=25, font=FONT, command=lambda i=i: play_file(i)) for i in range(9)
    ]
    for row, btn in enumerate(btns_play):
        btn.grid(row=row+1, column=8, sticky=tkinter.NSEW)

    # Create Stop Buttons
    btns_stop = [
        tkinter.Button(frm_right_middle, text="Stop", image=stop, font=FONT, width=25, command=lambda i=i: stop_file(i)) for i in range(9)
    ]
    for row, btn in enumerate(btns_stop):
        btn.grid(row=row+1, column=6, sticky=tkinter.NSEW)

     # Create Pause Buttons
    btns_pause = [
        tkinter.Button(frm_right_middle, text="Pause", image=pause, width=25, font=FONT, command=lambda i=i: pause_file(i)) for i in range(9)
    ]
    for row, btn in enumerate(btns_pause):
        btn.grid(row=row+1, column=7, sticky=tkinter.NSEW)

    # lbl_info = tkinter.Label(
    #     frm_right_up, text="Informaciones", width=50, height=4)
    # lbl_info.grid(row=0, column=0, sticky=tkinter.NSEW)

    # Settings
    btn_apply = tkinter.Button(
        frm_right_down, text="Apply", font=FONT)
    btn_open_project = tkinter.Button(
        frm_right_down, text="Open Project", font=FONT)
    btn_save_project = tkinter.Button(
        frm_right_down, text="Save Project", font=FONT)

    btn_apply.grid(row=0, column=2, sticky=tkinter.NSEW)
    btn_open_project.grid(row=0, column=0, sticky=tkinter.NSEW)
    btn_save_project.grid(row=0, column=1, sticky=tkinter.NSEW)

    root.mainloop()
    pygame.QUIT


if __name__ == "__main__":
    main()
