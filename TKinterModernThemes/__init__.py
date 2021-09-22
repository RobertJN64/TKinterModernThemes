import tkinter as tk
from tkinter import ttk
import os

class ThemeStyles:
    AccentButton = "Accent.TButton" #colored by default button
    ToggleButton = "Toggle.TButton" #toggle
    SlideSwitch = "Switch.TCheckbutton" #slide switch

class ThemedTKinterFrame(ttk.Frame):
    def __init__(self, title, theme='park', mode='dark', pathtothemes = ""):
        root = tk.Tk()
        root.title(title)
        root.tk.call("source", pathtothemes + "TKinterModernThemes/themes/" + theme + "/" + theme + ".tcl")
        root.tk.call("set_theme", mode)
        super().__init__(root)

    def run(self):
        self.pack(fill="both", expand=True)
        self.master.update()
        self.master.minsize(self.master.winfo_width(), self.master.winfo_height())
        x_cordinate = int((self.master.winfo_screenwidth() / 2) - (self.master.winfo_width() / 2))
        y_cordinate = int((self.master.winfo_screenheight() / 2) - (self.master.winfo_height() / 2))
        self.master.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))
        self.mainloop()




