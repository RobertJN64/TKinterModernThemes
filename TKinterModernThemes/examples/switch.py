import TKinterModernThemes as TKMT
from tkinter import ttk
import tkinter as tk

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Switch", theme, mode, usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)
        self.switchvar = tk.BooleanVar()
        self.switch = ttk.Checkbutton(self, text="Switch", variable=self.switchvar, style=TKMT.ThemeStyles.SlideSwitch)
        self.switch.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        #add your widgets here
        self.run()

if __name__ == "__main__":
    App("park", "dark")