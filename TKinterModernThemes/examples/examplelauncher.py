"""
UI for launcing examples
"""

import TKinterModernThemes as TKMT
import tkinter as tk

import TKinterModernThemes.examples.allwidgets as allwidgets_demo
import TKinterModernThemes.examples.switch as switch_demo
import TKinterModernThemes.examples.togglebutton as togglebutton_demo
import TKinterModernThemes.examples.accentbutton as accentbutton_demo
import TKinterModernThemes.examples.treeview as treeview_demo
import TKinterModernThemes.examples.combinationdemo as combination_demo
import TKinterModernThemes.examples.layoutdemo as layout_demo
import TKinterModernThemes.examples.font as font_demo
import TKinterModernThemes.examples.theme_swap as theme_demo

demos = {
    "All Widgets Demo": allwidgets_demo,
    "Slide Switch Demo": switch_demo,
    "Toggle Button Demo": togglebutton_demo,
    "Accent Button Demo": accentbutton_demo,
    "Treeview Demo": treeview_demo,
    "Combination Demo": combination_demo,
    "Layout Demo": layout_demo,
    "Font Demo": font_demo,
    "Theme Swap Demo": theme_demo
}

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

        self.buttonframe = self.addLabelFrame("Examples")
        for name, demo in demos.items():
            self.buttonframe.Button(name, self.runDemo, (demo,))
        self.buttonframe.Button("Matplotlib Demo", self.matplotdemo)

        self.menuframe = self.addLabelFrame("Config", col=1)
        self.menuframe.OptionMenu(self.themeoptions, self.themeoptionvar, self.flipSwitches)
        self.menuframe.OptionMenu(self.modeoptions, self.modeoptionvar, self.flipSwitches)
        self.menuframe.SlideSwitch("Use Command Parameters", self.usecommandargs)
        self.menuframe.SlideSwitch("Use Theme Config File", self.usethemeconfigfile)
        self.run()

    def runDemo(self, demo):
        theme = self.themeoptionvar.get()
        if theme == self.themeoptions[0]:
           theme = ""
        mode = self.modeoptionvar.get()
        if mode == self.modeoptions[0]:
           mode = ""
        demo.App(theme, mode, self.usecommandargs.get(), self.usethemeconfigfile.get())

    def matplotdemo(self):
        import TKinterModernThemes.examples.matplotlibexample as demo
        self.runDemo(demo)

    def flipSwitches(self, _):
        self.usecommandargs.set(False)
        self.usethemeconfigfile.set(False)

def run():
    App()

if __name__ == "__main__":
    run()