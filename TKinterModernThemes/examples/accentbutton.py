import TKinterModernThemes as TKMT
from tkinter import ttk

def handleButtonClick():
    print("Button clicked!")

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__(str("Accent Button"), str("park"), str("dark"), pathtothemes='../../')
        self.accentbutton = ttk.Button(self, text="Accent button", style=TKMT.ThemeStyles.AccentButton,
                                       command=handleButtonClick)
        self.accentbutton.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        #add your widgets here
        self.run()

App()