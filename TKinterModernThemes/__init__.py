import tkinter as tk
from tkinter import ttk
import json
import sys

class ThemeStyles:
    AccentButton = "Accent.TButton" #colored by default button
    ToggleButton = "Toggle.TButton" #toggle
    SlideSwitch = "Switch.TCheckbutton" #slide switch

class ThemedTKinterFrame(ttk.Frame):
    def __init__(self, title: str, theme: str='', mode: str='', usecommandlineargs=True, useconfigfile=True,
                 topLevel=False):
        """
        Loads tkinter and creates a themed frame.

        :param title: Window title
        :param theme: Main theme file. One of (azure / sun-valley / park). Defaults to park.
        :param mode: Light or dark theme. One of (light / dark). Defaults to dark.
        :param usecommandlineargs: If this is True (default), the frame checks for params passed into the script
            launch to grab a theme.
        :param useconfigfile: If this is True (default), the frame checks for a file named themeconfig.json and seaches
            for theme and mode. Config files override command line args.
        """

        if usecommandlineargs:
            args = sys.argv
            if len(args) == 3:
                theme = args[1]
                mode = args[2]

        if useconfigfile:
            try:
                with open("themeconfig.json") as f:
                    themeconfig = json.load(f)
                    if "theme" in themeconfig:
                        theme = themeconfig['theme']
                    if "mode" in themeconfig:
                        mode = themeconfig['mode']
            except (FileNotFoundError, json.JSONDecodeError):
                pass  # no config file was specified

        if theme == "":
            theme = "park"

        if mode == "":
            mode = "dark"

        if topLevel:
            root = tk.Toplevel()
        else:
            root = tk.Tk()

        root.title(title)
        try:
            root.tk.call("source", __file__ + "/../themes/" + theme.lower() + "/" +
                         theme.lower() + ".tcl")

        except tk.TclError:
            pass #theme already loaded...

        root.tk.call("set_theme", mode.lower())

        self.theme = theme.lower()
        self.mode = mode.lower()
        super().__init__(root)

    def run(self, cleanresize=True):
        """
        Runs the main loop of the tkinter frame. Also does some basic rendering stuff, such as packing
        and resizing the window.
        """
        if cleanresize:
            for index in range(self.grid_size()[0]):
                self.columnconfigure(index=index, weight=1)
            for index in range(self.grid_size()[1]):
                self.rowconfigure(index=index, weight=1)

        self.pack(fill="both", expand=True)
        self.master.update()
        self.master.minsize(self.master.winfo_width(), self.master.winfo_height())
        x_cordinate = int((self.master.winfo_screenwidth() / 2) - (self.master.winfo_width() / 2))
        y_cordinate = int((self.master.winfo_screenheight() / 2) - (self.master.winfo_height() / 2))
        self.master.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))
        self.mainloop()




