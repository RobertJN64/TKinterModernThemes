"""
Demo of layout edge cases
"""

import TKinterModernThemes as TKMT

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Layout Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)
        #None is because these aren't hooked up to commands
        self.leftframe = self.addLabelFrame("Left frame")
        self.leftframe.Button("TL Corner", None) #by default, widgets go to the top left
        self.leftframe.Button("Tall Button", None, rowspan=2) #buttons can span rows
        self.leftframe.Button("Wide Button", None, colspan=2) #buttons can span cols

        #if a button is large enough, it will extend past the edge of the frame
        self.leftframe.Button("Very wide button", None, col=1, colspan = 5)
        self.leftframe.Button("Another placeholder button", None, col=1)
        self.leftframe.Button("Another placeholder button", None, col=1)
        self.leftframe.Button("Another placeholder button", None, col=1)

        self.leftframe.Button("Col 2 button", None, col=2) #this button will autoplace down by row 3
        self.leftframe.Button("Col 3 button", None, col=3) #this button fits into the top row

        #this will throw an error because the buttons are forced to overlap
        self.leftframe.Button("You can't see this button", None, col=2)
        self.leftframe.Button("Because this button overlaps!", None, col=2, row=2)

        #but then placement will be correct again
        self.leftframe.Button("Very tall button", None, col=2, rowspan=3)

        #this will throw an error because a button overlaps with reserved space
        self.leftframe.Button("Half hidden button.", None, col=3, row=2, colspan=2, rowspan=2)
        self.leftframe.Button("Manually placed button.", None, col=4, row=3)

        #auto placed buttons should never throw an error or overlap

        self.rightframe = self.addLabelFrame("Right Frame", col=1)
        self.rightframe.Button("A", None,  col=1)
        self.rightframe.Button("B", None, colspan=2)
        self.rightframe.Button("C", None)
        self.rightframe.Button("D", None, col=1)

        self.debugPrint()
        self.run()


if __name__ == "__main__":
    App("park", "dark")