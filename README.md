[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

# Simple Sound Pad

Simple sound pad inspired by real professional sound pads. It allows to ascribe music file to the button and play it by pressing the button or key on keyboard.

As a big fun of tabletop RPGs and the game master I felt the urge to have such a program, but I could not find anything similar to it.

So I created it.

It was also my side project while I was learning python. That is why some more advanced in python people may find totally unnecessary pieces of code in the source code, ~~eg. abstract base class in audio module.~~

I am aware of that, but I am not going to change this as I believe that it is better to have program with some mistakes in the code then to have a perfect program that does not exist.

Please Notice that the program is still during the development process, therefore some feature may not work properly or at all, ~~eg. pause button.~~

If you are among the people that also need such a program please feel welcome to use it.

## Table of Contents

- [About Project](#simple-sound-pad)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Build With](#built-with)
- [To do](#todo)
- [Author](#authors)
- [License](#license)

## Installation

### Prerequisites

- [Python 3.6](https://www.python.org/download/releases/3.0/) or higher.
- [pip](https://pip.pypa.io/en/stable/) - python package installer
- [git](https://git-scm.com/) - version control system

### Steps

1. Clone repository

```Bash
git clone https://github.com/ajwalkiewicz/SoundPad.git
```

2. Go to the created directory

```Bash
cd SoundPad
```

3. Follow steps for your operating system

### Windows

4. Install python dependencies

```Bash
pip install -r requirements.txt
```

5. Run program

```Bash
python soundpad.py
```

### Linux

4. Install necessary libraries 

(Ubuntu)

```bash
sudo apt install python-dev python3-tkinter libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev
```

(Fedora)
```bash
sudo dnf install python3-devtools python3-tkinter
```

5. Install python dependencies

```Bash
pip3 install -r requirements.txt
```

6. Run program

```Bash
python3 soundpad.py
```

## Usage

![Screenshot image](https://github.com/ajwalkiewicz/sound-pad/blob/master/image.png)

### Features

1. 9 different sound tracks
2. Each track can be controlled separately
3. Key bindings for each track
4. Saving projects

### Settings

Settings can be change in: `module/data/settings/json`

```javascript
{
    "default_directory": "samples",
    "key_range": "system_wide",    // or "inside_app"
    "font_type": "Helvetica",
    "font_size": 10,
    "show_settings": false,        // DEPRECATED
    "fadeout_length": 2000,        // fadeout in milliseconds
    "on_top": false,               // Always on top when true
    "key_0_behavior": "pause"      // or "stop"
}
```

### Limitations

#### Windows

- Only `"key_range": "system_wide"` works.

#### Mac OS

- Not supported.

#### Linux

- `"key_range": "inside_app"` works only with numerical keyboard.

## Built With

- [Pygame](https://www.pygame.org/docs/) - set of Python modules designed for writing video games
- [Tkinter](https://docs.python.org/3/library/tk.html) - Python module for GUI
- [keyboard](https://pypi.org/project/keyboard/) - Python library for keyboard control
- [pynput](https://pypi.org/project/pynput/) - Python library for keyboard control
- [Open Iconic v1.1.1](https://github.com/iconic/open-iconic) - open source sibling of Iconic

## To Do

- [x] Play-pause feature
- [x] Set the volume of each audio track individually
- [x] Saves include volume and loop status
- [ ] [Show the progress of the each audio](https://github.com/ajwalkiewicz/SoundPad/issues/4)
- [ ] [Looping files doesn't require playing sound again](https://github.com/ajwalkiewicz/SoundPad/issues/5)
- [ ] [Open project directory in the last place where project was saved](https://github.com/ajwalkiewicz/SoundPad/issues/6)

## Author

**Adam Walkiewicz**

## License

### Music

All the audio samples used in this project are under [Creative Commons 0 License](https://creativecommons.org/publicdomain/zero/1.0/).

Files were downloaded from https://freesound.org/

- 149022\_\_foxen10\_\_train.wav
- 155346\_\_mario1298\_\_street-old-town-of-rhodes.wav
- 267128\_\_contramundum\_\_stepping-down-into-the-dungeon.mp3
- 424792\_\_bolkmar\_\_town-bells.wav
- 580442\_\_bennynz\_\_dungeon-lock-2.wav
- 581491\_\_carthny\_\_thunder-rush-28-july-2021.wav

### SoundPad

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
