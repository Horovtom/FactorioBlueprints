import os
import tkinter
from tkinter import ttk

import graphviz


class GenerateTab:
    def __init__(self, parent, graph):
        self.curr_gen_num = 0
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
        self.cmbx_filter_resource = ttk.Combobox(self.frame_filter, values=self.graph.get_resources_list())
        self.cmbx_filter_resource.grid(row=0, column=1)

        ttk.Label(self.frame_filter, text="Direction:").grid(row=1, column=0)
        self.cmbx_filter_direction = ttk.Combobox(self.frame_filter, values=["UP", "DOWN", "BOTH"])
        self.cmbx_filter_direction.set("UP")
        self.cmbx_filter_direction.grid(row=1, column=1)

        ttk.Label(self.frame_filter, text="Depth:").grid(row=2, column=0)
        self.entry_filter_depth = ttk.Entry(self.frame_filter)
        self.entry_filter_depth.insert(0, "1")
        self.entry_filter_depth.grid(row=2, column=1)

        ttk.Label(self.frame_filter, text="Omit:").grid(row=3, column=0)
        self.entry_filter_omit_var = tkinter.StringVar(self.frame_filter)
        self.entry_filter_omit = ttk.Entry(self.frame_filter, textvariable=self.entry_filter_omit_var)
        self.entry_filter_omit.grid(row=3, column=1)
        # TODO: Temporary
        with open("resources/on_bus.txt", "r") as f:
            self.entry_filter_omit_var.set(f.read())

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
        if not os.path.exists("output"):
            os.mkdir("output")
        try:
            self.curr_gen_num += 1
            dot.render("output/output{}".format(self.curr_gen_num), view=True, cleanup=True)
            self.lbl_status_value.set("Generated successfully...")
        except graphviz.backend.CalledProcessError:
            self.lbl_status_value.set("Failed to generate, target file opened.")
            if self.curr_gen_num < 10:
                self.try_to_render_dot(dot)

    def btn_generate_pressed(self):
        if not self.chck_filter_value.get():
            # Just simply draw the whole graph
            self.try_to_render_dot(self.graph.get_dot(self.chck_compress_water_value.get() == 1))
            return

        # It has to be filter.
        # Let's check its values are valid
        if not self.check_filter_fields_valid():
            return

        omit_list = []
        if self.entry_filter_omit.get().strip() != "":
            omit_list = self.entry_filter_omit.get().split(",")
        self.try_to_render_dot(self.graph.get_dot_with_filter(self.cmbx_filter_resource.get(),
                                                              int(self.entry_filter_depth.get()),
                                                              self.cmbx_filter_direction.get(),
                                                              omit_list,
                                                              self.chck_compress_water_value.get() == 1))

    def set_filter_frame_enabled(self, enabled=True):
        for child in self.frame_filter.winfo_children():
            child.configure(state=('enable' if enabled else "disable"))

    def chck_filter_changed(self):
        self.set_filter_frame_enabled(self.chck_filter_value.get())

    def check_filter_fields_valid(self):
        # Check whether the value in entry depth is a number:
        if not self.entry_filter_depth.get().isnumeric() or \
                int(self.entry_filter_depth.get()) <= 0:
            self.lbl_status_value.set("Depth has to be a positive number!")
            return False

        # Check whether there is something in the resource cmbx
        if self.cmbx_filter_resource.get() == "":
            self.lbl_status_value.set("There is no resource to set filter on!")
            return False

        return True
