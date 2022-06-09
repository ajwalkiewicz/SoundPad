# Simple Sound Pad

Simple sound pad inspired by real professional sound pads. It allows to ascribe music file to the button and play it by pressing the button or key on keyboard.

As a big fun of tabletop RPGs and the game master I felt the urge to have such a program, but I could not find anything similar to it. 

So I created it.

It was also my side project while I was learning python. That is why some more advanced in python people may find totally unnecessary pieces of code in the source code, eg. abstract base class in audio module.

I am aware of that, but I am not going to change this as I believe that it is better to have program with some mistakes in the code then to have a perfect program that does not exist.

Please Notice that the program is still during the development process, therefore some feature may not work properly or at all, eg. pause button. 

If you are among the people that also need such a program please feel welcome to use it.

## Table of Contents

- [About Project](#simple-sound-pad)
- [Table of Contents](#table-of-contents)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Build With](#built-with)
- [TODO](#todo)
- [Author](#authors)
- [License](#license)

## Getting Started

### Prerequisites

*  [Python 3.6](https://www.python.org/download/releases/3.0/) or higher.
*  [pip](https://pip.pypa.io/en/stable/) - python package installer

#### Ubuntu

Necessery libraries:
```
python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev
```

Install
```bash
sudo apt install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev
```
  
### Installing

1. Clone or download repository
2. In the downloaded loaction run the following commands:

#### Windows

```bash
pip install -r requirements.txt
```

To run the program type:

```bash
python soundpad.py
```

#### Linux

```bash
pip3 install -r requirements.txt
```

To run the program type:

```
python3 soundpad.py
```

## Usage

![Screenshot image](https://github.com/ajwalkiewicz/sound-pad/blob/master/image.png)

### Features

1. 9 different sound tracks
2. Each track can be controlled separatly
3. Key bindings for each track
4. Saving projects


### Settings

Settings can be change in: `module/data/settings/json`

```json
{
    "default_directory": "samples", 
    "key_range": "system_wide",    // or "inside_app"
    "font_type": "Helvetica",
    "font_size": 10,
    "show_settings": false,        // DEPRECATED
    "fadeout_length": 2000         // fadeout in miliseconds    
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

* [Pygame](https://www.pygame.org/docs/) - set of Python modules designed for writing video games
* [Tkinter](https://docs.python.org/3/library/tk.html) - Python module for GUI
* [keyboard](https://pypi.org/project/keyboard/) - Python library for keyboard control
* [pynput](https://pypi.org/project/pynput/) - Python library for keyboard control 
* [Open Iconic v1.1.1](https://github.com/iconic/open-iconic) - open source sibling of Iconic

## TODO

- [x] Play-pause feature.
- [x] Set the volume of each audio track individally.
- [ ] Show the progress of the each audio track.
- [ ] Looping files doesn't require playing sound again 

## Author

* **Adam Walkiewicz**

## License

### Music

All the audio samples used in this project are under  [Creative Commons 0 License](https://creativecommons.org/publicdomain/zero/1.0/).

Files were downloaded from https://freesound.org/

- 149022__foxen10__train.wav
- 155346__mario1298__street-old-town-of-rhodes.wav
- 267128__contramundum__stepping-down-into-the-dungeon.mp3
- 424792__bolkmar__town-bells.wav
- 580442__bennynz__dungeon-lock-2.wav
- 581491__carthny__thunder-rush-28-july-2021.wav

### SoundPad
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
