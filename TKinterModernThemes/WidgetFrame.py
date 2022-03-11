"""
Source for widget frame, including all widget creation functions
"""

from TKinterModernThemes.ThemeStyles import ThemeStyles
from functools import partial as PARTIAL #for calling funcs with args
from warnings import warn
from tkinter import ttk
from typing import List, Union, Tuple
from typing_extensions import Literal
import math
import tkinter as tk

toolbartype = None

#region validation funcs
def isFloat(x) -> bool:
    """
    Validation function used for a widget, returns true if x is float
    """
    try:
        float(x)
        return True
    except ValueError:
        return False

def isConstrainedFloat(lower, upper, x) -> bool:
    """
    Validation function used for a widget, returns true if x is within range
    :param lower: lower bound
    :param upper: upper bound
    :param x: value
    """
    return isFloat(x) and lower <= float(x) <= upper

def isMember(values, x) -> bool:
    """
    Validation function used for a widget, returns true if x is in values
    """
    return x in values

def adjust(lower, inputvar, pbvar, _var, _indx, _mode):
    """
    Copies variable value, but subtracts value
    """
    pbvar.set(inputvar.get() - lower)
#endregion
#region help funcs
def partial(command, *args):
    """
    Creates a partial function, but returns None if command is None
    """
    if command is not None:
        return PARTIAL(command, *args)
    return None

def noneDict(*args):
    """
    Used for replacing None with {}
    """
    l = []
    for arg in args:
        if arg is None:
            l.append({})
        else:
            l.append(arg)
    return l

#region classes
class Widget:
    def __init__(self, widget, name: str, row: int, col: int, rowspan: int, colspan: int, text="",
                 command=None, args=()):
        """
        Internal structure for storing widget information

        :param widget: refrence to tk widget
        :param name: friendly, printable name
        :param row: from grid
        :param col: from grid
        :param rowspan: from grid
        :param colspan: from grid
        :param text: more text for printing
        :param command: run when widget is interacted with
        :param args: args for command
        """
        self.widget = widget
        self.name = name
        self.row = row
        self.rowspan = rowspan
        self.colspan = colspan
        self.col = col
        self.text = text

        self.commandstr = ""
        if command is not None:
            self.commandstr = " -> " + command.__name__ + str(args)

    def __str__(self):
        if type(self.widget) in [WidgetFrame, Notebook]:
            return self.name + ": " + self.text
        if self.text == "":
            return self.name + self.commandstr
        else:
            return self.name + '("' + self.text + '")' + self.commandstr

    def debugPrint(self, recursive=True):
        """
        Calls internal debug print for widget
        """
        self.widget.debugPrint(recursive)
        
class WidgetList:
    def __init__(self):
        """Class for storing groups of widgets"""
        self.widgetlist = []
        
    def append(self, item: Widget):
        for widget in self.widgetlist:
            if (item.row <= widget.row + widget.rowspan - 1 < item.row + item.rowspan and 
                    item.col <= widget.col + widget.colspan - 1 < item.col + item.colspan):
                warn("Overlapping widgets! Row: " + str(item.row) + ", col: " + str(item.col) +
                     ", original: '" + str(widget) + "', new: '" + str(item) + "'")
        self.widgetlist.append(item)
        
    def __iter__(self):
        return self.widgetlist.__iter__()
#endregion
#region tabulate
def centerText(text, longesttext):
    """
    Internal function for printing debug info, called by tabulate
    """
    ldif = longesttext - len(text)
    return " " * math.floor(ldif / 2) + text + " " * math.ceil(ldif / 2)

def printRow(grid, i, longesttext):
    """
    Internal function for printing debug info, called by tabulate
    """
    s = '|'
    row = grid[i]
    for col in range(0, len(row)):
        widget = row[col]
        if widget is not None:
            s += centerText(str(widget), longesttext[col])
            if widget.colspan > 1:
                if col < len(grid[i]) - 1:
                    grid[i][col+1] = Widget(None, "", 0, 0, widget.rowspan, widget.colspan-1)
                s += " "
            else:
                s += '|'
        else:
            s += " " * longesttext[col] + "|"
    print(s)


