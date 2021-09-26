from TKinterModernThemes.ThemeStyles import ThemeStyles
from functools import partial as PARTIAL #for calling funcs with args
from warnings import warn
from tkinter import ttk
import math
import tkinter as tk


#region validation funcs
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
#endregion
#region help funcs
def partial(command, *args):
    if command is not None:
        return PARTIAL(command, *args)
    return None

def noneDict(*args):
    l = []
    for arg in args:
        if arg is None:
            l.append({})
        else:
            l.append(arg)
    return l

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
#endregion

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

class WidgetFrame:
    def __init__(self, master, name):
        """
        Creates a widget frame (a frame with some bonus features)
        References to the frame should be by self.master

        :param master: Should be a frame
        :param name: Name of widget, used in labeling
        """

        self.text = name
        self.master = master
        self.rowcounters = []
        self.widgets = []

    def getRow(self, row, col):
        for _ in range(len(self.rowcounters), col + 1):
            self.rowcounters.append(0)

        if row is None: #auto find row
            row = self.rowcounters[col]
        if row is not None:
            self.rowcounters[col] = row
        self.rowcounters[col] += 1
        for widget in self.widgets:
            if widget.row == row and widget.col == col:
                warn("Overlapping widgets! Row: " + str(row) + " col: " + str(col) +
                     " name: " + str(widget) + " name: " + str(widget))
        return row

    #region Widget Frames
    def addFrame(self, name: str, row: int, col: int, padx=(20,20), pady=(20,20), sticky="nsew", rowspan=1,
                 widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a widget frame based around a ttk.Frame

        :param name: Name for debugging
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param rowspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.Frame(self.master, **gridkwargs)
        frame = WidgetFrame(widget, name)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, **gridkwargs)
        self.widgets.append(Widget(frame, "Widget Frame", row, col, name))
        return frame

    def addLabelFrame(self, text: str, row: int, col: int, padx=(20, 20), pady=(20, 20), sticky="nsew", rowspan=1,
                 widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a widget frame based around a ttk.Frame

        :param text: Label text
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param rowspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.LabelFrame(self.master, text=text, **gridkwargs)
        frame = WidgetFrame(widget, text)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, **gridkwargs)
        self.widgets.append(Widget(frame, "Widget Frame", row, col, text))
        return frame

    #endregion
    #region widgets
    def Checkbutton(self, text: str, variable: tk.Variable, command = None, args=(), row: int =None, col: int =0,
                    padx=10, pady=10, sticky="nsew", disabled: bool = False, style = None,
                    widgetkwargs: dict = None, gridkwargs: dict = None):
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
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.Checkbutton(self.master, text=text, variable=variable, command=partial(command, *args),
                                 style=style, **widgetkwargs)

        if disabled:
            widget.state(["disabled !alternate"])

        row = self.getRow(row, col)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, **gridkwargs)
        widgetname = "CheckButton"
        if style == ThemeStyles.CheckbuttonStyles.ToggleButton:
            widgetname = "ToggleButton"
        elif style == ThemeStyles.CheckbuttonStyles.SlideSwitch:
            widgetname = "SlideSwitch"
        self.widgets.append(Widget(widget, widgetname, row, col, text, command, args))
        return widget

    def ToggleButton(self, text: str, variable: tk.Variable, command = None, args=(), row: int =None, col: int =0,
                    padx=10, pady=10, sticky="nsew", widgetkwargs: dict = None, gridkwargs: dict = None):
        """Wrapper function for creating a toggle button. All params same as checkbutton."""
        return self.Checkbutton(text, variable, command, args, row, col, padx, pady, sticky,
                                False, ThemeStyles.CheckbuttonStyles.ToggleButton, widgetkwargs, gridkwargs)

    def SlideSwitch(self, text: str, variable: tk.Variable, command=None, args=(), row: int = None, col: int = 0,
                    padx=10, pady=10, sticky="nsew", widgetkwargs: dict = None, gridkwargs: dict = None):
        """Wrapper function for creating a toggle button. All params same as checkbutton."""
        return self.Checkbutton(text, variable, command, args, row, col, padx, pady, sticky,
                                False, ThemeStyles.CheckbuttonStyles.SlideSwitch, widgetkwargs, gridkwargs)

    def Radiobutton(self, text: str, variable: tk.Variable, value, command=None, args=(), row: int = None, col: int = 0,
                    padx=10, pady=10, sticky="nsew", disabled: bool = False, widgetkwargs: dict = None,
                    gridkwargs: dict = None):
        """
        Creates a ttk.Radiobutton widget

        :param text: Label next to widget
        :param value: Value that variable is set to when button clicked
        :param variable: TK variable that auto updates when radiobutton changes
        :param command: Command that is called on change
        :param args: Args passsed to command
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param disabled: Puts checkbox in disabled state, default False
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        state = None
        if disabled:
            state = "disabled"
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.Radiobutton(self.master, text=text, variable=variable, value=value,
                                 command=partial(command, *args), state=state, **widgetkwargs)

        row = self.getRow(row, col)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, **gridkwargs)

        self.widgets.append(Widget(widget, "Radiobutton<" + str(value) + ">", row, col, text,
                                   command=partial(command, *args)))
        return widget

    # endregion
    def Button(self, text: str, command=None, args=(), row: int = None, col: int = 0, padx=10, pady=10, sticky="nsew",
               style=None, widgetkwargs: dict = None, gridkwargs: dict = None):
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
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.Button(self.master, text=text, command=partial(command, *args), style=style, **widgetkwargs)

        row = self.getRow(row, col)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, **gridkwargs)

        widgetname = "Button"
        if style is not None:
            if style == ThemeStyles.ButtonStyles.AccentButton:
                widgetname = "Accent Button"
        self.widgets.append(Widget(widget, widgetname, row, col, text, command, args))
        return widget

    def AccentButton(self, text: str, command=None, args=(), row: int = None, col: int = 0, padx=10, pady=10,
                     sticky="nsew", widgetkwargs: dict = None, gridkwargs: dict = None):
        """Wrapper function for making an accent button. All params same as Button"""
        return self.Button(text, command, args, row, col, padx, pady, sticky,
                           ThemeStyles.ButtonStyles.AccentButton, widgetkwargs, gridkwargs)

    def Entry(self, textvariable: tk.Variable, row: int = None, col: int = 0, padx=10, pady=10, sticky="nsew",
              validatecommand=None, validatecommandargs=(), validatecommandmode='%P', invalidcommand=None,
              invalidcommandargs=(), validate='all', widgetkwargs: dict = None, gridkwargs: dict = None):
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
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        validatefunc = self.master.register(partial(validatecommand, *validatecommandargs))
        invalidfunc = self.master.register(partial(invalidcommand, *invalidcommandargs))
        widget = ttk.Entry(self.master, textvariable=textvariable, validatecommand=(validatefunc, validatecommandmode),
                           invalidcommand=(invalidfunc, validatecommandmode), validate=validate, **widgetkwargs)

        row = self.getRow(row, col)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, **gridkwargs)
        self.widgets.append(Widget(widget, "TextInput", row, col))
        return widget

    def NumericaSpinbox(self, lower: float, upper: float, increment: float, variable: tk.Variable,
                        validatecommand=isConstrainedFloat, validatecommandargs=(), validatecommandmode='%P',
                        validate='focusout', row: int = None, col: int = 0, padx=10, pady=10, sticky="nsew",
                        widgetkwargs: dict = None, gridkwargs: dict = None):
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
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        validatefunc = self.master.register(partial(validatecommand, lower, upper, *validatecommandargs))
        widget = ttk.Spinbox(self.master, textvariable=variable, validatecommand=(validatefunc, validatecommandmode),
                             validate=validate, from_=lower, to=upper, increment=increment, **widgetkwargs)

        row = self.getRow(row, col)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, **gridkwargs)
        self.widgets.append(Widget(widget, "NumericalSpinbox" + str((lower, upper, increment)), row, col))
        return widget

    def NonnumericalSpinbox(self, values: list, variable: tk.Variable, validatecommand=isMember,
                            validatecommandargs=(), validatecommandmode='%P', validate='focusout',
                            row: int = None, col: int = 0, padx=10, pady=10, sticky="nsew", wrap: bool = True,
                            widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a ttk.Spinbox designed for lists.

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
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        :param wrap: Should Values warp around

        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        validatefunc = self.master.register(partial(validatecommand, values, *validatecommandargs))
        widget = ttk.Spinbox(self.master, textvariable=variable, validatecommand=(validatefunc, validatecommandmode),
                             validate=validate, values=values, wrap=wrap, **widgetkwargs)

        row = self.getRow(row, col)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        name = "Spinbox"
        if len(str(values)) < 25:
            name = "Spinbox(" + str(values)[1:-2] + ")"
        self.widgets.append(Widget(widget, name, row, col))
        return widget

    def Treeview(self, columnnames: list, columnwidths: list, height: int, data: dict, datasubfilename: str,
                 datacolumnnames: list = None, anchor='w', row: int = None, col: int =0, padx=10, pady=10,
                 sticky="nsew", widgetkwargs: dict = None, gridkwargs: dict = None):
        assert len(columnnames) == len(columnwidths), "Column params must be the same length"
        if datacolumnnames is None:
            datacolumnnames = columnnames
        else:
            assert len(columnnames) == len(datacolumnnames), "Column params must be the same length"
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widgetFrame = ttk.Frame(self.master)
        row = self.getRow(row, col)
        widgetFrame.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, **gridkwargs)
        scrollbar = ttk.Scrollbar(widgetFrame)
        scrollbar.pack(side="right", fill="y")

        columns = []
        for i in range(1, len(columnnames)):
            columns.append("#" + str(i))
        widget = ttk.Treeview(widgetFrame, yscrollcommand=scrollbar.set, columns=columns, height=height,
                              **widgetkwargs)
        widget.pack(expand=True, fill="both")
        scrollbar.config(command=widget.yview)

        for i in range(0, len(columnnames)):
            widget.column("#" + str(i), anchor=anchor, width=columnwidths[i])
            widget.heading("#" + str(i), text=columnnames[i], anchor="center")

        def traverse(p, t, iid):
            for obj in t:
                iid[0] += 1
                values = []
                for value in datacolumnnames[1:]:
                    values.append(obj.get(value, ""))
                widget.insert(p, index='end', iid=iid[0], text=obj[datacolumnnames[0]], values=values)
                if obj.get(datasubfilename, []):
                    widget.item(iid[0], open=True)  # Open parents
                traverse(iid[0], obj.get('subfiles', []), iid)

        traverse('', data, [0])
        self.widgets.append(Widget(widget, "Treeview", row, col))
        return widget


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