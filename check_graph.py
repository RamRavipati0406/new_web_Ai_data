import json
import pickle

# Check JSON
data = json.load(open('engineering_graph.json'))
print(f'Total nodes in JSON: {len(data["nodes"])}')
print(f'Total edges in JSON: {len(data["edges"])}')

depths = {}
for n in data['nodes']:
    d = n['depth']
    depths[d] = depths.get(d, 0) + 1
print(f'Nodes by depth: {depths}')

degree_counts = {}
for n in data['nodes']:
    ind = n['in_degree']
    degree_counts[ind] = degree_counts.get(ind, 0) + 1
print(f'\nIn-degree distribution:')
for deg in sorted(degree_counts.keys()):
    print(f'  In-degree {deg}: {degree_counts[deg]} nodes')

# Check pickle
try:
    G = pickle.load(open('engineering_graph.gpickle', 'rb'))
    print(f'\nPickle graph nodes: {len(G.nodes())}')
    print(f'Pickle graph edges: {len(G.edges())}')
    
    # Degree distribution
    degrees = [G.degree(n) for n in G.nodes()]
    from collections import Counter
    deg_dist = Counter(degrees)
    print(f'\nTotal degree distribution (from pickle):')
    for deg in sorted(deg_dist.keys())[:15]:
        print(f'  Degree {deg}: {deg_dist[deg]} nodes')
except Exception as e:
    print(f'Error reading pickle: {e}')
