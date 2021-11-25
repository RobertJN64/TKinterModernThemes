"""
Simple demo of toggle button widget
"""

import TKinterModernThemes as TKMT
import tkinter as tk

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Toggle button", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)
        self.togglebuttonframe = self.addLabelFrame("Toggle Button Frame")
        self.togglebuttonvar = tk.BooleanVar()
        # Togglebutton
        self.togglebutton = self.togglebuttonframe.ToggleButton(text="Toggle button", variable=self.togglebuttonvar)
        self.run()

if __name__ == "__main__":
    App("park", "dark")