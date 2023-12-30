"""
Demo of different ways to set fonts
"""

import TKinterModernThemes as TKMT
from tkinter import ttk

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Font Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        s = ttk.Style()
        s.configure('.', font=('Courier', 20))  # change default font
        s.configure('my_custom_style.TButton', font=('Helvetica', 12))

        self.frame = self.addLabelFrame("This uses ttk style")
        self.frame.Text("This uses ttk style")
        self.frame.Text("This uses fontargs", fontargs=('-family', 'MS Serif'))

        self.frame.Label("This doesn't obey ttk style")
        self.frame.Label("But can be set with fontargs", fontargs=('-family', 'MS Serif'))

        self.frame.Button("This always obeys ttk style", command=None)

        cust_button = self.frame.Button("Unless you set a custom style", command=None)
        cust_button.configure(style='my_custom_style.TButton')

        self.run()

if __name__ == "__main__":
    App("park", "dark")