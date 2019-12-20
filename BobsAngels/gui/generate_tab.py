import tkinter
from tkinter import ttk

import graphviz


class GenerateTab:
    def __init__(self, parent, graph):
        self.parent = parent
        self.graph = graph
        self.master = ttk.Frame(self.parent)
        # Add to parent
        self.parent.add(self.master, text="Generate")

        self.chck_filter_value = tkinter.IntVar()
        self.chck_filter = tkinter.Checkbutton(self.master, text="Filter output resource",
                                               variable=self.chck_filter_value,
                                               command=self.chck_filter_changed)

        self.chck_filter.grid(column=0, row=0, padx=10)

        self.frame_filter = ttk.LabelFrame(self.master, padding=(10, 10, 10, 10))
        self.frame_filter.grid(column=0, row=1, padx=10)

        ttk.Label(self.frame_filter, text="Resource:").grid(row=0, column=0)
        self.frame_filter_resource = ttk.Combobox(self.frame_filter, values=self.graph.get_resources_list())
        self.frame_filter_resource.grid(row=0, column=1)

        ttk.Label(self.frame_filter, text="Direction:").grid(row=1, column=0)
        self.frame_filter_direction = ttk.Combobox(self.frame_filter, values=["UP", "DOWN", "BOTH"])
        self.frame_filter_direction.grid(row=1, column=1)

        ttk.Label(self.frame_filter, text="Depth:").grid(row=2, column=0)
        self.entry_filter_depth = ttk.Entry(self.frame_filter, text="1")
        self.entry_filter_depth.grid(row=2, column=1)

        self.chck_compress_water_value = tkinter.IntVar()
        self.chck_compress_water = tkinter.Checkbutton(self.master, text="Compress water node",
                                                       variable=self.chck_compress_water_value)
        self.chck_compress_water.grid(row=2, column=0)
        ttk.Checkbutton(self.master, text="Compress water node", )

        self.btn_generate = ttk.Button(self.master, text="Generate and open", command=self.btn_generate_pressed)
        self.btn_generate.grid(column=0, row=3)

        self.lbl_status_value = tkinter.StringVar()
        self.lbl_status_value.set("Loaded: {} recipes".format(len(graph.recipes)))
        self.lbl_status = tkinter.Label(self.master, text="", textvariable=self.lbl_status_value)
        self.lbl_status.grid(column=0, row=4)

        self.set_filter_frame_enabled(self.chck_filter_value.get())

    def try_to_render_dot(self, dot):
        try:
            dot.render("output", view=True)
            self.lbl_status_value.set("Generated succesfully...")
        except graphviz.backend.CalledProcessError:
            self.lbl_status_value.set("Failed to generate, target file opened.")

    def btn_generate_pressed(self):
        if not self.chck_filter_value.get():
            # Just simply draw the whole graph
            self.try_to_render_dot(self.graph.get_dot(self.chck_compress_water_value.get() == 1))
        else:
            # Check whether the value in entry depth is a number:
            if not self.entry_filter_depth.get().isnumeric() or \
                    int(self.entry_filter_depth.get()) <= 0:
                self.lbl_status_value.set("Depth has to be a positive number!")

            # Check whether there is something in the resource cmbx

    def set_filter_frame_enabled(self, enabled=True):
        for child in self.frame_filter.winfo_children():
            child.configure(state=('enable' if enabled else "disable"))

    def chck_filter_changed(self):
        self.set_filter_frame_enabled(self.chck_filter_value.get())
