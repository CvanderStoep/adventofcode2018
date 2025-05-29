import networkx as nx

def solve(lines):
    G = nx.DiGraph()
    for line in lines:
        parts = line.split(" ")
        G.add_edge(parts[1], parts[7])
    print(list(nx.lexicographical_topological_sort(G)))
    print(''.join(nx.lexicographical_topological_sort(G)))
    return G

def read_input_file(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.read().splitlines()

lines = read_input_file('input/input7.txt')
G= solve(lines)

n_workers = 5

# Add amount of work for each node
for node in G.nodes:
    G.nodes[node]['work'] = 61 + ord(node) - ord('A')

time = 0
while G.nodes:
    # Find nodes available for work
    available_nodes = [node for node in G.nodes if G.in_degree(node) == 0]

    # Sort available nodes: Work on nodes with least remaining work
    available_nodes.sort(key=lambda node: G.nodes[node]['work'])

    # Reduce remaining work for n_workers of the available nodes
    for worker, node in zip(range(n_workers), available_nodes):
        # print("{}: Worker {} is on task {}".format(time, worker, node))
        G.nodes[node]['work'] -= 1

        # Remove finished nodes
        if G.nodes[node]['work'] == 0:
            # print("{}: Node {} is finished!".format(time, node))
            G.remove_node(node)

    # Increase time
    time += 1

print("Finishing all the work took {} seconds".format(time))