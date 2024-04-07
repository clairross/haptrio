## Documentation

### Processing (py5)

[py5 module](http://py5coding.org/)

### Haply 2DIY

[Source Code](https://gitlab.com/Haply/public/python_samples)

[Pyhapi repository](https://gitlab.com/Haply/2diy/pyhapi)

[Pyhapi repository - source code](https://gitlab.com/Haply/2diy/pyhapi/-/blob/master/src/HaplyHAPI.py?ref_type=heads)

## Setup

### Setting Up Environment

Create a file called ".env" at the root of the project (it should be in the same folder as `main.py`) and put add the following information:

```
{
    "port": "COM6", // Enter the string for the device you want to connect to. This likely starts with "COM"
    "debug_mode": false, // Turning this on will use more resources but display extra information, make sure it is off when demoing
    "keyboard_enabled": false, // This allows control of the player with the keyboard instead of the Haply. Can be used for testing purposes but should remain off otherwise
    "mouse_enabled": false, // This allows control of the player with the mouse instead of the Haply. Can be used for testing purposes but should remain off otherwise
    "flip_y_haply": false // this flips the y-axis input for the haply since some of them are set up differently
}
```

This file is not added to the repository since it is unique to each physical machine.

#### Installing Dependencies

Download and install Python (version 3.12 and up) and a Python package manager, such as `conda` or `pip`.

To install `pip`, in the command line use

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
rm .\get-pip.py
```

Then type `pip help` to check that it worked. It should show a list of commands. If so, install the following dependencies using the `pip install *` command, replacing `*` with the following:

- `py5`, Python support of [Processing 5](http://py5coding.org/).
- `HaplyHAPI` - The Python implementation of hAPI, [Pyhapi](https://gitlab.com/Haply/2diy/pyhapi/-/tree/master).
- `ujson` - A faster library than the built-in `json` which allows the reading of `.json` files from the computer.
- `pygame` - Uses the `pygame.mixer` module to play audio in multiple channels.
- `install-jdk` - The Java Development Kit for Python, which allows the use of Processing, which is originally based in Java.

To install the right version of Java use `python -c "import jdk; print('Java installed to', jdk.install('17'))"`

### Running in VSCode

When running in VSCode, press `F5` to start the program. Debugging is set up, and breakpoints should work.
