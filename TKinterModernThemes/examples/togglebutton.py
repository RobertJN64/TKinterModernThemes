import TKinterModernThemes as TKMT
from tkinter import ttk
import tkinter as tk

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Toggle button", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)
        self.togglebuttonvar = tk.BooleanVar()
        # Togglebutton
        self.togglebutton = ttk.Checkbutton(self, text="Toggle button", style=TKMT.ThemeStyles.ToggleButton,variable=self.togglebuttonvar)
        self.togglebutton.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        #add your widgets here
        self.run()

if __name__ == "__main__":
    App("park", "dark")