def printSeperator(grid: List[List[Widget]], i, longesttext):
    """
    Internal function for printing debug info, called by tabulate
    """
    s = "+"
    if i == 0:
        row = [None] * len(grid[0])
    else:
        row: List[Union[Widget, None]] = grid[i-1]

    for col in range(0, len(grid[0])):
        widget: Widget = row[col]
        if widget is None or widget.rowspan == 1:
            s += "-" * longesttext[col]
        else:
            s += " " * longesttext[col]
            if i < len(grid):
                grid[i][col] = Widget(None, "", 0, 0, widget.rowspan-1, widget.colspan)
        s += "+"
    print(s)

def tabulate(widgets):
    """
    Internal function for printing debug info
    """
    maxrow = 0
    maxcol = 0

    for widget in widgets:
        maxrow = max(widget.row, maxrow)
        maxcol = max(widget.col, maxcol)

    longesttext = [0] * (maxcol + 1)
    for widget in widgets:
        longesttext[widget.col] = max(longesttext[widget.col], len(str(widget)))

    for i in range(0, len(longesttext)):
        longesttext[i] = max(longesttext[i] + 2, 3)

    grid: List[List] = []
    for i in range(0, maxrow+1):
        grid.append([None]*(maxcol+1))

    for widget in widgets:
        grid[widget.row][widget.col] = widget

    i = 0
    for i in range(0, maxrow+1):
        printSeperator(grid, i, longesttext)
        printRow(grid, i, longesttext)
    printSeperator(grid, i+1, longesttext)
    print()
#endregion
#endregion

class Notebook:
    def __init__(self, master, name, **widgetkwargs):
        """Creates a widget frame based notebook."""
        self.notebook = ttk.Notebook(master, **widgetkwargs)
        self.tabs = []
        self.frames = []
        self.name = name

    def addTab(self, text):
        """
        Adds a tab to the notebook. Text is used as label. Returns a WidgetFrame

        :param text: Text to label tab
        """

        tab = ttk.Frame(self.notebook)
        self.tabs.append(tab)
        widgetFrame = WidgetFrame(tab, self.name + " Tab: " + text)
        self.frames.append(widgetFrame)
        self.notebook.add(tab, text=text)
        return widgetFrame

    def makeResizable(self, recursive=True, onlyFrames=True):
        """See make resizable in WidgetFrame"""
        if recursive:
            for frame in self.frames:
                frame.makeResizable(onlyFrames=onlyFrames)

    def debugPrint(self, recursive=True):
        for frame in self.frames:
            frame.debugPrint(recursive)

class PanedWindow:
    def __init__(self, master, name, orient: Literal["vertical", 'horiztonal'] = 'vertical', **widgetkwargs):
        """Creates a widget frame based panedwindow."""
        self.panedwindow = ttk.PanedWindow(master, orient=orient, **widgetkwargs)
        self.windows = []
        self.frames = []
        self.name = name

    def addWindow(self, weight=1):
        """
        Adds a tab to the notebook.

        :param weight: Weight for window, windows with higher weight get more space allocated
        """

        window = ttk.Frame(self.panedwindow)
        self.windows.append(window)
        widgetFrame = WidgetFrame(window, self.name + " Window: " + str(len(self.windows)))
        self.frames.append(widgetFrame)
        self.panedwindow.add(window, weight=weight)
        return widgetFrame

    def makeResizable(self, recursive=True, onlyFrames=True):
        """See make resizable in WidgetFrame"""
        if recursive:
            for frame in self.frames:
                frame.makeResizable(onlyFrames=onlyFrames)

    def debugPrint(self, recursive=True):
        for frame in self.frames:
            frame.debugPrint(recursive)

