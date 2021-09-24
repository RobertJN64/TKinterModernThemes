import TKinterModernThemes as TKMT
from tkinter import ttk
from functools import partial
import tkinter as tk


class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True, topLevel=False):
        super().__init__("TKinter Custom Themes Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile, topLevel=topLevel)

        self.checkbox1 = tk.BooleanVar()
        self.checkbox2 = tk.BooleanVar(value=True)

        self.radiobuttonvar = tk.StringVar(value='button2')
        self.togglebuttonvar = tk.BooleanVar()

        self.textinputvar = tk.StringVar(value="Type text here.")
        self.spinboxcolorvar = tk.StringVar(value="blue")

        self.option_menu_list = ["a", "b", "c", "d"]
        self.optionmenuvar = tk.StringVar(value=self.option_menu_list[0])

        self.slidervar = tk.IntVar(value=50)

        def buildCheckboxFrame():
            self.check_frame = ttk.LabelFrame(self, text="Checkbuttons", padding=(20, 20))
            self.check_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

            self.check_1 = ttk.Checkbutton(self.check_frame, text="Unchecked", variable=self.checkbox1,
                                           command=partial(self.printcheckboxvars, 1))
            self.check_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.check_2 = ttk.Checkbutton(self.check_frame, text="Checked", variable=self.checkbox2,
                                           command=partial(self.printcheckboxvars, 2))
            self.check_2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            self.check_3 = ttk.Checkbutton(self.check_frame, text="Disabled Unchecked", state="disabled",
                                           variable=self.checkbox1)
            self.check_3.state(["disabled !alternate"])
            self.check_3.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

            self.check_5 = ttk.Checkbutton(self.check_frame, text="Disabled Checked", state="disabled",
                                           variable=self.checkbox2)
            self.check_5.state(["disabled !alternate"])
            self.check_5.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        buildCheckboxFrame()
        # Separator
        self.separator = ttk.Separator(self)
        self.separator.grid(row=1, column=0, padx=(20, 10), pady=10, sticky='ew')

        def buildRadiobuttonFrame():
            # Create a Frame for the Radiobuttons
            self.radio_frame = ttk.LabelFrame(self, text="Radiobuttons", padding=(20, 20))
            self.radio_frame.grid(row=2, column=0, padx=(20, 20), pady=10, sticky="nsew")

            # Radiobuttons
            self.radio_1 = ttk.Radiobutton(self.radio_frame, text="Unselected", variable=self.radiobuttonvar,
                                           value="button1")
            self.radio_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.radio_2 = ttk.Radiobutton(self.radio_frame, text="Selected", variable=self.radiobuttonvar,
                                           value='button2')
            self.radio_2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            self.radio_4 = ttk.Radiobutton(self.radio_frame, text="Disabled", state="disabled",
                                           variable=self.radiobuttonvar, value='button3')
            self.radio_4.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
            self.radiobuttonvar.trace_add('write', self.printradiobuttons)

            # Create a Frame for input widgets
            self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
            self.widgets_frame.grid(
                row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
            )
        buildRadiobuttonFrame()

        self.switch = ttk.Checkbutton(self, text="Switch", style=TKMT.ThemeStyles.SlideSwitch)
        self.switch.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        def buildButtonFrame():
            self.button_frame = ttk.LabelFrame(self, text="Buttons", padding=(20, 20))
            self.button_frame.grid(row=0, column=1, padx=(20, 20), pady=10, sticky="nsew")
            # Button
            self.button = ttk.Button(self.button_frame, text="Button", command=self.handleButtonClick)
            self.button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

            # Accentbutton
            self.accentbutton = ttk.Button(self.button_frame, text="Accent button", style=TKMT.ThemeStyles.AccentButton,
                                           command=self.handleButtonClick)
            self.accentbutton.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

            # Togglebutton
            self.togglebutton = ttk.Checkbutton(self.button_frame, text="Toggle button",
                                                style=TKMT.ThemeStyles.ToggleButton,variable=self.togglebuttonvar)
            self.togglebutton.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        buildButtonFrame()

        def buildInputFrame():
            # Create a Frame for input widgets
            self.widgets_frame = ttk.LabelFrame(self, text="InputMethods", padding=(10, 10, 10, 10))
            self.widgets_frame.grid(row=1, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
            self.textinputvar.trace_add('write', self.textupdate)

            # Entry
            vfunc = self.register(self.validateText)
            self.entry = ttk.Entry(self.widgets_frame, textvariable=self.textinputvar,
                                   validatecommand=(vfunc, '%P'), validate='all')
            self.entry.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")

            # Spinbox
            self.spinbox = ttk.Spinbox(self.widgets_frame, from_=0, to=100, increment=5)
            self.spinbox.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

            self.spinbox2 = ttk.Spinbox(self.widgets_frame, textvariable=self.spinboxcolorvar,
                                        values=['red', 'green', 'blue'], wrap=True)
            self.spinbox2.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

            # Combobox
            self.combobox = ttk.Combobox(self.widgets_frame, values=["You", "can", "edit", "these", "options."])
            self.combobox.current(0)
            self.combobox.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

            # Menu for the Menubutton
            self.menu = tk.Menu(self)
            self.menu.add_command(label="Menu item 1", command=partial(self.menuprint, "1"))
            self.menu.add_command(label="Menu item 2", command=partial(self.menuprint, "2"))
            self.menu.add_command(label="Menu item 3", command=partial(self.menuprint, "3"))
            self.menu.add_command(label="Menu item 4", command=partial(self.menuprint, "4"))

            # Menubutton
            self.menubutton = ttk.Menubutton(self.widgets_frame, text="Pick an option", menu=self.menu, direction="below")
            self.menubutton.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

            # OptionMenu
            self.optionmenu = ttk.OptionMenu(self.widgets_frame, self.optionmenuvar, self.option_menu_list[0],
                                             command=lambda x: print("Menu:",x), *self.option_menu_list)
            self.optionmenu.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")
        buildInputFrame()

        def buildTreeView():
            # Panedwindow
            self.panedwindow = ttk.PanedWindow(self)
            self.panedwindow.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

            def treeviewPane():
                # Pane #1
                self.pane_1 = ttk.Frame(self.panedwindow, padding=5)
                self.panedwindow.add(self.pane_1, weight=1)

                # Scrollbar
                self.scrollbar = ttk.Scrollbar(self.pane_1)
                self.scrollbar.pack(side="right", fill="y")

                # Treeview
                self.treeview = ttk.Treeview(
                    self.pane_1,
                    selectmode="browse",
                    yscrollcommand=self.scrollbar.set,
                    columns=('#1',),
                    height=10,
                )
                self.treeview.pack(expand=True, fill="both")
                self.scrollbar.config(command=self.treeview.yview)

                # Treeview columns
                self.treeview.column("#0", anchor="w", width=120)
                self.treeview.column("#1", anchor="w", width=120)

                # Treeview headings
                self.treeview.heading("#0", text="Files", anchor="center")
                self.treeview.heading("#1", text="Purpose", anchor="center")

                # Define treeview data
                tree = [{'name': 'azure', 'subfiles': [{'name': 'azure.tcl', 'purpose': "Main theme file."},
                                                       {'name': 'theme', 'subfiles':
                                                           [{'name': 'dark.tcl', 'purpose': "Dark theme config."},
                                                            {'name': 'light.tcl', 'purpose': "Light theme config."},
                                                            {'name': 'dark', 'purpose': "Dark theme images."},
                                                            {'name': 'light', 'purpose': "Light theme images."}]}]},
                        {'name': 'forest', 'subfiles': [{'name': 'forest.tcl', 'purpose': "Main theme file."},
                                                       {'name': 'theme', 'subfiles':
                                                           [{'name': 'dark.tcl', 'purpose': "Dark theme config."},
                                                            {'name': 'light.tcl', 'purpose': "Light theme config."},
                                                            {'name': 'dark', 'purpose': "Dark theme images."},
                                                            {'name': 'light', 'purpose': "Light theme images."}]}]},
                        {'name': 'sun-valley', 'subfiles': [{'name': 'sun-valley.tcl', 'purpose': "Main theme file."},
                                                        {'name': 'theme', 'subfiles':
                                                            [{'name': 'dark.tcl', 'purpose': "Dark theme config."},
                                                             {'name': 'light.tcl', 'purpose': "Light theme config."},
                                                             {'name': 'dark', 'purpose': "Dark theme images."},
                                                             {'name': 'light', 'purpose': "Light theme images."}]}]},
                        {'name': 'park', 'subfiles': [{'name': 'park.tcl', 'purpose': "Main theme file."},
                                                        {'name': 'theme', 'subfiles':
                                                            [{'name': 'dark.tcl', 'purpose': "Dark theme config."},
                                                             {'name': 'light.tcl', 'purpose': "Light theme config."},
                                                             {'name': 'dark', 'purpose': "Dark theme images."},
                                                             {'name': 'light', 'purpose': "Light theme images."}]}]},
                        ]


                def traverse(p, t, iid):
                    for obj in t:
                        iid[0] += 1
                        self.treeview.insert(p, index='end', iid=iid[0], text=obj['name'], values=(obj.get('purpose', ""),))
                        if obj.get('subfiles', []):
                            self.treeview.item(iid[0], open=True)  # Open parents
                        traverse(iid[0], obj.get('subfiles', []), iid)
                traverse('', tree, [0])
            treeviewPane()

            def notebookPane():
                # Notebook, pane #2
                self.pane_2 = ttk.Frame(self.panedwindow, padding=5)
                self.panedwindow.add(self.pane_2, weight=3)

                self.notebook = ttk.Notebook(self.pane_2)
                self.notebook.pack(fill="both", expand=True)

                # Tab #1
                self.tab_1 = ttk.Frame(self.notebook)
                for col in [0, 1]:
                    self.tab_1.columnconfigure(index=col, weight=1)
                    self.tab_1.rowconfigure(index=col, weight=1)
                self.notebook.add(self.tab_1, text="Tab 1")

                # Scale
                self.scale = ttk.Scale(self.tab_1, from_=100, to=0, variable=self.slidervar)
                self.scale.grid(row=0, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")

                # Progressbar
                self.progress = ttk.Progressbar(self.tab_1, value=0, variable=self.slidervar, mode="determinate")
                self.progress.grid(row=1, column=0, padx=(10, 20), pady=(20, 0), sticky="ew")

                # Tab #2
                self.tab_2 = ttk.Frame(self.notebook)
                self.notebook.add(self.tab_2, text="Tab 2")

                # Label
                self.label = ttk.Label(self.tab_2, text="Label text here.", justify="center",
                                       font=("-size", 15, "-weight", "bold"),)
                self.label.grid(row=0, column=0, pady=10)

                # Tab #3
                self.tab_3 = ttk.Frame(self.notebook)
                self.notebook.add(self.tab_3, text="Tab 3")

                self.textbox = tk.Label(self.tab_3, text='Normal text here.')
                self.textbox.grid(row=0, column=0, pady=10, padx=5)

                self.themelabel = ttk.Label(self, text=self.theme.capitalize() + " theme: " + self.mode,
                                            font=('-size', 15, '-weight', 'bold'))
                self.themelabel.grid(row=3, column=2)
            notebookPane()
        buildTreeView()
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