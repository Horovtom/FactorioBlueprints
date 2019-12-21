from graphviz import Digraph


class DotWrapper(Digraph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.used_nodes = []
        self.used_edges = {}

    def node(self, name, *args, **kwargs):
        if name in self.used_nodes:
            return
        self.used_nodes.append(name)

        super().node(name, *args, **kwargs)

    def edge(self, from_node, to_node, *args, **kwargs):
        if from_node in self.used_edges:
            if to_node in self.used_edges[from_node]:
                return
            self.used_edges[from_node].append(to_node)
        else:
            self.used_edges[from_node] = [to_node]

        super().edge(from_node, to_node, *args, **kwargs)
