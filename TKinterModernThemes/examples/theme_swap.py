"""
Demo of changing from light to dark theme
"""

import TKinterModernThemes as TKMT
import tkinter as tk

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Theme Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.frame = self.addLabelFrame("Theme Control")
        self.light_dark_bool = tk.BooleanVar(value=self.mode == "dark")
        self.frame.SlideSwitch("Light / Dark", self.light_dark_bool, self.change_mode)
        self.frame.AccentButton("Do Nothing", None)

        self.run()


    def change_mode(self):
        print()
        print("Old mode: ", self.mode)

        if self.light_dark_bool.get():
            self.root.tk.call("set_theme", "dark")
            self.mode = "dark"
        else:
            self.root.tk.call("set_theme", "light")
            self.mode = "light"
        print("New mode: ", self.mode)


if __name__ == "__main__":
    App("park", "light")