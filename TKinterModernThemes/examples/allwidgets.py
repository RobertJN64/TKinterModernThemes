import TKinterModernThemes as TKMT
from functools import partial
import tkinter as tk
from tkinter import ttk
import json

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True, topLevel=False):
        super().__init__("TKinter Custom Themes Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile, topLevel=topLevel)

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

        self.slidervar = tk.IntVar(value=50)

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

        self.button_frame = self.addLabelFrame("Buttons", col=1)
        self.button_frame.Button("Button", self.handleButtonClick)
        self.button_frame.AccentButton("Accent Button", self.handleButtonClick)
        self.button_frame.ToggleButton("Toggle Button", variable=self.togglebuttonvar)

        # Create a Frame for input widgets
        self.input_frame = self.addLabelFrame("InputMethods", col=1, rowspan=2)
        self.textinputvar.trace_add('write', self.textupdate)
        self.input_frame.Entry(self.textinputvar, validatecommand=self.validateText)
        self.input_frame.NumericalSpinbox(0,100,5,self.spinboxnumvar)
        self.input_frame.NonnumericalSpinbox(['red', 'green', 'blue'], self.spinboxcolorvar, wrap=True)
        self.input_frame.Combobox(["You", "can", "edit", "these", "options."], self.comboboxvar)

        # Menu for the Menubutton
        self.menu = tk.Menu(self.master)
        self.menu.add_command(label="Menu item 1", command=partial(self.menuprint, "1"))
        self.menu.add_command(label="Menu item 2", command=partial(self.menuprint, "2"))
        self.menu.add_command(label="Menu item 3", command=partial(self.menuprint, "3"))
        self.menu.add_command(label="Menu item 4", command=partial(self.menuprint, "4"))


        # Menubutton
        #self.menubutton = ttk.Menubutton(self.widgets_frame, text="Pick an option", menu=self.menu, direction="below")
        #self.menubutton.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

        # OptionMenu
        self.input_frame.OptionMenu(self.option_menu_list, self.optionmenuvar, lambda x: print("Menu:",x))

        self.displayframe = self.addLabelFrame("Display Frame", col=2, rowspan=3)

        # Define treeview data
        with open('treeviewdata.json') as f:
            tree = json.load(f)
        self.displayframe.Treeview(['Files', 'Purpose'], [120,120], 10, tree, 'subfiles', ['name', 'purpose'])


            # def notebookPane():
            #     # Notebook, pane #2
            #
            #     self.notebook = ttk.Notebook(self.pane_2)
            #     self.notebook.pack(fill="both", expand=True)
            #
            #     # Tab #1
            #     self.tab_1 = ttk.Frame(self.notebook)
            #     for col in [0, 1]:
            #         self.tab_1.columnconfigure(index=col, weight=1)
            #         self.tab_1.rowconfigure(index=col, weight=1)
            #     self.notebook.add(self.tab_1, text="Tab 1")
            #
            #     # Scale
            #     self.scale = ttk.Scale(self.tab_1, from_=100, to=0, variable=self.slidervar)
            #     self.scale.grid(row=0, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")
            #
            #     # Progressbar
            #     self.progress = ttk.Progressbar(self.tab_1, value=0, variable=self.slidervar, mode="determinate")
            #     self.progress.grid(row=1, column=0, padx=(10, 20), pady=(20, 0), sticky="ew")
            #
            #     # Tab #2
            #     self.tab_2 = ttk.Frame(self.notebook)
            #     self.notebook.add(self.tab_2, text="Tab 2")
            #
            #     # Label
            #     self.label = ttk.Label(self.tab_2, text="Label text here.", justify="center",
            #                            font=("-size", 15, "-weight", "bold"),)
            #     self.label.grid(row=0, column=0, pady=10)
            #
            #     # Tab #3
            #     self.tab_3 = ttk.Frame(self.notebook)
            #     self.notebook.add(self.tab_3, text="Tab 3")
            #
            #     self.textbox = tk.Label(self.tab_3, text='Normal text here.')
            #     self.textbox.grid(row=0, column=0, pady=10, padx=5)
            #
            #     self.themelabel = ttk.Label(self, text=self.theme.capitalize() + " theme: " + self.mode,
            #                                 font=('-size', 15, '-weight', 'bold'))
            #     self.themelabel.grid(row=3, column=2)
            #notebookPane()
        #buildTreeView()
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