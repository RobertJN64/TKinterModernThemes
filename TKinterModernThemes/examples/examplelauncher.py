import TKinterModernThemes as TKMT
from tkinter import ttk
import tkinter as tk
from functools import partial

import TKinterModernThemes.examples.allwidgets as demo1
import TKinterModernThemes.examples.switch as demo2
import TKinterModernThemes.examples.togglebutton as demo3
import TKinterModernThemes.examples.accentbutton as demo4

demos = [demo1, demo2, demo3, demo4]
names = ["All Widgets Demo", "Slide Switch Demo", "Toggle Button Demo", "Accent Button Demo"]

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Example TKMT Launcher")

        #vars
        self.themeoptions = ['Pick a Theme', "Park", "Azure", "Sun-Valley"]
        self.modeoptions = ['Pick a Mode', "Light", "Dark"]
        self.themeoptionvar = tk.StringVar()
        self.modeoptionvar = tk.StringVar()

        self.usecommandargs = tk.BooleanVar(value=True)
        self.usethemeconfigfile = tk.BooleanVar(value=True)

        self.buttonframe = ttk.LabelFrame(self, text="Examples")
        self.buttonframe.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        for i in range(0, len(demos)):
            demobutton = ttk.Button(self.buttonframe, text=names[i], command=partial(self.runDemo, demos[i]))
            demobutton.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")

        self.menuframe = ttk.LabelFrame(self, text="Config")
        self.menuframe.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')


        self.thememenu = ttk.OptionMenu(self.menuframe, self.themeoptionvar, self.themeoptions[0], *self.themeoptions,
                                        command=self.flipSwitches)
        self.thememenu.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.thememenu = ttk.OptionMenu(self.menuframe, self.modeoptionvar, self.modeoptions[0], *self.modeoptions,
                                        command=self.flipSwitches)
        self.thememenu.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.commandargsswitch = ttk.Checkbutton(self.menuframe, variable=self.usecommandargs,
                                                 style=TKMT.ThemeStyles.SlideSwitch, text="Use Command Parameters")
        self.commandargsswitch.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.commandargsswitch = ttk.Checkbutton(self.menuframe, variable=self.usethemeconfigfile,
                                                 style=TKMT.ThemeStyles.SlideSwitch, text="Use Theme Config File")
        self.commandargsswitch.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.run()

    def runDemo(self, demo):
        theme = self.themeoptionvar.get()
        if theme == self.themeoptions[0]:
            theme = ""
        mode = self.modeoptionvar.get()
        if mode == self.modeoptions[0]:
            mode = ""
        demo.App(theme, mode, self.usecommandargs.get(), self.usethemeconfigfile.get())

    def flipSwitches(self, _):
        self.usecommandargs.set(False)
        self.usethemeconfigfile.set(False)

def run():
    App()

if __name__ == "__main__":
    run()