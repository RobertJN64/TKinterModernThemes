import TKinterModernThemes as TKMT
from tkinter import ttk
import tkinter as tk

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__(str("Toggle button"), str("park"), str("dark"), pathtothemes='../../')
        self.togglebuttonvar = tk.BooleanVar()
        # Togglebutton
        self.togglebutton = ttk.Checkbutton(self, text="Toggle button", style=TKMT.ThemeStyles.ToggleButton,variable=self.togglebuttonvar)
        self.togglebutton.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        #add your widgets here
        self.run()

App()