import TKinterModernThemes as TKMT
from tkinter import ttk
import tkinter as tk

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__(str("Switch"), str("park"), str("dark"), pathtothemes='../../')
        self.switchvar = tk.BooleanVar()
        self.switch = ttk.Checkbutton(self, text="Switch", variable=self.switchvar, style=TKMT.ThemeStyles.SlideSwitch)
        self.switch.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        #add your widgets here
        self.run()

App()