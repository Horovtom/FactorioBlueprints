import tkinter
from tkinter import ttk


class AddTab:
    def __init__(self, parent, graph):
        self.parent = parent
        self.graph = graph
        self.master = ttk.Frame(self.parent)
        # Add to parent
        self.parent.add(self.master, text="Add Recipe")

        lbl = tkinter.Label(self.master, text="Ahoj")
        lbl.pack()
