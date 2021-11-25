"""
Source for ThemedTKinterFrame, an entry point into the widget frame system.
"""

from TKinterModernThemes.ThemeStyles import ThemeStyles
from TKinterModernThemes.WidgetFrame import WidgetFrame
import tkinter as tk
import json
import sys

firstWindow = True

class ThemedTKinterFrame(WidgetFrame):
    def __init__(self, title: str, theme: str='', mode: str='', usecommandlineargs=True, useconfigfile=True):
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

        #Create tk root
        global firstWindow #singleton
        if firstWindow:
            self.root = tk.Tk()
            firstWindow = False
        else:
            self.root = tk.Toplevel()
        self.root.protocol("WM_DELETE_WINDOW", self.handleExit)

        self.root.title(title)

        #region Set Theme
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

        try:
            self.root.tk.call("source", __file__ + "/../themes/" + theme.lower() + "/" + theme.lower() + ".tcl")
        except tk.TclError:
            pass #theme already loaded...
        self.root.tk.call("set_theme", mode.lower())

        self.theme = theme.lower()
        self.mode = mode.lower()
        # endregion

        super().__init__(self.root, "Master Frame")

    def run(self, cleanresize=True, recursiveResize=True, onlyFrames=True):
        """
        Runs the main loop of the tkinter frame. Also does some basic rendering stuff, such as packing
        and resizing the window.

        :param cleanresize: Makes grid resizable
        :param recursiveResize: Resize applies to subframes
        :param onlyFrames: Only resize frame rows (makes widgets look better)
        """
        if cleanresize:
            self.makeResizable(recursiveResize, onlyFrames=onlyFrames)

        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        x_cordinate = int((self.root.winfo_screenwidth() / 2) - (self.root.winfo_width() / 2))
        y_cordinate = int((self.root.winfo_screenheight() / 2) - (self.root.winfo_height() / 2))
        self.root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))
        self.root.mainloop()

    def handleExit(self):
        global firstWindow
        self.root.destroy()
        self.root.quit()
        firstWindow = True