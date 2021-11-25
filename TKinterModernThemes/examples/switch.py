"""
Simple demo of switch widget
"""

import TKinterModernThemes as TKMT
import tkinter as tk

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Switch", theme, mode, usecommandlineargs=usecommandlineargs,
                         useconfigfile=usethemeconfigfile)
        self.switchframe = self.addLabelFrame("Switch Frame")
        self.switchvar = tk.BooleanVar()
        self.switchframe.SlideSwitch("Switch", self.switchvar)
        self.run()

if __name__ == "__main__":
    App("park", "dark")