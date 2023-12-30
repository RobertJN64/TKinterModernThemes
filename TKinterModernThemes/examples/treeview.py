"""
Simple demo of treeview widget
"""

import TKinterModernThemes as TKMT

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Treeview", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        tree_data = [
            {"fruit": "apple"},
            {"fruit": "orange"},
            {"fruit": "lemon"},
        ]

        self.frame = self.addLabelFrame("Treeview Frame")
        self.treeview_widget = self.frame.Treeview(['Fruit'], [120], 10, tree_data, None, ['fruit'])
        self.frame.AccentButton("Print Selected Items", self.print_selected_cmd)

        tree_data_2 = [
            {"fruit": "apple", "color": "red", "open": True, "subdata": [
                {"fruit": "pear"}
            ]},
            {"fruit": "orange", "color": "orange", "open": False, "subdata": [
                {"fruit": "pear"}
            ]},
            {"fruit": "lemon"},
        ]

        self.frame = self.addLabelFrame("Treeview Frame")
        self.frame.Treeview(['Fruit', 'Color'], [120, 120], 10, tree_data_2, 'subdata', ['fruit', 'color'],
                            openkey='open')

        self.run()

    def print_selected_cmd(self):
        print("Currently selected:", self.treeview_widget.selection())
        for item in self.treeview_widget.selection():
            print('--', self.treeview_widget.item(item))

if __name__ == "__main__":
    App("park", "dark")
