import tkinter
from tkinter import ttk

from gui.add_tab import AddTab
from gui.generate_tab import GenerateTab
from gui.on_bus_tab import OnBusTab


class GUI:
    def __init__(self, graph):
        self.master: tkinter.Tk = tkinter.Tk()
        self.master.title("Factorio Recipe Graph Generator")
        self.graph = graph

        # Create tabs
        self.tab_parent = ttk.Notebook(self.master)

        self.tab_generate = GenerateTab(self.tab_parent, self.graph)
        self.tab_add = AddTab(self.tab_parent, self.graph)
        self.tab_bus = OnBusTab(self.tab_parent, self.graph)

        self.tab_parent.pack(expand=1, fill="both")

    def run(self):
        self.master.mainloop()
