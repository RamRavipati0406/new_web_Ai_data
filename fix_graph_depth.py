# fix_graph_depth.py
# Fix the depth values in the existing graph using BFS from seed topics

import pickle
import json
import networkx as nx
from collections import deque

# Seed topics (should be at depth 0)
SEED_TOPICS = [
    "Engineering",
    "Mechanical Engineering",
    "Electrical Engineering",
    "Civil Engineering",
    "Chemical Engineering",
    "Computer Engineering",
    "Industrial Engineering",
    "Aerospace Engineering",
    "Biomedical Engineering",
    "Environmental Engineering",
    "Systems Engineering",
    "Systems Theory",
    "Control Theory",
    "Robotics",
    "Automation",
    "Cybernetics",
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Neural Network",
    "Natural Language Processing",
    "Computer Vision",
    "Reinforcement Learning",
    "Data Science",
    "Computational Engineering",
    "Software Engineering",
    "Information Technology"
]

print("Loading graph...")
G = pickle.load(open('engineering_graph.gpickle', 'rb'))

print(f"Original graph: {len(G.nodes())} nodes, {len(G.edges())} edges")
print(f"Original depth distribution: {{}}")
old_depths = {}
for node in G.nodes():
    d = G.nodes[node].get('depth', -1)
    old_depths[d] = old_depths.get(d, 0) + 1
for d in sorted(old_depths.keys()):
    print(f"  Depth {d}: {old_depths[d]} nodes")

# Correct depths using shortest path distance from any seed topic
# This gives us: depth 0 = seeds, depth 1 = directly connected to seeds, etc.
print("\nRecalculating depths using shortest path distance from seed topics...")
new_depth = {}
seed_nodes = [t for t in SEED_TOPICS if t in G.nodes()]

# For each node, calculate shortest distance to any seed topic
for node in G.nodes():
    min_distance = float('inf')
    
    for seed in seed_nodes:
        try:
            # Try shortest path from seed to node (following edges)
            distance = nx.shortest_path_length(G, seed, node)
            min_distance = min(min_distance, distance)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            # Try reverse direction (from node to seed)
            try:
                distance = nx.shortest_path_length(G, node, seed)
                min_distance = min(min_distance, distance)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                pass
    
    # Assign depth, cap at 2 for visualization
    if node in seed_nodes:
        new_depth[node] = 0
    elif min_distance == float('inf'):
        new_depth[node] = 3  # Orphan nodes
    else:
        new_depth[node] = min(min_distance, 2)

# Apply corrected depths to graph
for node in G.nodes():
    if node in new_depth:
        G.nodes[node]['depth'] = new_depth[node]
    else:
        # Orphan nodes (not reachable from seed topics) get depth = max + 1
        G.nodes[node]['depth'] = 3

print("\nNew depth distribution:")
new_depths = {}
for node in G.nodes():
    d = G.nodes[node].get('depth', -1)
    new_depths[d] = new_depths.get(d, 0) + 1
for d in sorted(new_depths.keys()):
    print(f"  Depth {d}: {new_depths[d]} nodes")

# Save corrected graph
print("\nSaving corrected graph...")
pickle.dump(G, open('engineering_graph.gpickle', 'wb'))

# Save corrected JSON
data = {
    'nodes': [
        {
            'id': node,
            'depth': G.nodes[node].get('depth', 0),
            'summary': G.nodes[node].get('summary', ''),
            'short_summary': G.nodes[node].get('short_summary', ''),
            'url': G.nodes[node].get('url', ''),
            'content_preview': G.nodes[node].get('content_preview', ''),
            'categories': G.nodes[node].get('categories', []),
            'sections': G.nodes[node].get('sections', []),
            'images': G.nodes[node].get('images', []),
            'references': G.nodes[node].get('references', []),
            'content_length': G.nodes[node].get('content_length', 0),
            'word_count': G.nodes[node].get('word_count', 0),
            'degree_centrality': G.nodes[node].get('degree_centrality', 0),
            'in_degree': G.nodes[node].get('in_degree', 0),
            'out_degree': G.nodes[node].get('out_degree', 0),
            'pagerank': G.nodes[node].get('pagerank', 0)
        }
        for node in G.nodes()
    ],
    'edges': [
        {'source': u, 'target': v}
        for u, v in G.edges()
    ]
}

with open('engineering_graph.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done! Graph corrected and saved.")
