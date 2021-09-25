from tkinter import ttk
from functools import partial as PARTIAL #for calling funcs with args
import math
from TKinterModernThemes.ThemeStyles import ThemeStyles

def partial(command, *args):
    if command is not None:
        return PARTIAL(command, *args)
    return None

def isFloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def isConstrainedFloat(lower, upper, x):
    return isFloat(x) and lower <= float(x) <= upper

def isMember(values, x):
    return x in values


class Widget:
    def __init__(self, widget, name, row, col, text="", command=None, args=()):
        self.widget = widget
        self.name = name
        self.row = row
        self.col = col
        self.text = text

        self.commandstr = ""
        if command is not None:
            self.commandstr = " -> " + command.__name__ + str(args)

    def __str__(self):
        if type(self.widget) == WidgetFrame:
            return self.name + ": " + self.text
        if self.text == "":
            return self.name + self.commandstr
        else:
            return self.name + '("' + self.text + '")' + self.commandstr

    def debugPrint(self, recursive=True):
        self.widget.debugPrint(recursive)

def tabulate(widgets):
    longesttext = 0
    maxrow = 0
    maxcol = 0

    subframes = []
    for widget in widgets:
        longesttext = max(len(str(widget)), longesttext)
        maxrow = max(widget.row, maxrow)
        maxcol = max(widget.col, maxcol)
        if type(widget.widget) == WidgetFrame:
            subframes.append(widget)

    longesttext += 2

    def printSeperator():
        s = "+"
        for i in range(0, maxcol+1):
            s += "-" * longesttext + "+"
        print(s)

    def centerText(text):
        ldif = longesttext - len(text)
        return " " * math.floor(ldif/2) + text + " " * math.ceil(ldif/2)

    def printRow(row):
        s = '|'
        for col in range(0, maxcol+1):
            for w in widgets:
                if w.row == row and w.col == col:
                    s += centerText(str(w)) + '|'
                    break
            else:
                s += " " * longesttext + "|"
        print(s)

    for r in range(0, maxrow+1):
        printSeperator()
        printRow(r)
    printSeperator()
    print()

