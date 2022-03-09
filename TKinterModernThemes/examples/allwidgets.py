"""
Demo of all widgets
"""

import TKinterModernThemes as TKMT
from functools import partial
import tkinter as tk
import json

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("TKinter Custom Themes Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.checkbox1 = tk.BooleanVar()
        self.checkbox2 = tk.BooleanVar(value=True)

        self.radiobuttonvar = tk.StringVar(value='button2')
        self.togglebuttonvar = tk.BooleanVar()

        self.textinputvar = tk.StringVar(value="Type text here.")
        self.spinboxnumvar = tk.IntVar(value=25)
        self.spinboxcolorvar = tk.StringVar(value="blue")
        self.comboboxvar = tk.StringVar()

        self.option_menu_list = ["a", "b", "c", "d"]
        self.optionmenuvar = tk.StringVar(value=self.option_menu_list[0])

        self.slidervar = tk.IntVar(value=25)

        self.check_frame = self.addLabelFrame("CheckButtons")
        self.check_frame.Checkbutton("Unchecked", self.checkbox1, self.printcheckboxvars, (1,))
        self.check_frame.Checkbutton("Unchecked", self.checkbox2, self.printcheckboxvars, (1,))
        self.check_frame.Checkbutton("Disabled Unchecked", self.checkbox1, disabled=True)
        self.check_frame.Checkbutton("Disabled Checked", self.checkbox2, disabled=True)
        self.check_frame.SlideSwitch("Slide Switch", None)

        # Separator
        self.Seperator()
        self.radio_frame = self.addLabelFrame("RadioButtons")
        self.radio_frame.Radiobutton("Unselected", self.radiobuttonvar, value="button1")
        self.radio_frame.Radiobutton("Selected", self.radiobuttonvar, value="button2")
        self.radio_frame.Radiobutton("Disabled", self.radiobuttonvar, value="button3", disabled=True)
        self.radiobuttonvar.trace_add('write', self.printradiobuttons)

        self.nextCol()
        self.button_frame = self.addLabelFrame("Buttons")
        self.button_frame.Button("Button", self.handleButtonClick)
        self.button_frame.AccentButton("Accent Button", self.handleButtonClick)
        self.button_frame.ToggleButton("Toggle Button", self.togglebuttonvar)

        # Menu for the Menubutton
        menu = tk.Menu(self.master)
        menu.add_command(label="Menu item 1", command=partial(self.menuprint, "1"))
        menu.add_command(label="Menu item 2", command=partial(self.menuprint, "2"))
        menu.add_command(label="Menu item 3", command=partial(self.menuprint, "3"))
        menu.add_command(label="Menu item 4", command=partial(self.menuprint, "4"))

        self.button_frame.MenuButton(menu, "Pick an option")

        # Create a Frame for input widgets
        self.input_frame = self.addLabelFrame("InputMethods", rowspan=2)
        self.textinputvar.trace_add('write', self.textupdate)
        self.input_frame.Entry(self.textinputvar, validatecommand=self.validateText)
        self.input_frame.NumericalSpinbox(0,100,5,self.spinboxnumvar)
        self.input_frame.NonnumericalSpinbox(['red', 'green', 'blue'], self.spinboxcolorvar, wrap=True)
        self.input_frame.Combobox(["You", "can", "edit", "these", "options."], self.comboboxvar)
        self.input_frame.OptionMenu(self.option_menu_list, self.optionmenuvar, lambda x: print("Menu:",x))

        self.nextCol()
        self.panedWindow = self.PanedWindow("Paned Window Test", rowspan=3)
        self.pane1 = self.panedWindow.addWindow()

        # Define treeview data
        with open('treeviewdata.json') as f:
            tree = json.load(f)
        self.pane1.Treeview(['Files', 'Purpose'], [120,120], 10, tree, 'subfiles', ['name', 'purpose'], openkey='open')

        self.pane2 = self.panedWindow.addWindow()
        self.notebook = self.pane2.Notebook("Test Notebook")
        self.tab_1 = self.notebook.addTab("Tab 1")
        self.tab_1.Scale(100, 0, self.slidervar)
        self.tab_1.Progressbar(self.slidervar)
        self.tab_1.makeResizable(onlyFrames=False)

        self.tab_2 = self.notebook.addTab("Tab 2")
        self.tab_2.Label("Label text here.")

        self.tab_3 = self.notebook.addTab("Tab 3")
        self.tab_3.Text("Normal text here.")

        self.pane3 = self.panedWindow.addWindow()
        self.pane3.Label(self.theme.capitalize() + " theme: " + self.mode)

        self.debugPrint()
        self.run()

    def printcheckboxvars(self, number):
        print("Checkbox number:", number, "was pressed")
        print("Checkboxes: ", self.checkbox1.get(), self.checkbox2.get())

    def printradiobuttons(self, _var, _indx, _mode):
        print("Radio button: ", self.radiobuttonvar.get(), "pressed.")

    def handleButtonClick(self):
        print("Button clicked. Current toggle button state: ", self.togglebuttonvar.get())

    def textupdate(self, _var, _indx, _mode):
        print("Current text status:", self.textinputvar.get())

    def menuprint(self, item):
        if self == self:
            pass
        print("Menu item chosen: ", item)

    def validateText(self, text):
        if self == self:
            pass
        if 'q' not in text:
            return True
        print("The letter q is not allowed.")
        return False

if __name__ == '__main__':
    app = App(input("Theme (azure / park / sun-valley): ").lower(), input("dark / light: ").lower())