class WidgetFrame:
    def __init__(self, master, name):
        """
        Creates a widget frame (a frame with some bonus features)
        References to the frame should be by self.master.

        :param master: Should be a frame
        :param name: Name of widget, used in labeling
        """

        self.name = name
        self.master = master
        self.rowcounters: List[int] = []
        self.skiprows: List[List[int]] = [] #used for preventing colspan overlap
        self.widgets = WidgetList()
        self.activecol = 0
        self.resizableWidgets = None
        
    def setActiveCol(self, value):
        """Set col for newly placed widgets to drop into"""
        self.activecol = value

    def nextCol(self):
        """Increments col by one"""
        self.activecol += 1

    def makeResizable(self, recursive=True, onlyFrames=True):
        """
        Makes all subframes resize nicely. Configure resizable widgets in self.resizableWidgets

        :param recursive: Resize applies to subframes of subframes
        :param onlyFrames: Only resize frame rows (makes widgets look better)
        """
        allFrames = True
        for widget in self.widgets:
            if self.resizableWidgets is None:
                resizableWidgets = [Notebook, WidgetFrame, PanedWindow, ttk.Separator, ttk.Label,
                                           ttk.Treeview, toolbartype]
            else:
                resizableWidgets = self.resizableWidgets
            if type(widget.widget) not in resizableWidgets:
                allFrames = False

        if allFrames or not onlyFrames:
            for index in range(self.master.grid_size()[0]):
                self.master.columnconfigure(index=index, weight=1)

            for index in range(self.master.grid_size()[1]):
                self.master.rowconfigure(index=index, weight=1)

        if recursive:
            for widget in self.widgets:
                if type(widget.widget) in [Notebook, PanedWindow, WidgetFrame]:
                    widget.widget.makeResizable(onlyFrames=onlyFrames)

    def getRow(self, row, col, rowspan, colspan) -> Tuple[int, int]:
        if col is None:
            col = self.activecol

        for _ in range(len(self.rowcounters), col + 1):
            self.rowcounters.append(0)
            self.skiprows.append([])

        if row is None: #auto find row
            row = self.rowcounters[col]
            done = False
            while not done:
                done = True
                for c in range(col, col+colspan):
                    if c >= len(self.skiprows):
                        self.skiprows.append([])

                    for r in range(row, row+rowspan):
                        if r in self.skiprows[c]:
                            done = False
                if not done:
                    row += 1

        self.rowcounters[col] = row + rowspan

        for i in range(col, col+colspan):
            if i < len(self.skiprows):
                self.skiprows[i].append(row)
            else:
                self.skiprows.append([row])
        return row, col

    #region Widget Frames
    def addFrame(self, name: str, row: int = None, col: int = None, padx=(20,20), pady=(20,20), sticky="nsew",
                 rowspan: int = 1, colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a widget frame based around a ttk.Frame

        :param name: Name for debugging
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.Frame(self.master, **gridkwargs)
        frame = WidgetFrame(widget, name)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan,
                    columnspan = colspan, **gridkwargs)
        self.widgets.append(Widget(frame, "Widget Frame", row, col, rowspan, colspan, name))
        return frame

    def addLabelFrame(self, text: str, row: int = None, col: int = None, padx=(20, 20), pady=(20, 20), sticky="nsew",
                      rowspan: int = 1, colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a widget frame based around a ttk.Frame

        :param text: Label text
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.LabelFrame(self.master, text=text, **gridkwargs)
        frame = WidgetFrame(widget, text)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan,
                    **gridkwargs)
        self.widgets.append(Widget(frame, "Widget Frame", row, col, rowspan, colspan, text))
        return frame

    #endregion
    #region widgets
    def Checkbutton(self, text: str, variable: tk.Variable, command = None, args=(), row: int =None, col: int =0,
                    padx=10, pady=10, sticky="nsew", disabled: bool = False, style = None, rowspan: int = 1,
                    colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):
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
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.Checkbutton(self.master, text=text, variable=variable, command=partial(command, *args),
                                 style=style, **widgetkwargs)

        if disabled:
            widget.state(["disabled !alternate"])
        row, col = self.getRow(row, col, rowspan, colspan)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan, **gridkwargs)
        widgetname = "CheckButton"
        if style == ThemeStyles.CheckbuttonStyles.ToggleButton:
            widgetname = "ToggleButton"
        elif style == ThemeStyles.CheckbuttonStyles.SlideSwitch:
            widgetname = "SlideSwitch"
        self.widgets.append(Widget(widget, widgetname, row, col, rowspan, colspan, text, command, args))
        return widget

    def ToggleButton(self, text: str, variable: tk.Variable, command = None, args=(), row: int =None, col: int =0,
                    padx=10, pady=10, sticky="nsew", rowspan: int = 1, colspan: int = 1,
                     widgetkwargs: dict = None, gridkwargs: dict = None):
        """Wrapper function for creating a toggle button. All params same as checkbutton."""
        return self.Checkbutton(text, variable, command, args, row, col, padx, pady, sticky, False,
                                ThemeStyles.CheckbuttonStyles.ToggleButton, rowspan, colspan,widgetkwargs, gridkwargs)

    def SlideSwitch(self, text: str, variable: tk.Variable, command=None, args=(), row: int = None, col: int = None,
                    padx=10, pady=10, sticky="nsew", rowspan: int = 1, colspan: int = 1,
                    widgetkwargs: dict = None, gridkwargs: dict = None):
        """Wrapper function for creating a toggle button. All params same as checkbutton."""
        return self.Checkbutton(text, variable, command, args, row, col, padx, pady, sticky, False,
                                ThemeStyles.CheckbuttonStyles.SlideSwitch, rowspan, colspan, widgetkwargs, gridkwargs)

    def Radiobutton(self, text: str, variable: tk.Variable, value, command=None, args=(), row: int = None,
                    col: int = None, padx=10, pady=10, sticky="nsew", disabled: bool = False, rowspan: int = 1,
                    colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):
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
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        state = None
        if disabled:
            state = "disabled"
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.Radiobutton(self.master, text=text, variable=variable, value=value,
                                 command=partial(command, *args), state=state, **widgetkwargs)

        row, col = self.getRow(row, col, rowspan, colspan)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan, **gridkwargs)

        self.widgets.append(Widget(widget, "Radiobutton<" + str(value) + ">", row, col, rowspan, colspan, text,
                                   command=partial(command, *args)))
        return widget

    def Seperator(self, row: int = None, col: int = None, padx=10, pady=10, sticky="ew", rowspan: int = 1,
                  colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Adds a ttk.Seperator

        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid, defaults to 'ew' (recommended)
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """

        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.Separator(self.master, **widgetkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan, **gridkwargs)
        self.widgets.append(Widget(widget, "Seperator", row, col, rowspan, colspan))
        return widget

    def Button(self, text: str, command, args=(), row: int = None, col: int = None, padx=10, pady=10, sticky="nsew",
               style=None, rowspan: int = 1, colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):
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
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.Button(self.master, text=text, command=partial(command, *args), style=style, **widgetkwargs)

        row, col = self.getRow(row, col, rowspan, colspan)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan, **gridkwargs)

        widgetname = "Button"
        if style is not None:
            if style == ThemeStyles.ButtonStyles.AccentButton:
                widgetname = "Accent Button"
        self.widgets.append(Widget(widget, widgetname, row, col, rowspan, colspan, text, command, args))
        return widget

    def AccentButton(self, text: str, command, args=(), row: int = None, col: int = None, padx=10, pady=10,
                     rowspan: int = 1, colspan: int = 1, sticky="nsew", widgetkwargs: dict = None,
                     gridkwargs: dict = None):
        """Wrapper function for making an accent button. All params same as Button"""
        return self.Button(text, command, args, row, col, padx, pady, sticky,
                           ThemeStyles.ButtonStyles.AccentButton, rowspan, colspan, widgetkwargs, gridkwargs)

    def Entry(self, textvariable: tk.Variable, row: int = None, col: int = None, padx=10, pady=10, sticky="nsew",
              validatecommand=None, validatecommandargs=(), validatecommandmode='%P', invalidcommand=None,
              invalidcommandargs=(), validate=None, rowspan: int = 1, colspan: int = 1,
              widgetkwargs: dict = None, gridkwargs: dict = None):
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
        :param validate: When the widget should validate, default is 'all' if command is supplied, none otherwise
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """

        if validate is None:
            if validatecommand is not None:
                validate = 'all'
            else:
                validate = 'none'

        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        validatefunc = self.master.register(partial(validatecommand, *validatecommandargs))
        invalidfunc = self.master.register(partial(invalidcommand, *invalidcommandargs))
        widget = ttk.Entry(self.master, textvariable=textvariable, validatecommand=(validatefunc, validatecommandmode),
                           invalidcommand=(invalidfunc, validatecommandmode), validate=validate, **widgetkwargs)

        row, col = self.getRow(row, col, rowspan, colspan)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan, **gridkwargs)
        self.widgets.append(Widget(widget, "TextInput", row, col, rowspan, colspan))
        return widget

    def NumericalSpinbox(self, lower: float, upper: float, increment: float, variable: tk.Variable,
                         validatecommand=isConstrainedFloat, validatecommandargs=(), validatecommandmode='%P',
                         validate:Literal['none', 'focus', 'focusin', 'focusout', 'key', 'all']='focusout',
                         row: int = None, col: int = None, padx=10, pady=10, sticky="nsew",
                         rowspan: int = 1, colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):
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
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        validatefunc = self.master.register(partial(validatecommand, lower, upper, *validatecommandargs))
        widget = ttk.Spinbox(self.master, textvariable=variable, validatecommand=(validatefunc, validatecommandmode),
                             validate=validate, from_=lower, to=upper, increment=increment, **widgetkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan, **gridkwargs)
        self.widgets.append(Widget(widget, "NumericalSpinbox" + str((lower, upper, increment)),
                                   row, col, rowspan, colspan))
        return widget

    def NonnumericalSpinbox(self, values: list, variable: tk.Variable, validatecommand=isMember,
                            validatecommandargs=(), validatecommandmode='%P',
                            validate:Literal['none', 'focus', 'focusin', 'focusout', 'key', 'all']='focusout',
                            row: int = None, col: int = None, padx=10, pady=10, sticky="nsew", wrap: bool = True,
                            rowspan: int = 1, colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):
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
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param gridkwargs: Passed to grid placement
        :param wrap: Should values warp around

        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        validatefunc = self.master.register(partial(validatecommand, values, *validatecommandargs))
        widget = ttk.Spinbox(self.master, textvariable=variable, validatecommand=(validatefunc, validatecommandmode),
                             validate=validate, values=values, wrap=wrap, **widgetkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget.grid(row=row, column=col, padx=padx, pady=pady, columnspan=colspan, rowspan=rowspan, sticky=sticky,
                    **gridkwargs)
        name = "Spinbox"
        if len(str(values)) < 25:
            name = "Spinbox(" + str(values)[1:-2] + ")"
        self.widgets.append(Widget(widget, name, row, col, rowspan, colspan))
        return widget

    def Treeview(self, columnnames: list, columnwidths: list, height: int, data: dict, subentryname: str,
                 datacolumnnames: list = None, openkey = None, anchor='w', newframe = True, row: int = None,
                 col: int =0, padx=10, pady=10, sticky="nsew", rowspan: int = 1, colspan: int = 1,
                 widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a ttk.Treeview. Will load in data presented in a nested dict.

        :param columnnames: Column header names
        :param columnwidths: Width of each column
        :param height: number of rows
        :param data: nested dict
        :param subentryname: key in dict to go to next layer
        :param datacolumnnames: defaults to columnnames, a mapping of columnnames to the data file
        :param openkey: bool key to set subentries open or closed
        :param anchor: text position
        :param newframe: creates a frame for the treeview and scrollbar, needed if master frame contains other widgets
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        assert len(columnnames) == len(columnwidths), "Column params must be the same length"
        if datacolumnnames is None:
            datacolumnnames = columnnames
        else:
            assert len(columnnames) == len(datacolumnnames), "Column params must be the same length"
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        if newframe:
            widgetFrame = ttk.Frame(self.master)
            widgetFrame.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, columnspan=colspan,
                             rowspan=rowspan, **gridkwargs)
        else:
            widgetFrame = self.master

        scrollbar = ttk.Scrollbar(widgetFrame)
        scrollbar.pack(side="right", fill="y")

        columns = []
        for i in range(1, len(columnnames)):
            columns.append("#" + str(i))
        widget = ttk.Treeview(widgetFrame, yscrollcommand=scrollbar.set, columns=columns, height=height, **widgetkwargs)
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
                if obj.get(subentryname, []):
                    if openkey is None:
                        widget.item(iid[0], open=True)  # Open parents
                    else:
                        widget.item(iid[0], open=obj[openkey])
                traverse(iid[0], obj.get(subentryname, []), iid)

        traverse('', data, [0])
        self.widgets.append(Widget(widget, "Treeview", row, col, rowspan, colspan))
        return widget

    def OptionMenu(self, values: list, variable: tk.Variable, command=None, args=(), default=None, row: int=None,
                   col: int = None, padx=10, pady=10, sticky="nsew", rowspan: int = 1, colspan: int = 1,
                   widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a ttk.OptionMenu

        :param variable: holds current state
        :param values: options
        :param command: Called on value selection with param value
        :param args: Passed to command (before menu value)
        :param default: default value, defaults to first item
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        if default is None:
            default = values[0]
        widget = ttk.OptionMenu(self.master, variable, default, command=partial(command,*args), *values, **widgetkwargs)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan,
                    **gridkwargs)
        name = "OptionMenu"
        if len(str(values)) < 25:
            name = "OptionMenu(" + str(values)[1:-2] + ")"
        self.widgets.append(Widget(widget, name, row, col, rowspan, colspan))
        return widget

    def Combobox(self, values: list, variable: tk.Variable, default = 0, row: int = None, col: int = None, padx=10,
                 pady=10, sticky="nsew", rowspan: int = 1, colspan: int = 1,
                 widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a ttk.Combobox (editable drop down menu)

        :param values: List of menu values
        :param default: Default menu values
        :param variable: Is set to value of box
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """

        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget = ttk.Combobox(self.master, textvariable = variable, values=values, **widgetkwargs)
        widget.current(default)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan, **gridkwargs)
        name = "Combobox"
        if len(str(values)) < 25:
            name = "Combobox(" + str(values)[1:-2] + ")"
        self.widgets.append(Widget(widget, name, row, col, rowspan, colspan))
        return widget

    def MenuButton(self, menu: tk.Menu, defaulttext: str, row: int = None, col: int = None, padx=10, pady=10,
                   sticky="nsew", rowspan: int = 1, colspan: int = 1,
                   widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a ttk.MenuButton

        :param menu: tk.Menu
        :param defaulttext: text to be displayed on top of dropdown
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """

        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget = ttk.Menubutton(self.master, text=defaulttext, menu=menu, **widgetkwargs)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan, **gridkwargs)
        self.widgets.append(Widget(widget, "MenuButton", row, col, rowspan, colspan, defaulttext))
        return widget

    def Notebook(self, name, row: int = None, col: int = None, padx=10, pady=10, sticky="nsew", rowspan: int = 1,
                 colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a ttk.Notebook

        :param name: Name for debugging
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget = Notebook(self.master, name, **widgetkwargs)
        widget.notebook.grid(row = row, column=col, padx=padx, pady=pady, sticky=sticky,
                             columnspan=colspan, rowspan=rowspan, **gridkwargs)
        self.widgets.append(Widget(widget, "Notebook", row, col, rowspan, colspan, name))

        return widget

    def PanedWindow(self, name, orient: Literal["vertical", 'horiztonal'] = 'vertical', row: int = None,
                    col: int = None, padx=10, pady=10, sticky="nsew",
                    rowspan: int = 1, colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):

        """
        Creates a ttk.PanedWindow with widgetframe compatability

        :param name: Name for debugging
        :param orient: "vertical" or "horizontal"
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """

        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget = PanedWindow(self.master, name, orient, **widgetkwargs)
        widget.panedwindow.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan = rowspan,
                                columnspan = colspan, **gridkwargs)
        self.widgets.append(Widget(widget, "Paned Window", row, col, rowspan, colspan, name))

        return widget

    def Blank(self, name = "Blank", row: int = None, col: int = None, rowspan=1, colspan=1):
        """
        Adds a blank space to prevent widget placement

        :param name: for debugging
        :param row: Passed to widget, defaults to +1 of last item in col
        :param col: Passed to widget, defaults to 0
        :param rowspan: Passed to widget
        :param colspan: Passed to widget
        """
        row, col = self.getRow(row, col, rowspan, colspan)
        self.widgets.append(Widget(None, name, row, col, rowspan, colspan))

    def Label(self, text: str, size=15, weight='bold', fontargs=(), row: int = None, col: int = None,
              padx=10, pady=10, sticky=None, rowspan: int = 1, colspan: int = 1,
              widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a ttk.label with a large font and bold text

        :param text: text to be displayed
        :param size: font size
        :param weight: font weight
        :param fontargs: additional font args
        :param row: Passed to widget, defaults to +1 of last item in col
        :param col: Passed to widget, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid - use to align text
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """

        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        font = ('-size', size, '-weight', weight) + fontargs
        widget = ttk.Label(self.master, text=text, font=font, **widgetkwargs)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan, **gridkwargs)
        self.widgets.append(Widget(widget, "Label: ", row, col, rowspan, colspan, text))

        return widget

    def Text(self, text: str, fontargs=(), row: int = None, col: int = None,
             padx=10, pady=10, sticky="nsw", rowspan: int = 1, colspan: int = 1,
             widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a ttk.label with normal text

        :param text: text to be displayed
        :param fontargs: additional font args
        :param row: Passed to widget, defaults to +1 of last item in col
        :param col: Passed to widget, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid - use to align text
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """

        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget = ttk.Label(self.master, text=text, font=fontargs, **widgetkwargs)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan,
                    **gridkwargs)
        self.widgets.append(Widget(widget, "Text: ", row, col, rowspan, colspan, text))

        return widget

    def Scale(self, lower: float, upper: float, variable: Union[tk.IntVar, tk.DoubleVar], row: int = None,
              col: int = None, padx=10, pady=10, sticky="ew", rowspan: int = 1, colspan: int = 1,
              widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a ttk.Scale (horizontal only, vertical is not supported with these themes)

        :param lower: Min value
        :param upper: Max value
        :param variable: Variable to hold value
        :param row: Passed to grid, defaults to +1 of last item in col
        :param col: Passed to grid, defaults to 0
        :param padx: Passed to grid
        :param pady: Passed to grid
        :param sticky: Passed to grid
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: Passed to widget creation
        :param gridkwargs: Passed to grid placement
        """
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        widget = ttk.Scale(self.master, variable=variable, from_=lower, to=upper, **widgetkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan, **gridkwargs)
        self.widgets.append(Widget(widget, "Scale" + str((lower, upper)), row, col, rowspan, colspan))
        return widget

    def Progressbar(self, variable: tk.Variable, mode: Literal["determinate", "indeterminate"] ="determinate", lower=0,
                    upper=100, row: int = None, col: int = None, padx=10, pady=10, sticky="ew", rowspan: int = 1,
                    colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a ttk.Progressbar. If lower is not 0, it will link a second variable for processing

        :param variable: tk.Variable to control progressbar
        :param mode: "determinate" for variable control, "indeterminate" for animation
        :param lower: min value (0 is highly recommended)
        :param upper: max value
        :param row: passed to grid
        :param col: passed to grid
        :param padx: passed to grid
        :param pady: passed to grid
        :param sticky: passed to grid
        :param rowspan: Passed to grid
        :param colspan: Passed to grid
        :param widgetkwargs: passed to widget
        :param gridkwargs: passed to grid
        """

        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)
        if lower != 0:
            var = tk.DoubleVar(value=variable.get() - lower)
            variable.trace_add("write", partial(adjust, lower, variable, var))
        else:
            var = variable
        widget = ttk.Progressbar(self.master, mode=mode, variable=var, maximum = upper - lower, **widgetkwargs)
        row, col = self.getRow(row, col, rowspan, colspan)
        widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan, columnspan=colspan, **gridkwargs)
        self.widgets.append(Widget(widget, "Progressbar" + str((lower, upper)), row, col, rowspan, colspan))
        return widget

    def matplotlibFrame(self, name, projection = None, toolbar = True, figsize=(4,4), figpadx: int = None,
                        figpady: int = None, row: int = None, col: int = None, padx=10, pady=10, sticky="ew",
                        rowspan: int = 1, colspan: int = 1, widgetkwargs: dict = None, gridkwargs: dict = None):
        """
        Creates a frame and drops in a matplotlib figure and axes.
        Returns canvas, fig, axes, backgroundcolor, accentcolor.


        :param name: Name for debugging
        :param projection: Figure projection, use '3d' for 3D
        :param toolbar: Shows a matplotlib toolbar
        :param figpadx: Extra padding around graph to stop rendering issues, default to 5 in 2d, 30 in 3d
        :param figpady: Extra padding around graph to stop rendering issues, default to 5 in 2d, (5,20) in 3d
        :param figsize: Sets figure creation size. Fig will not resize to below this point
        :param row: passed to grid
        :param col: passed to grid
        :param padx: passed to grid
        :param pady: passed to grid
        :param sticky: passed to grid
        :param rowspan: passed to grid
        :param colspan: passed to grid
        :param widgetkwargs: passed to widget
        :param gridkwargs: passed to grid
        """
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        except ImportError:
            warn("Matplotlib is required to use this feature.")
            return None, None, None, None

        if figpadx is None:
            if projection == '3d':
                figpadx = 30
            else:
                figpadx = 5

        if figpady is None:
            if projection == '3d':
                figpady = (5,20)
            else:
                figpady = 5

        if "dark" in self.master.tk.call("ttk::style", "theme", "use"):
            plt.style.use('dark_background')
        else:
            plt.style.use('default')
        backgroundcolor = self.master.option_get('background', ".")
        accentcolor = self.master.option_get("selectBackground", ".")
        fig = plt.figure(figsize=figsize, facecolor=backgroundcolor)
        ax = fig.add_subplot(111, projection=projection, facecolor=backgroundcolor)
        widgetkwargs, gridkwargs = noneDict(widgetkwargs, gridkwargs)

        graphframe = self.addFrame(name, row, col, padx, pady, sticky, rowspan, colspan,
                                            widgetkwargs=widgetkwargs, gridkwargs=gridkwargs)


        canvas = FigureCanvasTkAgg(fig, master=graphframe.master)  # A tk.DrawingArea.
        canvas.draw()
        row, col = self.getRow(row, col, 1, 1)
        canvas.get_tk_widget().grid(row=row, column=col, sticky='nsew', padx=figpadx, pady=figpady)
        if toolbar:
            toolbar = NavigationToolbar2Tk(canvas, self.master, pack_toolbar=False)
            toolbar.update()
            row, col = self.getRow(row, col, 1, 1)
            toolbar.grid(row=row, column=col, padx=5, sticky="sw")
            global toolbartype
            toolbartype = type(toolbar)
            self.widgets.append(Widget(toolbar, "Graph Toolbar", row, col, 1, 1))

        return canvas, fig, ax, backgroundcolor, accentcolor


    # endregion
    def debugPrint(self, recursive=True):
        subframes = []
        for widget in self.widgets:
            if type(widget.widget) in [WidgetFrame, Notebook, PanedWindow]:
                subframes.append(widget)

        print("Widget Frame: " + self.name)
        tabulate(self.widgets)
        if recursive:
            for frame in subframes:
                frame.debugPrint(True)