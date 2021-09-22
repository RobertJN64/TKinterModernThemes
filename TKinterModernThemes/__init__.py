import tkinter as tk
from tkinter import ttk

class ThemeStyles:
    AccentButton = "Accent.TButton" #colored by default button
    ToggleButton = "Toggle.TButton" #toggle
    SlideSwitch = "Switch.TCheckbutton" #slide switch

class ThemedTKinterFrame(ttk.Frame):
    def __init__(self, title: str, theme: str='park', mode: str='dark', pathtothemes:str = "venv/Lib/site-packages/"):
        """
        Loads tkinter and creates a themed frame.

        :param title: Window title
        :param theme: Main theme file. One of (azure / sun-valley / park)
        :param mode: Light or dark theme. One of (light / dark)
        :param pathtothemes: Relative path to themes. Default is correct if you are in
        main project directory and using a venv
        """
        root = tk.Tk()
        root.title(title)
        root.tk.call("source", pathtothemes + "TKinterModernThemes/themes/" + theme + "/" + theme + ".tcl")
        root.tk.call("set_theme", mode)
        super().__init__(root)

    def run(self):
        """
        Runs the main loop of the tkinter frame. Also does some basic rendering stuff, such as packing
        and resizing the window.
        """
        self.pack(fill="both", expand=True)
        self.master.update()
        self.master.minsize(self.master.winfo_width(), self.master.winfo_height())
        x_cordinate = int((self.master.winfo_screenwidth() / 2) - (self.master.winfo_width() / 2))
        y_cordinate = int((self.master.winfo_screenheight() / 2) - (self.master.winfo_height() / 2))
        self.master.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))
        self.mainloop()




