"""
Demo of matplotilb integration
"""

import TKinterModernThemes as TKMT
from warnings import warn
import random

valid = True

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        if valid:
            super().__init__("Matplotlib Example", theme, mode,
                             usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

            self.graphframe = self.addLabelFrame("2D Graph")
            self.graphframe2 = self.addLabelFrame("3D Graph", col=1)
            self.canvas, fig, self.ax, background, self.accent = self.graphframe.matplotlibFrame("Graph Frame Test")
            self.canvas2, fig2, self.ax2, _, _ = self.graphframe2.matplotlibFrame("Graph 3D", projection='3d')
            buttonframe = self.addLabelFrame("Control Buttons", colspan=2)
            buttonframe.Button("Add Data", self.addData)
            self.debugPrint()
            self.run()

    def addData(self):
        x = []
        y = []
        z = []

        for i in range(0, 100):
            for l in [x, y, z]:
                l.append(random.random() * 100)

        self.ax.scatter(x, y, c=self.accent)
        self.ax2.scatter(x, y, z, c=self.accent)
        self.canvas.draw()
        self.canvas2.draw()

try:
    import matplotlib

except ImportError:
    valid = False
    warn("Matplotlib is required to run this example!")

if __name__ == "__main__":
    App("park", "dark")