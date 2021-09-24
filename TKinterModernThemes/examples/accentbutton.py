import TKinterModernThemes as TKMT
from tkinter import ttk

def handleButtonClick():
    print("Button clicked!")

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True, topLevel=False):
        super().__init__("Accent button", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile, topLevel=topLevel)
        self.accentbutton = ttk.Button(self, text="Accent button", style=TKMT.ThemeStyles.AccentButton,
                                       command=handleButtonClick)
        self.accentbutton.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        #add your widgets here
        self.run()

if __name__ == "__main__":
    App("park", "dark")