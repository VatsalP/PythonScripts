from typing import NamedTuple, List, Tuple

class Node(NamedTuple):
    x: int
    y: int

def get_neighbour(node: Node, graph: List[List[int]]) -> List[Node]:
    neighbour = []
    if node.x+1 != len(g[0]) and g[node.y][node.x+1] != 0:
        neighbour.append(
            Node(x=node.x+1, y=node.y)
            )
    if node.y+1 != len(g) and g[node.y+1][node.x] != 0:
        neighbour.append(
            Node(x=node.x, y=node.y+1)
            )
    return neighbour
    

def dfs(node: Node, graph: List[List[int]]) -> Tuple[bool, List[Node]]:
    if graph[node.y][node.x] == 9:
        return (True, [node])
    for neigbour in get_neighbour(node, graph):
        ret = dfs(neigbour, graph)
        if ret[0]:
            ret[1].insert(0, node)
            return ret
    return (False, [])

if __name__ == "__main__":
    # find shortest path
    # restriction that you can only go right or down
    # so can do with dfs
    g = [
        [1, 0, 0],
        [1, 1, 0],
        [1, 1, 9]
    ]
    print(dfs(Node(x=0, y=0), g))
    g = [
        [1, 1, 1, 1],
        [0, 1, 1, 1],
        [0, 1, 9, 1],
        [0, 0, 1, 1]
    ]
    print(dfs(Node(x=0, y=0), g))
