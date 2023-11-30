class Node:
    def __init__(
        self,
        name: str,
        in_time: int = None,
        out_time: int = None,
        is_complete: bool = False,
    ) -> None:
        self.name = name
        self.is_complete = is_complete
        self.in_time = in_time
        self.out_time = out_time
        self.edges = []

    def get_processing_time(self):
        if self.in_time and self.out_time:
            return self.out_time - self.in_time
        return None


class Edge:
    def __init__(self, from_node: Node, to_node: Node) -> None:
        self.from_node = from_node
        self.to_node = to_node


class Graph:
    def __init__(self, trace_id: str) -> None:
        self.root = None
        self.trace_id = trace_id
        self.nodes = {}

    def display(self):
        for _, node in self.nodes.items():
            print(f"{node.name} ({node.get_processing_time()}s)")
            for edge in node.edges:
                print(f"  -> {edge.to_node.name}")
            print()

    def _get_or_create_node(self, node_name: str) -> Node:
        if not node_name:
            return None

        if node_name not in self.nodes:
            self.nodes[node_name] = Node(node_name)

        return self.nodes[node_name]

    def generate_graph(self, traces: list):
        for trace in traces:
            from_node = self._get_or_create_node(trace["from_node"])
            to_node = self._get_or_create_node(trace["to_node"])

            if not from_node:
                self.root = to_node
            else:
                edge = Edge(
                    from_node,
                    to_node,
                )
                from_node.edges.append(edge)

            to_node.in_time = trace["in_time"]
            to_node.out_time = trace["out_time"]
            to_node.is_complete = trace["is_complete"]

    def get_sanky_graph_data(self, traces: list):
        sanky_nodes = []
        sanky_edges = []
        for _, node in self.nodes.items():
            node_data = {
                "name": node.name,
                "isComplete": node.is_complete,
                "processingTime": node.get_processing_time(),
            }
            sanky_nodes.append(node_data)
            for edge in node.edges:
                edge_data = {
                    "source": edge.from_node.name,
                    "target": edge.to_node.name,
                }
                sanky_edges.append(edge_data)

        return {"nodes": sanky_nodes, "edges": sanky_edges}

    def _dfs(self, node: Node) -> dict:
        if not node:
            return

        node_data = {
            "name": node.name,
            "isComplete": node.is_complete,
            "processingTime": node.get_processing_time(),
            "children": [],
        }

        for edge in node.edges:
            child_data = self._dfs(edge.to_node)
            node_data["children"].append(child_data)

        return node_data

    def get_tree_graph(self, traces: list) -> dict:
        self.generate_graph(traces)
        return self._dfs(self.root)
