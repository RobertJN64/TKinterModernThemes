"""
Demo of using tk widgets with widget frame widgets
"""

import TKinterModernThemes as TKMT
from TKinterModernThemes.WidgetFrame import Widget
from tkinter import ttk

def buttonCMD():
        print("Button clicked!")

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Combination Demo", theme, mode, usecommandlineargs, usethemeconfigfile)
        self.Button("Auto placed button!", buttonCMD) #placed at row 0, col 0

        self.button_frame = self.addLabelFrame(str("Frame Label")) #placed at row 1, col 0

        self.button_frame.Button(str("Button Text"), buttonCMD) #the button is dropped straight into the frame

        button = ttk.Button(self.button_frame.master, text="Button in frame!")
        button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        button = ttk.Button(self.master, text="Button outside frame!")
        button.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        button = ttk.Button(self.master, text="debugPrint() finds this button")
        button.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
        self.widgets.widgetlist.append(Widget(button, "Button", 3, 0, 1, 1,
                                              "debugPrint() finds this button"))

        self.debugPrint()
        self.run()

if __name__ == "__main__":
    App("park", "dark")