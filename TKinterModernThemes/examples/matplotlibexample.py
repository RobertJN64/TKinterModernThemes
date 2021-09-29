import TKinterModernThemes as TKMT
from warnings import warn

class MatplotApp(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True, topLevel=False):
        super().__init__("TKinter Custom Themes Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile, topLevel=topLevel)

def App(theme, mode, usecommandlineargs=True, usethemeconfigfile=True, topLevel=False):
    try:
        import matplotlib.pyplot as plt
        MatplotApp(theme, mode, usecommandlineargs, usethemeconfigfile, topLevel)

    except ImportError:
        warn("Matplotlib is required to run this example!")

if __name__ == "__main__":
    App("park", "dark")