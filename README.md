# TKinter Modern Themes

![](TKinterModernThemes/images/parkdark.jpg)

Tkinter is a powerful UI library included in the python standard library.
Unfortunately, it is hard to customize and looks ugly by default.
This library contains a set of modern themes to improve the look of tkinter.

The themes in this library were developed by rdbende and licensed under the MIT license.
https://github.com/rdbende
This library makes these themes consistent and easier to implement into an existing project.

## Why use themes?
Tkinter looks really ugly be default.

![](TKinterModernThemes/images/notheme.jpg)

These themes look much better, and take the same amount of time to code
because they don't need to be manually customized.

## Included Themes

Each theme has a light and dark mode.

### Park
Park is a modified version of Forest in order to make it consistent
with the other themes. It is inspired by Excel.

![](TKinterModernThemes/images/parkdark.jpg)
![](TKinterModernThemes/images/parklight.jpg)

### Sun-valley
Sun-valley is designed to look like Windows 11.

![](TKinterModernThemes/images/sun-valleydark.jpg)
![](TKinterModernThemes/images/sun-valleylight.jpg)

### Azure
Azure is similar to forest, with a blue as the accent color.

![](TKinterModernThemes/images/azuredark.jpg)
![](TKinterModernThemes/images/azurelight.jpg)

## Installation

`pip install git+https://RobertJN64/TKinterModernThemes`

## Integration

These themes can be added by creating a themed frame.
A theme and mode (dark/light) can be specified.
If you need multiple windows, all but one should be marked as topLevel.


## Example:
```python
import TKinterModernThemes as TKMT

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__(str("TITLE"), str("park"), str("dark"))
        
        #add your widgets here
        self.run()
```

## Setting the theme:

The theme is set by default to "park" with mode "dark". This can be overrided
with parameters in `super().__init__()`

- title: Window title 
- theme: Main theme file. One of (azure / sun-valley / park). Defaults to park.
- mode: Light or dark theme. One of (light / dark). Defaults to dark.
- usecommandlineargs: If this is True (default), the frame checks for params passed into the script
        launch to grab a theme.
- useconfigfile: If this is True (default), the frame checks for a file named themeconfig.json and seaches for
        theme and mode. Config files override command line args.
- topLevel: If this is True (default = False), this window will be a topLevel window
        and inherit its theme and root from the main window. This is necessary if you
        have multiple windows.

By default, themeconfig.json overrides command line args, which overrides manually passed in themes,
which override the defaults.

## Widgets:

### SlideSwitch

A variant of a checkbox that looks like a switch.
```python
import TKinterModernThemes as TKMT
from tkinter import ttk
import tkinter as tk

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__(str("Switch"), str("park"), str("dark"))
        self.switchvar = tk.BooleanVar()
        self.switch = ttk.Checkbutton(self, text="Switch", variable=self.switchvar, style=TKMT.ThemeStyles.SlideSwitch)
        self.switch.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        #add your widgets here
        self.run()

App()
```


### ToggleButton

A variant of a checkbox that looks like a button.
```python
import TKinterModernThemes as TKMT
from tkinter import ttk
import tkinter as tk

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__(str("Toggle button"), str("park"), str("dark"))
        self.togglebuttonvar = tk.BooleanVar()
        # Togglebutton
        self.togglebutton = ttk.Checkbutton(self, text="Toggle button", style=TKMT.ThemeStyles.ToggleButton,variable=self.togglebuttonvar)
        self.togglebutton.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        #add your widgets here
        self.run()

App()
```


### AccentButton

A button that has a default color of a clicked button.
```python
import TKinterModernThemes as TKMT
from tkinter import ttk

def handleButtonClick():
    print("Button clicked!")

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__(str("Accent Button"), str("park"), str("dark"))
        self.accentbutton = ttk.Button(self, text="Accent button", style=TKMT.ThemeStyles.AccentButton, 
                                       command=handleButtonClick)
        self.accentbutton.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        #add your widgets here
        self.run()

App()
```

See [allwidgets.py](TKinterModernThemes/examples/allwidgets.py) for info on each widget.
See [examples](TKinterModernThemes/examples) for more examples on using TKMT frames.
