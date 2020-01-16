import tkinter
from tkinter import ttk


class OnBusTab:
    def __init__(self, parent, graph):
        self.parent = parent
        self.graph = graph
        self.master = ttk.Frame(self.parent)
        # Add to parent
        self.parent.add(self.master, text="Resources On Bus")

        lbl = tkinter.Label(self.master, text="Ahoj")
        lbl.pack()
