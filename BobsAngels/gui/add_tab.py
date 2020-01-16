import tkinter
from tkinter import ttk


class AddTab:
    def __init__(self, parent, graph):
        self.parent = parent
        self.graph = graph
        self.master = ttk.Frame(self.parent)
        # Add to parent
        self.parent.add(self.master, text="Add Recipe")

        ttk.Label(self.master, text="Recipe name:").grid(row=0, column=0)
        self.entry_recipe_name = ttk.Entry(self.master)
        self.entry_recipe_name.grid(row=0, column=1)

        ttk.Label(self.master, text="Incoming").grid(row=1, column=0)
        self.incoming_frame = ttk.Frame(self.master, padding=(10, 10, 10, 10))
        self.incoming_frame.grid(row=2, column=0)

        self.incoming_resources = []
        self.incoming_amounts = []
        self.incoming_resources_var = []
        for i in range(5):
            self.incoming_resources_var.append(tkinter.StringVar())
            self.incoming_resources.append(ttk.Entry(self.incoming_frame, textvariable=self.incoming_resources_var[i]))
            self.incoming_resources[i].grid(row=i, column=0)
            self.incoming_amounts.append(ttk.Entry(self.incoming_frame))
            self.incoming_amounts[i].grid(row=i, column=1)

        ttk.Label(self.master, text="Outgoing", padding=(10, 0, 10, 0)).grid(row=1, column=1)
        self.outgoing_frame = ttk.Frame(self.master)
        self.outgoing_frame.grid(row=2, column=1)

        self.outgoing_resources = []
        self.outgoing_amounts = []
        self.outgoing_resources_var = []
        for i in range(5):
            self.outgoing_resources_var.append(tkinter.StringVar())
            self.outgoing_resources.append(ttk.Entry(self.outgoing_frame, textvariable=self.outgoing_resources_var[i]))
            self.outgoing_resources[i].grid(row=i, column=0)
            self.outgoing_amounts.append(ttk.Entry(self.outgoing_frame))
            self.outgoing_amounts[i].grid(row=i, column=1)

        ttk.Label(self.master, text="Time to craft:").grid(row=3, column=0)
        self.time_var = tkinter.StringVar(self.master)
        self.time = ttk.Entry(self.master, textvariable=self.time_var)
        self.time.grid(row=3, column=1)

        ttk.Label(self.master, text="Machine name").grid(row=4, column=0)
        self.machine_var = tkinter.StringVar(self.master)
        self.machine = ttk.Entry(self.master, textvariable=self.machine_var)
        self.machine.grid(row=4, column=1)

        self.enter_button = ttk.Button(self.master, text="Save", command=self.save_click)
        self.enter_button.grid(row=5, column=1)

    def save_click(self):
        # TODO
        pass
