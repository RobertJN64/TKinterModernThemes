"""
Simple demo of accent button widget
"""

import TKinterModernThemes as TKMT

def handleButtonClick():
    print("Button clicked!")

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Accent button", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.frame = self.addLabelFrame("Accent Button Frame")
        self.frame.AccentButton("Accent Button", handleButtonClick)
        self.run()

if __name__ == "__main__":
    App("park", "dark")