class WidgetFrame(ttk.LabelFrame):
    def __init__(self, master, text, row, col, padx=(20,20), pady=(20,20), rowspan=1, sticky="nsew"):
        """
        Creates a widget frame (a label frame with some bonus features)
        :param master: passed to LabelFrame, normally root or another frame
        :param text: passed to LabelFrame
        :param row: passed to grid
        :param col: passed to grid
        :param padx: passed to grid
        :param pady: passed to grid
        :param sticky: passed to grid
        """
        super().__init__(master, text=text)
        self.text = text
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan)

        self.rowcounters = []
        self.widgets = []

    #Widgets
    def getRow(self, row, col):
        for _ in range(len(self.rowcounters), col + 1):
            self.rowcounters.append(0)

        if row is None: #auto find row
            row = self.rowcounters[col]
        if row is not None:
            self.rowcounters[col] = row
        self.rowcounters[col] += 1
        return row

    def Checkbutton(self, text, variable, command = None, args=(),
                    row=None, col=0, padx=10, pady=10, sticky="nsew", disabled=False, style=None):
        """
        Creates a ttk.Checkbutton widget
        :param text: Label next to widget
        :param variable: TK variable that auto updates when checkbox changes
        :param command: Command that is called on change
        :param args: Args passsed to command
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param disabled: Puts checkbox in disabled state, default False
        :param style: One of ThemeStyles.CheckbuttonStyles
        :return: ttk.Checkbutton
        """
        checkbutton = ttk.Checkbutton(self, text=text, variable=variable, command=partial(command, *args), style=style)

        if disabled:
            checkbutton.state(["disabled !alternate"])

        row = self.getRow(row, col)
        checkbutton.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        widgetname = "CheckButton"
        if style == ThemeStyles.CheckbuttonStyles.ToggleButton:
            widgetname = "ToggleButton"
        elif style == ThemeStyles.CheckbuttonStyles.SlideSwitch:
            widgetname = "SlideSwitch"
        self.widgets.append(Widget(checkbutton, widgetname, row, col, text, command, args))
        return checkbutton

    def ToggleButton(self, text, variable, command = None, args=(), row=None, col=0, padx=10, pady=10, sticky="nsew"):
        """Wrapper function for creating a toggle button. All params same as checkbutton."""
        return self.Checkbutton(text, variable, command, args, row, col, padx, pady, sticky,
                                style=ThemeStyles.CheckbuttonStyles.ToggleButton)

    def SlideSwitch(self, text, variable, command = None, args=(), row=None, col=0, padx=10, pady=10, sticky="nsew"):
        """Wrapper function for creating a slide switch. All params same as checkbutton."""
        return self.Checkbutton(text, variable, command, args, row, col, padx, pady, sticky,
                                style=ThemeStyles.CheckbuttonStyles.SlideSwitch)

    def Radiobutton(self, text, variable, value, command = None, args=(),
                    row=None, col=0, padx=10, pady=10, sticky="nsew", disabled=False):
        """
        Creates a ttk.Radiobutton widget
        :param text: Label next to widget
        :param variable: TK variable that auto updates when radiobutton changes
        :param value: Value that the variable is set to
        :param command: Command that is called on change
        :param args: Args passsed to command
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param disabled: Puts radiobutton in disabled state, default False
        :return: ttk.Radiobutton
        """
        state = None
        if disabled:
            state = "disabled"
        radiobutton = ttk.Radiobutton(self, text=text, variable=variable, value=value,
                                      command=partial(command, *args), state=state)

        row = self.getRow(row, col)
        radiobutton.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)

        self.widgets.append(Widget(radiobutton, "Radiobutton<" + str(value) + ">", row, col, text,
                                   command=partial(command, *args)))
        return radiobutton

    def Button(self, text, command, args=(), row=None, col=0, padx=10, pady=10, sticky="nsew", style=None):
        """
        Creates a ttk.Button widget
        :param text: Label on button
        :param command: Command that is called on press
        :param args: Args passsed to command
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param style: Button style, could be AccentButton. Find more in TKMT.ThemeStyles
        :return: ttk.Button
        """

        button = ttk.Button(self, text=text, command=partial(command, *args), style=style)

        row = self.getRow(row, col)
        button.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)

        widgetname = "Button"
        if style is not None:
            if style == ThemeStyles.ButtonStyles.AccentButton:
                widgetname = "Accent Button"
        self.widgets.append(Widget(button, widgetname, row, col, text, command, args))
        return button

    def AccentButton(self, text, command, args=(), row=None, col=0, padx=10, pady=10, sticky="nsew"):
        """Wrapper function for making an accent button. All params same as Button"""
        return self.Button(text, command, args, row, col, padx, pady, sticky,
                           style=ThemeStyles.ButtonStyles.AccentButton)

    def Entry(self, textvariable, row=None, col=0, padx=10, pady=10, sticky="nsew",
              validatecommand=None, validatecommandargs=(), validatecommandmode='%P',
              invalidcommand=None, invalidcommandargs=(), validate='all'):
        """
        Creates a ttk.Entry widget.
        :param textvariable: Variable to be used for tracking text
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param validatecommand: Command to be called for validation
        :param validatecommandargs: Args to be passed to validate command
        :param validatecommandmode: Callback substitution code, defaults to 'new value'
        :param invalidcommand: Command to be called if text is invalid
        :param invalidcommandargs: Args to be passed to invalid command
        :param validate: When the widget should validate, default is 'all'
        :return: ttk.Entry widget
        """
        validatefunc = self.register(partial(validatecommand, *validatecommandargs))
        invalidfunc = self.register(partial(invalidcommand, *invalidcommandargs))
        entry = ttk.Entry(self, textvariable=textvariable, validatecommand=(validatefunc, validatecommandmode),
                          invalidcommand=(invalidfunc, validatecommandmode), validate=validate)

        row = self.getRow(row, col)
        entry.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)

        self.widgets.append(Widget(entry, "TextInput", row, col))

        return entry

    def NumericaSpinbox(self, lower, upper, increment, variable, validatecommand=isConstrainedFloat,
                        validatecommandargs=(), validatecommandmode='%P', validate='focusout',
                        row=None, col=0, padx=10, pady=10, sticky="nsew"):
        """
        Creates a ttk.Spinbox designed for numbers.
        :param lower: Min value
        :param upper: Max value
        :param increment: Change when arrow is pressed
        :param variable: Variable to hold value
        :param validatecommand: Command called to validate input, defaults to isFloat
            Will always contain lower and upper as first two params
        :param validatecommandargs: Args passed to command
        :param validatecommandmode: Command validation mode, defaults to new text
        :param validate: When input should be validated, defaults to all
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :return: ttk.Spinbox
        """
        validatefunc = self.register(partial(validatecommand, lower, upper, *validatecommandargs))
        spinbox = ttk.Spinbox(self, textvariable=variable, validatecommand=(validatefunc, validatecommandmode),
                              validate=validate, from_=lower, to=upper, increment=increment)

        row = self.getRow(row, col)
        spinbox.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)

        self.widgets.append(Widget(spinbox, "NumericalSpinbox" + str((lower, upper, increment)), row, col))
        return spinbox


    def NonnumericalSpinbox(self, values, variable, validatecommand=isMember,
                        validatecommandargs=(), validatecommandmode='%P', validate='focusout',
                        row=None, col=0, padx=10, pady=10, sticky="nsew", wrap=True):
        """
        Creates a ttk.Spinbox designed for numbers.
        :param values: Values for spinbox to rotate through
        :param variable: Variable to hold value
        :param validatecommand: Command called to validate input
        :param validatecommandargs: Args passed to command, always contains values
        :param validatecommandmode: Command validation mode, defaults to new text
        :param validate: When input should be validated, defaults to on click out
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param wrap: Values warp around
        :return: ttk.Spinbox
        """
        validatefunc = self.register(partial(validatecommand, values, *validatecommandargs))
        spinbox = ttk.Spinbox(self, textvariable=variable, validatecommand=(validatefunc, validatecommandmode),
                              validate=validate, values=values, wrap=wrap)

        row = self.getRow(row, col)
        spinbox.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        name = "Spinbox"
        if len(str(values)) < 25:
            name = "Spinbox(" + str(values)[1:-2] + ")"
        self.widgets.append(Widget(spinbox, name, row, col))
        return spinbox

    def Treeview(self, columnnames, columnwidths, height, data, datasubfilename, datacolumnnames=None,
                 anchor='w', row=None, col=0, padx=10, pady=10, sticky="nsew"):
        assert len(columnnames) == len(columnwidths), "Column params must be the same length"
        if datacolumnnames is None:
            datacolumnnames = columnnames
        else:
            assert len(columnnames) == len(datacolumnnames), "Column params must be the same length"
        treeViewFrame = ttk.Frame(self)
        row = self.getRow(row, col)
        treeViewFrame.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        scrollbar = ttk.Scrollbar(treeViewFrame)
        scrollbar.pack(side="right", fill="y")

        columns = []
        for i in range(1, len(columnnames)):
            columns.append("#" + str(i))
        treeview = ttk.Treeview(treeViewFrame, yscrollcommand=scrollbar.set, columns=columns, height=height)
        treeview.pack(expand=True, fill="both")
        scrollbar.config(command=treeview.yview)

        for i in range(0, len(columnnames)):
            treeview.column("#" + str(i), anchor=anchor, width=columnwidths[i])
            treeview.heading("#" + str(i), text=columnnames[i], anchor="center")

        def traverse(p, t, iid):
            for obj in t:
                iid[0] += 1
                values = []
                for value in datacolumnnames[1:]:
                    values.append(obj.get(value, ""))
                treeview.insert(p, index='end', iid=iid[0], text=obj[datacolumnnames[0]], values=values)
                if obj.get(datasubfilename, []):
                    treeview.item(iid[0], open=True)  # Open parents
                traverse(iid[0], obj.get('subfiles', []), iid)

        traverse('', data, [0])
        self.widgets.append(Widget(treeview, "Treeview", row, col))
        return treeview


    def debugPrint(self, recursive=True):
        subframes = []
        for widget in self.widgets:
            if type(widget.widget) == WidgetFrame:
                subframes.append(widget)

        print("Widget Frame: " + self.text)
        tabulate(self.widgets)
        if recursive:
            for frame in subframes:
                frame.debugPrint(True)